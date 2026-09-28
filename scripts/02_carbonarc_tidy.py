"""Step 2: tidy Carbon Arc pulls into long format.
Carbon Arc MCP responses (framework_to_insight) were saved verbatim as tables in data/raw/carbonarc_*_raw.csv;
the exact framework requests are in notes/02_carbonarc.md so each pull can be re-run.
This script only reshapes and converts units (value = YoY growth in percent). No values are filled or interpolated.
Rerun: python3 scripts/02_carbonarc_tidy.py"""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]
RAW = R / "data/raw"
CC = {"Brazil": "BR", "Germany": "DE", "India": "IN", "Indonesia": "ID", "Mexico": "MX", "Philippines": "PH",
      "United Kingdom": "GB", "United States of America": "US", "Worldwide": "WW"}
LAST_REFRESH = "2026-09-26"
out = []

def wide(fname, datecol, metric, freq, src):
    d = pd.read_csv(RAW / fname)
    if datecol == "month":  # 'YYYY-MM' -> month-end date to match other monthly pulls
        d["date"] = pd.PeriodIndex(d["month"], freq="M").to_timestamp(how="end").normalize()
    else:
        d["date"] = pd.to_datetime(d[datecol])
    l = d.drop(columns=[datecol]).melt(id_vars="date", var_name="country_name", value_name="value")
    l["country"] = l.country_name.map(CC)
    l = l.assign(metric=metric, source=src, frequency=freq, app="SPOT ticker (all mapped apps)")
    return l

src = f"Carbon Arc CA0013 App Growth (Mobile App panel ~1M users), entity SPOT ticker id 622, refreshed {LAST_REFRESH}"
out += [wide("carbonarc_users_yoy_raw.csv", "month_end", "app_users_yoy_pct", "month", src + ", insight 522"),
        wide("carbonarc_downloads_yoy_raw.csv", "month", "app_downloads_yoy_pct", "month", src + ", insight 521"),
        wide("carbonarc_users_yoy_weekly_raw.csv", "week_start", "app_users_yoy_pct", "week", src + ", insight 522"),
        wide("carbonarc_downloads_yoy_weekly_raw.csv", "week_start", "app_downloads_yoy_pct", "week", src + ", insight 521")]
s = pd.concat(out, ignore_index=True)

# flags (no values changed)
s["flag"] = ""
s.loc[(s.frequency == "month") & (s.date == "2026-09-30"), "flag"] = "partial_month_data_to_2026-09-26"
s.loc[(s.frequency == "week") & (s.date == "2026-09-21") & (s.metric == "app_downloads_yoy_pct"),
      "flag"] = "likely_incomplete_week_all_countries_-34_to_-54pct"
s.loc[(s.frequency == "week") & (s.date == "2026-09-21") & (s.metric == "app_users_yoy_pct"), "flag"] = "latest_week_may_be_incomplete"
wr = s.date.dt.month.eq(12) & s.date.dt.day.le(7) & s.frequency.eq("week")
s.loc[wr & s.flag.eq(""), "flag"] = "wrapped_week"
s = s[["date", "country", "metric", "value", "source", "frequency", "app", "country_name", "flag"]].sort_values(
    ["frequency", "metric", "country", "date"])
s["date"] = s.date.dt.strftime("%Y-%m-%d")
s.to_csv(R / "data/carbonarc_app_spotify.csv", index=False)
print("spotify:", s.shape, s.groupby(["frequency", "metric"]).date.agg(["min", "max", "count"]).to_string(), "NaN:", s.value.isna().sum())

# rivals (app-level entities, India/Indonesia), fractions -> percent
rows = []
for f, m in [("carbonarc_rivals_users_yoy_raw.csv", "app_users_yoy_pct"), ("carbonarc_rivals_downloads_yoy_raw.csv", "app_downloads_yoy_pct")]:
    d = pd.read_csv(RAW / f)
    d = d.assign(date=d.month_end, country=d.country.map(CC), metric=m, value=d.value_fraction * 100,
                 source=f"Carbon Arc CA0013, app entity (YouTube Music 6697, Apple Music 349, Spotify 5395), refreshed {LAST_REFRESH}",
                 frequency="month", flag=(d.month_end == "2026-09-30").map({True: "partial_month_data_to_2026-09-26", False: ""}))
    rows.append(d[["date", "country", "metric", "value", "source", "frequency", "app", "flag"]])
rv = pd.concat(rows).sort_values(["metric", "app", "country", "date"])
rv.to_csv(R / "data/carbonarc_app_rivals.csv", index=False)
print("rivals:", rv.shape, rv.date.min(), rv.date.max(), sorted(rv.app.unique()))

# consistency check: ticker vs app-entity Spotify monthly users YoY (India, Indonesia)
t = s[(s.frequency == "month") & (s.metric == "app_users_yoy_pct") & s.country.isin(["IN", "ID"])].set_index(["date", "country"]).value
a = rv[(rv.app.str.startswith("Spotify")) & (rv.metric == "app_users_yoy_pct")].set_index(["date", "country"]).value
print("ticker minus app-entity (pp): mean", round((t - a).mean(), 2), "max abs", round((t - a).abs().max(), 2))

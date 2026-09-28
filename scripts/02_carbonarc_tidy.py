"""Step 2: tidy Carbon Arc pulls into long format (full history 2021-01 onward, re-pulled 2026-09-28).
Carbon Arc computes YoY INSIDE the requested date window, so every pull starts 2020-01-01 and output starts 2021-01.
Sources (data/raw/carbonarc_v2/):
  users_yoy_monthly.csv, downloads_yoy_monthly.csv : wide, percent, 2 dp (MCP chat table, transcribed verbatim;
      downloads table had no month column, months assigned by row order and verified on the 21-month overlap)
  users_yoy_weekly_long.csv, downloads_yoy_weekly_long.csv : parsed from MCP-saved JSON (scripts/02c_...), full precision;
      raw DATE = week END (Sunday) -> week_start (Monday) = DATE - 6 days
  rivals_*_yoy_2021_2024.csv : fraction, 2 dp (= whole-pp precision); 2025-01 row is an overlap check, dropped here.
Rivals 2025-01 onward come from the earlier full-precision pull (data/raw/carbonarc_rivals_*_raw.csv).
This script only reshapes and converts units (value = YoY growth in percent). No values are filled or interpolated.
Rerun: python3 scripts/02_carbonarc_tidy.py"""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]
RAW, V2 = R / "data/raw", R / "data/raw/carbonarc_v2"
CC = {"Brazil": "BR", "Germany": "DE", "India": "IN", "Indonesia": "ID", "Mexico": "MX", "Philippines": "PH",
      "United Kingdom": "GB", "United States of America": "US", "Worldwide": "WW"}
LAST_REFRESH = "2026-09-26"
src = f"Carbon Arc CA0013 App Growth (Mobile App panel ~1M users), entity SPOT ticker id 622, refreshed {LAST_REFRESH}"

def monthly(fname, metric, ins):
    d = pd.read_csv(V2 / fname)
    d["date"] = pd.PeriodIndex(d["month"], freq="M").to_timestamp(how="end").normalize()
    l = d.drop(columns=["month"]).melt(id_vars="date", var_name="country", value_name="value")
    return l.assign(metric=metric, frequency="month", precision="0.01pp", source=f"{src}, insight {ins}")

def weekly(fname, metric, ins):
    d = pd.read_csv(V2 / fname)
    d = d[pd.to_datetime(d.date_raw) >= "2021-01-01"]
    d["date"] = pd.to_datetime(d.date_raw) - pd.Timedelta(days=6)
    return pd.DataFrame({"date": d.date, "country": d.country_name.map(CC), "value": d.value_pct, "metric": metric,
                         "frequency": "week", "precision": "full", "source": f"{src}, insight {ins}"})

s = pd.concat([monthly("users_yoy_monthly.csv", "app_users_yoy_pct", 522),
               monthly("downloads_yoy_monthly.csv", "app_downloads_yoy_pct", 521),
               weekly("users_yoy_weekly_long.csv", "app_users_yoy_pct", 522),
               weekly("downloads_yoy_weekly_long.csv", "app_downloads_yoy_pct", 521)], ignore_index=True)
s["app"] = "SPOT ticker (all mapped apps)"

# flags (no values changed)
s["flag"] = ""
s.loc[(s.frequency == "month") & (s.date == "2026-09-30"), "flag"] = "partial_month_data_to_2026-09-26"
s.loc[(s.frequency == "week") & (s.date == "2026-09-21") & (s.metric == "app_downloads_yoy_pct"),
      "flag"] = "likely_incomplete_week_all_countries_-34_to_-54pct"
s.loc[(s.frequency == "week") & (s.date == "2026-09-21") & (s.metric == "app_users_yoy_pct"), "flag"] = "latest_week_may_be_incomplete"
wr = s.date.dt.month.eq(12) & s.date.dt.day.le(7) & s.frequency.eq("week")
s.loc[wr & s.flag.eq(""), "flag"] = "wrapped_week"
s = s[["date", "country", "metric", "value", "source", "frequency", "app", "precision", "flag"]].sort_values(
    ["frequency", "metric", "country", "date"])
s["date"] = s.date.dt.strftime("%Y-%m-%d")
s.to_csv(R / "data/carbonarc_app_spotify.csv", index=False)
print("spotify:", s.shape, "NaN:", int(s.value.isna().sum()))
print(s.groupby(["frequency", "metric"]).date.agg(["min", "max", "count"]).to_string())

# rivals (app-level entities, India/Indonesia), fractions -> percent
rsrc = f"Carbon Arc CA0013, app entity (YouTube Music 6697, Apple Music 349, Spotify 5395), refreshed {LAST_REFRESH}"
rows = []
for new, old, m in [("rivals_users_yoy_2021_2024.csv", "carbonarc_rivals_users_yoy_raw.csv", "app_users_yoy_pct"),
                    ("rivals_downloads_yoy_2021_2024.csv", "carbonarc_rivals_downloads_yoy_raw.csv", "app_downloads_yoy_pct")]:
    a = pd.read_csv(V2 / new)
    a = a[a.month < "2025-01"].melt(id_vars="month", var_name="k", value_name="frac")
    a["app"], a["country"] = a.k.str.split("|").str[0], a.k.str.split("|").str[1]
    a = a.assign(date=pd.PeriodIndex(a.month, freq="M").to_timestamp(how="end").normalize().strftime("%Y-%m-%d"),
                 value=a.frac * 100, precision="1pp")
    b = pd.read_csv(RAW / old).rename(columns={"month_end": "date"})
    b = b.assign(value=b.value_fraction * 100, precision="full")
    d = pd.concat([a[["date", "app", "country", "value", "precision"]], b[["date", "app", "country", "value", "precision"]]])
    d = d.assign(country=d.country.map(CC), metric=m, source=rsrc, frequency="month",
                 flag=(d.date == "2026-09-30").map({True: "partial_month_data_to_2026-09-26", False: ""}))
    rows.append(d[["date", "country", "metric", "value", "source", "frequency", "app", "precision", "flag"]])
rv = pd.concat(rows).sort_values(["metric", "app", "country", "date"])
rv.to_csv(R / "data/carbonarc_app_rivals.csv", index=False)
print("rivals:", rv.shape, rv.date.min(), rv.date.max(), "NaN:", int(rv.value.isna().sum()))

# consistency check: ticker vs app-entity Spotify monthly users YoY (India, Indonesia)
t = s[(s.frequency == "month") & (s.metric == "app_users_yoy_pct") & s.country.isin(["IN", "ID"])].set_index(["date", "country"]).value
ap = rv[(rv.app.str.startswith("Spotify")) & (rv.metric == "app_users_yoy_pct")].set_index(["date", "country"]).value
dd = (t - ap).dropna()
print("ticker minus app-entity (pp): n", len(dd), "mean", round(dd.mean(), 2), "max abs", round(dd.abs().max(), 2))

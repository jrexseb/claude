"""Step 4c: tidy kworb outputs.
data/kworb_streams_daily.csv  : one row per country x chart day captured (top-200 streams sum).
data/kworb_streams_weekly.csv : long, three metrics (kept separate; they are NOT interchangeable):
  - top200_weekly_chart_streams : Streams sum of a captured WEEKLY chart page (a complete chart week).
      date = chart date printed by kworb (see notes for convention); days_observed = 7 by construction.
  - top200_daily_streams_sum_observed : sum of captured DAILY charts inside an ISO week (Mon start);
      days_observed = number of captured days (0-7). Partial weeks are NOT scaled up.
  - top200_daily_streams_mean_observed : mean per captured day in that ISO week (same days_observed).
No interpolation; weeks without captures are absent. Rerun: python3 scripts/04c_kworb_tidy.py"""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CC = {c: c.upper() for c in ["in", "id", "br", "mx", "ph", "us", "gb", "de"]}
d = pd.read_csv(R / "data/raw/kworb_daily.csv")
d["date"] = pd.to_datetime(d.chart_date)
daily = d.assign(country=d.country.map(CC), metric="top200_daily_streams", value=d.streams_sum,
                 source="kworb.net {cc}_daily.html via Wayback capture (or live page)")[
    ["chart_date", "country", "metric", "value", "source", "rows", "snapshot_url"]].rename(columns={"chart_date": "date"})
daily.to_csv(R / "data/kworb_streams_daily.csv", index=False)

d["week_start"] = d.date - pd.to_timedelta(d.date.dt.weekday, unit="D")
g = d.groupby(["country", "week_start"]).agg(s=("streams_sum", "sum"), m=("streams_sum", "mean"),
                                            n=("date", "nunique")).reset_index()
src_d = "kworb.net daily charts via Wayback captures; ISO week (Mon start); observed days only"
a = pd.concat([
    g.assign(metric="top200_daily_streams_sum_observed", value=g.s),
    g.assign(metric="top200_daily_streams_mean_observed", value=g.m)])
a = a.assign(date=a.week_start.dt.strftime("%Y-%m-%d"), country=a.country.map(CC), source=src_d, days_observed=a.n)
out = [a[["date", "country", "metric", "value", "source", "days_observed"]]]
wp = R / "data/raw/kworb_weekly_charts.csv"
if wp.exists() and wp.stat().st_size > 50:
    w = pd.read_csv(wp)
    if len(w):
        out.append(w.assign(date=w.chart_date, country=w.country.map(CC), metric="top200_weekly_chart_streams",
                            value=w.streams_sum, days_observed=7,
                            source="kworb.net {cc}_weekly.html via Wayback capture (or live page); date = kworb chart date")[
            ["date", "country", "metric", "value", "source", "days_observed"]])
t = pd.concat(out).sort_values(["metric", "country", "date"])
t.to_csv(R / "data/kworb_streams_weekly.csv", index=False)
print(daily.shape, t.shape); print(t.groupby(["metric", "country"]).date.agg(["min", "max", "count"]).to_string())

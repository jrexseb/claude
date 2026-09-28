"""Reported quarterly KPIs (levels, millions) from panel_all.csv, tidy long. Used to compare app-panel YoY with
reported Ad-Supported MAU y/y. Levels only; y/y is left to the analysis session.
Rerun: python3 scripts/02b_reported_kpis.py"""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]
p = pd.read_csv(R / "panel_all.csv").rename(columns={"Unnamed: 0": "date"})
m = {"ad_mau": "ad_supported_mau", "subs": "premium_subs", "mau": "mau_total"}
d = p[["date", *m]].melt(id_vars="date", var_name="metric", value_name="value").replace({"metric": m})
d = d.assign(country="WW", source="panel_all.csv (company 6-K reported, per repo panel)")[["date", "country", "metric", "value", "source"]]
d.to_csv(R / "data/reported_kpis_quarterly.csv", index=False)
print(d.shape, d.date.min(), d.date.max(), "NaN:", d.value.isna().sum())

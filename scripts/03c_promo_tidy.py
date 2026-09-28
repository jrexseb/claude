"""Step 3c: tidy data/raw/promo_parsed_wide.csv -> data/promo_depth.csv (long).
metric = {list_price|trial_months|intro_price|intro_months}_{plan}; list prices in local currency.
Blank = not shown / not parsed (see parse_status). Also writes the missing-month table used in notes/03_promos.md.
Rerun: python3 scripts/03c_promo_tidy.py"""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]
d = pd.read_csv(R / "data/raw/promo_parsed_wide.csv")
d = d[d.plan.notna()]
rows = []
for _, r in d.iterrows():
    for f in ["list_price", "trial_months", "intro_price", "intro_months"]:
        v = r.get(f)
        if pd.notna(v):
            rows.append({"date": f"{str(int(r.month))[:4]}-{str(int(r.month))[4:]}", "country": r.country.upper(),
                         "metric": f"{f}_{r.plan}", "value": v,
                         "source": "spotify.com premium page via Wayback Machine",
                         "currency": r.currency if f.endswith("price") else "",
                         "list_price_source": r.list_price_source if f == "list_price" else "",
                         "snapshot_url": r.snapshot_url, "effective_url": r.effective_url,
                         "effective_timestamp": r.effective_timestamp})
t = pd.DataFrame(rows).sort_values(["country", "metric", "date"])
t.to_csv(R / "data/promo_depth.csv", index=False)
# coverage / gaps
allm = pd.period_range("2023-01", "2026-09", freq="M").strftime("%Y-%m")
cov = {cc: sorted(set(allm) - set(t[(t.country == cc) & (t.metric == "list_price_individual")].date)) for cc in sorted(t.country.unique())}
pd.DataFrame([{"country": k, "n_missing": len(v), "missing_months": " ".join(v)} for k, v in cov.items()]).to_csv(
    R / "data/raw/promo_missing_months.csv", index=False)
print(t.shape, t.date.min(), t.date.max())
print(t.groupby("metric").size().to_string())
for k, v in cov.items(): print(k, "missing individual list price:", len(v))

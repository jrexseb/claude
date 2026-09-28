"""Tidy Google Trends pulls -> data/google_trends_weekly.csv (long). value = pull-1 index (0-100; '<1' stored as 0.5
and flagged). Pull 2 kept as value_pull2 plus abs difference, so the analysis can see sampling noise per point.
isPartial rows (latest incomplete week) flagged. Rerun: python3 scripts/05b_trends_tidy.py"""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]; C = R / "data/raw/trends"
rows = []
for f in sorted(C.glob("*_pull1.csv")):
    geo = f.name.split("_")[0]
    a = pd.read_csv(f, parse_dates=["date"])
    f2 = C / f"{geo}_pull2.csv"
    b = pd.read_csv(f2, parse_dates=["date"]) if f2.exists() else None
    for term in [c for c in a.columns if c not in ("date", "isPartial")]:
        d = a[["date", term, "isPartial"]].rename(columns={term: "value"})
        d["value_pull2"] = b.set_index("date")[term].reindex(d.date).values if b is not None else None
        d = d.assign(country=geo, metric=f"trends_index:{term}", source="Google Trends via pytrends; web search; weekly; geo-normalised")
        rows.append(d)
t = pd.concat(rows)
t["abs_diff_pulls"] = (t.value - t.value_pull2).abs()
t["flag"] = t.isPartial.map({True: "partial_week", False: ""})
t["date"] = t.date.dt.strftime("%Y-%m-%d")
t[["date", "country", "metric", "value", "source", "value_pull2", "abs_diff_pulls", "flag"]].sort_values(
    ["country", "metric", "date"]).to_csv(R / "data/google_trends_weekly.csv", index=False)
s = t.groupby(["country", "metric"]).agg(mean=("value", "mean"), zeros=("value", lambda x: (x == 0).mean()),
                                        mad=("abs_diff_pulls", "mean"), maxd=("abs_diff_pulls", "max")).round(2)
s.to_csv(R / "data/raw/trends_quality.csv")
print(t.shape, t.date.min(), t.date.max()); print(s.to_string())

# single-term pulls (05c): own scale per country-term -> separate file, metric prefix 'trends_single:'
S = R / "data/raw/trends_single"
rows = []
for f in sorted(S.glob("*.csv")):
    geo, term = f.stem.split("__"); term = term.replace("_", " ")
    try:
        a = pd.read_csv(f, parse_dates=["date"])
    except Exception:
        continue
    if a.empty or term not in a.columns: continue
    d = a[["date", term, "isPartial"]].rename(columns={term: "value"}).assign(
        country=geo, metric=f"trends_single:{term}",
        source="Google Trends via pytrends; single-term request (own 0-100 scale); weekly")
    rows.append(d)
if rows:
    s1 = pd.concat(rows)
    s1["flag"] = s1.isPartial.map({True: "partial_week", False: ""})
    s1["date"] = s1.date.dt.strftime("%Y-%m-%d")
    s1[["date", "country", "metric", "value", "source", "flag"]].sort_values(["country", "metric", "date"]).to_csv(
        R / "data/google_trends_single_term_weekly.csv", index=False)
    q = s1.groupby(["country", "metric"]).value.agg(mean="mean", zero_share=lambda x: (x == 0).mean()).round(2)
    print(q.to_string())

"""Step 1: regional consensus table from the Bloomberg MODL export (SPOTModelBloom-nums.xlsx).
Rerun: python3 scripts/01_regional_consensus.py  -> data/regional_consensus.csv
No values are computed except RoW MAU (total MAU minus Europe, North America, Latin America), which the
task defines; it is written as a separate metric next to the MODL 'Other Countries' row."""
import re, openpyxl, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = "SPOTModelBloom-nums.xlsx"
ws = openpyxl.load_workbook(ROOT / SRC, data_only=True)["Multiple Periods"]

# column headers: row 3 = '2024 Q2 (Rep)' / '2026 Q3 (Fwd)'; row 4 = period-end Excel serial
cols = {}
for c in range(5, ws.max_column + 1):
    h = ws.cell(3, c).value
    m = re.match(r"(\d{4}) Q(\d) \((Rep|Fwd)\)", str(h or ""))
    if m:
        cols[c] = (int(m[1]), int(m[2]), "reported" if m[3] == "Rep" else "forecast")

# (excel row, metric, region)  -- row numbers verified against labels below
ROWS = [
    (60, "mau_total", "Total"),                       # Monthly Active Users (MAUs), M4640
    (20, "mau_total_highlights", "Total"),            # same field, Highlights block
    (22, "ad_supported_mau", "Total"),                # Highlights: Ad-Supported Users, M4640 seg 454644
    (58, "ad_supported_mau_mau_block", "Total"),      # MAU block: Ad-Supported Users, same field
    (21, "premium_subs_mau_field", "Total"),          # Highlights: Premium Subscribers, M4640 seg 454645
    (44, "premium_subs", "Total"),                    # Premium Subscribers, M5897 (paying users)
    (57, "premium_subs_mau_block", "Total"),          # MAU block: Premium, M4640 seg 454645
    (79, "free_premium_ratio_modl", "Total"),         # 'Free/Premium Ratio' row as shipped in the sheet
    (61, "mau", "Europe"), (64, "mau", "North America"), (67, "mau", "Latin America"),
    (70, "mau_modl_other_countries", "Rest of World"),
    (46, "premium_subs", "Europe"), (48, "premium_subs", "North America"),
    (50, "premium_subs", "Latin America"), (52, "premium_subs", "Rest of World"),
]
EXPECT = {20: "Monthly Active Users (MAUs)", 21: "Premium Subscribers", 22: "Ad-Supported Users",
          44: "Premium Subscribers", 46: "Europe", 48: "North America", 50: "Latin America",
          52: "Rest Of World", 57: "Premium", 58: "Ad-Supported Users", 60: "Monthly Active Users (MAUs)",
          61: "Europe", 64: "North America", 67: "Latin America", 70: "Other Countries",
          79: "Free/Premium Ratio"}
for r, lab in EXPECT.items():
    assert str(ws.cell(r, 1).value).strip() == lab, (r, ws.cell(r, 1).value)

recs = []
for r, metric, region in ROWS:
    for c, (y, q, flag) in cols.items():
        if (y, q) < (2024, 2) or (y, q) > (2027, 4):
            continue
        v = ws.cell(r, c).value
        recs.append(dict(date=f"{y}Q{q}", country=region, metric=metric,
                         value=v if isinstance(v, (int, float)) else None,
                         source=f"Bloomberg MODL {SRC} row {r} ({ws.cell(r,2).value or 'no field code'})",
                         flag=flag))
df = pd.DataFrame(recs)

# RoW MAU = total MAU (row 60) minus the three named regions (task definition). NaN if any input missing.
w = df[df.metric.isin(["mau_total", "mau"])].pivot_table(index="date", columns="country", values="value", aggfunc="first")
row = (w["Total"] - w["Europe"] - w["North America"] - w["Latin America"]).rename("value").reset_index()
flags = df.drop_duplicates("date").set_index("date").flag
row = row.assign(country="Rest of World", metric="mau_row_derived",
                 source="derived: row60 - row61 - row64 - row67", flag=row.date.map(flags))
df = pd.concat([df, row[df.columns]], ignore_index=True)
df = df[["date", "country", "metric", "value", "source", "flag"]].sort_values(["metric", "country", "date"])
df.to_csv(ROOT / "data/regional_consensus.csv", index=False)
print(df.shape, df.date.min(), df.date.max(), "missing values:", df.value.isna().sum())

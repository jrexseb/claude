# Step 1: regional consensus table

**Output:** `data/regional_consensus.csv` (255 rows; 2024Q2 to 2027Q4; 0 missing values)
**Script:** `scripts/01_regional_consensus.py`
**Source:** `SPOTModelBloom-nums.xlsx`, sheet "Multiple Periods". Bloomberg company-model export: SPOT US Equity, periodicity Q, currency EUR, estimate source BST (Bloomberg consensus mean), actual source Bloomberg.

## File naming
The task names `MODL_SPOT_US_B2.xlsx`, but that file is not in the repo. `SPOTModelBloom-nums.xlsx` is a Bloomberg MODL export with the same described content (regional subscribers EU/NA/LatAm/RoW; regional MAU EU/NA/LatAm/Other; Q2'24A to Q3'28E, matching the plan's vault table). Treated as the MODL source. Confirm with the Bloomberg owner (Joel) that it is the same pull.

## Columns
- `date`: fiscal quarter (`2026Q3`). Spotify's fiscal year is the calendar year; the period-end is in the sheet's row 4.
- `flag`: `reported` for 2024Q2 to 2026Q2 (sheet header "(Rep)"); `forecast` for 2026Q3 to 2027Q4 ("(Fwd)" = consensus mean).
- `value`: millions of users, except `free_premium_ratio_modl` (a ratio).
- `source`: Excel row plus Bloomberg field code.

## Metrics and rows
| metric | country | Excel row | Bloomberg field |
|---|---|---|---|
| mau_total | Total | 60 | MONTHLY_ACTIVE_USERS (M4640) |
| mau_total_highlights | Total | 20 | same field, identical values |
| ad_supported_mau | Total | 22 | M4640, segment Ad-Supported |
| ad_supported_mau_mau_block | Total | 58 | same, identical to row 22 |
| premium_subs_mau_field | Total | 21 | M4640, segment Premium |
| premium_subs_mau_block | Total | 57 | same, identical to row 21 |
| premium_subs | Total | 44 | MONTHLY_PAYING_USERS (M5897), segment Premium |
| premium_subs | Europe / North America / Latin America / Rest of World | 46 / 48 / 50 / 52 | M5897 by region |
| mau | Europe / North America / Latin America | 61 / 64 / 67 | M4640 by region |
| mau_modl_other_countries | Rest of World | 70 | M4640, "Other Countries" |
| mau_row_derived | Rest of World | derived | row 60 − 61 − 64 − 67 (the task's definition) |
| free_premium_ratio_modl | Total | 79 | no field code; see below |

A regional Rest of World subscriber row exists (row 52).

## Reconciliation to handoff (Q3'26E: free 498m, subs 305m, ratio 1.63)
- **Free 498m:** rows 22 and 58 (498.2). They agree.
- **Subs 305m:** rows 21 and 57 (M4640 Premium segment, 305.1). **Row 44 (M5897 paying users) gives 301.6.**
- **Ratio 1.63:** 498.2 / 305.1 = 1.633. Using row 44: 498.2 / 301.6 = 1.652.
- **Row 79 "Free/Premium Ratio" = 1.647 for Q3'26.** It equals row 78 / row 77, the beginning-of-period (BOP) Ad-Supported and Premium counts. In reported quarters this is the prior quarter's end ratio. It is a lagged ratio, not the quarter-end ratio.
- Neither subscriber row was picked. Both are in the CSV.

## Internal consistency (per quarter; in millions)
- **Row 44 vs row 21:** 0.0 in all reported quarters. In forecast quarters row 44 is below row 21 by 2.9 to 5.7m (Q3'26 −3.6, Q4'26 −5.7, Q2'27 −4.8). The two fields have different contributor sets.
- **Sum of the four regional sub rows vs row 44:** 0.0 in 5 of 9 reported quarters. It is off in Q3'24 (+2.5), Q4'24 (−2.6), Q3'25 (−2.8) and Q4'25 (−2.9). In forecasts, the regions sum 3.3 to 6.3m above row 44, which puts it close to row 21. Regional rows likely have fewer contributors than the totals; the file has no contributor counts.
- **Derived RoW MAU vs "Other Countries" (row 70):** 0 in most reported quarters. It is −14 in Q3'24, −15 in Q4'25 and Q1'26, and +7.77 in Q2'26 (a non-integer gap in a reported quarter; a possible data-entry issue in the Bloomberg regional row). In forecasts the gap is within ±1.3.
- **Ad-Supported + Premium (row 21) − total MAU:** +13 to +17 every quarter, including reported quarters. This is Spotify's own reporting: the sum of the segments exceeds total MAU. The 6-K definitions explain the overlap; it is not a data error.

## Check against historical panel
Reported quarters (2024Q2 to 2026Q2) of rows 21, 44, 22 and 60 match `panel_all.csv` columns `subs`, `ad_mau` and `mau` exactly (0.00 difference).

## Gaps
- No contributor count, high/low or dispersion (mean only). This is research-plan Bloomberg ask 5.
- No regional Ad-Supported split. Regional free users can only be approximated as regional MAU minus regional subs, which inherits the segment overlap above. Not computed here.
- 2028 quarters are in the sheet but out of the requested range and were not extracted.

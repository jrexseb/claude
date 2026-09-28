# Step 2: Carbon Arc app data

**Outputs**
- `data/carbonarc_app_spotify.csv`: SPOT ticker; app users YoY and app downloads YoY; monthly and weekly; 9 geographies. 2,016 rows, 0 NaN.
- `data/carbonarc_app_rivals.csv`: app-level YouTube Music, Apple Music and Spotify (check series); India and Indonesia; monthly. 252 rows.
- `data/reported_kpis_quarterly.csv`: reported Ad-Supported MAU, Premium subs and total MAU (levels, m), 2021Q1 to 2026Q2, from `panel_all.csv`. `mau_total` is missing for 2021Q1 to 2022Q2 in the source panel.
- Raw responses: `data/raw/carbonarc_*_raw.csv`. Tidy script: `scripts/02_carbonarc_tidy.py`; reported KPIs: `scripts/02b_reported_kpis.py`.

`value` is YoY growth in **percent** (4.4 = +4.4%). Country codes: IN, ID, BR, MX, PH, US, GB, DE, WW (Worldwide).

## Source and definitions
- **Dataset:** CA0013 "App Growth", Carbon Arc tearsheet "Mobile App". Opt-in panel of ~1M users; weekly frequency; history listed as 2014 to present; lag T+2 days; last refresh 2026-09-26 03:32 UTC. Provider not named.
- **Insight 522, "App Users Growth YoY":** YoY % change in panel app users. Insight 35 ("App Users Growth Pct") is a separate, unused metric; the docs could not say how it differs (docs search returned no answer).
- **Insight 521, "App Download Growth YoY":** YoY % change in downloads.
- **Aggregation:** the only option offered is `mean`.
- **Monthly vs weekly are not the same measure.** Monthly values are **not** the average of the weekly values (e.g. India Jan 2025: monthly 12.80 vs weekly Jan average ≈ 9). They likely compare different user windows (monthly vs weekly actives). Do not mix frequencies in one series.
- **Entity:** SPOT ticker (id 622), as requested. The ticker maps to more than one Spotify app. The main-app entity "Spotify - Music and Podcasts" (id 5395) gives users YoY within 0.37pp of the ticker (mean difference −0.1pp; India/Indonesia monthly).
- **Date convention:** monthly `date` = month end; weekly `date` = week start (Monday).

## Coverage
| Series | Range | Geos | Note |
|---|---|---|---|
| Monthly users/downloads YoY | 2025-01 to 2026-09 | 9 | 2024 months are NaN at source; not included |
| Weekly users/downloads YoY | 2024-12-30 to 2026-09-21 | 9 | requested from 2024-12-30 |
| Rivals monthly (users, downloads) | 2025-01 to 2026-09 | IN, ID | YouTube Music, Apple Music, Spotify app |

**YoY is NaN for all of 2024**, even though the history is listed from 2014, so the SPOT/app mapping appears to start in 2024. There is no YoY series before Jan 2025, which means no pre-Sept-2025 baseline longer than 8 months.

## Precision
- Monthly SPOT users: 4 decimals (percent). This came from a second call; the first call returned the table rounded to 0.01 in fraction terms (1pp). The two agree at that rounding.
- Monthly SPOT downloads: 4 decimals.
- Weekly: 2 decimals (percent).
- Rivals: full precision (fractions × 100).

## Flags (`flag` column; values are unchanged)
- `partial_month_data_to_2026-09-26`: Sep 2026 monthly rows. Sep 2026 monthly downloads are −10% to −37% in every country at once.
- `likely_incomplete_week_all_countries_-34_to_-54pct`: week of 2026-09-21, downloads. Every geography drops at once. Treat as incomplete.
- `latest_week_may_be_incomplete`: week of 2026-09-21, users.
- `wrapped_week`: weeks starting Dec 1-7 (Spotify Wrapped). Weekly downloads that week jump in ID (+38%), PH (+46%), GB (+15%) and WW (+13%).

## Anomalies to know (not interpreted)
- **India monthly downloads:** −39% (Feb 2025), −39% (Mar 2025) and +33% (Sep 2025). Weekly India downloads range from −54% to +44%, so they are volatile.
- **Worldwide weekly downloads** are +23% and +22% in the weeks of 2025-09-15 and 2025-09-22, which cover the Sept 15, 2025 free-tier upgrade date. The US is also positive (+6%) that week.
- **Germany users YoY rises from ~1% (Mar 2026) to 7.3% (Sep 2026). UK and US also rise from mid-2026.**
- **Downloads spikes in GB/DE:** weekly GB downloads are +31% to +42% in early Aug 2026.
- **Apple Music YoY:** large percentages (+100% to +360%) in IN/ID, likely from a small base. Levels are unavailable, so its weight can't be assessed.
- **YouTube Music downloads:** +158% in IN and ID in Feb 2025, then −57% and −70% in Feb 2026, which is the lap.

## Level series: unusable (logged, not included)
- CA0054 "App Intelligence" insight 192635 (Monthly App Users) was tried on both the SPOT ticker and the app entity 5395. Values flip ~2× between months (US 9m ↔ 18m, India 2.3m ↔ 4.7m). Indonesia shows 64 to 2,563 users; Philippines and Worldwide are mostly missing.
- The Android-only query returns 35 to 73,677 users per country-month, and the app entity returns identical numbers.
- CA0054 history starts 12/2023. Aggregate options: `mean` only.
- **Not used.** Daily App Downloads (775) was not pulled for the same reason.

## Not available
- JioSaavn: no app entity in Carbon Arc (search returned JioHotstar and unrelated apps). Amazon Music was not searched.
- No DAU/MAU level series at usable quality; no panel size per country.

## Credit log (Carbon Arc tokens; the daily limit is 2,000, per the user)
| # | Query | Cost |
|---|---|---|
| 1 | 522 users YoY, month, 9 geos (rounded output) | 4.99 |
| 2 | same, re-run for 4-decimal output | 4.99 (the docs say an identical re-run is free; it was billed) |
| 3 | 521 downloads YoY, month | 4.99 |
| 4 | 522 users YoY, week | 6.18 |
| 5 | 521 downloads YoY, week | 6.18 |
| 6 | 192635 monthly app users, ticker (unusable) | 16.95 |
| 7 | 192635 Android only, ticker (diagnostic) | 6.23 |
| 8 | 192635 Android only, app 5395 (diagnostic) | 6.23 |
| 9 | 522 rivals + Spotify app, IN/ID, month | 4.99 |
| 10 | 521 rivals + Spotify app, IN/ID, month | 4.99 |
| | **Session total** | **≈ 66.7** |

## Exact framework requests (re-run via `framework_to_insight`)
- SPOT: `entities=[{carc_id:622, representation:"ticker"}]`, `insight_id` 522 or 521, `location_resolution="country"`, `date_resolution="month"` or `"week"`, `aggregate="mean"`, `filters.country=["Worldwide","United States of America","India","Indonesia","Brazil","Mexico","Philippines","United Kingdom","Germany"]`. Date filters are ignored in the echoed request; the full history is returned.
- Rivals: `entities=[{6697,"app"},{349,"app"},{5395,"app"}]`, insight 522 or 521, month, `country=["India","Indonesia"]`.
- The MCP returns a markdown table only (no file download). Tables were transcribed to `data/raw/` without edits.

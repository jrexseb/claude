# Step 2: Carbon Arc app data

**Outputs**
- `data/carbonarc_app_spotify.csv`: SPOT ticker; app users YoY and app downloads YoY; monthly and weekly; 9 geographies; **2021-01 to 2026-09**. 6,642 rows, 0 NaN. Has a `precision` column.
- `data/carbonarc_app_rivals.csv`: app-level YouTube Music, Apple Music and Spotify (check series); India and Indonesia; monthly; **2021-01 to 2026-09**. 828 rows, 0 NaN.
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

## Coverage (re-pulled 2026-09-28 with full history)
| Series | Range | Geos | Note |
|---|---|---|---|
| Monthly users/downloads YoY | 2021-01 to 2026-09 | 9 | 69 months, no gaps |
| Weekly users/downloads YoY | week of 2020-12-28 to 2026-09-21 | 9 | 300 weeks, no gaps |
| Rivals monthly (users, downloads) | 2021-01 to 2026-09 | IN, ID | YouTube Music, Apple Music, Spotify app |

**Carbon Arc computes YoY inside the requested date window.** The first pull started at 2024-01-01, so all of 2024 came back NaN; that was a query-window artifact, not missing data. All series were re-pulled with `start_date=2020-01-01`, which yields YoY from 2021-01 (2020 rows are NaN by construction and dropped). **Any future pull must start 12 months before the first YoY month wanted.**

Re-pull checks against the earlier pull on the overlap: max abs difference 0.005pp (monthly users, monthly downloads, weekly users, weekly downloads; 21 months / 91 weeks) and ≤0.005 in fraction (rivals, Jan 2025). The only differences are rounding.

## Precision (`precision` column)
- **Monthly SPOT users/downloads:** 2 decimals in percent (`0.01pp`), transcribed from the MCP chat table. The monthly downloads table came back **without its month column**; months were assigned by row order (69 rows = 2021-01…2026-09) and verified on the 21-month overlap (max diff 0.005pp).
- **Weekly SPOT users/downloads:** full precision. The MCP saved these results to file; they were parsed directly (`scripts/02c_carbonarc_parse_saved.py`; verbatim JSON in `data/raw/carbonarc_v2/`). The raw weekly date is the week **end** (Sunday) and is converted to week start (Monday).
- **Rivals 2021-01 to 2024-12:** fractions to 2 decimals, i.e. **whole-percentage-point precision (`1pp`)**. **Rivals 2025-01 onward:** full precision from the earlier pull.

## Ticker vs Spotify app entity
The SPOT ticker pools every app mapped to Spotify; the app entity is "Spotify - Music and Podcasts" only. Monthly users YoY, max |ticker − app| by year:

| Year | ID | IN |
|---|---|---|
| 2021 | 10.0pp | 2.7pp |
| 2022 | 1.6 | 1.2 |
| 2023 | 3.5 | 0.5 |
| 2024 | 3.3 | 0.6 |
| 2025 | 0.4 | 0.2 |
| 2026 | 0.1 | 0.0 |

Up to ±0.5pp is rounding (the app-level series is at 1pp precision in 2021-24). The larger 2021 and 2023-24 Indonesia gaps suggest the ticker includes other Spotify apps (possibly Spotify Lite) in those years. **Not verified.**

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
| | **First session total** | **≈ 66.7** |
| 11 | 522 users YoY, month, IN+US, from 2020-01 (window test) | 4.99 |
| 12 | 522 users YoY, month, 9 geos, from 2020-01 | 4.99 |
| 13 | 521 downloads YoY, month, 9 geos, from 2020-01 | 4.99 |
| 14 | 522 users YoY, week, 9 geos, from 2020-01 | 15.22 |
| 15 | 521 downloads YoY, week, 9 geos, from 2020-01 | ≈15 |
| 16-17 | 522/521 rivals + Spotify app, IN/ID, month, from 2020-01 | 4.99 each |
| | **Re-pull total** | **≈ 55** |

## Exact framework requests (re-run via `framework_to_insight`)
- SPOT: `entities=[{carc_id:622, representation:"ticker"}]`, `insight_id` 522 or 521, `location_resolution="country"`, `date_resolution="month"` or `"week"`, `aggregate="mean"`, `filters.country=["Worldwide","United States of America","India","Indonesia","Brazil","Mexico","Philippines","United Kingdom","Germany"]`, `filters.start_date="2020-01-01"`, `end_date="2026-09-28"`. The echoed request omits dates, but they are applied (they change which months get a YoY).
- Rivals: `entities=[{6697,"app"},{349,"app"},{5395,"app"}]`, insight 522 or 521, month, `country=["India","Indonesia"]`, same dates.
- The MCP returns a markdown table in chat for small results; those were transcribed to `data/raw/` without edits. Large results are saved to file by the MCP and parsed by script.

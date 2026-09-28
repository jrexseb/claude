# Data index: SPOT margin pillar (free users per payer)

Data collection only; no conclusions here. Read `CLAUDE.md` first. Each step's note has the exact queries, coverage and caveats. Every `data/*.csv` is long format with `date, country, metric, value, source` first. Scripts in `/scripts` rerun each pull.

## Files
| File | Contents | Coverage | Note |
|---|---|---|---|
| `data/regional_consensus.csv` | Bloomberg MODL consensus: MAU and Premium subs by region (EU, NA, LatAm, RoW) plus totals; `flag` = reported or forecast | 2024Q2-2027Q4 (reported to 2026Q2) | `01_regional.md` |
| `data/reported_kpis_quarterly.csv` | Reported Ad-Supported MAU, Premium subs, total MAU (m) | 2021Q1-2026Q2 (total MAU missing 2021Q1-2022Q2) | `02_carbonarc.md` |
| `data/carbonarc_app_spotify.csv` | Carbon Arc app users YoY % and downloads YoY %, SPOT ticker; monthly and weekly | 9 geos (IN, ID, BR, MX, PH, US, GB, DE, WW); monthly 2021-01-2026-09; weekly 2020-12-28-2026-09-21 | `02_carbonarc.md` |
| `data/carbonarc_app_rivals.csv` | Same metrics for YouTube Music, Apple Music and the Spotify app entity | IN, ID; monthly 2021-01-2026-09 | `02_carbonarc.md` |
| `data/promo_depth.csv` | spotify.com premium page: list price, trial months, intro price/months by plan; snapshot URL per row | 10 countries (+TR, NG); monthly 2023-01-2026-09 | `03_promos.md` |
| `data/kworb_streams_daily.csv` | Daily top-200 chart streams sum (captured days only) | 8 countries; 2023-01-2026-09-26; 83-456 days each | `04_kworb.md` |
| `data/kworb_streams_weekly.csv` | Weekly chart totals (full weeks) plus weekly sum/mean of captured daily charts with `days_observed` | same | `04_kworb.md` |
| `data/google_trends_weekly.csv` | Google Trends index, 5 terms per request (comparable across terms within a country) | 8 countries; weekly 2023-01-01-2026-09-27 | `05_google_trends.md` |
| `data/google_trends_single_term_weekly.csv` | Google Trends, one term per request (own scale; low-volume terms) plus local-language cancel terms for BR/MX/DE | same | `05_google_trends.md` |
| `data/raw/` | Raw pulls, logs, parse audit tables | | |

## Must-know before analysis
1. **Two subscriber totals in MODL.** Q3'26E subs = **305.1m** (rows 21/57, MAU field, Premium segment; matches the handoff) vs **301.6m** (row 44, paying-users field). They are identical in reported quarters and differ by 2.9-5.7m in forecasts. The MODL "Free/Premium Ratio" row (1.647 for Q3'26) is a **beginning-of-period** ratio (lagged one quarter), not the quarter-end ratio (1.633).
2. **Regional rows don't add up exactly.** The four regional sub rows sum to 3-6m above the row-44 total in forecast quarters, and are off by ±2.5-2.9m in 4 reported quarters. Derived RoW MAU vs the MODL "Other Countries" row differs by −14/−15m in some reported quarters and by +7.77 in 2026Q2. There is no regional Ad-Supported split and no contributor counts.
3. **Carbon Arc YoY runs from Jan 2021** (re-pulled; the first pull's empty 2024 was a query-window artifact: Carbon Arc computes YoY only within the requested window). Precision is mixed: see the `precision` column (monthly 0.01pp, weekly full, rivals 2021-24 whole pp). The SPOT ticker and the Spotify app entity differ by up to 10pp in Indonesia 2021 and ~3.5pp in 2023-24. Monthly and weekly series measure different windows: a monthly value ≠ the mean of that month's weekly values. Don't mix frequencies.
4. **Latest-period flags:** Sep 2026 monthly values are a partial month (data to 2026-09-26). The downloads week of 2026-09-21 falls −34% to −54% in every country at once (likely incomplete). Filter on `flag`.
5. **Level series unavailable:** Carbon Arc active-user levels are unusable (month-to-month 2× flips; tiny Indonesia counts). There are no country-level MAU levels from any source here, so app data can't be weighted by country size.
6. **India/Indonesia plan restructuring (Nov-Dec 2025):** the Individual plan is replaced by **Standard / Platinum / Lite** on the premium pages. These are stored as separate plans, not mapped to `individual`. IN Standard ₹139 with a "₹799 for 1 year" intro; ID Standard Rp 59,900 with an intro of Rp 29,900 × 3.
7. **Trial length alternates month to month (1↔3 months)** in most markets. One capture per month samples the promo calendar but can't show all of it. The `intro_price` wording (per month vs total for the period) is not specified on the pages.
8. **kworb India stops at 2026-08-26**, and Jul-Sep 2026 has few captured days in friction markets (IN 4, ID 2) and in the PH control market (1). Captured days are not random (they follow Wayback crawl activity).
9. **Seasonality and event spikes:** Spotify Wrapped (first week of December; weekly downloads up to +46% in PH, +38% in ID), Christmas/New Year in streams, and Feb 28 billing-date spikes in the ALTD card panel. Weekly WW downloads are +22-23% in the weeks of 2025-09-15/22, which covers the Sept 15, 2025 free-tier upgrade date.
10. **Price-change timing:** promo prices are dated by the first monthly capture after the change, not the actual change date.
11. **Google Trends:** a relative index (0-100 per request). Never compare levels across countries or across single-term series. The sampling-noise check was inconclusive (Google served identical cached samples), and English 'cancel Spotify' is mostly 0 outside English markets.
12. **Carbon Arc spend:** ≈122 credits across the two pulls (2,000/day limit). Small results were returned as markdown and transcribed to `data/raw/` without edits; large ones were saved to file by the MCP and parsed by script.

## Key dates (context)
Sept 15, 2025: free tier upgraded globally. ~Aug 1, 2026: free-tier friction in India and Indonesia only. Jan 2026: US price increase (US list $12.99 first seen 2026-02). Q3'26 consensus: free 498m, subs 305m, ratio 1.63.

## Not collected (gaps for a future session)
- Play Store reviews and Bloomberg contributor dispersion (research plan workstreams 8-9). Google Trends is now collected (Step 6).
- Similarweb/Apptopia by country from Bloomberg.
- JioSaavn (not in Carbon Arc); Amazon Music (not searched).

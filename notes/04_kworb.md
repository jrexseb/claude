# Step 4: stream volume (kworb.net Spotify charts)

**Outputs**
- `data/kworb_streams_daily.csv`: one row per country × captured chart day; `value` = sum of the Streams column of the daily top-200 chart.
- `data/kworb_streams_weekly.csv`: long, three **separate** metrics (not interchangeable):
  - `top200_weekly_chart_streams`: Streams sum of a captured **weekly** chart page, which covers a complete chart week. `date` = kworb's chart date (always a Thursday; see below). `days_observed` = 7 by construction.
  - `top200_daily_streams_sum_observed`: sum of the captured daily charts within an ISO week (Monday start). `days_observed` = 1-7. **Partial weeks are not scaled up.** No week has all 7 days (median 1-2).
  - `top200_daily_streams_mean_observed`: mean per captured day in that ISO week (same `days_observed`).
- **Raw:** `data/raw/kworb_captures.csv` (every capture, snapshot URL, parse status), `kworb_daily.csv`, `kworb_weekly_charts.csv`, `kworb_cdx_log.csv`, `kworb_weekly_cdx_log.csv`. The HTML cache is gitignored.
- **Scripts:** `scripts/04_kworb_streams.py` (daily), `04b_kworb_weekly_charts.py` (weekly), `04c_kworb_tidy.py` (tidy).

## Why Wayback
kworb.net serves **only the latest chart** (`/spotify/country/{cc}_daily.html`, `{cc}_weekly.html`). It has no dated archive. The `*_totals.html` pages are cumulative per-song totals, not totals per day. History therefore comes from Wayback captures of those two pages:
- CDX: `https://web.archive.org/cdx/search/cdx?url=kworb.net/spotify/country/{cc}_daily.html&from=2023&output=json&filter=statuscode:200&collapse=timestamp:8` (at most one capture per calendar day), and the same for `_weekly.html`.
- The live page was added for the latest chart.
- The chart date comes from the page (title or header "… Chart - {Country} - YYYY/MM/DD"), **not** from the capture timestamp. Captures showing the same chart date are de-duplicated; their sums never conflicted.

## Coverage (2023-01 to 2026-09-26)
| Country | Daily chart days | Longest gap (days) | Weekly charts | Note |
|---|---|---|---|---|
| US | 456 | 40 | 96 | |
| GB | 349 | 40 | 53 | |
| DE | 255 | 57 | 48 | |
| PH | 163 | **190 (to 2026-09-26)** | 36 | no daily capture from ~Mar 2026 until the live page |
| BR | 128 | 68 | 40 | the weekly CDX for BR failed once (`000`); recovered on rerun |
| ID | 122 | 86 (to 2026-09-26) | 46 | |
| MX | 98 | 49 | 45 | |
| IN | 83 | 67 | 44 | **kworb's India charts stop at 2026-08-26 (daily) and 2026-08-20 (weekly)**; other countries run to 2026-09-26 / 09-24 |

Daily days per year for IN: 22 / 21 / 29 / 11 (2023-26); ID 35 / 34 / 41 / 12; MX 32 / 29 / 22 / 15. For the Jul-Sep 2026 window (after the Aug 1 friction date): IN 4 days, ID 2, PH 1, MX 5, BR 6, US 20.

## Definitions and caveats
- The top-200 sum covers only the 200 most-streamed tracks in a country, not total Spotify streams. It includes Premium and free streams and follows Spotify Charts' own counting rules. Chart rows are 198-200 per page, so a few pages are missing 1-2 rows.
- The weekly chart date is always a **Thursday**. Spotify weekly charts run Friday to Thursday, so it is the week-end date; it is recorded as printed and not shifted.
- Daily and weekly-chart sums have different scales (1 day vs 7 days). Don't combine them in one series.
- Wayback captures are irregular: they cluster around news events and heavy-traffic periods, so the captured days are **not a random sample**.

## Anomalies to know (not interpreted)
- **Early Dec (Spotify Wrapped) and late Dec (Christmas):** chart streams have holiday and seasonal patterns; check `date` before comparing single days.
- **India chart freeze after 2026-08-26 on kworb:** the cause is unknown; it may be a kworb scraping issue. This matters because it overlaps the Aug 2026 friction window.
- kworb itself was about a month stale for India when the live page was first checked on 2026-09-28.

## Blocks and failures (logged)
- CDX returned intermittent 503/504 and `000` (tunnel resets). Retried up to 5× with backoff; see the logs. Two daily captures failed to fetch after 5 attempts (`fetch_failed` in `kworb_captures.csv`).
- No rate-limit (429) responses were seen. Requests were paced at 1.5 s.

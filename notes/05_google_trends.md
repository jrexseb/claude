# Step 6: Google Trends search interest

**Outputs**
- `data/google_trends_weekly.csv`: 5 terms in **one request per country**, so the index is comparable **across terms within a country**. 7,840 rows. Also has `value_pull2` and `abs_diff_pulls`.
- `data/google_trends_single_term_weekly.csv`: **one term per request**, each on its own 0-100 scale (usable resolution for low-volume terms). 6,860 rows. **Not comparable across terms or countries.**
- **Raw:** `data/raw/trends/` (5-term, 2 pulls per country), `data/raw/trends_single/`, plus logs (`trends_log.csv`, `trends_single_log.csv`) and `trends_quality.csv`.
- **Scripts:** `05_google_trends.py` (5-term), `05c_trends_single_terms.py` (single-term), `05b_trends_tidy.py` (tidy).

## Query
- **Client:** `pytrends` (unofficial Google Trends client). `hl=en-US`, `tz=0`, web search, all categories.
- **Timeframe:** `2023-01-01 2026-09-27` → weekly points (weeks start Sunday); 196 weeks.
- **Geos:** IN, ID, BR, MX, PH, US, GB, DE.
- **Terms (English strings in every geo):** "Spotify", "Spotify Premium", "cancel Spotify", "Spotify mod", "Spotify apk".
- **Local-language cancel terms (single-term file only):** "cancelar Spotify" (BR, MX) and "Spotify kündigen" (DE). **None for ID, IN or PH.**
- **Runs:** all 51 requests succeeded (16 five-term + 35 single-term); no rate-limit waits in the single-term run.

## Reliability: read before using
- **The index is relative, not a volume:** 0-100 scaled to the peak week within that request (geo × term set). Values are whole numbers; "<1" arrives as 0.
- **Cross-country comparisons of levels are invalid.** Only compare shapes (changes over time) across countries.
- **Low resolution in the 5-term file:** "Spotify" sets the 100, so the minor terms get compressed. For example "cancel Spotify" is 0 in 93-100% of weeks and "Spotify mod" in 62%. Use the single-term file for minor terms.
- **English "cancel Spotify" is still sparse in non-English markets:** 0 in 73-84% of weeks for BR, DE, ID and MX even as a single term. Use the local phrases for BR/MX/DE; ID has no equivalent here.
- **Sampling noise was NOT measured.** Google builds Trends from a random sample, so a pull on a different day can differ. Both 5-term pulls, made minutes apart, returned **identical** values (corr 1.0), which is consistent with Google serving a cached sample. The check is inconclusive. A proper test would repeat the pull on a later day.
- **Term meaning is broad:**
  - "Spotify" includes navigational searches (people typing it to open the site).
  - "Spotify mod"/"apk" capture interest in modified or pirated apps but also ordinary download searches.
  - "Spotify Premium" mixes purchase intent with support queries.
- **Latest week (2026-09-27)** is flagged `partial_week`.
- **The series is known to shift** when Google changes its data collection (Google shows notes on its charts); none were captured here.

## Coverage
All 8 countries × all terms have 196 weekly points and no missing weeks.

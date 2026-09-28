# Step 3: promo depth (Wayback snapshots of spotify.com premium pages)

**Output:** `data/promo_depth.csv` (2,641 rows, long format; 2023-01 to 2026-09; 10 countries)
**Scripts:** `scripts/03a_wayback_cdx.py` (snapshot list), `scripts/03b_wayback_promos.py` (fetch and parse), `scripts/03c_promo_tidy.py` (tidy output and gap table)
**Raw:** `data/raw/wayback_cdx.csv`, `wayback_cdx_log.csv` (every CDX attempt and HTTP status), `promo_parsed_wide.csv` (one row per country-month-plan, including the card text used), `promo_missing_months.csv`. The HTML cache (`data/raw/wayback_html/`) is gitignored; rerunning 03b re-fetches it.

## Method
- **CDX query:** `https://web.archive.org/cdx/search/cdx?url=spotify.com/{pattern}/premium/&from=202301&output=json&filter=statuscode:200&collapse=timestamp:6` (first HTTP-200 capture per month).
- **Patterns tried:** `{cc}`, `{cc}-en` and the local language (`in-hi`, `id-id`, `br-pt`, `mx-es`, `ph-fil`, `us-es`, `de-de`, `tr-tr`). For the UK: `uk`, `uk-en`, `gb`, `gb-en`.
- **Snapshot choice:** one per country-month. English (`-en`) is preferred when several patterns have a capture that month, then the earliest capture. The `pattern` column in the raw file shows which one was used.
- **Fetch:** `https://web.archive.org/web/{ts}id_/{original}`, following redirects. `snapshot_url` (requested) and `effective_url`/`effective_timestamp` (served) are in every row. In 2 country-months the served capture falls in a different month.
- **Parse:** structural. Each plan-name element is matched to the smallest HTML container holding a per-month price and no other plan name (the plan card). The card gives:
  - `list_price` (the price immediately before or after "/month", "per month", "/mês", "ayda", etc.)
  - `trial_months` ("N months free", "$0 for N months")
  - `intro_price` / `intro_months` ("₹59 for 3 months"; "for 1 year" = 12 months)
- **Fallback:** where no card price exists, the page's English FAQ sentence ("The Spotify Premium Individual plan costs $X per month…") is used. `list_price_source` = `card` or `faq`; 34 rows use the FAQ.
- **Validation:** card and FAQ prices both exist on many pages. They agree in every case (0 conflicts).

## Columns / definitions
- `date` = snapshot month (YYYY-MM). A price change shows up in the first month captured after it happened, not on the actual change date.
- `metric` = `{list_price|trial_months|intro_price|intro_months}_{plan}`. Plans: `individual`, `duo`, `family`, `student`, `mini`, `lite`, `standard`, `platinum`.
- `value` is in local currency; `currency` shows the symbol as printed (Rp and IDR are the same currency, as are $ and MX$ in Mexico, and ₦ and NGN).
- **`intro_price`** is the price displayed for the intro period, exactly as printed. The pages don't say whether "₹59 for 3 months" means per month or for the whole period; for IN/ID/PH several intro offers equal the list price ("IDR 54,990 for 3 months, then IDR 54,990 per month"). Not interpreted.
- **Prepaid cards:** the same plan also appears as a prepaid card ("Pay once in advance… Does not auto-renew") with a per-month equivalent price. The subscription card (first) is kept; the prepaid prices are listed in `other_card_prices` in the raw file (194 rows).

## Coverage (Individual list price, 45 possible months, 2023-01 to 2026-09)
| Country | Missing months | Note |
|---|---|---|
| DE | 0 | |
| GB | 1 (2023-08) | page served without plan cards |
| US | 1 (2023-08) | same |
| TR | 6 | no capture |
| BR | 7 | no capture |
| MX | 8 | no capture (Jan-Feb 2023 not archived) |
| IN | 12 | 2024-10 no capture; **2025-11 on: Individual replaced by Standard/Platinum** (below) |
| PH | 13 | no capture |
| ID | 21 | sparse captures in 2023-24; **2025-11 on: Individual replaced by Standard/Platinum** |
| NG | 24 | sparse captures; `ng-en` CDX failed |

Exact missing months: `data/raw/promo_missing_months.csv`.

## Plan restructuring in India and Indonesia (a definitions break, not a parse failure)
- **IN from 2025-12 and ID from 2025-11:** the pages list **Premium Standard, Premium Platinum and Premium Lite** in place of Individual. These are stored as `standard`, `platinum` and `lite`, **not** mapped to `individual`.
- **IN 2026-08:** Standard ₹139/month with an intro offer of "₹799 for 1 year"; Platinum ₹299/month; Student ₹69.
- **ID 2026-08:** Standard Rp 59,900 (intro Rp 29,900 × 3 months); Platinum Rp 119,900.
- The analysis session must decide whether Standard is the continuation of Individual.
- IN 2025-11 and TR 2025-11: the captured page was a Spotify error page ("Cette page s'est emmêlé les pinceaux"). Logged as `no_plan_blocks_found`.

## Anomalies to know
- **Trial length alternates month to month** (1 ↔ 3 months, sometimes 2 or 4) in most markets. With one capture per month, this series samples a promo calendar; it doesn't show the full calendar. Offer end dates are sometimes printed ("Offer ends September 23, 2026") in `headline_text` in the raw file.
- **Price changes seen (Individual/Standard, first month observed):**
  - US 10.99 (2023-09), 11.99 (2024-07), 12.99 (2026-02)
  - GB 10.99 (2023-09), 11.99 (2024-05), 12.99 (2025-11)
  - DE 10.99 (2023-10), 12.99 (2025-09)
  - IN 139 (2025-08); ID 59,900 (2025-08); PH 169 (2025-08); BR 23.90 (2025-08); MX 129 (2023-09), 139 (2025-09); NG 1,300 (2024-12), 1,600 (2025-08); TR 29.99 (2023-02), 39.99 (2023-07), 59.99 (2024-02), 99 (2025-10)
- Mexico 2025-03, 2025-07 and 2026-02: intro "$19 for 2 months" (from a list price of $129 to $139).

## Blocks and failures (logged, not worked around)
- **CDX API:** frequent 503/504. Every request was retried up to 5 times with backoff; all attempts are in `wayback_cdx_log.csv`. Four patterns failed all 5 attempts: `uk-en`, `gb`, `gb-en` and `ng-en`. The UK is covered by `/uk/premium/` (45 months).
- **Plain `http://` to web.archive.org** is refused by this environment's egress allowlist; all requests use `https://`.
- The egress tunnel occasionally resets connections mid-transfer; these were retried.

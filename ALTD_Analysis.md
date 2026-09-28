# SPOT alternative data: full read of the Bloomberg ALTD export (Sept 24, 2026)

Files: `Alternative Data (1).xlsx` (daily levels) and `Alt Data Year over Year growth  (1).xlsx` (daily YoY, compared with the same weekday 364 days earlier). Coverage runs from Oct 1, 2017 to Sep 16, 2026, 3,273 days with no gaps. Apptopia data ends Sep 9 (7 days missing). Similarweb starts Sep 22, 2021.
See also: [[Projects/Equity Research/SPOT Short/README]] | [[Projects/Equity Research/SPOT_Label_Power_Report_v4.pdf]]

## What each column is
- **Second Measure (US card panel):**
  - Observed Sales: $ charged by Spotify to panel cards.
  - Transactions: billing events. Monthly transactions roughly equal the number of paying accounts, because each account is billed once a month.
  - Customers: distinct payers per day.
  - ATV: sales per transaction, the closest proxy for US gross ARPU. It includes sales tax and plan mix.
  - Transactions per customer and sales per customer.
  - Coverage: only US subscribers billed directly to a card. App Store, Google Play, carrier and bundle billing and gift cards are excluded, and a Family plan counts as one payer.
- **Apptopia:** app time spent and app downloads. Apptopia doesn't say whether these are US-only or global.
- **Similarweb:** web traffic visits.

## Key numbers
| Metric | Level now | Trend |
|---|---|---|
| US ATV | $14.85 (Sep '26) vs $9.74 (Dec '19): +52%, against a +30% list-price rise ($9.99 to $12.99) | ATV steps up ~10-12% on each hike; +11-13% YoY every month Mar-Sep '26 |
| Avg daily transactions (US paying accounts) | ~41-43k/day since Jun '25; ~39-40k in 2024 | Flat for ~15 months after a Jun-Aug '25 step-up |
| Panel sales | $198m (2025); YTD '26 +14.4% | 2019 +22%, 2020 +15%, 2021 +19%, 2022 +10%, 2023 +13%, 2024 +17%, 2025 +7% |
| App time spent | ~221B/day | Growth slowed from +35% (2017) to +20% (2022), +12-14% (2024) and +7-9% (2025-26) |
| App downloads | ~0.86m/day, down from a ~1.1-1.2m 2022 peak | Negative YoY in most months since Jan '23; -1% to -17% in 2026 |
| Web visits | ~19m/day | +9-18% YoY in 2026, faster than in 2024-25 |

## Price-increase events (7-day ATV)
- **Jul 2023 ($9.99 to $10.99):** ATV went from $10.99 (Aug 12) to $11.41 (Aug 26) to $12.04 (Sep 9), fully through in ~6 weeks. Customer growth held at +7-8% YoY, so no visible churn.
- **Jun 2024 ($10.99 to $11.99):** ATV went from $12.29 (Jun 22) to $12.85 (Jul 6) to $13.50 (Jul 20), through in ~4 weeks. **Customer growth then slowed:** +4-5% before, +2-4% in H2'24, around -2% in Apr-May '25. This is the first sign of elasticity.
- **Jan 2026 ($11.99 to $12.99, plus Family, Duo and Student):** a staggered rollout. ATV went from $13.30 (Jan 3) to $13.53 (Jan 17), then $14.68 (Feb 28) and $14.89 (Apr 25). Full effect arrived by April (+12% vs Dec). Paying accounts stayed flat.
- **Cadence:** Jul 2023, Jun 2024, Jan 2026, roughly every 11-19 months. **The Jan 2026 hike laps in Jan-Apr 2027**, so without a new hike US ATV growth falls from ~12% to near 0% in 1H27. ATV YoY also sat at about 0% for Jul-Dec 2025, when the previous hike lapped.

## Inflections and outliers
1. **The Jun-Aug 2025 volume step-up came with lower ATV.** Daily transactions rose from ~38-39k to ~42k while ATV fell to $13.14 in Aug '25 (-3.0% YoY, the lowest since the 2024 hike). This looks like accounts bought with discounted or promotional pricing, consistent with the team's price audit (three free months; the India annual plan at a 52% discount). It also explains why 1H26 volume growth looks like +6-9% YoY: that is the lap of the step-up, and the level has been flat since.
2. **The Jul-Sep 2026 customer "stall"** (+0.5% QTD) is the step-up anniversary, not a fresh break. The underlying level has been flat since mid-2025. **US paid volume is not growing; all US growth is price.**
3. **Feb 28 spikes** (+170-180% every year) are billing-date artifacts: accounts billed on the 29th-31st are charged on the 28th. They are not material, but they inflate February daily averages.
4. **Dec 1-8 spikes** each year are Spotify Wrapped: app time +12-15%, downloads +75% (2024) and +126% (2025), web +54-103%. They show engagement, not monetization.
5. **2017-2019 ATV was falling** (-1% to -2% YoY) during the Student and discount mix era. ATV rose ~4-5% a year in 2020-22 with no Individual price change, driven by Family and Duo hikes and mix.
6. **Weekday and day-of-month effects:** Friday is the highest (~43k in 2025) and the 31st the lowest. Not material.

## Links to gross margin, pricing power and take rate
- **Spotify's Premium GM expansion tracks US price realization.** Correlation between panel ATV YoY and Premium GM y/y bps is 0.87 for Q1'25-Q2'26 and 0.72 including Q4'24.

  | Quarter | ATV YoY | Premium GM y/y |
  |---|---|---|
  | Q1'25 | +9.5% | +332bps |
  | Q2'25 | +8.6% | +171bps |
  | Q3'25 | -1.6% | -34bps |
  | Q4'25 | +0.2% | +10bps |
  | Q1'26 | +6.0% | +129bps |
  | Q2'26 | +11.4% | +174bps |

  **When there is no price increase, margin expansion stops**: costs per subscriber (PSM step-ups, video) keep rising while ARPU does not. Under a pure revenue share a price rise would leave GM% unchanged, so the fact that GM% rises with price means part of the cost base is fixed per subscriber or not tied to price (floors, bundle allocation, Marketplace).
- **FY27 risk (thesis point):** consensus FY27E needs Premium ARPU +5.1% and a music-cost lag of about 1.6pp (Section 11). The US price tailwind laps in 1H27, and 2025 shows what a no-hike stretch does to GM (-34 and +10bps). Consensus therefore implicitly assumes another US hike in 2027, or EM pricing, while label escalators are contractual "irrespective of retail pricing."
- **Take rate (counter-evidence):** H1'26 vs H1'25, panel ATV was +8.7% (sales +15.5%, transactions +6.2%). RIAA shows US wholesale revenue per premium subscriber up only 2.1%. That implies the rights-holder share of US retail fell ~6%, so for now **Spotify is keeping most of the US price increase**. Possible reasons: the audiobook bundle allocation lowering the base labels and publishers are paid on (the MLC case shows the bundle treatment for publishing), Marketplace, and lagged minimum true-ups. RIAA is industry-wide, so this is indicative. H2'26 RIAA data (Mar 2027) is the test.
- **US revenue cross-check:** panel USD growth ran close to Spotify's reported US revenue in 2024 (+16.7% vs +17.4% in EUR). YTD 2026 panel sales are +14.4% in USD. At a weaker dollar, that is roughly low double digits in EUR vs consensus FY26E US revenue +12.5% (EUR 7,277m), which is in line to slightly light. This is rough: the panel excludes app-store billing and ad revenue.
- **Engagement vs monetization:** app time +7-9% against flat US paying accounts means engagement per payer is rising. Music royalties are revenue-based, so this mainly matters for consumption-linked costs (video Partner Program, free-tier streams). Falling downloads point to a saturated US funnel, which supports the mix thesis (North America is 16% of consensus FY26-28 net adds).

## Open questions and caveats
- Is the mid-2025 volume step-up promos, a panel change, or real? Check Spotify Q2-Q3'25 commentary on US promotions.
- Is Apptopia US-only or global? Bloomberg's ALTD help (DOCS 2229054) should say.
- Panel bias: card-billed US payers only; Family plans count as one payer; free trials are invisible.

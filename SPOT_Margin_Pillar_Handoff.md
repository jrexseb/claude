# SPOT margin pillar: handoff (Sept 28, 2026)

Condensed state of the Citadel SPOT short margin pillar after the Sept 27 sessions. Detail lives in `SPOT_Margin_Variant_Views.md` (sections 12-14) and `SPOT_FreeToPaid_LabelPayout_Analysis.pdf` (15 pages, restyled Sept 27).

## Thesis (current structure)

1. **Lead: forward KPI call.** Bloomberg consensus holds free users per payer flat at ~1.63-1.65 through FY28 only by assuming free-user growth falls from +14% to ~+8% by Q2'27 while subscriber growth holds 8-9%. If subscriber growth slows (Jan 2026 price increase laps in 1H27; US/EU base saturating), Spotify either (A) lets free users grow and the ratio rises (1.69 at +11% free growth, 1.73 at +14%, Q2'27) or (B) adds free-tier friction and MAU / ad growth miss consensus. Both are worse than consensus.
2. **Margin kicker.** 20-F (FY21-FY25): the royalty % for certain labels depends on subscriber numbers, the free-to-paid ratio and churn. A rising ratio puts those targets at risk. Precedent: UMG 2017, ~55% to ~52% on subscriber goals.
3. **Statistics = supporting evidence, not proof.** Contract mechanics to be confirmed via primary research / channel checks at the finalist stage.

## Stats to cite (two-pager)

| Finding | Result |
|---|---|
| Premium GM y/y vs ratio y/y (18 qtrs) | r = -0.46, p = 0.054 |
| After price control | -81bp per +0.1 ratio (p = 0.10); R² 0.50 to 0.59 |
| Robustness | negative in 9 of 10 specs |
| Annual 2020-25 | r = -0.68 (n = 6) |
| UMG growth gap vs Spotify cost ratio | r = 0.62, p = 0.013 (strongest stat; rate moves are real transfers) |
| Quote | McCarthy (CFO), Feb 26, 2019: "Because of the structure of our license agreements. The labels want a less good experience. So that people migrate to premium." |

**Do not cite:** fully controlled coefficients (-22 to -44bp, p 0.17-0.52), subscriber growth as a driver (p = 0.34), UMG residual (r = 0.18). Counter-evidence to have ready: rate term -EUR 511m in 2024 with ratio flat; -EUR 135m in 1H26 while ratio rose. Say "directionally consistent," never "significant."

## Q3'26 markers (early Nov)

Consensus: free 498m, subs 305m, ratio 1.63. Free >~505m with subs at/below consensus = outcome A; free <~490m with subs at/below consensus = outcome B. Also watch "prior period estimates" on rights-holder liabilities.

## Next high-usage session: research plan

Pull from the Bloomberg terminal first: (a) new ALTD export through late Sept with country-level Apptopia (downloads, DAU) and Similarweb if available; (b) Second Measure refresh plus cohort retention view; (c) MODL regional MAU rows; (d) contributor-level consensus for ad-supported MAU and subs (Q4'26, Q2'27).

| # | Workstream | Proves |
|---|---|---|
| 1 | Regional MAU/sub mix from 6-Ks vs Bloomberg regional forecasts; regional free-per-payer ratio | Whether flat consensus depends on EM free growth collapsing |
| 2 | Country app data (India, Indonesia, Brazil, Mexico, US, UK, Germany) pre/post Aug 2026 friction | Whether free growth slows outside friction markets (Sept 2025 free-tier upgrade still live elsewhere) |
| 3 | US card panel refresh | US paying growth ~0%, so 8-9% must come from lower-ARPU markets |
| 4 | Promo depth by market (Wayback snapshots of premium pages) | Sub growth bought with promos that must lap |
| 5 | Google Trends "Spotify" / "cancel Spotify" by country | Free momentum and churn intent |
| 6 | Q3 guide vs consensus; friction/conversion commentary since Q3'25 | Consensus position vs guide |
| 7 | Label comments on free tier (Streaming 2.0) | Why Spotify can't just let free users run |
| 8 | Consensus dispersion | Tight consensus vs one or two optimistic brokers |

Also check the Carbon Arc connector (now connected) for country-level Spotify card spend or app data before paying for exports; its discovery tools are free, queries are billed.

Run 1 and 2 first. If the free-user slowdown depends almost entirely on India/Indonesia, the forward call is strong; if free growth is already slowing everywhere, rethink before the two-pager.

## Open items

- Align one subscriber forecast with the teammate who owns the pricing pillar.
- Section 13 tests (2017 calibration, 2025 renewal baseline, regional ratio) are lower priority for the two-pager.
- Submission deadline: early October 2026.

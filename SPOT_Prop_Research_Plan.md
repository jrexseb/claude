# SPOT margin pillar: prop / alt-data research plan (Sept 28, 2026)

Plan only; no scraping or billed queries run yet. Builds on `SPOT_Margin_Pillar_Handoff.md`.

## The two questions the data must answer

1. **Free users:** does free-user growth fall from +14% to ~+8% by Q2'27 (what consensus needs for a flat ~1.65 ratio), and if it does, is that only because of the Aug 2026 friction in India/Indonesia?
2. **Subscribers:** can subs hold +8-9% once the Jan 2026 US price rise laps, or is growth being bought with promos in lower-ARPU markets?

Everything below maps to one of these. Anything that does not was cut.

## Vault check (Alternative-3rd Party Data-Prop Research; the `ALT Data` folder is empty)

| Already have | Coverage | Gap |
|---|---|---|
| Second Measure (US card panel), daily | Oct 2017 to Sep 16, 2026 | Last 2 weeks of Q3; no cohort retention |
| Apptopia time spent + downloads | to Sep 9, 2026; geography unknown (probably global) | No country split, no DAU/MAU, no competitors |
| Similarweb visits | Sep 2021 to Sep 16, 2026; single series | No country split |
| MODL regional rows (`MODL_SPOT_US_B2.xlsx`) | Subs by EU/NA/LatAm/RoW; MAU by EU/NA/LatAm; Q2'24A to Q3'28E | Only the mean; no contributor count or dispersion |
| Guidance vs actual (`FreeToPaid_Analysis/spot_guidance_vs_actual.csv`) | Historical | Q3'26 guide to confirm against 6-K |

So the handoff's Bloomberg item (c), regional MODL rows, is already done. Do not re-pull it.

## Workstreams, ranked

| # | Data | Source | Countries / scope | What it proves | Kill signal |
|---|---|---|---|---|---|
| 1 | **Regional free per payer, actual vs consensus** | 6-Ks (have) + MODL regional rows (have) | EU, NA, LatAm, RoW (RoW MAU = total less the three) | Whether consensus's free slowdown is concentrated in RoW (friction markets) | Consensus slows free growth evenly across regions |
| 2 | **Country app usage, pre/post friction** | Carbon Arc app data if available; else Bloomberg ALTD Apptopia by country | India, Indonesia (friction) vs Brazil, Mexico, Philippines (EM control) vs US, UK, Germany | Free growth slows only where friction was added; still ~+14% in control EM | Control EM app MAU already slowing to ~+8% |
| 3 | **Competitor app share in India/Indonesia** | Same app source: YouTube Music, JioSaavn, Apple Music, Amazon Music | India, Indonesia | Friction pushes users to rivals (outcome B: MAU loss, not conversion) | Rival downloads flat while Spotify conversion rises |
| 4 | **Country stream volume** | kworb.net mirror of Spotify Charts (daily top-200 total streams by country) | Same 8 countries, 2023 to now | Independent usage series; checks app data | Diverges from app data with no explanation |
| 5 | **Promo depth by market** | Wayback snapshots of `spotify.com/{cc}/premium` (monthly, 2023 to now) + live pages | Same 8 + Turkey, Nigeria | Trial length and discount depth rising where subs grow fastest; lap risk | Promos flat or shallower |
| 6 | **US paying accounts + retention** | Second Measure refresh (Bloomberg) and Carbon Arc US card spend as cross-check | US | US paid volume ~0%; so 8-9% must come from lower-ARPU markets | US accounts reaccelerate |
| 7 | **Search intent** | Google Trends (free) | Same 8 countries; "Spotify", "Spotify Premium", "cancel Spotify", "Spotify premium apk" / "Spotify mod" | Free momentum, churn intent, and piracy substitution after friction | No change around Aug 2026 |
| 8 | **Friction reaction** | Google Play reviews (google-play-scraper), Spotify app | India, Indonesia vs Brazil | Volume of reviews citing ads / verification / "premium" after Aug 2026 | No change in complaint share |
| 9 | **Consensus dispersion** | Bloomberg BEst by broker | Q3'26, Q4'26, Q2'27, FY27 | Tight consensus vs one or two optimistic brokers | Wide dispersion (no clear consensus to bet against) |

Run 1 and 2 first (handoff rule): if the free slowdown in consensus depends on RoW and control EM is still growing ~+14%, the forward call holds; if free growth is already slowing everywhere, rethink before the two-pager.

## The build: a Q3'26 free-user nowcast

Combine 2, 4 and 7 into a regional free-MAU nowcast: regress reported regional Ad-Supported MAU on country app MAU/DAU (aggregated to region) and chart streams, backtest Q1'22 to Q2'26, then forecast Q3'26 against consensus 498m. Pre-registered read: >~505m with subs at/below 305m = outcome A; <~490m = outcome B. Caveat: Spotify MAU includes web, desktop and connected devices, so the backtest error sets how much weight it gets.

## Carbon Arc (connected; discovery free, queries billed)

Step 1, free discovery only: `search_entities` for Spotify and the four competitors, `get_insights_from_entity` on each, `data_library` for field definitions and geography.

Step 2, billed queries only where discovery shows coverage that fills a gap above:

| Priority | Query | Replaces / cross-checks |
|---|---|---|
| 1 | Spotify app MAU/DAU/downloads by country, weekly, Jan 2024 to latest | Bloomberg Apptopia country ask (WS2) |
| 2 | Same for YouTube Music, JioSaavn, Apple Music in India/Indonesia | WS3 |
| 3 | Spotify card spend, transactions, customers; US plus any non-US geography; cohort retention if offered | Second Measure refresh (WS6); non-US would be new |
| 4 | Web traffic by country | Similarweb country ask |

Skip Carbon Arc's filing/transcript/thesis search: those sources are already in the vault.

## Bloomberg terminal: exact asks

Pull only what Carbon Arc does not cover after Step 1.

| # | Function | What | Period | Needed if |
|---|---|---|---|---|
| 1 | ALTD > Second Measure | Daily sales, transactions, customers, ATV; plus the cohort / retention view | Sep 16 to latest (append to existing file) | Always (Q3 close) |
| 2 | ALTD > Apptopia | Country filter: downloads, DAU, MAU for SPOT and, if offered, the four competitors; also confirm what geography the existing series is (DOCS 2229054) | Jan 2024 to latest, weekly | Carbon Arc lacks country app data |
| 3 | ALTD > Similarweb | Visits by country | Jan 2024 to latest | Carbon Arc lacks country web |
| 4 | BEst / EE by broker | Contributor-level Ad-Supported MAU, Premium subs, MAU, Ad-Supported revenue: count, high, low, and 4-week revisions | Q3'26, Q4'26, Q2'27, FY27 | Always |
| 5 | BEst by broker | How many brokers supply the regional sub/MAU rows | Q4'26, FY27 | Always (tells us how thin regional consensus is) |
| 6 | SI / OMON | Short interest, days to cover, borrow cost; options implied move into Q3 | Latest | For the timing slide |

Not needed from Bloomberg: regional MODL rows (have), historical KPIs (6-Ks), transcripts (have), SPLC.

## Order of work (deadline early Oct)

1. Carbon Arc free discovery (minutes; decides Bloomberg asks 2-3).
2. Bloomberg pull (Joel): asks 1, 4, 5, 6 plus whichever of 2-3 remain.
3. Workstream 1 from files already in the vault.
4. Scrapes in parallel: Google Trends, kworb, Wayback promo pages, Play reviews.
5. Billed Carbon Arc queries.
6. Nowcast and one exhibit: free growth by country, friction vs control, with Sept 15, 2025 and Aug 2026 marked.

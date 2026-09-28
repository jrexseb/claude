# Analysis 1: is free-user growth slowing only where friction was added, or everywhere?

Session date 2026-09-28. Branch built on `claude/inspiring-davinci-tjhtfe` (PR #1 not merged). Script: `scripts/10_free_growth_analysis.py`; tables: `analysis/tables/`. **No final charts yet.** This summary comes first for review.

Groups are **unweighted** country means (no country MAU levels exist; INDEX item 5). Friction = IN, ID. Other EM = BR, MX, PH. Developed = US, GB, DE. Flagged partial periods are excluded (Sep 2026 monthly, the week of 2026-09-21). "YoY" = Carbon Arc app-panel YoY %.

## Bottom line
1. **Not slowing everywhere, and friction did not cause the friction-market slowdown.** IN/ID app-user growth fell from ~20% (mid-2025) to ~1-2% by Jun-Jul 2026, **before** the Aug 1 friction. There was no further step down after Aug 1: the friction-minus-EM gap changed by −0.05pp (weekly, 9 weeks pre vs 7 post, Welch p = 0.90; autocorrelation makes that p optimistic). Other EM stayed flat at ~4-5%. Developed markets **accelerated**, from about −1% (Mar-Apr 2026) to +6% (Aug-Sep 2026).
2. **Reported free growth is already outpacing paid, and the gap is widening.** Ad-Supported MAU y/y minus subs y/y went from −3.1pp (Q1'25) to +1.7 (Q4'25), +4.9 (Q1'26) and +5.4pp (Q2'26). Free per payer went from 1.57 to 1.65. This is the thesis, in reported numbers.
3. **But the app panel stopped tracking reported free users in 2026, so items 1-3 below carry less weight.** Before the upgrade, WW app-user YoY tracked Ad-Supported MAU y/y closely: q/q changes r = 0.66, p = 0.004, n = 17 (full sample); residuals within ±3pp through Q4'25. In Q1-Q2'26, reported free growth ran **+5.8 and +6.1pp above** what the app panel implies. In the 2024Q2-2026Q2 window alone, levels are r = 0.13, p = 0.75, n = 9. The app panel also correlates as strongly with subs as with free users (it counts all app users), so it cannot separate free from paid.
4. **The Q3'26 read depends on which regime holds.** App model only: ad MAU +9.9% y/y ≈ **490m** (at the outcome-B line, under consensus 498m). App model plus the 1H26 residual: +15.8% ≈ **517m** (outcome A). The same pre-registered thresholds fall on either side, so the app panel alone can't call Q3.

## Build results
**1. App users YoY, weekly (window means, %)**

| Window | Friction | Other EM | Developed | WW |
|---|---|---|---|---|
| Jun 16-Sep 8, 2025 (pre upgrade) | 17.0 | 5.3 | 1.4 | 6.3 |
| Sep 15-Dec 8, 2025 (post upgrade) | 14.0 | 4.8 | 1.7 | 6.5 |
| Apr-Jun 2026 | 3.2 | 4.0 | 0.8 | 4.0 |
| Jun 1-Jul 27, 2026 (pre friction) | 1.8 | 4.4 | 3.0 | 4.5 |
| Aug 3-Sep 14, 2026 (post friction) | 1.9 | 4.5 | 6.0 | 6.1 |

Monthly data give the same shape: IN from 18.8% (Sep 2025) to 5.7% (Aug 2026); ID from 15.6% to 4.8%; DE from 1.5% (Mar 2026) to 6.6%; US from −3.1% (Apr) to +2.2% (Aug).

**2. Friction minus other-EM gap:** +25 to +45pp in 2022-23 (ID/IN boom), +8 to +14pp through 2025, then it crossed zero around May 2026 and has been −2 to −3pp since. The convergence happened in Nov 2025-Jun 2026, not at Aug 2026.

**3. Downloads YoY:** too noisy to carry weight. Against reported free users: r = 0.37, p = 0.13, n = 18. IN weekly downloads run from −54% to +44%. Direction only: the friction group was −4% to −13% in 2026 with no clear Aug break (gap −5.7pp post vs pre, p = 0.14). Developed markets turned positive in 2026 (US +4 to +11% Feb-May; GB +26% and DE +13% in Aug).

**4. WW app vs reported (quarterly, %)**

| Qtr | App users WW (weekly avg) | Reported ad MAU y/y | App-implied | Residual | Subs y/y |
|---|---|---|---|---|---|
| Q1'25 | 5.5 | 9.0 | 9.9 | −0.9 | 12.1 |
| Q3'25 | 6.2 | 10.9 | 10.7 | +0.3 | 11.5 |
| Q4'25 | 6.5 | 12.0 | 11.1 | +0.9 | 10.3 |
| Q1'26 | 4.4 | 14.2 | 8.4 | **+5.8** | 9.3 |
| Q2'26 | 4.0 | 14.1 | 8.0 | **+6.1** | 8.7 |

The fit uses 2022Q1-2025Q3 (n = 15, R² = 0.93). The level fit is dominated by the 2023-24 downtrend, so treat R² as flattering. Subs ran **below** app-implied by 1.5-2.4pp in Q4'25-Q2'26: paid growth lagged app activity while free growth beat it.

## Corroboration
| Source | Read | For / against thesis |
|---|---|---|
| **Rivals (Carbon Arc)** | YouTube Music users YoY slowed alongside Spotify: IN from 30% to 7%, ID from 25% to 6% (Jun 2025 to Sep 2026). There is no post-Aug jump in YTM, so no visible switching from friction. | The IN/ID slowdown looks like the whole category maturing, not Spotify friction. **For** "not a friction effect". **Against** in that IN/ID free growth may be slowing on its own, which is what consensus needs. |
| **Regional consensus (MODL)** | Consensus Europe MAU slows from +12% (Q1'26A) to +2% (Q4'26E) and −1% (Q1'27E) while Europe subs hold +5-6%. RoW free (approx.) stays at +16-20% until Q1'27, then drops to ~10%. | **For:** the consensus slowdown needs Europe free growth to fall hard as the Sept 2025 upgrade laps, yet developed-market app users are *accelerating*. Europe reported: MAU +4% → +12% while subs went +8.6% → +5.8% (free outpacing paid in the EU). |
| **kworb** (top-200 chart streams) | Negative YoY almost everywhere after Aug 1 (US −11%, GB −12%, MX −13%, IN −11%, ID +5%). India had 1 weekly chart and 4 daily days, and India stops on 2026-08-26. | **Neither.** Chart concentration ≠ usage; the samples are tiny. Low weight. |
| **Google Trends** "Spotify" (YoY of window mean) | IN +3%, ID +2% after Aug (no drop). US −13%, DE −26%, BR −14%, MX −14%, GB +10%. | **Against** the developed-market acceleration (search interest in US/DE fell); **for** "no friction shock". Relative index; sampling noise unmeasured. |
| **Trends "Spotify Premium"** | Up after Aug in IN (+42%) and ID (+33%), but also in PH (+33%), BR (+30%) and GB (+46%). | Not specific to friction markets. Neutral. |
| **Trends mod/apk** | Down 27-66% YoY everywhere, including IN/ID after Aug. | No sign of a shift to piracy. Neutral. |
| **Promo depth** | IN/ID: Standard launched at ₹199 / Rp 79,900 (Dec 2025-Mar 2026), cut back to ₹139 / Rp 59,900 by Jun 2026; with friction came "₹799 for 1 year" (IN, Aug) and Rp 29,900 × 3 (ID, ~50% off). US/GB/DE trial length flat at ~1.7-2.3 months. | **Against (subs side):** friction came with deeper promos, which can lift IN/ID subs near term. **For (later):** promo-bought subs lap in 2027. Developed markets show no promo escalation. |

## Evidence for the thesis (free outpacing paid)
- Reported: free y/y − subs y/y widened for 4 straight quarters, to +5.4pp; ratio 1.57 → 1.65.
- Subs have come in below app-implied for 3 quarters; the US paid volume has been flat since mid-2025 (ALTD); Europe subs slowed from +8.6% to +5.8%.
- Developed-market app users are accelerating (US/GB/DE from about −1% to +6%), while US paid accounts are flat. That points to growth skewed toward free users (an inference: app users include payers).
- The friction-market slowdown predates friction and also hits YouTube Music. So it is not evidence that friction "works", and nothing shows a global free slowdown outside IN/ID.

## Evidence against
- **The WW app panel slowed from 6.5% (late 2025) to 4.0% (Q2'26)**, though it was back to 6.1% in Aug-Sep 2026 on the developed-market pickup. If the pre-2026 app-to-free relationship comes back, Q3 ad MAU ≈ 490m, below consensus. That would mean consensus's free slowdown is happening and the ratio stays flat. This is the strongest counter.
- IN/ID app growth fell to ~4-5%. These are large free markets; if RoW free growth follows, consensus's RoW slowdown may arrive early.
- Deeper IN/ID promos could support sub growth near term.
- Google Trends "Spotify" fell YoY in US/DE/BR/MX in Aug-Sep 2026.

## Data gaps that affect these conclusions
- **App users ≠ free users** (includes payers; r with subs ≈ r with free). There are no country MAU levels, so groups are unweighted and IN/ID can't be sized within RoW (INDEX 5).
- **The 2026 app-vs-reported break is unexplained.** Candidates: growth on non-app surfaces (web, TV, cars), markets outside the panel, or reactivations from the Sept 2025 upgrade. None can be tested with data here.
- **The post-friction window is 7 weeks.** Sep 2026 monthly is partial; the last downloads week is incomplete (INDEX 4).
- ID 2023-24 ticker vs app-entity gap (possibly Spotify Lite) inflates ID's 2023-24 boom and the lap that followed (INDEX 3).
- kworb India stops 2026-08-26, and post-friction samples are 4 days (IN), 2 (ID) and 1 (PH) (INDEX 8).
- Trends sampling noise was not measured; there are no local-language cancel terms for IN/ID/PH (INDEX 11).
- Regional MAU Q4'25-Q2'26 carries the −15m / +7.8m Other-Countries discrepancies (INDEX 2), so the Europe free-growth spike is approximate.
- Not collected: Play Store reviews, contributor dispersion, country Similarweb/Apptopia.

## Charts (`analysis/charts/`, script `scripts/11_charts.py`)
1. `01_app_users_yoy_groups.png`: app users YoY by group plus WW, monthly and weekly, 2021 on; Sept 15, 2025 and Aug 1, 2026 marked.
2. `02_friction_minus_em_gap.png`: India/Indonesia minus Brazil/Mexico/Philippines, weekly and monthly.
3. `03_app_downloads_yoy_groups.png`: downloads YoY by group, monthly (weekly too volatile to read).
4. `04_ww_app_vs_reported.png`: reported Ad-Supported MAU and subs y/y vs app-implied, quarterly.
5. `05_regional_mau_vs_subs.png`: Europe and North America MAU vs subs y/y, reported and consensus.
6. `06_in_id_spotify_vs_youtube_music.png`: Spotify vs YouTube Music app users YoY, India and Indonesia.

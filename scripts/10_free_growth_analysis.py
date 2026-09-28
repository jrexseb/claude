"""Analysis 1: is free-user growth slowing only where friction was added (IN/ID, ~Aug 2026), or everywhere?

Builds the tables behind analysis/01_free_growth_summary.md. No charts (pending review of the summary).
Inputs: data/carbonarc_app_spotify.csv, data/carbonarc_app_rivals.csv, data/reported_kpis_quarterly.csv,
data/regional_consensus.csv, data/kworb_streams_weekly.csv, data/google_trends_*.csv, data/promo_depth.csv.
Outputs: analysis/tables/*.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

FRIC, EM, DEV = ["IN", "ID"], ["BR", "MX", "PH"], ["US", "GB", "DE"]
EVENTS = {"free_tier_upgrade": "2025-09-15", "friction_in_id": "2026-08-01"}


def add_groups(w):
    w = w.copy()
    w["FRICTION"] = w[FRIC].mean(axis=1)
    w["OTHER_EM"] = w[EM].mean(axis=1)
    w["DEVELOPED"] = w[DEV].mean(axis=1)
    w["GAP_FRICTION_MINUS_EM"] = w["FRICTION"] - w["OTHER_EM"]
    return w


# ---- Carbon Arc app data (exclude flagged partial/incomplete periods; keep wrapped weeks) ----
ca = pd.read_csv(ROOT / "data/carbonarc_app_spotify.csv", parse_dates=["date"])
ca = ca[ca.flag.isna() | (ca.flag == "wrapped_week")]
panels = {}
for freq in ["month", "week"]:
    for metric in ["app_users_yoy_pct", "app_downloads_yoy_pct"]:
        w = ca[(ca.frequency == freq) & (ca.metric == metric)].pivot(index="date", columns="country", values="value")
        w = add_groups(w)
        for k, v in EVENTS.items():
            w[f"event_{k}"] = (w.index >= pd.Timestamp(v)) & (w.index - pd.Timedelta(days=31 if freq == "month" else 7) < pd.Timestamp(v))
        w.to_csv(OUT / f"app_{metric.replace('_yoy_pct', '')}_yoy_{freq}ly_groups.csv")
        panels[(freq, metric)] = w

# ---- Window means (weekly) and Aug-2026 pre/post test on the friction gap ----
WINDOWS = {
    "Jun16-Sep08_2025 (pre upgrade)": ("2025-06-16", "2025-09-08"),
    "Sep15-Dec08_2025 (post upgrade)": ("2025-09-15", "2025-12-08"),
    "Apr06-Jun29_2026": ("2026-04-06", "2026-06-29"),
    "Jun01-Jul27_2026 (pre friction)": ("2026-06-01", "2026-07-27"),
    "Aug03-Sep14_2026 (post friction)": ("2026-08-03", "2026-09-14"),
}
rows, tests = [], []
for metric in ["app_users_yoy_pct", "app_downloads_yoy_pct"]:
    w = panels[("week", metric)]
    for lab, (a, b) in WINDOWS.items():
        r = w.loc[a:b, FRIC + EM + DEV + ["WW", "FRICTION", "OTHER_EM", "DEVELOPED", "GAP_FRICTION_MINUS_EM"]].mean()
        rows.append({"metric": metric, "window": lab, "n_weeks": len(w.loc[a:b]), **r.round(2).to_dict()})
    pre = w.loc["2026-06-01":"2026-07-27", "GAP_FRICTION_MINUS_EM"]
    post = w.loc["2026-08-03":"2026-09-14", "GAP_FRICTION_MINUS_EM"]
    t = stats.ttest_ind(post, pre, equal_var=False)
    tests.append({"metric": metric, "test": "friction gap post-Aug1 minus pre (weekly, Welch)",
                  "diff_pp": round(post.mean() - pre.mean(), 2), "p": round(t.pvalue, 3),
                  "n_pre": len(pre), "n_post": len(post),
                  "caveat": "weekly YoY is autocorrelated; p is optimistic"})
pd.DataFrame(rows).to_csv(OUT / "app_window_means_weekly.csv", index=False)

# ---- Step 4: does WW app users YoY track reported Ad-Supported MAU y/y? ----
k = pd.read_csv(ROOT / "data/reported_kpis_quarterly.csv").pivot(index="date", columns="metric", values="value")
k.index = pd.PeriodIndex(k.index, freq="Q")
kyoy = (k / k.shift(4) - 1) * 100


def q_mean(freq, metric, c="WW"):
    s = panels[(freq, metric)][c].dropna()
    return s.groupby(s.index.to_period("Q")).mean()


tq = pd.DataFrame({
    "app_users_ww_monthly": q_mean("month", "app_users_yoy_pct"),
    "app_users_ww_weekly": q_mean("week", "app_users_yoy_pct"),
    "app_downloads_ww_monthly": q_mean("month", "app_downloads_yoy_pct"),
    "reported_ad_mau_yoy": kyoy["ad_supported_mau"],
    "reported_subs_yoy": kyoy["premium_subs"],
    "reported_mau_yoy": kyoy["mau_total"],
}).loc["2022Q1":]
tq["reported_free_minus_subs_pp"] = tq.reported_ad_mau_yoy - tq.reported_subs_yoy
tq["ad_mau_level_m"] = k["ad_supported_mau"]
tq["subs_level_m"] = k["premium_subs"]
tq["free_per_payer"] = k["ad_supported_mau"] / k["premium_subs"]

corr = []
full = tq.dropna(subset=["reported_ad_mau_yoy"])
for a in ["app_users_ww_monthly", "app_users_ww_weekly", "app_downloads_ww_monthly"]:
    for b in ["reported_ad_mau_yoy", "reported_subs_yoy", "reported_mau_yoy"]:
        for label, sub in [("2022Q1-2026Q2", full), ("2024Q2-2026Q2", full.loc["2024Q2":])]:
            x = sub[[a, b]].dropna()
            r, p = stats.pearsonr(x[a], x[b])
            dx = x.diff().dropna()
            r2, p2 = stats.pearsonr(dx[a], dx[b]) if len(dx) > 3 else (np.nan, np.nan)
            corr.append({"app": a, "reported": b, "sample": label, "r_levels": round(r, 2), "p_levels": round(p, 3),
                         "n": len(x), "r_qoq_changes": round(r2, 2), "p_qoq_changes": round(p2, 3), "n_changes": len(dx)})
pd.DataFrame(corr).to_csv(OUT / "app_vs_reported_correlations.csv", index=False)

# Fit on 2022Q1-2025Q3 (before the Sept 2025 upgrade shows up), HAC SEs; residuals after.
fit = full.loc[:"2025Q3"]
nowcast = {}
for dep in ["reported_ad_mau_yoy", "reported_subs_yoy"]:
    m = sm.OLS(fit[dep], sm.add_constant(fit.app_users_ww_weekly)).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    pred = m.predict(sm.add_constant(tq.app_users_ww_weekly))
    tq[f"{dep}_app_implied"] = pred
    tq[f"{dep}_residual"] = tq[dep] - pred
    nowcast[dep] = {"const": m.params["const"], "slope": m.params["app_users_ww_weekly"],
                    "slope_p_hac": m.pvalues["app_users_ww_weekly"], "r2": m.rsquared, "n_fit": int(m.nobs)}
tq.to_csv(OUT / "ww_app_vs_reported_quarterly.csv")
pd.DataFrame(nowcast).T.to_csv(OUT / "app_to_reported_fit.csv")

# Q3'26 implied ad-supported MAU level: (a) model only, (b) model + average Q1-Q2'26 residual.
base = k.loc[pd.Period("2025Q3", "Q"), "ad_supported_mau"]
app_q3 = tq.loc[pd.Period("2026Q3", "Q"), "app_users_ww_weekly"]
nc = nowcast["reported_ad_mau_yoy"]
g_model = nc["const"] + nc["slope"] * app_q3
resid = tq.loc["2026Q1":"2026Q2", "reported_ad_mau_yoy_residual"].mean()
pd.DataFrame([
    {"case": "app model only", "yoy_pct": g_model, "ad_mau_m": base * (1 + g_model / 100)},
    {"case": "app model + Q1-Q2'26 residual", "yoy_pct": g_model + resid, "ad_mau_m": base * (1 + (g_model + resid) / 100)},
    {"case": "consensus (MODL row 22)", "yoy_pct": (498.2 / base - 1) * 100, "ad_mau_m": 498.2},
]).round(1).to_csv(OUT / "q3_26_ad_mau_app_nowcast.csv", index=False)

# ---- Regional consensus: approx regional free = MAU - subs (inherits segment overlap; see notes/01) ----
rc = pd.read_csv(ROOT / "data/regional_consensus.csv").pivot_table(index="date", columns=["metric", "country"], values="value")
reg = {}
for name, mau_metric in [("Europe", "mau"), ("North America", "mau"), ("Latin America", "mau"), ("Rest of World", "mau_row_derived")]:
    mau, subs = rc[(mau_metric, name)], rc[("premium_subs", name)]
    free = mau - subs
    reg[f"{name}|mau_yoy"] = (mau / mau.shift(4) - 1) * 100
    reg[f"{name}|subs_yoy"] = (subs / subs.shift(4) - 1) * 100
    reg[f"{name}|free_approx_yoy"] = (free / free.shift(4) - 1) * 100
    reg[f"{name}|free_per_payer_approx"] = free / subs
reg = pd.DataFrame(reg)
reg["flag"] = rc[("mau", "Europe")].index.map(lambda d: "reported" if d <= "2026Q2" else "forecast")
reg.to_csv(OUT / "regional_consensus_growth.csv")

# ---- Rivals (IN/ID monthly users YoY) ----
rv = pd.read_csv(ROOT / "data/carbonarc_app_rivals.csv", parse_dates=["date"])
rv = rv[(rv.metric == "app_users_yoy_pct") & rv.flag.isna()].pivot_table(index="date", columns=["country", "app"], values="value")
rv.columns = [f"{c}|{a}" for c, a in rv.columns]
rv.to_csv(OUT / "rivals_users_yoy_monthly.csv")

# ---- kworb: YoY of weekly chart totals vs nearest chart 357-371 days earlier ----
kw = pd.read_csv(ROOT / "data/kworb_streams_weekly.csv", parse_dates=["date"])
kw = kw[kw.metric == "top200_weekly_chart_streams"]
ky = []
for c, g in kw.groupby("country"):
    s = g.set_index("date").value.sort_index()
    for dt, v in s.items():
        lag = s[(s.index >= dt - pd.Timedelta(days=371)) & (s.index <= dt - pd.Timedelta(days=357))]
        if len(lag):
            ky.append({"date": dt, "country": c, "yoy_pct": (v / lag.iloc[0] - 1) * 100, "lag_date": lag.index[0]})
ky = pd.DataFrame(ky)
ky["period"] = np.select([ky.date >= "2026-08-01", ky.date >= "2026-01-01", ky.date >= "2025-07-01"],
                         ["2026-08-01 on (post friction)", "2026H1-Jul", "2025H2"], "earlier")
ky.pivot_table(index="period", columns="country", values="yoy_pct", aggfunc=["mean", "count"]).round(1) \
  .to_csv(OUT / "kworb_weekly_chart_yoy_by_period.csv")

# ---- Google Trends: YoY of window means ----
TW = {"Jun-Aug 2025": ("2025-06-01", "2025-09-07"), "Sep15-Dec 2025": ("2025-09-14", "2025-12-07"),
      "Jun-Jul 2026 (pre friction)": ("2026-06-01", "2026-07-31"), "Aug-Sep 2026 (post friction)": ("2026-08-02", "2026-09-20")}
g5 = pd.read_csv(ROOT / "data/google_trends_weekly.csv", parse_dates=["date"])
g1 = pd.read_csv(ROOT / "data/google_trends_single_term_weekly.csv", parse_dates=["date"])
g1 = g1[g1.flag.isna()]
trows = []
for df, metric in [(g5, "trends_index:Spotify")] + [(g1, m) for m in g1.metric.unique()]:
    x = df[df.metric == metric].pivot(index="date", columns="country", values="value")
    x = x[x.index < "2026-09-27"]
    for lab, (a, b) in TW.items():
        cur = x.loc[a:b].mean()
        prev = x.loc[pd.Timestamp(a) - pd.Timedelta(days=364):pd.Timestamp(b) - pd.Timedelta(days=364)].mean()
        yo = (cur / prev - 1) * 100
        trows.append({"metric": metric, "window": lab, **yo.replace([np.inf, -np.inf], np.nan).round(0).to_dict()})
pd.DataFrame(trows).to_csv(OUT / "google_trends_window_yoy.csv", index=False)

# ---- Promo depth: trial months (individual) by half-year; IN/ID standard intro offers ----
pr = pd.read_csv(ROOT / "data/promo_depth.csv")
pr["half"] = pr.date.str[:4] + np.where(pr.date.str[5:7].astype(int) <= 6, "H1", "H2")
tm = pr[pr.metric == "trial_months_individual"].pivot_table(index="half", columns="country", values="value", aggfunc=["mean", "count"])
tm.round(2).to_csv(OUT / "promo_trial_months_by_half.csv")
pr[pr.country.isin(FRIC) & (pr.date >= "2025-06")].pivot_table(index="date", columns=["country", "metric"], values="value", aggfunc="first") \
  .to_csv(OUT / "promo_in_id_plans_2025_26.csv")

pd.DataFrame(tests).to_csv(OUT / "tests.csv", index=False)
print("tables written:", sorted(p.name for p in OUT.glob("*.csv")))

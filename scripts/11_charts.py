"""Charts for analysis 1 (free-user growth: friction vs other markets). Reads analysis/tables/ from
scripts/10_free_growth_analysis.py; writes analysis/charts/*.png. Run 10 first."""
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "analysis" / "tables"
OUT = ROOT / "analysis" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# Reference palette (dataviz skill), light mode. Slots 1-3 validated all-pairs; aqua < 3:1 so every
# series is direct-labelled and the tables in analysis/tables are the table view.
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
SHORT = {"FRICTION": "IN+ID", "OTHER_EM": "BR+MX+PH", "DEVELOPED": "US+UK+DE", "WW": "Worldwide"}
GROUPS = [("FRICTION", "India + Indonesia (friction)", ORANGE),
          ("OTHER_EM", "Brazil + Mexico + Philippines", AQUA),
          ("DEVELOPED", "US + UK + Germany", BLUE),
          ("WW", "Worldwide", MUTED)]
EVENTS = [("2025-09-15", "Free tier upgraded\n(Sep 15, 2025)"), ("2026-08-01", "IN/ID friction\n(Aug 1, 2026)")]
SOURCE = "Source: Carbon Arc app panel (CA0013), SPOT ticker; unweighted country means. Flagged partial periods excluded."

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURFACE, "figure.facecolor": SURFACE,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.spines.top": False,
    "axes.spines.right": False, "axes.spines.left": False, "legend.frameon": False,
    "lines.linewidth": 2, "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
})


def frame(ax, zero=True):
    ax.grid(axis="x", visible=False)
    ax.tick_params(length=0)
    if zero:
        ax.axhline(0, color=INK2, lw=0.8, zorder=1)


def events(ax, label=True):
    top = ax.get_ylim()[1]
    for d, txt in EVENTS:
        ax.axvline(pd.Timestamp(d), color=MUTED, lw=0.8, zorder=1)
        if label:
            ax.text(pd.Timestamp(d) - pd.Timedelta(days=12), top, txt, ha="right", va="top", fontsize=7.5, color=INK2)


def end_labels(ax, series, min_gap, unit="%"):
    """Label line ends in text ink with a colour key; spread labels that would collide."""
    items = sorted([(s.dropna().iloc[-1], s.dropna().index[-1], name, c) for s, name, c in series], key=lambda t: t[0])
    ys = []
    for v, _, _, _ in items:
        ys.append(v if not ys or v - ys[-1] >= min_gap else ys[-1] + min_gap)
    for (v, x, name, c), y in zip(items, ys):
        ax.plot([x], [v], "o", ms=5, color=c, mec=SURFACE, mew=1.5, zorder=5)
        ax.annotate(f"{name}  {v:+.1f}{unit}", xy=(x, v), xytext=(x + pd.Timedelta(days=20), y), fontsize=7.5,
                    color=INK, va="center", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.8) if abs(y - v) > 0.01 else None)


def layout(fig, left=0.06, right=0.8, bottom_in=0.75, **kw):
    h = fig.get_figheight()
    fig.subplots_adjust(left=left, right=right, top=1 - 1.25 / h, bottom=bottom_in / h, **kw)


def legend(fig, ax, ncol):
    h = fig.get_figheight()
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", ncol=ncol, fontsize=8, bbox_to_anchor=(0.005, 1 - 0.72 / h),
               handlelength=2.2, columnspacing=1.6)


def finish(fig, name, title, subtitle, note):
    h = fig.get_figheight()
    fig.text(0.01, 1 - 0.12 / h, title, ha="left", va="top", fontsize=12, fontweight="bold", color=INK)
    fig.text(0.01, 1 - 0.45 / h, subtitle, ha="left", va="top", fontsize=9, color=INK2)
    fig.text(0.01, 0.01, note, ha="left", fontsize=7, color=MUTED, wrap=True)
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def load(name):
    return pd.read_csv(TAB / name, index_col=0, parse_dates=True)


def date_axis(ax, start="2021-01-01", end="2026-12-31"):
    ax.set_xlim(pd.Timestamp(start), pd.Timestamp(end))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


# ---- 1. App users YoY by group, monthly and weekly ----
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
layout(fig, hspace=0.2)
for ax, fname, lab in [(axes[0], "app_app_users_yoy_monthly_groups.csv", "Monthly"),
                       (axes[1], "app_app_users_yoy_weekly_groups.csv", "Weekly")]:
    w = load(fname)
    for col, name, c in GROUPS:
        ax.plot(w.index, w[col], color=c, lw=1.5 if col == "WW" else 2, label=name, zorder=3 if col != "WW" else 2)
    frame(ax)
    ax.set_ylim(-10, 80)
    ax.set_title(lab, loc="left", fontsize=9.5, color=INK, fontweight="bold")
    ax.set_ylabel("App users, YoY %")
    events(ax, label=(lab == "Monthly"))
    end_labels(ax, [(w[col], SHORT[col], c) for col, name, c in GROUPS], min_gap=6)
date_axis(axes[1])
legend(fig, axes[0], 4)
finish(fig, "01_app_users_yoy_groups.png",
       "India/Indonesia app growth converged with other markets before the Aug 2026 friction",
       "Spotify app users, YoY %, by country group, Jan 2021 to Sep 2026. US/UK/DE accelerated from mid-2026.",
       SOURCE + " Monthly and weekly measure different user windows; do not compare levels across panels.")

# ---- 2. Friction minus other-EM gap ----
fig, ax = plt.subplots(figsize=(10, 4.6))
layout(fig)
wk, mo = load("app_app_users_yoy_weekly_groups.csv"), load("app_app_users_yoy_monthly_groups.csv")
ax.plot(wk.index, wk.GAP_FRICTION_MINUS_EM, color=ORANGE, lw=1.2, alpha=0.45, label="Weekly")
ax.plot(mo.index, mo.GAP_FRICTION_MINUS_EM, color=ORANGE, lw=2, label="Monthly")
frame(ax)
ax.set_ylim(-10, 55)
ax.set_ylabel("Percentage points")
events(ax)
date_axis(ax)
end_labels(ax, [(mo.GAP_FRICTION_MINUS_EM, "Monthly", ORANGE), (wk.GAP_FRICTION_MINUS_EM, "Weekly", ORANGE)], min_gap=4, unit="pp")
legend(fig, ax, 2)
finish(fig, "02_friction_minus_em_gap.png",
       "The friction-market premium closed Nov 2025-May 2026, before friction; no step change after Aug 1",
       "App users YoY: India/Indonesia average minus Brazil/Mexico/Philippines average, pp",
       SOURCE + " Weekly gap change, 9 weeks pre vs 7 weeks post Aug 1: -0.05pp (Welch p = 0.90; autocorrelated, p optimistic).")

# ---- 3. Downloads YoY by group (monthly; weekly is too volatile to read) ----
fig, ax = plt.subplots(figsize=(10, 4.8))
layout(fig)
d = load("app_app_downloads_yoy_monthly_groups.csv")
for col, name, c in GROUPS:
    ax.plot(d.index, d[col], color=c, lw=1.5 if col == "WW" else 2, label=name)
frame(ax)
ax.set_ylim(-45, d[[g[0] for g in GROUPS]].max().max() + 10)
ax.set_ylabel("App downloads, YoY %")
events(ax)
date_axis(ax)
end_labels(ax, [(d[col], SHORT[col], c) for col, name, c in GROUPS], min_gap=9)
legend(fig, ax, 4)
finish(fig, "03_app_downloads_yoy_groups.png",
       "Downloads are noisy; US/UK/DE turned positive in 2026 while other groups stayed negative",
       "Spotify app downloads, YoY %, monthly, by country group",
       SOURCE + " Downloads do not track reported free users (r = 0.37, p = 0.13, n = 18 quarters); low weight. Sep 2026 partial month excluded.")

# ---- 4. WW app-implied vs reported Ad-Supported MAU and subs y/y ----
q = pd.read_csv(TAB / "ww_app_vs_reported_quarterly.csv", index_col=0)
q.index = pd.PeriodIndex(q.index, freq="Q").to_timestamp(how="end").normalize()
q = q.loc["2022-03-31":"2026-06-30"]
fig, ax = plt.subplots(figsize=(10, 4.8))
layout(fig)
ax.axvspan(pd.Timestamp("2026-02-01"), pd.Timestamp("2026-07-15"), color=GRID, alpha=0.45, lw=0, zorder=0)
ser = [("reported_ad_mau_yoy", "Reported Ad-Supported MAU", BLUE, "-"),
       ("reported_ad_mau_yoy_app_implied", "App-implied Ad-Supported MAU", BLUE, ":"),
       ("reported_subs_yoy", "Reported Premium subs", ORANGE, "-")]
for col, name, c, ls in ser:
    ax.plot(q.index, q[col], color=c, ls=ls, marker="o", ms=4, mec=SURFACE, mew=1.2, label=name)
frame(ax)
ax.set_ylim(0, 36)
ax.set_ylabel("y/y %")
ax.set_xticks(q.index[::2])
ax.set_xticklabels([f"Q{t.quarter}'{t.year % 100}" for t in q.index[::2]])
for dt in ["2026-03-31", "2026-06-30"]:
    r = q.loc[dt]
    ax.annotate(f"+{r.reported_ad_mau_yoy_residual:.1f}pp", xy=(pd.Timestamp(dt), r.reported_ad_mau_yoy + 1.2),
                ha="center", fontsize=7, color=INK)
ax.text(pd.Timestamp("2026-02-15"), 34.5, "App panel stops\ntracking\nreported free", fontsize=7.5, color=INK2, va="top")
end_labels(ax, [(q[c], n, col) for c, n, col, _ in ser], min_gap=1.8)
legend(fig, ax, 3)
finish(fig, "04_ww_app_vs_reported.png",
       "Reported free growth beat the app panel by ~6pp in 1H26 while subs grew slower than it implied",
       "Worldwide, quarterly y/y %: reported Ad-Supported MAU and Premium subs vs Ad-Supported MAU implied by app users",
       "App-implied = OLS of reported Ad-Supported MAU y/y on WW weekly app-users YoY (quarterly mean), fit 2022Q1-2025Q3, n = 15. "
       "Q/q changes: r = 0.66, p = 0.004, n = 17. Sources: 6-K KPIs; Carbon Arc.")

# ---- 5. Europe / North America: MAU vs subs y/y, reported and consensus ----
rg = pd.read_csv(TAB / "regional_consensus_growth.csv", index_col=0)
rg.index = pd.PeriodIndex(rg.index, freq="Q").to_timestamp(how="end").normalize()
rg = rg.loc["2025-06-30":]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
layout(fig, right=0.97, wspace=0.08)
for ax, reg in zip(axes, ["Europe", "North America"]):
    ax.axvspan(pd.Timestamp("2026-07-15"), rg.index[-1] + pd.Timedelta(days=30), color=GRID, alpha=0.45, lw=0, zorder=0)
    for col, name, c in [(f"{reg}|mau_yoy", "MAU", BLUE), (f"{reg}|subs_yoy", "Premium subs", ORANGE)]:
        ax.plot(rg.index, rg[col], color=c, marker="o", ms=4, mec=SURFACE, mew=1.2, label=name)
    frame(ax)
    ax.set_title(reg, loc="left", fontsize=9.5, fontweight="bold", color=INK)
    ax.text(pd.Timestamp("2026-08-15"), 13.2, "Consensus", fontsize=7.5, color=INK2)
    ax.set_xticks(rg.index[::2])
    ax.set_xticklabels([f"Q{t.quarter}'{t.year % 100}" for t in rg.index[::2]])
axes[0].set_ylabel("y/y %")
axes[0].set_ylim(-3, 14)
legend(fig, axes[0], 2)
finish(fig, "05_regional_mau_vs_subs.png",
       "Consensus has Europe MAU growth falling from +12% to -1% by Q1'27 as the free-tier upgrade laps",
       "Bloomberg MODL: MAU and Premium subs y/y %, reported to Q2'26, consensus mean after (shaded)",
       "Source: SPOTModelBloom-nums.xlsx (Bloomberg consensus mean). Regional rows have known reconciliation gaps "
       "(notes/01_regional.md); no regional Ad-Supported split exists.")

# ---- 6. IN/ID: Spotify vs YouTube Music app users YoY ----
rv = load("rivals_users_yoy_monthly.csv").loc["2024-01-01":]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
layout(fig, right=0.88, wspace=0.28)
for ax, cc, name in zip(axes, ["IN", "ID"], ["India", "Indonesia"]):
    ser = [(rv[f"{cc}|Spotify - Music and Podcasts"], "Spotify", BLUE), (rv[f"{cc}|YouTube Music"], "YouTube Music", ORANGE)]
    for s, n, c in ser:
        ax.plot(s.index, s, color=c, label=n)
    frame(ax)
    ax.set_title(name, loc="left", fontsize=9.5, fontweight="bold", color=INK)
    ax.set_ylim(-5, 90 if cc == "ID" else 90)
    events(ax, label=(cc == "IN"))
    ax.set_xlim(pd.Timestamp("2024-01-01"), pd.Timestamp("2026-12-31"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    end_labels(ax, ser, min_gap=4)
axes[0].set_ylabel("App users, YoY %")
legend(fig, axes[0], 2)
finish(fig, "06_in_id_spotify_vs_youtube_music.png",
       "YouTube Music slowed alongside Spotify in India and Indonesia: a category slowdown, not friction",
       "App users YoY %, monthly, Spotify app entity vs YouTube Music",
       "Source: Carbon Arc app panel. 2024 values at whole-pp precision. Apple Music omitted (YoY up to +180% off a small base; levels unavailable). "
       "Sep 2026 partial month excluded.")

print("charts:", sorted(p.name for p in OUT.glob("*.png")))

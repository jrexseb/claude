# SPOT short: margin pillar data repo

Citadel stock pitch, short Spotify (SPOT). This repo collects and cleans data for the margin pillar.
Data sessions do not draw conclusions, write findings, or make charts. Analysis sessions work from /data and /notes.

## Context (read first, in order)
1. SPOT_Margin_Pillar_Handoff.md
2. SPOT_Prop_Research_Plan.md
3. ALTD_Analysis.md
Other inputs: MODL_SPOT_US_B2.xlsx (Bloomberg consensus by quarter, regional subs/MAU rows),
panel_all.csv and spot_guidance_vs_actual.csv (historical KPI panel), two Bloomberg ALTD exports
(US card panel, Apptopia, Similarweb, daily).

## Forward call being tested
- Consensus holds free users per payer (reported Ad-Supported MAUs / Premium subscribers) at ~1.63-1.65
  through FY28 only by assuming free-user growth falls from +14% y/y to ~+8% by Q2'27 while subscriber
  growth holds at 8-9%.
- Our view: subscriber growth slows as the Jan 2026 US price increase laps in 1H27. Spotify then either
  (A) lets free users grow and the ratio rises, or (B) adds more free-tier friction and MAU/ad growth miss.
- Key dates: Sept 15, 2025 (free tier upgraded globally); ~Aug 1, 2026 (free-tier friction, India and
  Indonesia only).
- Q3'26 consensus: free 498m, subs 305m, ratio 1.63.
- Decisive question: is free-user growth slowing only where friction was added, or everywhere?

## Rules
- Never print raw rows to the conversation; print short coverage summaries only (date range, row counts,
  missing periods).
- Never invent or interpolate values. Missing stays missing, and gets logged in /notes.
- If a source blocks or rate-limits, log it and move on. Do not work around blocks.
- Commit and push after each step.
- Carbon Arc: discovery tools are free; state expected credit cost before any billed query. Session cap
  20 credits unless the user approves more.

## Layout
- /data: CSVs in tidy long format: date, country, metric, value, source (extra columns allowed, e.g.
  flag, snapshot_url, but these five come first).
- /notes: one short .md per step: source, exact query or URL pattern, coverage, gaps, anomalies,
  definitions. notes/00_INDEX.md is the entry point.
- /scripts: reproducible code; each pull must be rerunnable from here.

## Rules for analysis sessions
- Say "directionally consistent", not "significant", unless p < 0.05 with n stated.
- Report evidence against the thesis alongside evidence for it.
- Check notes/00_INDEX.md for known gaps, definitions and anomalies (holidays, Wrapped in early Dec,
  Feb 28 billing spikes) before using any series.

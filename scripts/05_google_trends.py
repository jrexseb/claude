"""Step 6: Google Trends search interest (weekly, 2023-01-01 to 2026-09-27), 8 countries.
One request per country with all 5 terms, so the 0-100 index is comparable ACROSS terms within a country,
but NOT across countries (each geo is normalised to its own peak).
Terms: "Spotify", "Spotify Premium", "cancel Spotify", "Spotify mod", "Spotify apk" (English strings in every geo;
no local-language variants, see notes). Client: pytrends (unofficial Google Trends client).
Reliability check: every country is pulled TWICE (pull=1, pull=2) because Google computes Trends from a random
sample; the difference between pulls measures sampling noise.
Efficiency: responses cached to data/raw/trends/*.csv (reruns skip cached pulls); 15 s spacing between requests;
on HTTP 429 wait 60 s once, then log and skip (no workaround). Progress + ETA printed after every request.
Rerun: python3 scripts/05_google_trends.py"""
import time, json
import pandas as pd
from pathlib import Path
from pytrends.request import TrendReq
R = Path(__file__).resolve().parents[1]
C = R / "data/raw/trends"; C.mkdir(parents=True, exist_ok=True)
TERMS = ["Spotify", "Spotify Premium", "cancel Spotify", "Spotify mod", "Spotify apk"]
GEOS = ["IN", "ID", "BR", "MX", "PH", "US", "GB", "DE"]
TF = "2023-01-01 2026-09-27"
jobs = [(g, k) for k in (1, 2) for g in GEOS]
log, t0, done_live, per = [], time.time(), 0, []
p = TrendReq(hl="en-US", tz=0, timeout=(10, 30))
for n, (geo, pull) in enumerate(jobs, 1):
    f = C / f"{geo}_pull{pull}.csv"
    if f.exists():
        status = "cached"
    else:
        status = "fail"
        for attempt in (1, 2):
            t = time.time()
            try:
                p.build_payload(TERMS, timeframe=TF, geo=geo)
                df = p.interest_over_time()
                df.to_csv(f); status = "ok"; per.append(time.time() - t); break
            except Exception as e:
                status = f"error:{type(e).__name__}:{str(e)[:80]}"
                if "429" in str(e) and attempt == 1:
                    time.sleep(60); continue
                break
        time.sleep(15)
    log.append({"geo": geo, "pull": pull, "status": status, "ts": pd.Timestamp.utcnow().isoformat()})
    left = len(jobs) - n
    eta = left * ((sum(per) / len(per) if per else 2) + 15)
    print(f"[{n}/{len(jobs)}] {geo} pull{pull}: {status} | elapsed {int(time.time()-t0)}s | ETA ~{int(eta//60)}m{int(eta%60):02d}s", flush=True)
pd.DataFrame(log).to_csv(R / "data/raw/trends_log.csv", index=False)
print("DONE", flush=True)

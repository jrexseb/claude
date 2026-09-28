"""Google Trends, one term per request (own 0-100 scale per country-term), so low-volume terms keep resolution.
Needed because in the 5-term requests (05_google_trends.py) 'Spotify' sets the 100 and 'cancel Spotify' is 0 in ~96% of
weeks. Values here are NOT comparable across terms (each term normalised to its own peak within a country).
Terms: Spotify Premium, cancel Spotify, Spotify mod, Spotify apk (all 8 geos) + local-language cancel terms:
'cancelar Spotify' (BR, MX), 'Spotify kündigen' (DE). Cached per request; 15 s spacing; on 429 wait 60 s once, then log.
Rerun: python3 scripts/05c_trends_single_terms.py"""
import time
import pandas as pd
from pathlib import Path
from pytrends.request import TrendReq
R = Path(__file__).resolve().parents[1]; C = R / "data/raw/trends_single"; C.mkdir(parents=True, exist_ok=True)
GEOS = ["IN", "ID", "BR", "MX", "PH", "US", "GB", "DE"]
TF = "2023-01-01 2026-09-27"
jobs = [(g, t) for t in ["Spotify Premium", "cancel Spotify", "Spotify mod", "Spotify apk"] for g in GEOS]
jobs += [("BR", "cancelar Spotify"), ("MX", "cancelar Spotify"), ("DE", "Spotify kündigen")]
p = TrendReq(hl="en-US", tz=0, timeout=(10, 30)); log, t0, per = [], time.time(), []
for n, (geo, term) in enumerate(jobs, 1):
    f = C / f"{geo}__{term.replace(' ', '_')}.csv"
    status = "cached" if f.exists() else "fail"
    if not f.exists():
        for attempt in (1, 2):
            t = time.time()
            try:
                p.build_payload([term], timeframe=TF, geo=geo)
                df = p.interest_over_time()
                if df.empty: status = "empty_response"; pd.DataFrame().to_csv(f); break
                df.to_csv(f); status = "ok"; per.append(time.time() - t); break
            except Exception as e:
                status = f"error:{type(e).__name__}:{str(e)[:80]}"
                if "429" in str(e) and attempt == 1: time.sleep(60); continue
                break
        time.sleep(15)
    log.append({"geo": geo, "term": term, "status": status})
    eta = (len(jobs) - n) * ((sum(per) / len(per) if per else 2) + 15)
    print(f"[{n}/{len(jobs)}] {geo} '{term}': {status} | elapsed {int(time.time()-t0)}s | ETA ~{int(eta//60)}m{int(eta%60):02d}s", flush=True)
pd.DataFrame(log).to_csv(R / "data/raw/trends_single_log.csv", index=False)
print("DONE", flush=True)

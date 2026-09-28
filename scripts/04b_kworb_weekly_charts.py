"""Step 4b: weekly top-200 total streams from kworb.net WEEKLY chart pages ({cc}_weekly.html), via Wayback captures
(+ live page). Each captured page is a full chart week, so its Streams sum is a complete weekly total, unlike
summing sparse daily captures. Chart date = date printed in the page title (kworb shows the chart week's date).
CDX: https://web.archive.org/cdx/search/cdx?url=kworb.net/spotify/country/{cc}_weekly.html&from=2023&output=json
     &filter=statuscode:200&collapse=timestamp:8
Output: data/raw/kworb_weekly_charts.csv. Rerun: python3 scripts/04b_kworb_weekly_charts.py"""
import json, time, hashlib, importlib.util
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("k", R / "scripts/04_kworb_streams.py"); k = importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
recs, log = [], []
for cc in k.CCS:
    page = f"kworb.net/spotify/country/{cc}_weekly.html"
    body, att = k.curl(f"https://web.archive.org/cdx/search/cdx?url={page}&from=2023&output=json&filter=statuscode:200&collapse=timestamp:8")
    caps = []
    if body and body.strip():
        data = json.loads(body); caps = [dict(zip(data[0], r)) for r in data[1:]]
    log.append({"country": cc, "cdx_result": att, "captures": len(caps)})
    for c in caps:
        url = f"https://web.archive.org/web/{c['timestamp']}id_/{c['original']}"
        f = k.CACHE / (hashlib.md5(url.encode()).hexdigest() + ".html")
        cached = f.exists()
        html = f.read_text(errors="ignore") if cached else k.curl(url, f)[0]
        p = k.parse(html) if html else None
        recs.append({"country": cc, "capture_ts": c["timestamp"], "snapshot_url": url,
                     **(p or {"chart_date": None, "streams_sum": None, "rows": None}),
                     "parse_status": "ok" if p else ("fetch_failed" if html is None else "parse_failed")})
        if not cached: time.sleep(1.5)
    html, att = k.curl(f"https://kworb.net/spotify/country/{cc}_weekly.html")
    p = k.parse(html) if html else None
    recs.append({"country": cc, "capture_ts": "live", "snapshot_url": f"https://kworb.net/spotify/country/{cc}_weekly.html",
                 **(p or {"chart_date": None, "streams_sum": None, "rows": None}), "parse_status": "ok" if p else "live_failed"})
    print(cc, "captures", len(caps), flush=True)
d = pd.DataFrame(recs)
pd.DataFrame(log).to_csv(R / "data/raw/kworb_weekly_cdx_log.csv", index=False)
ok = d[d.parse_status == "ok"].sort_values("capture_ts").drop_duplicates(["country", "chart_date"])
ok = ok[ok.chart_date >= "2023-01-01"].sort_values(["country", "chart_date"])
ok.to_csv(R / "data/raw/kworb_weekly_charts.csv", index=False)
print("weekly charts:", len(ok)); print(ok.groupby("country").chart_date.agg(["min", "max", "count"]).to_string())

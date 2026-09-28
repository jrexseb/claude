"""Step 3a: list Wayback snapshots (one per month, HTTP 200) of Spotify premium pages via the CDX API.
URL patterns tried per country: spotify.com/{cc}/premium/ and spotify.com/{cc}-{lang}/premium/ (several langs).
CDX query: https://web.archive.org/cdx/search/cdx?url=<pattern>&from=202301&output=json
           &filter=statuscode:200&collapse=timestamp:6   (collapse:6 = first capture per YYYYMM)
Retries: up to 5 per request with backoff (CDX returns intermittent 503/504 and the egress tunnel resets); every failure is logged.
Plain http:// to web.archive.org is refused by this environment's egress allowlist; https only.
Output: data/raw/wayback_cdx.csv, data/raw/wayback_cdx_log.csv.  Rerun: python3 scripts/03a_wayback_cdx.py"""
import csv, json, time, requests
from pathlib import Path
R = Path(__file__).resolve().parents[1]
PATTERNS = {
    "in": ["in", "in-en", "in-hi"], "id": ["id", "id-id", "id-en"], "br": ["br", "br-pt", "br-en"],
    "mx": ["mx", "mx-es", "mx-en"], "ph": ["ph", "ph-en", "ph-fil"], "us": ["us", "us-en", "us-es"],
    "gb": ["uk", "uk-en", "gb", "gb-en"], "de": ["de", "de-de", "de-en"], "tr": ["tr", "tr-tr", "tr-en"],
    "ng": ["ng", "ng-en"],
}
S = requests.Session(); S.headers["User-Agent"] = "research-data-pull (academic stock pitch; contact via repo)"
rows, log = [], []
for cc, pats in PATTERNS.items():
    for p in pats:
        url = f"spotify.com/{p}/premium/"
        q = {"url": url, "from": "202301", "output": "json", "filter": "statuscode:200", "collapse": "timestamp:6"}
        for attempt in range(1, 6):
            try:
                r = S.get("https://web.archive.org/cdx/search/cdx", params=q, timeout=120)
                status = r.status_code
            except requests.RequestException as e:
                status = f"error:{type(e).__name__}"
            log.append({"country": cc, "pattern": url, "attempt": attempt, "status": status})
            if status == 200:
                data = r.json() if r.text.strip() else []
                for rec in data[1:]:
                    d = dict(zip(data[0], rec))
                    rows.append({"country": cc, "pattern": url, **d})
                break
            if status == 429:
                time.sleep(60)  # rate limited: wait, no evasion
            else:
                time.sleep(5 * 2 ** (attempt - 1))
        time.sleep(2)
with open(R / "data/raw/wayback_cdx.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["country", "pattern", "urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"])
    w.writeheader(); w.writerows(rows)
with open(R / "data/raw/wayback_cdx_log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["country", "pattern", "attempt", "status"]); w.writeheader(); w.writerows(log)
import collections
c = collections.Counter((r["country"], r["pattern"]) for r in rows)
fails = [(l["country"], l["pattern"]) for l in log if l["attempt"] == 5 and l["status"] != 200]
print("snapshots per pattern:"); [print(" ", k, v) for k, v in sorted(c.items())]
print("patterns failing all 5 attempts:", fails)

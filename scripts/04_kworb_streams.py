"""Step 4: daily top-200 total streams by country from kworb.net Spotify daily chart pages.
kworb only serves the LATEST daily chart (no dated archive), so history comes from Wayback captures of
  kworb.net/spotify/country/{cc}_daily.html
CDX: https://web.archive.org/cdx/search/cdx?url=kworb.net/spotify/country/{cc}_daily.html&from=2023&output=json
     &filter=statuscode:200&collapse=timestamp:8   (first capture per calendar day)
Plus the live page (today's chart). Each page is parsed for its chart date (title 'Spotify Daily Chart - X - YYYY/MM/DD'),
the sum of the 'Streams' column, and the row count. Pages are de-duplicated by chart date (several captures can show
the same chart). Days with no capture are simply absent (no interpolation).
Outputs: data/raw/kworb_daily.csv (one row per country x chart date), data/kworb_streams_weekly.csv (tidy weekly).
Rerun: python3 scripts/04_kworb_streams.py"""
import re, json, time, subprocess, hashlib
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
R = Path(__file__).resolve().parents[1]
CACHE = R / "data/raw/kworb_html"; CACHE.mkdir(parents=True, exist_ok=True)
CCS = ["in", "id", "br", "mx", "ph", "us", "gb", "de"]

def curl(url, out=None):
    for attempt in range(1, 6):
        p = subprocess.run(["curl", "-sL", "--compressed", "-m", "120", "-o", str(out) if out else "-", "-w", "\n%{http_code}", url],
                           capture_output=True, text=True, errors="ignore")
        body, _, code = p.stdout.rpartition("\n")
        if code == "200":
            return (out.read_text(errors="ignore") if out else body), attempt
        time.sleep(60 if code == "429" else 5 * 2 ** (attempt - 1))
    return None, f"failed:{code}"

def parse(html):
    s = BeautifulSoup(html, "lxml")
    m = re.search(r"(\d{4})/(\d{2})/(\d{2})", s.title.text if s.title else "") or re.search(r"(?:Daily|Weekly) Chart - .*? - (\d{4})/(\d{2})/(\d{2})", s.get_text(" "))
    t = s.find("table")
    if not (m and t): return None
    hdr = [th.get_text(strip=True) for th in t.find_all("th")]
    if "Streams" not in hdr: return None
    j = hdr.index("Streams")
    vals = []
    for tr in t.find_all("tr")[1:]:
        td = tr.find_all("td")
        if len(td) > j:
            v = td[j].get_text(strip=True).replace(",", "")
            if v.isdigit(): vals.append(int(v))
    return {"chart_date": f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "streams_sum": sum(vals), "rows": len(vals)}

if __name__ == "__main__":
    recs, log = [], []
    for cc in CCS:
        page = f"kworb.net/spotify/country/{cc}_daily.html"
        q = f"https://web.archive.org/cdx/search/cdx?url={page}&from=2023&output=json&filter=statuscode:200&collapse=timestamp:8"
        body, att = curl(q)
        caps = []
        if body and body.strip():
            data = json.loads(body); caps = [dict(zip(data[0], r)) for r in data[1:]]
        log.append({"country": cc, "step": "cdx", "result": att if body is not None else att, "captures": len(caps)})
        for c in caps:
            url = f"https://web.archive.org/web/{c['timestamp']}id_/{c['original']}"
            f = CACHE / (hashlib.md5(url.encode()).hexdigest() + ".html")
            html = f.read_text(errors="ignore") if f.exists() else curl(url, f)[0]
            p = parse(html) if html else None
            recs.append({"country": cc, "capture_ts": c["timestamp"], "snapshot_url": url,
                         **(p or {"chart_date": None, "streams_sum": None, "rows": None}),
                         "parse_status": "ok" if p else ("fetch_failed" if html is None else "parse_failed")})
            if not f.exists() or html is None: time.sleep(1.5)
        live = f"https://kworb.net/spotify/country/{cc}_daily.html"
        html, att = curl(live)
        p = parse(html) if html else None
        recs.append({"country": cc, "capture_ts": "live", "snapshot_url": live, **(p or {"chart_date": None, "streams_sum": None, "rows": None}),
                     "parse_status": "ok" if p else "live_failed"})
        print(cc, "captures", len(caps), "parsed", sum(r["parse_status"] == "ok" for r in recs if r["country"] == cc), flush=True)
    d = pd.DataFrame(recs)
    d.to_csv(R / "data/raw/kworb_captures.csv", index=False)
    pd.DataFrame(log).to_csv(R / "data/raw/kworb_cdx_log.csv", index=False)
    ok = d[d.parse_status == "ok"].copy()
    # same chart date captured more than once: keep first capture; log any conflicting sums
    conf = ok.groupby(["country", "chart_date"]).streams_sum.nunique()
    print("chart dates with conflicting sums across captures:", int((conf > 1).sum()))
    daily = ok.sort_values("capture_ts").drop_duplicates(["country", "chart_date"])
    daily = daily[daily.chart_date >= "2023-01-01"].sort_values(["country", "chart_date"])
    daily.to_csv(R / "data/raw/kworb_daily.csv", index=False)
    # weekly: ISO weeks (Mon start). Sum only observed days; report days_observed so partial weeks are visible.
    daily["date"] = pd.to_datetime(daily.chart_date)
    daily["week_start"] = daily.date - pd.to_timedelta(daily.date.dt.weekday, unit="D")
    w = daily.groupby(["country", "week_start"]).agg(value=("streams_sum", "sum"), days_observed=("date", "nunique"),
                                                      min_rows=("rows", "min")).reset_index()
    w = w.assign(date=w.week_start.dt.strftime("%Y-%m-%d"), metric="top200_streams_sum_observed_days",
                 source="kworb.net daily chart via Wayback captures (+live page)")
    w[["date", "country", "metric", "value", "source", "days_observed", "min_rows"]].to_csv(R / "data/kworb_streams_weekly.csv", index=False)
    print("daily rows", len(daily), "weeks", len(w), "complete weeks (7 days)", int((w.days_observed == 7).sum()))

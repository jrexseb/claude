"""Step 3b: fetch one Wayback snapshot per country-month (from data/raw/wayback_cdx.csv) and parse plan prices.
Fetch: https://web.archive.org/web/{timestamp}id_/{original}   (id_ = raw archived page, no Wayback toolbar)
       curl --compressed -L with retries; redirects are followed and the EFFECTIVE snapshot URL/timestamp is recorded.
Raw HTML cached in data/raw/wayback_html/ (gitignored). Parsed text blocks kept in the output for audit.
Parsing is rule-based on visible text; anything not matched is left blank with parse_status set. Nothing is guessed.
Rerun: python3 scripts/03b_wayback_promos.py"""
import re, subprocess, time, hashlib, json
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
R = Path(__file__).resolve().parents[1]
CACHE = R / "data/raw/wayback_html"; CACHE.mkdir(parents=True, exist_ok=True)

PLAN_NAMES = {  # visible plan header -> canonical plan
    "individual": "individual", "premium individual": "individual", "individuel": "individual", "bireysel": "individual",
    "individu": "individual", "einzelperson": "individual", "premium individu": "individual", "premium bireysel": "individual",
    "duo": "duo", "premium duo": "duo",
    "family": "family", "premium family": "family", "família": "family", "familia": "family", "keluarga": "family",
    "aile": "family", "premium family ": "family", "premium familia": "family", "premium família": "family",
    "premium keluarga": "family", "premium aile": "family",
    "student": "student", "premium student": "student", "estudante": "student", "estudiantes": "student",
    "universitário": "student", "mahasiswa": "student", "öğrenci": "student", "premium student ": "student",
    "premium estudiantes": "student", "premium universitários": "student", "premium universitário": "student",
    "premium mahasiswa": "student", "premium öğrenci": "student",
    "mini": "mini", "premium mini": "mini", "lite": "lite", "premium lite": "lite",
}
CUR = r"(₹|Rp\.?\s?|R\$\s?|MX\$|\$|US\$|£|€|₺|TL\s?|₱|PHP\s?|₦|NGN\s?)"
NUM = r"(\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)"
PRICE = re.compile(CUR + r"\s?" + NUM + r"|" + NUM + r"\s?(€|TL|₺)")
PER_MONTH = re.compile(r"/\s?(month|mo|mes|mês|monat|ay|bulan|buwan)|per month|a month|pro monat|por mes|por mês|per bulan|aylık|/mês", re.I)
FREE_N = re.compile(r"(\d+|one|two|three|four|six|1|un|um|dos|três|tres|satu|bir)\s*(month|months|mes|meses|mês|monat|monate|ay|bulan)\s*(free|gratis|grátis|kostenlos|ücretsiz|gratuit)|"
                    r"(free|gratis|grátis|kostenlos|ücretsiz)\s*(for\s*)?(\d+)\s*(month|months|mes|meses|monat|monate|ay|bulan)", re.I)
N_FOR_PRICE = re.compile(r"(\d+)\s*(month|months|mes|meses|mês|monat|monate|ay|bulan)\s*(for|por|für|için|seharga|untuk)\s*" + r"(?:" + CUR + r"\s?" + NUM + r"|" + NUM + r"\s?(€|TL|₺))", re.I)
PRICE_FOR_N = re.compile(r"(?:" + CUR + r"\s?" + NUM + r"|" + NUM + r"\s?(€|TL|₺))\s*(for|por|für|için|untuk|selama)\s*(\d+)\s*(month|months|mes|meses|mês|monat|monate|ay|bulan)", re.I)
WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "six": 6, "un": 1, "um": 1, "dos": 2, "três": 3, "tres": 3, "satu": 1, "bir": 1}

def fetch(ts, original):
    url = f"https://web.archive.org/web/{ts}id_/{original}"
    f = CACHE / (hashlib.md5(url.encode()).hexdigest() + ".html")
    meta = f.with_suffix(".json")
    if f.exists() and meta.exists():
        return f.read_text(errors="ignore"), json.loads(meta.read_text())
    for attempt in range(1, 6):
        p = subprocess.run(["curl", "-sL", "--compressed", "-m", "120", "-o", str(f), "-w", "%{http_code} %{url_effective}", url],
                           capture_output=True, text=True)
        code, _, eff = p.stdout.partition(" ")
        if code == "200":
            m = {"request_url": url, "effective_url": eff, "http": code, "attempts": attempt}
            meta.write_text(json.dumps(m)); return f.read_text(errors="ignore"), m
        time.sleep(60 if code == "429" else 5 * 2 ** (attempt - 1))
    return None, {"request_url": url, "effective_url": "", "http": code, "attempts": attempt}

def num(s):
    s = s.strip().replace(" ", "")
    if re.search(r"[.,]\d{3}$", s) and not re.search(r"[.,]\d{1,2}$", s):   # 49.990 / 1,000 thousands sep
        return float(re.sub(r"[.,]", "", s))
    if re.search(r"[.,]\d{3}[.,]\d{1,2}$", s):
        return float(re.sub(r"[.,]", "", s[:-3]) + "." + s[-2:])
    return float(s.replace(",", "."))

def first_price(txt):
    m = PRICE.search(txt)
    if not m: return None, None
    cur = (m.group(1) or m.group(4) or "").strip(); val = m.group(2) or m.group(3)
    return cur, num(val)

def parse(html):
    lines = [l.strip() for l in BeautifulSoup(html, "lxml").get_text("\n", strip=True).split("\n") if l.strip()]
    idx = [(i, PLAN_NAMES[l.lower()]) for i, l in enumerate(lines) if l.lower() in PLAN_NAMES]
    plans = {}
    for k, (i, plan) in enumerate(idx):
        # offer badges ("1 month free") sit just ABOVE the plan name, so each block starts up to 3 lines before
        # the name (but not before the previous plan's name) and ends 3 lines before the next plan's name.
        start = max(idx[k - 1][0] + 1 if k else 0, i - 3)
        end = idx[k + 1][0] - 3 if k + 1 < len(idx) else min(len(lines), i + 15)
        block = lines[start:i] + lines[i + 1:max(end, i + 2)]
        if plan in plans: continue
        rec = {"block": " | ".join(block)[:400]}
        # list price: a per-month price line; prefer lines mentioning 'after'
        cands = [l for l in block if PRICE.search(l) and PER_MONTH.search(l)]
        after = [l for l in cands if re.search(r"after|depois|después|danach|sonra|setelah|berikutnya|luego|thereafter", l, re.I)]
        pl = (after or cands or [None])[0]
        if pl: rec["currency"], rec["list_price"] = first_price(pl)
        # intro offers
        for l in block:
            m = FREE_N.search(l)
            if m and "trial_months" not in rec:
                n = m.group(1) or m.group(6); rec["trial_months"] = int(WORDNUM.get(str(n).lower(), n))
            m = N_FOR_PRICE.search(l)
            if m and "intro_months" not in rec:
                cur, val = first_price(l[m.start(3):])
                if val == 0: rec.setdefault("trial_months", int(m.group(1)))
                else: rec["intro_months"], rec["intro_price"] = int(m.group(1)), val
            m = PRICE_FOR_N.search(l)
            if m and "intro_months" not in rec:
                cur, val = first_price(l)
                n = int([g for g in m.groups() if g and g.isdigit()][-1])
                if val == 0: rec.setdefault("trial_months", n)
                else: rec["intro_months"], rec["intro_price"] = n, val
        plans[plan] = rec
    # headline (first ~15 lines): page-level offer text
    head = " | ".join(lines[:20])[:400]
    return plans, head

if __name__ == "__main__":
    cdx = pd.read_csv(R / "data/raw/wayback_cdx.csv", dtype=str)
    cdx["month"] = cdx.timestamp.str[:6]
    # prefer English-language pattern when several patterns have a capture in the same month
    cdx["pref"] = cdx.pattern.str.contains(r"-en/").map({True: 0, False: 1})
    pick = cdx.sort_values(["country", "month", "pref", "timestamp"]).drop_duplicates(["country", "month"])
    out = []
    for _, r in pick.iterrows():
        html, meta = fetch(r.timestamp, r.original)
        base = {"country": r.country, "month": r.month, "cdx_timestamp": r.timestamp, "pattern": r.pattern,
                "snapshot_url": meta["request_url"], "effective_url": meta["effective_url"], "http": meta["http"]}
        eff_ts = re.search(r"/web/(\d{14})", meta["effective_url"] or "")
        base["effective_timestamp"] = eff_ts.group(1) if eff_ts else ""
        if html is None:
            out.append({**base, "plan": "", "parse_status": "fetch_failed"}); continue
        plans, head = parse(html)
        if not plans:
            out.append({**base, "plan": "", "parse_status": "no_plan_blocks_found", "headline_text": head}); continue
        for plan, rec in plans.items():
            st = "ok" if rec.get("list_price") is not None else "no_list_price"
            out.append({**base, "plan": plan, **rec, "headline_text": head, "parse_status": st})
        time.sleep(1.5)
    pd.DataFrame(out).to_csv(R / "data/raw/promo_parsed_wide.csv", index=False)
    print("rows", len(out))

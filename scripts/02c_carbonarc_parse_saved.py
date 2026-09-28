"""Parse Carbon Arc framework_to_insight results that the MCP saved to file (large results) into long CSVs.
Input: data/raw/carbonarc_v2/*.json (verbatim MCP result copies). Output: <name>_long.csv next to it.
Raw 'DATE' for weekly results is the week END (Sunday); week_start = DATE - 6 days (Monday), matching the earlier
weekly files. Values are fractions in the source; value_pct = fraction * 100. NaN stays NaN.
Usage: python3 scripts/02c_carbonarc_parse_saved.py <json> <out_csv>"""
import json, sys
import pandas as pd
src, out = sys.argv[1], sys.argv[2]
j = json.load(open(src))
rows = [l for l in j["data"].split("\n") if l.startswith("|")]
hdr = [c.strip() for c in rows[0].strip("|").split("|")]
recs = [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]
d = pd.DataFrame(recs, columns=hdr)
vcol = hdr[-1]
d = d.assign(date_raw=d["DATE"], value_pct=pd.to_numeric(d[vcol], errors="coerce") * 100)
name_col = "ENTITY NAME"
keep = ["date_raw", "COUNTRY", name_col, "value_pct"]
d = d[keep].rename(columns={"COUNTRY": "country_name", name_col: "entity"})
d["price_credits"] = j["metadata"]["price"]
d.to_csv(out, index=False)
print(out, d.shape, d.date_raw.min(), d.date_raw.max(), "NaN:", int(d.value_pct.isna().sum()))

"""Turn a saved Meta ads_get_ad_entities weekly result (time_increment "7") into data.json weekly rows.

Usage: python3 -I scripts/meta_weekly.py <tool-result-file> > rows.json
The file is the JSON the connector saved: {"ad_entities": "<json string>", ...} or a bare list.
Output: [{week, id, spend, impressions, clicks, link_clicks, results}] for weeks with spend or impressions.
"""
import json
import sys


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main(path):
    raw = json.load(open(path))
    rows = raw.get("ad_entities", raw) if isinstance(raw, dict) else raw
    if isinstance(rows, str):
        rows = json.loads(rows)
    out = []
    for r in rows:
        vals = (r.get("results") or {}).get("values")
        row = {
            "week": r["date_start"],
            "id": r["id"],
            "spend": round(num((r.get("amount_spent") or {}).get("value")), 2),
            "impressions": int(num(r.get("impressions"))),
            "clicks": int(num(r.get("clicks"))),
            "link_clicks": int(num(r.get("link_click"))),
            "results": int(num(vals[0]["value"])) if vals else None,
        }
        if row["spend"] or row["impressions"]:
            out.append(row)
    out.sort(key=lambda x: (x["week"], x["id"]))
    json.dump(out, sys.stdout, indent=1)
    print(f"{len(out)} rows, spend {sum(x['spend'] for x in out):.2f}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])

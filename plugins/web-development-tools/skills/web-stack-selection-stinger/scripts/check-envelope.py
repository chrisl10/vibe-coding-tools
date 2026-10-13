#!/usr/bin/env python3
"""Check archive/link integrity and encoded selection contracts, not app behavior."""
from pathlib import Path
import hashlib,json,re
base=Path(__file__).resolve().parents[1]
rows=json.loads((base/"references/research/source-ledger.json").read_text());available={r["id"] for r in rows if "path" in r}
for row in rows:
    if "path" in row:assert hashlib.sha256((base/row["path"]).read_bytes()).hexdigest()==row["archive_sha256"],row["id"]
for p in base.rglob("*.md"):
    text=p.read_text();assert "\u2014" not in text,str(p)
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
        if "://" not in target and not target.startswith("#"):assert (p.parent/target.split("#")[0]).exists(),f"{p}: {target}"
for case in json.loads((base/"references/examples/decision-fixtures.json").read_text()):
    errors=[]
    if len(case["recommendations"])!=1:errors.append("one recommendation required")
    if not case["sources"] or any(s not in available for s in case["sources"]):errors.append("source evidence missing")
    if case["missing_implementation_owner"] and case["implementation_status"]!="blocked":errors.append("owner gap concealed")
    if case["runtime_verified"]:errors.append("selection cannot establish runtime proof")
    result="REVISE" if errors else "PASS";assert result==case["expected"],case["id"]
    print(f"{case['id']}: {result}; {', '.join(errors) or 'encoded contract preserved'}")
print(f"PASS: {len(available)} archive hashes, local links and 4 encoded selection exercises. No implementation or runtime qualification.")

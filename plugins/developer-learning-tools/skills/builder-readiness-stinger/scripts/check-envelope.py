#!/usr/bin/env python3
"""Check archive/links and encoded advisory boundaries, not learner competence."""
from pathlib import Path
import hashlib,json,re
base=Path(__file__).resolve().parents[1]
rows=json.loads((base/"references/research/source-ledger.json").read_text());count=0
for row in rows:
    if "path" in row:
        assert hashlib.sha256((base/row["path"]).read_bytes()).hexdigest()==row["archive_sha256"],row["id"];count+=1
for p in base.rglob("*.md"):
    if "raw" in p.relative_to(base).parts:continue
    text=p.read_text();assert "\u2014" not in text,str(p)
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
        if "://" not in target and not target.startswith("#"):assert (p.parent/target.split("#")[0]).exists(),f"{p}: {target}"
for case in json.loads((base/"references/examples/readiness-fixtures.json").read_text()):
    errors=[]
    if case["material_unknowns"]:
        if case["status"]!="blocked":errors.append("material unknowns concealed")
    elif len(case["recommendations"])!=1:errors.append("one scoped recommendation required")
    if case["understanding"]!="pending":errors.append("no learner response supports understanding")
    if case["implemented"]:errors.append("advice is not implementation")
    result="REVISE" if errors else "PASS";assert result==case["expected"],case["id"]
    print(f"{case['id']}: {result}; {', '.join(errors) or 'encoded advisory boundary preserved'}")
print(f"PASS: {count} archive hashes, authored local links and 3 encoded readiness cases. No learner or runtime qualification.")

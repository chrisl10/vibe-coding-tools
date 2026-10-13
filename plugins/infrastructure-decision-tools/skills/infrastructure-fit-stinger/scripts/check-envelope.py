#!/usr/bin/env python3
"""Validate evidence/local links and encoded advisory contracts, not provider fit."""
from pathlib import Path
import hashlib,json,re
base=Path(__file__).resolve().parents[1]
rows=json.loads((base/"references/research/source-ledger.json").read_text())
available={r["id"] for r in rows if "path" in r}
for row in rows:
    if "path" in row: assert hashlib.sha256((base/row["path"]).read_bytes()).hexdigest()==row["archive_sha256"],row["id"]
for p in base.rglob("*.md"):
    text=p.read_text();assert "\u2014" not in text,str(p)
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
        if "://" not in target and not target.startswith("#"):assert (p.parent/target.split("#")[0]).exists(),f"{p}: {target}"
for case in json.loads((base/"references/examples/decision-fixtures.json").read_text()):
    errors=[]
    if len(case["recommendations"])!=1:errors.append("one recommendation required")
    if case["eligible"] and (not case["source_evidence"] or any(s not in available for s in case["source_evidence"])):errors.append("eligibility evidence missing")
    if case["operator"] in {"", "unknown"}:errors.append("operator missing")
    if case["cost_status"]=="unpriced" and case["monthly_total"] is not None:errors.append("unknown rate became total")
    result="REVISE" if errors else "PASS";assert result==case["expected"],case["id"]
    print(f"{case['id']}: {result}; {', '.join(errors) or 'encoded contract preserved'}")
print(f"PASS: {len(available)} archive hashes, local links and 4 encoded decision exercises. No provisioning, cost calculation or runtime proof.")

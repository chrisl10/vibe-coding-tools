#!/usr/bin/env python3
"""Check captured source integrity and encoded fidelity fixtures, not understanding."""
from pathlib import Path
import hashlib, json, re
base = Path(__file__).resolve().parents[1]
checks = 0
for row in json.loads((base / "references/research/source-ledger.json").read_text()):
    key = "path" if "path" in row else "fallback_path"
    digest = "archive_sha256" if key == "path" else "fallback_archive_sha256"
    p = base / row[key]
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row[digest], row["id"]
    checks += 1
for p in base.rglob("*.md"):
    text = p.read_text()
    assert "\u2014" not in text, f"em dash: {p}"
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        assert (p.parent / target.split("#")[0]).exists(), f"missing link: {p}: {target}"
        checks += 1
for case in json.loads((base / "references/examples/fidelity-fixtures.json").read_text()):
    mismatches = [k for k, v in case["source"].items() if case["candidate"].get(k) != v]
    result = "REVISE" if mismatches else "PASS"
    assert result == case["expected"], case["id"]
    print(f"Fixture {case['id']}: {result}; differences: {', '.join(mismatches) or 'none'}")
    checks += 1
print(f"PASS: {checks} evidence, local-link and encoded fixture checks. No human comprehension or host-runtime proof.")

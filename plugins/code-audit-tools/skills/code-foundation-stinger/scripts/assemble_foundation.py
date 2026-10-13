#!/usr/bin/env python3
"""Merge scanner output and Drone judgment into contract-valid Foundation outputs.

Reads the JSON from foundation_scan.py, applies the Drone's decisions, validates
every finding and measure against Audit My Code contract 1.0, computes the
dimension verdict (contract section 8), and writes into the workspace:

  <out-dir>/findings.jsonl
  <out-dir>/metrics.json
  <out-dir>/notes.md            (seeded only if it does not exist yet)
  <out-dir>/raw/foundation_scan.json

Drone decisions come from an optional JSON-lines file. Each line is either:
  a new finding (full contract object), or
  {"id": "FND-ENV-009", "_action": "drop", "reason": "..."}                   remove a scanner finding
  {"id": "FND-ENV-009", "_action": "update", "severity": "...", ...fields}     change fields

Findings tagged needs-drone-read must be resolved (updated or dropped, with the
tag removed) unless --allow-unresolved is passed. Python 3.11+, stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from foundation_scan import SECRET_PATTERNS  # noqa: E402

SEV = ["info", "low", "medium", "high", "critical"]
CONF = {"confirmed", "likely", "possible"}
EFFORT = {"S", "M", "L"}
BANDS = {"healthy", "moderate", "at-risk", "critical", "not-run"}
AREAS = "LIB|AGENT|CI|TEST|LINT|DEPS|DOCS|REPO|ENV"
ID_RE = re.compile(rf"^FND-({AREAS})-\d{{3}}$")
REQUIRED = ["id", "dimension", "source", "title", "severity", "confidence", "locations", "evidence", "why_it_matters", "remediation", "effort", "refs", "verified_by"]
DASH = re.compile("[\u2014\u2013]")


def validate_finding(f: dict, i: int) -> list[str]:
    e = []
    tag = f.get("id", f"#{i}")
    for k in REQUIRED:
        if k not in f:
            e.append(f"{tag}: missing field {k}")
    if e:
        return e
    if not ID_RE.match(f["id"]):
        e.append(f"{tag}: id must match FND-<{AREAS}>-NNN")
    if f["dimension"] != "foundation":
        e.append(f"{tag}: dimension must be foundation")
    if f["severity"] not in SEV:
        e.append(f"{tag}: bad severity {f['severity']!r}")
    if f["confidence"] not in CONF:
        e.append(f"{tag}: bad confidence {f['confidence']!r}")
    elif f["confidence"] == "possible" and f["severity"] in ("high", "critical"):
        e.append(f"{tag}: confidence possible cannot have severity above medium")
    if f["effort"] not in EFFORT:
        e.append(f"{tag}: bad effort {f['effort']!r}")
    if not isinstance(f["locations"], list):
        e.append(f"{tag}: locations must be a list")
    else:
        for l in f["locations"]:
            p = l.get("path", "") if isinstance(l, dict) else ""
            if not p or p.startswith("/") or ".." in p.split("/"):
                e.append(f"{tag}: location path must be repo-relative: {p!r}")
    if not isinstance(f["refs"], list) or not f["refs"]:
        e.append(f"{tag}: refs must be a non-empty list")
    for k in ("title", "evidence", "why_it_matters", "remediation", "verified_by"):
        if not isinstance(f[k], str) or not f[k].strip():
            e.append(f"{tag}: {k} must be a non-empty string")
        elif DASH.search(f[k]):
            e.append(f"{tag}: {k} contains an em or en dash")
    if isinstance(f["evidence"], str):
        if f["evidence"].count("\n") > 15:
            e.append(f"{tag}: evidence is longer than 15 lines")
        for name, rx in SECRET_PATTERNS:
            m = rx.search(f["evidence"])
            if m and not m.group(0).endswith("****") and len(m.group(0)) > 12:
                e.append(f"{tag}: evidence appears to contain an unredacted {name}; keep 4 characters then ****")
    if "needs-drone-read" in f.get("tags", []):
        e.append(f"{tag}: still tagged needs-drone-read (resolve with an update or drop line)")
    return e


def verdict(findings: list[dict], measures: list[dict]) -> str:
    if any(f["severity"] == "critical" and f["confidence"] in ("confirmed", "likely") for f in findings):
        return "critical"
    if any(f["severity"] == "high" for f in findings) or sum(1 for m in measures if m["band"] == "critical") >= 2:
        return "at-risk"
    if any(f["severity"] == "medium" for f in findings) or any(m["band"] in ("at-risk", "moderate") for m in measures):
        return "moderate"
    return "healthy"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scan", required=True, type=Path)
    ap.add_argument("--judgment", type=Path)
    ap.add_argument("--measures-extra", type=Path, help="JSON list of measure objects that replace scanner measures with the same key (or add new ones)")
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--summary", required=True, help="one or two sentences answering: is this repository set up for humans and agents to work in safely?")
    ap.add_argument("--cap", action="append", default=[], help="extra coverage cap text (repeatable)")
    ap.add_argument("--allow-unresolved", action="store_true")
    a = ap.parse_args()
    scan = json.loads(a.scan.read_text())
    findings = {f["id"]: f for f in scan["findings"]}
    extra = []
    if a.judgment and a.judgment.exists():
        for n, line in enumerate(a.judgment.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                o = json.loads(line)
            except ValueError as ex:
                print(f"judgment line {n}: not JSON ({ex})", file=sys.stderr)
                return 1
            act = o.pop("_action", None)
            o.pop("reason", None)
            if act == "drop":
                findings.pop(o["id"], None)
            elif act == "update":
                if o["id"] not in findings:
                    print(f"judgment line {n}: cannot update unknown id {o['id']}", file=sys.stderr)
                    return 1
                findings[o["id"]].update({k: v for k, v in o.items() if k != "id"})
            else:
                extra.append(o)
    ids = list(findings)
    for o in extra:
        if o.get("id") in findings:
            print(f"duplicate id {o.get('id')}", file=sys.stderr)
            return 1
        findings[o.get("id", f"new-{len(findings)}")] = o
    final = list(findings.values())
    if a.allow_unresolved:
        for f in final:
            f["tags"] = [t for t in f.get("tags", []) if t != "needs-drone-read"]
    errors = []
    for i, f in enumerate(final):
        errors += validate_finding(f, i)
    seen = set()
    for f in final:
        if f.get("id") in seen:
            errors.append(f"duplicate id {f.get('id')}")
        seen.add(f.get("id"))
    measures = {m["key"]: m for m in scan["measures"]}
    if a.measures_extra:
        for m in json.loads(a.measures_extra.read_text()):
            measures[m["key"]] = m
    for m in measures.values():
        for k in ("key", "label", "value", "unit", "band", "threshold", "source"):
            if k not in m:
                errors.append(f"measure {m.get('key')}: missing {k}")
        if m.get("band") not in BANDS:
            errors.append(f"measure {m.get('key')}: bad band {m.get('band')!r}")
    if DASH.search(a.summary):
        errors.append("summary contains an em or en dash")
    if errors:
        print("VALIDATION FAILED:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1
    final.sort(key=lambda f: (-SEV.index(f["severity"]), f["id"]))
    ms = list(measures.values())
    cov = dict(scan["coverage"])
    cov["caps"] = list(cov.get("caps", [])) + a.cap
    for f in final:
        f.setdefault("tags", [])
    out = a.out_dir
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "findings.jsonl").write_text("".join(json.dumps(f, ensure_ascii=False) + "\n" for f in final), encoding="utf-8")
    metrics = {"dimension": "foundation", "verdict": verdict(final, ms), "summary": a.summary, "measures": ms,
               "coverage": {"files_scanned": cov["files_scanned"], "lines_scanned": cov["lines_scanned"], "skipped": cov["skipped"], "caps": cov["caps"]}}
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "raw" / "foundation_scan.json").write_text(json.dumps(scan, indent=2) + "\n", encoding="utf-8")
    notes = out / "notes.md"
    if not notes.exists():
        notes.write_text("# Foundation audit notes\n\n## Scope and method\n\n## What was run\n\n## Coverage caps\n\n## Not confirmed\n\n## Handoffs to other Drones\n", encoding="utf-8")
    print(json.dumps({"findings": len(final), "verdict": metrics["verdict"], "measures": len(ms), "out": str(out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

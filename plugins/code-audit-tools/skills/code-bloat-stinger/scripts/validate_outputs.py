#!/usr/bin/env python3
"""Check 01-bloat/findings.jsonl and 01-bloat/metrics.json against the
Audit My Code contract (version 1.0) before handing off.

Checks: required fields and enums; id pattern BLOAT-(DUP|DEAD|SIZE|STRUCT)-NNN
and uniqueness; repo-relative locations; `possible` confidence never above
medium; evidence length; measures fields and band scale; coverage fields;
verdict at least as severe as the contract's section 8 default; no em or en
dashes in text written for the reader.

Exit code 0 when clean, 1 when any ERROR. Python 3.9+ standard library only.

Example:
  python3 validate_outputs.py --dir <workspace>/01-bloat
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

SEVERITY = ["info", "low", "medium", "high", "critical"]
CONFIDENCE = {"confirmed", "likely", "possible"}
EFFORT = {"S", "M", "L"}
SCALE = ["healthy", "moderate", "at-risk", "critical"]
BANDS = set(SCALE) | {"not-run"}
ID_RE = re.compile(r"^BLOAT-(DUP|DEAD|SIZE|STRUCT)-\d{3}$")
DASHES = re.compile("[\u2013\u2014]")
REQUIRED = ["id", "dimension", "source", "title", "severity", "confidence", "locations", "evidence",
            "why_it_matters", "remediation", "effort", "refs", "verified_by"]
PROSE = ["title", "why_it_matters", "remediation", "verified_by"]


def expected_verdict(findings: list[dict], measures: list[dict]) -> str:
    sev = [f.get("severity") for f in findings]
    crit_conf = [f for f in findings if f.get("severity") == "critical" and f.get("confidence") in ("confirmed", "likely")]
    bands = [m.get("band") for m in measures]
    if crit_conf:
        return "critical"
    if "high" in sev or bands.count("critical") >= 2:
        return "at-risk"
    if "medium" in sev or any(b in ("at-risk", "moderate", "critical") for b in bands):
        return "moderate"
    return "healthy"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True, help="the 01-bloat folder")
    args = ap.parse_args()
    errors, warns = [], []

    fpath = os.path.join(args.dir, "findings.jsonl")
    mpath = os.path.join(args.dir, "metrics.json")
    npath = os.path.join(args.dir, "notes.md")
    findings: list[dict] = []
    if not os.path.isfile(fpath):
        errors.append("findings.jsonl is missing (write an empty file if there are no findings)")
    else:
        seen = set()
        with open(fpath, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    f = json.loads(line)
                except ValueError as e:
                    errors.append(f"findings.jsonl line {n}: not JSON ({e})")
                    continue
                findings.append(f)
                where = f"finding {f.get('id', '?')} (line {n})"
                for k in REQUIRED:
                    if k not in f:
                        errors.append(f"{where}: missing field '{k}'")
                if not ID_RE.match(str(f.get("id", ""))):
                    errors.append(f"{where}: id must match BLOAT-(DUP|DEAD|SIZE|STRUCT)-NNN")
                if f.get("id") in seen:
                    errors.append(f"{where}: duplicate id")
                seen.add(f.get("id"))
                if f.get("dimension") != "bloat":
                    errors.append(f"{where}: dimension must be 'bloat'")
                if f.get("severity") not in SEVERITY:
                    errors.append(f"{where}: severity must be one of {SEVERITY}")
                if f.get("confidence") not in CONFIDENCE:
                    errors.append(f"{where}: confidence must be one of {sorted(CONFIDENCE)}")
                if f.get("confidence") == "possible" and f.get("severity") in ("high", "critical"):
                    errors.append(f"{where}: confidence 'possible' cannot have severity above medium")
                if f.get("effort") not in EFFORT:
                    errors.append(f"{where}: effort must be S, M, or L")
                if not isinstance(f.get("refs"), list):
                    errors.append(f"{where}: refs must be an array")
                if "tags" in f and not isinstance(f["tags"], list):
                    errors.append(f"{where}: tags must be an array")
                locs = f.get("locations")
                if not isinstance(locs, list):
                    errors.append(f"{where}: locations must be an array")
                else:
                    for loc in locs:
                        p = (loc or {}).get("path", "") if isinstance(loc, dict) else ""
                        if not p:
                            errors.append(f"{where}: every location needs a path")
                        elif p.startswith("/") or re.match(r"^[A-Za-z]:\\", p) or ".scratch/" in p:
                            errors.append(f"{where}: location '{p}' must be repo-relative, not a scratch or absolute path")
                        for k in ("line_start", "line_end"):
                            if isinstance(loc, dict) and k in loc and not isinstance(loc[k], int):
                                errors.append(f"{where}: {k} must be an integer")
                ev = str(f.get("evidence", ""))
                if not ev.strip():
                    errors.append(f"{where}: evidence is empty (no finding without evidence)")
                if ev.count("\n") >= 15:
                    warns.append(f"{where}: evidence has more than 15 lines; trim code excerpts to 15 lines")
                for k in PROSE:
                    if DASHES.search(str(f.get(k, ""))):
                        errors.append(f"{where}: '{k}' contains an em or en dash")

    measures: list[dict] = []
    if not os.path.isfile(mpath):
        errors.append("metrics.json is missing")
    else:
        try:
            with open(mpath, encoding="utf-8") as fh:
                m = json.load(fh)
        except ValueError as e:
            errors.append(f"metrics.json: not JSON ({e})")
            m = {}
        if m.get("dimension") != "bloat":
            errors.append("metrics.json: dimension must be 'bloat'")
        if m.get("verdict") not in SCALE + ["not-run"]:
            errors.append(f"metrics.json: verdict must be one of {SCALE + ['not-run']}")
        if not str(m.get("summary", "")).strip():
            errors.append("metrics.json: summary is empty")
        if DASHES.search(str(m.get("summary", ""))):
            errors.append("metrics.json: summary contains an em or en dash")
        measures = m.get("measures") or []
        keys = set()
        for i, me in enumerate(measures):
            for k in ("key", "label", "value", "unit", "band", "threshold", "source"):
                if k not in me:
                    errors.append(f"metrics.json measures[{i}]: missing '{k}'")
            if me.get("band") not in BANDS:
                errors.append(f"metrics.json measures[{i}] ({me.get('key')}): band must be one of {sorted(BANDS)}")
            if me.get("key") in keys:
                errors.append(f"metrics.json measures[{i}]: duplicate key {me.get('key')}")
            keys.add(me.get("key"))
            if DASHES.search(str(me.get("label", "")) + str(me.get("threshold", ""))):
                errors.append(f"metrics.json measures[{i}]: label or threshold contains an em or en dash")
        cov = m.get("coverage")
        if not isinstance(cov, dict):
            errors.append("metrics.json: coverage object missing")
        else:
            for k in ("files_scanned", "lines_scanned", "skipped", "caps"):
                if k not in cov:
                    errors.append(f"metrics.json coverage: missing '{k}'")
            if isinstance(cov.get("caps"), list) and not cov["caps"]:
                warns.append("coverage.caps is empty: that claims no limit applied. jscpd always has a size cap; record it as lifted.")
        for want in ("dup_std_50", "dup_both_50", "dup_std_100", "dup_both_100"):
            if want not in keys:
                warns.append(f"metrics.json: expected measure '{want}' not present (mark it band 'not-run' if the step did not run)")
        if m.get("verdict") in SCALE:
            exp = expected_verdict(findings, measures)
            if SCALE.index(m["verdict"]) < SCALE.index(exp):
                errors.append(f"metrics.json: verdict '{m['verdict']}' is milder than the contract default '{exp}' for these findings and bands")

    if not os.path.isfile(npath):
        errors.append("notes.md is missing")
    else:
        with open(npath, encoding="utf-8") as fh:
            notes = fh.read()
        if DASHES.search(notes):
            errors.append("notes.md contains an em or en dash")
        if "Not confirmed" not in notes:
            warns.append("notes.md has no 'Not confirmed' section (add one, even if it says 'none')")

    for w in warns:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(findings)} findings, {len(measures)} measures: {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

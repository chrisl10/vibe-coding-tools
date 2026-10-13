#!/usr/bin/env python3
"""Check a findings JSONL file and a metrics JSON file against the Audit My Code contract 1.0.

Standard library only. Read-only.

Usage:
    python3 validate_findings.py FINDINGS.jsonl [--metrics METRICS.json]
                                 [--prefix SEC-POLY] [--source polyglot-security-wasp-drone]
                                 [--repo REPO_ROOT]

Checks: required fields and enums, id pattern and uniqueness, `possible`
confidence capped at `medium`, evidence at most 15 code lines, obvious
unredacted secrets in evidence, repo-relative paths (and that they exist when
--repo is given), metrics shape, verdict consistent with contract section 8.

Exit 0 when there are no errors (warnings allowed), 1 when any error, 2 on bad input.

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["id", "dimension", "source", "title", "severity", "confidence", "locations", "evidence",
            "why_it_matters", "remediation", "effort", "refs", "verified_by"]
SEVERITY = ["info", "low", "medium", "high", "critical"]
CONFIDENCE = {"confirmed", "likely", "possible"}
DIMENSIONS = {"foundation", "bloat", "security", "quality"}
EFFORT = {"S", "M", "L"}
BANDS = {"healthy", "moderate", "at-risk", "critical", "not-run"}
SECRET_SHAPES = re.compile(
    r"(AKIA[A-Z2-7]{16}|gh[pousr]_[0-9A-Za-z]{36}|github_pat_\w{40,}|(sk|rk)_(live|prod)_[0-9A-Za-z]{10,}"
    r"|AIza[\w-]{35}|sk-(proj|svcacct|admin)-[\w-]{20,}|sk-ant-[\w-]{20,}|xox[bpe]-\d{6,}|npm_[A-Za-z0-9]{36}"
    r"|-----BEGIN[ A-Z]*PRIVATE KEY-----\s*\n\s*[A-Za-z0-9+/=]{20,})"
)


def check_findings(lines, prefix, source, repo):
    errors, warnings, findings = [], [], []
    seen = set()
    id_rx = re.compile(r"^" + re.escape(prefix) + r"-\d{3,}$") if prefix else re.compile(r"^[A-Z]+-[A-Z0-9]+-\d{3,}$")
    for n, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        where = f"line {n}"
        try:
            f = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{where}: not valid JSON ({exc.msg})")
            continue
        if not isinstance(f, dict):
            errors.append(f"{where}: not a JSON object")
            continue
        findings.append(f)
        fid = f.get("id", "?")
        where = f"{where} ({fid})"
        for k in REQUIRED:
            if k not in f:
                errors.append(f"{where}: missing field {k}")
            elif k not in ("locations", "refs") and (f[k] is None or (isinstance(f[k], str) and not f[k].strip())):
                errors.append(f"{where}: empty field {k}")
        if not id_rx.match(str(fid)):
            errors.append(f"{where}: id does not match {id_rx.pattern}")
        if fid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(fid)
        if f.get("dimension") not in DIMENSIONS:
            errors.append(f"{where}: bad dimension {f.get('dimension')!r}")
        if source and f.get("source") != source:
            errors.append(f"{where}: source should be {source}")
        sev, conf = f.get("severity"), f.get("confidence")
        if sev not in SEVERITY:
            errors.append(f"{where}: bad severity {sev!r}")
        if conf not in CONFIDENCE:
            errors.append(f"{where}: bad confidence {conf!r}")
        if conf == "possible" and sev in ("high", "critical"):
            errors.append(f"{where}: confidence possible cannot have severity {sev} (contract rule 3)")
        if f.get("effort") not in EFFORT:
            errors.append(f"{where}: bad effort {f.get('effort')!r}")
        if not isinstance(f.get("refs"), list):
            errors.append(f"{where}: refs must be an array")
        elif not any(str(r).startswith("CWE-") for r in f["refs"]):
            warnings.append(f"{where}: no CWE in refs (cross-Drone merge keys on CWE)")
        if "tags" in f and not isinstance(f["tags"], list):
            errors.append(f"{where}: tags must be an array")
        locs = f.get("locations")
        if not isinstance(locs, list):
            errors.append(f"{where}: locations must be an array")
        else:
            if not locs:
                warnings.append(f"{where}: empty locations (allowed only for repo-wide findings)")
            for loc in locs:
                if not isinstance(loc, dict) or "path" not in loc:
                    errors.append(f"{where}: each location needs a path")
                    continue
                p = str(loc["path"])
                if p.startswith("/") or re.match(r"^[A-Za-z]:\\", p) or ".." in Path(p).parts:
                    errors.append(f"{where}: path must be repo-relative: {p}")
                for key in ("line_start", "line_end"):
                    if key in loc and not (isinstance(loc[key], int) and loc[key] >= 0):
                        errors.append(f"{where}: {key} must be a non-negative integer")
                if isinstance(loc.get("line_start"), int) and isinstance(loc.get("line_end"), int) and loc["line_end"] < loc["line_start"]:
                    errors.append(f"{where}: line_end before line_start")
                if repo and not (Path(repo) / p).exists():
                    warnings.append(f"{where}: path not found under repo: {p}")
        ev = f.get("evidence")
        if isinstance(ev, str):
            if SECRET_SHAPES.search(ev):
                errors.append(f"{where}: evidence looks like it holds an unredacted secret (keep 4 chars then ****)")
            code_lines = [l for l in ev.splitlines() if l.strip()]
            if len(code_lines) > 16:  # 15 lines plus one header line such as path:lines
                warnings.append(f"{where}: evidence has {len(code_lines)} lines; contract allows a 15-line excerpt")
        for k in ("title",):
            if isinstance(f.get(k), str) and ("\u2014" in f[k] or "\u2013" in f[k]):
                warnings.append(f"{where}: {k} contains an em or en dash")
    return findings, errors, warnings


def expected_verdict(findings, measures):
    if any(f.get("severity") == "critical" and f.get("confidence") in ("confirmed", "likely") for f in findings):
        return "critical"
    crit_bands = sum(1 for m in measures if m.get("band") == "critical")
    if any(f.get("severity") == "high" for f in findings) or crit_bands >= 2:
        return "at-risk"
    if any(f.get("severity") == "medium" for f in findings) or any(m.get("band") in ("at-risk", "moderate") for m in measures):
        return "moderate"
    return "healthy"


def check_metrics(path, findings):
    errors, warnings = [], []
    try:
        m = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"metrics: cannot read JSON ({exc.__class__.__name__})"], []
    for k in ("dimension", "verdict", "summary", "measures", "coverage"):
        if k not in m:
            errors.append(f"metrics: missing {k}")
    if m.get("verdict") not in BANDS:
        errors.append(f"metrics: bad verdict {m.get('verdict')!r}")
    measures = m.get("measures") if isinstance(m.get("measures"), list) else []
    for i, meas in enumerate(measures):
        for k in ("key", "label", "value", "band", "source"):
            if k not in meas:
                errors.append(f"metrics.measures[{i}]: missing {k}")
        if meas.get("band") not in BANDS:
            errors.append(f"metrics.measures[{i}]: bad band {meas.get('band')!r}")
    cov = m.get("coverage") if isinstance(m.get("coverage"), dict) else {}
    if "caps" not in cov or not isinstance(cov.get("caps"), list):
        errors.append("metrics.coverage.caps must be an array (empty claims no limit applied)")
    elif not cov["caps"]:
        warnings.append("metrics.coverage.caps is empty: this claims no tool limit or skipped scope applied")
    exp = expected_verdict(findings, measures)
    order = ["healthy", "moderate", "at-risk", "critical"]
    v = m.get("verdict")
    if v in order and order.index(v) < order.index(exp):
        errors.append(f"metrics: verdict {v} is softer than the contract default {exp}")
    elif v in order and v != exp:
        warnings.append(f"metrics: verdict {v} differs from the contract default {exp}; make sure a guide states the stricter rule")
    if v == "not-run" and findings:
        warnings.append("metrics: verdict not-run but findings exist")
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate findings.jsonl and metrics.json against Audit My Code contract 1.0.")
    ap.add_argument("findings")
    ap.add_argument("--metrics")
    ap.add_argument("--prefix", default="SEC-POLY", help="required id prefix (default SEC-POLY; empty string for any)")
    ap.add_argument("--source", default="polyglot-security-wasp-drone", help="required source value (empty for any)")
    ap.add_argument("--repo", help="audited repo root, to warn on paths that do not exist")
    args = ap.parse_args(argv)
    p = Path(args.findings)
    if not p.is_file():
        print(f"not a file: {args.findings}", file=sys.stderr)
        return 2
    findings, errors, warnings = check_findings(p.read_text(encoding="utf-8").splitlines(), args.prefix, args.source, args.repo)
    if args.metrics:
        e2, w2 = check_metrics(args.metrics, findings)
        errors += e2
        warnings += w2
    counts = {s: sum(1 for f in findings if f.get("severity") == s) for s in reversed(SEVERITY)}
    print(json.dumps({"findings": len(findings), "by_severity": counts, "errors": errors, "warnings": warnings}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

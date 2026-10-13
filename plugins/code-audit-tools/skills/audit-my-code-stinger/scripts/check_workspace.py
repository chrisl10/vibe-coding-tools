#!/usr/bin/env python3
"""Check an Audit My Code workspace against contract 1.0.

Usage:
    python3 check_workspace.py <workspace>                      # whole run, before the brief
    python3 check_workspace.py <workspace> --dimension security # one dimension, after its Drone returns

Exit code 0 when clean, 1 when any check fails. Every failure is printed on its own line.
Standard library only, so it runs on any harness without an install step.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CONTRACT = "1.0"
DIMENSIONS = {
    "foundation": "00-foundation",
    "bloat": "01-bloat",
    "security": "02-security",
    "quality": "03-quality",
}
TIER_DIMENSIONS = {
    "foundation": ["foundation"],
    "vibe": ["foundation", "bloat"],
    "basic": ["foundation", "bloat", "security"],
    "full": ["foundation", "bloat", "security", "quality"],
    "mario": ["foundation", "bloat", "security", "quality"],
}
SEVERITIES = {"critical", "high", "medium", "low", "info"}
CONFIDENCES = {"confirmed", "likely", "possible"}
EFFORTS = {"S", "M", "L"}
BANDS = {"healthy", "moderate", "at-risk", "critical", "not-run"}
REQUIRED = ("id", "dimension", "source", "title", "severity", "confidence", "locations",
            "evidence", "why_it_matters", "remediation", "effort", "refs", "verified_by")
ID_RE = re.compile(r"^(FND|BLOAT|SEC|QA)-[A-Z0-9]+-\d{3,}$")
SECRET_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:sk-ant-|sk_live_|rk_live_|ghp_|github_pat_|xox[abpsr]-|AKIA|ASIA)[A-Za-z0-9_-]{12,}"
    r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing: {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON: {path}: {exc}")
    return None


def check_metrics(path: Path, dimension: str, errors: list[str]) -> None:
    data = load_json(path, errors)
    if data is None:
        return
    for key in ("verdict", "summary", "measures", "coverage"):
        if key not in data:
            errors.append(f"{path}: missing '{key}'")
    if data.get("verdict") not in BANDS:
        errors.append(f"{path}: verdict '{data.get('verdict')}' is not one of {sorted(BANDS)}")
    if data.get("dimension") not in (None, dimension):
        errors.append(f"{path}: dimension '{data.get('dimension')}' does not match folder '{dimension}'")
    for i, m in enumerate(data.get("measures") or []):
        if m.get("band") not in BANDS:
            errors.append(f"{path}: measures[{i}] band '{m.get('band')}' is not legal")
        for key in ("key", "label", "value", "threshold"):
            if key not in m:
                errors.append(f"{path}: measures[{i}] missing '{key}'")
    coverage = data.get("coverage") or {}
    if "caps" not in coverage:
        errors.append(f"{path}: coverage.caps missing (an empty list is a claim that no limit applied)")


def check_findings(path: Path, dimension: str, seen: set[str], errors: list[str]) -> int:
    if not path.exists():
        errors.append(f"missing: {path} (write an empty file when there are no findings)")
        return 0
    count = 0
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        where = f"{path.name}:{n}"
        try:
            f = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{where}: invalid JSON: {exc}")
            continue
        count += 1
        missing = [k for k in REQUIRED if k not in f]
        if missing:
            errors.append(f"{where}: missing {missing}")
        fid = str(f.get("id", ""))
        if not ID_RE.match(fid):
            errors.append(f"{where}: id '{fid}' does not match <DIM>-<SOURCE>-<NNN>")
        if fid in seen:
            errors.append(f"{where}: duplicate id '{fid}'")
        seen.add(fid)
        if f.get("dimension") != dimension:
            errors.append(f"{where}: dimension '{f.get('dimension')}' in the {dimension} folder")
        if f.get("severity") not in SEVERITIES:
            errors.append(f"{where}: severity '{f.get('severity')}' is not legal")
        if f.get("confidence") not in CONFIDENCES:
            errors.append(f"{where}: confidence '{f.get('confidence')}' is not legal")
        if f.get("effort") not in EFFORTS:
            errors.append(f"{where}: effort '{f.get('effort')}' is not S, M, or L")
        if f.get("confidence") == "possible" and f.get("severity") in {"critical", "high"}:
            errors.append(f"{where}: 'possible' confidence cannot carry severity above medium")
        for key in ("evidence", "verified_by", "remediation"):
            if not str(f.get(key, "")).strip():
                errors.append(f"{where}: empty '{key}'")
        if not isinstance(f.get("locations"), list):
            errors.append(f"{where}: locations must be a list")
        if SECRET_RE.search(line):
            errors.append(f"{where}: unredacted secret-looking string (keep 4 chars, then ****)")
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("workspace", type=Path)
    ap.add_argument("--dimension", choices=sorted(DIMENSIONS))
    a = ap.parse_args()
    ws = a.workspace.resolve()
    errors: list[str] = []

    intake = load_json(ws / "intake.json", errors) or {}
    tier = str(intake.get("tier", "")).lower()
    if intake and intake.get("contract") != CONTRACT:
        errors.append(f"intake.json: contract '{intake.get('contract')}' is not {CONTRACT}")
    if intake and tier not in TIER_DIMENSIONS:
        errors.append(f"intake.json: unknown tier '{intake.get('tier')}'")
    for key in ("repo", "stacks", "scope", "workspace"):
        if intake and key not in intake:
            errors.append(f"intake.json: missing '{key}'")
    execution = intake.get("execution") if intake else None
    if intake and not isinstance(execution, dict):
        errors.append("intake.json: missing 'execution' (the user's answer about running repository code)")
    elif intake:
        mode = execution.get("mode")
        if mode not in {"none", "container", "host"}:
            errors.append(f"intake.json: execution.mode '{mode}' is not none, container, or host")
        elif bool(execution.get("allowed")) != (mode != "none"):
            errors.append("intake.json: execution.allowed must be true exactly when mode is container or host")

    wanted = [a.dimension] if a.dimension else TIER_DIMENSIONS.get(tier, [])
    seen: set[str] = set()
    total = 0
    for dim in wanted:
        folder = ws / DIMENSIONS[dim]
        merged = folder / "findings.jsonl"
        per_source = sorted(folder.glob("findings-*.jsonl"))
        if dim == "security" and per_source and not merged.exists():
            # Security Drones write per-source files; the orchestrator merges them after W1.
            if a.dimension is None:
                errors.append(f"{folder}: per-source files not merged yet (run merge_security.py)")
            for p in sorted(folder.glob("metrics-*.json")):
                check_metrics(p, dim, errors)
            for p in per_source:
                total += check_findings(p, dim, seen, errors)
        else:
            check_metrics(folder / "metrics.json", dim, errors)
            total += check_findings(merged, dim, seen, errors)
        if dim == "security" and per_source and not merged.exists():
            for p in per_source:
                notes = folder / ("notes-" + p.stem.removeprefix("findings-") + ".md")
                if not notes.exists():
                    errors.append(f"missing: {notes}")
        elif not (folder / "notes.md").exists():
            errors.append(f"missing: {folder / 'notes.md'}")
    if not a.dimension and tier == "mario":
        for name in ("roadmap.md", "plan.json"):
            if not (ws / "04-remediation" / name).exists():
                errors.append(f"missing: {ws / '04-remediation' / name}")
    if not a.dimension and not (ws / "evidence-index.md").exists():
        errors.append(f"missing: {ws / 'evidence-index.md'}")

    for e in errors:
        print(f"FAIL {e}")
    print(f"{'OK' if not errors else 'FAILED'}: {len(wanted)} dimension(s), {total} finding(s), {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

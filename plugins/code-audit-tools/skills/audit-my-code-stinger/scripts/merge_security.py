#!/usr/bin/env python3
"""Merge per-source security output into 02-security/findings.jsonl and metrics.json.

Usage:
    python3 merge_security.py <workspace>

Each security Drone writes findings-<source>.jsonl and metrics-<source>.json so parallel
Drones never write the same file. This script concatenates the findings (ids are already
unique by prefix), combines measures and coverage, and sets the merged verdict with the
contract's section 8 rule. The per-source files are kept for the evidence index.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ORDER = ["healthy", "moderate", "at-risk", "critical"]


def verdict_from(findings: list[dict], measures: list[dict], source_verdicts: list[str]) -> str:
    """Contract section 8, applied to the merged security findings, measures, and source verdicts."""
    ran = findings or any(m.get("band") not in (None, "not-run") for m in measures) \
        or any(v in ORDER for v in source_verdicts)
    if not ran:
        return "not-run"
    if any(f["severity"] == "critical" and f["confidence"] in {"confirmed", "likely"} for f in findings):
        computed = "critical"
    elif any(f["severity"] == "high" for f in findings) or any(m.get("band") == "critical" for m in measures):
        computed = "at-risk"
    elif any(f["severity"] == "medium" for f in findings) or any(m.get("band") in {"at-risk", "moderate"} for m in measures):
        computed = "moderate"
    else:
        computed = "healthy"
    # A source Drone may apply a stricter rule from its own guide; never report better than it did.
    return max([computed, *(v for v in source_verdicts if v in ORDER)], key=ORDER.index)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    folder = Path(sys.argv[1]).resolve() / "02-security"
    findings: list[dict] = []
    for p in sorted(folder.glob("findings-*.jsonl")):
        findings += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    measures: list[dict] = []
    summaries: list[str] = []
    files_scanned = 0
    lines_scanned = 0
    source_verdicts: list[str] = []
    skipped: list[str] = []
    caps: list[str] = []
    sources: list[str] = []
    for p in sorted(folder.glob("metrics-*.json")):
        m = json.loads(p.read_text(encoding="utf-8"))
        source = p.stem.removeprefix("metrics-")
        sources.append(source)
        measures += [dict(x, source=x.get("source", source)) for x in m.get("measures", [])]
        if m.get("summary"):
            summaries.append(m["summary"])
        cov = m.get("coverage", {})
        files_scanned = max(files_scanned, int(cov.get("files_scanned") or 0))
        lines_scanned = max(lines_scanned, int(cov.get("lines_scanned") or 0))
        source_verdicts.append(str(m.get("verdict", "")))
        skipped += cov.get("skipped", [])
        caps += [f"{source}: {c}" for c in cov.get("caps", [])]
    if not sources:
        print(f"no metrics-*.json in {folder}")
        return 1
    severities = {s: sum(1 for f in findings if f["severity"] == s) for s in ("critical", "high", "medium", "low", "info")}
    merged = {
        "dimension": "security",
        "verdict": verdict_from(findings, measures, source_verdicts),
        "summary": " ".join(summaries),
        "measures": measures,
        "coverage": {"files_scanned": files_scanned, "lines_scanned": lines_scanned, "skipped": sorted(set(skipped)), "caps": caps},
        "sources": sources,
        "severity_counts": severities,
    }
    notes = ["# Security notes\n", f"Merged from {len(sources)} sources: {', '.join(sources)}.\n"]
    for p in sorted(folder.glob("notes-*.md")):
        notes.append(f"\n## {p.stem.removeprefix('notes-')}\n\n" + p.read_text(encoding="utf-8").strip() + "\n")
    (folder / "notes.md").write_text("".join(notes), encoding="utf-8")
    (folder / "findings.jsonl").write_text("".join(json.dumps(f) + "\n" for f in findings), encoding="utf-8")
    (folder / "metrics.json").write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    print(f"merged {len(findings)} findings from {len(sources)} sources: verdict {merged['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

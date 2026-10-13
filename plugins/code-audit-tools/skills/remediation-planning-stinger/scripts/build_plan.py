#!/usr/bin/env python3
"""build_plan.py: first-cut remediation plan from an Audit My Code workspace.

Reads every findings.jsonl under the workspace (00-foundation, 01-bloat,
02-security, 03-quality), merges duplicate findings, clusters them into work
packages by code area (path prefix) plus root-cause kind (CWE, else the kind
segment of the finding id), assigns waves (now, next, later) from severity,
confidence and effort, and writes 04-remediation/plan.json.

This is a first cut. The remediation-planning-wasp-drone refines it with
judgment (see guides/01 and guides/02). Python 3.9+ standard library only.

Usage:
  python3 build_plan.py WORKSPACE [--repo REPO_PATH] [--depth 2]
                        [--out PLAN_JSON] [--roadmap-draft PATH] [--quiet]

Exit codes: 0 ok, 1 no findings files found, 2 usage or parse error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

CONTRACT = "1.0"
DIMENSION_DIRS = ["00-foundation", "01-bloat", "02-security", "03-quality"]
SEV_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
SEV_WEIGHT = {"critical": 10, "high": 6, "medium": 3, "low": 1, "info": 0}
CONF_FACTOR = {"confirmed": 1.0, "likely": 0.8, "possible": 0.5}
# Rough hours per finding effort bucket (S under 1h, M under 1 day, L over 1 day).
EFFORT_HOURS = {"S": 0.75, "M": 5.0, "L": 16.0}
WAVES = ["now", "next", "later"]
CWE_RE = re.compile(r"CWE-\d+", re.I)
ID_RE = re.compile(r"^([A-Z]+)-([A-Z0-9]+)-\d+$")


def slugify(text: str, limit: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:limit].strip("-") or "area"


def load_findings(workspace: Path):
    findings, files = [], []
    for d in DIMENSION_DIRS:
        p = workspace / d / "findings.jsonl"
        if not p.is_file():
            continue
        files.append(str(p.relative_to(workspace)))
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{p}:{n}: invalid JSON ({exc})")
            if not isinstance(obj, dict) or "id" not in obj:
                raise SystemExit(f"{p}:{n}: finding without id")
            findings.append(obj)
    return findings, files


def cwe_of(f: dict) -> str:
    for r in f.get("refs") or []:
        m = CWE_RE.search(str(r))
        if m:
            return m.group(0).upper()
    return ""


def kind_of(f: dict) -> str:
    """Root-cause key: CWE when present, else the source segment of the id."""
    c = cwe_of(f)
    if c:
        return c
    m = ID_RE.match(str(f.get("id", "")))
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return str(f.get("dimension", "misc")).upper()


def area_of(path: str, depth: int) -> str:
    parts = [p for p in path.replace("\\", "/").split("/") if p and p != "."]
    if not parts:
        return "(repo-wide)"
    if len(parts) == 1:
        return "(repo-root)"
    return "/".join(parts[: min(depth, len(parts) - 1)])


def primary_location(f: dict):
    locs = f.get("locations") or []
    return locs[0] if locs else None


def overlap(a: dict, b: dict) -> bool:
    if a.get("path") != b.get("path"):
        return False
    a0, a1 = a.get("line_start", 0) or 0, a.get("line_end", a.get("line_start", 0)) or 0
    b0, b1 = b.get("line_start", 0) or 0, b.get("line_end", b.get("line_start", 0)) or 0
    return a0 <= b1 and b0 <= a1


ADVISORY_RE = re.compile(r"\b(CVE-\d{4}-\d{4,}|GHSA(?:-[0-9a-z]{4}){3})\b", re.I)
NON_KEY_CWES = {"CWE-1395", "CWE-1104"}   # generic component CWEs: never a merge key (mirrors render_brief.py)
MANIFEST_RE = re.compile(r"(^|/)(package(-lock)?\.json|pnpm-lock\.yaml|yarn\.lock|npm-shrinkwrap\.json|bun\.lockb?|"
                         r"requirements[^/]*\.txt|poetry\.lock|Pipfile(\.lock)?|pyproject\.toml|Cargo\.(toml|lock)|go\.(mod|sum))$")


def merge_cwe(f: dict) -> str:
    for r in f.get("refs") or []:
        for m in CWE_RE.finditer(str(r)):
            c = m.group(0).upper()
            if c not in NON_KEY_CWES:
                return c
    return ""


def advisories_of(f: dict) -> frozenset:
    return frozenset(m.group(1).upper() for r in (f.get("refs") or []) for m in ADVISORY_RE.finditer(str(r)))


def merge_duplicates(findings):
    """Same path, overlapping lines, same CWE (when both have one): keep higher severity.
    Findings whose CVE or GHSA ids differ never merge, and CWE-1395 and CWE-1104 are not merge keys."""
    kept, dup_of = [], {}
    ordered = sorted(findings, key=lambda f: -SEV_ORDER.get(f.get("severity", "info"), 0))
    for f in ordered:
        loc, c = primary_location(f), merge_cwe(f)
        match = None
        if loc and c:
            for k in kept:
                kl = primary_location(k)
                if kl and merge_cwe(k) == c and advisories_of(k) == advisories_of(f) and overlap(loc, kl):
                    match = k
                    break
        if match:
            dup_of[f["id"]] = match["id"]
        else:
            kept.append(f)
    return kept, dup_of


OWNER_BY_EXT = [
    (re.compile(r"\.svelte$|\.svelte\.(ts|js)$"), "svelte-wasp-drone"),
    (re.compile(r"\.(tsx|jsx)$"), "react-wasp-drone"),
    (re.compile(r"\.py$"), "python-wasp-drone"),
    (re.compile(r"\.rs$|Cargo\.toml$"), "rust-wasp-drone"),
    (re.compile(r"\.go$|go\.mod$"), "go-wasp-drone"),
    (re.compile(r"(^|/)Dockerfile|docker-compose|\.github/workflows/"), "devops-wasp-drone"),
    (re.compile(r"package(-lock)?\.json$|pnpm-lock|yarn\.lock|requirements.*\.txt$|poetry\.lock"), "dependency-audit-wasp-drone"),
    (re.compile(r"\.sql$|(^|/)migrations?/|drizzle|schema\.prisma$"), "db-wasp-drone"),
    (re.compile(r"\.(ts|js|mjs|cjs)$"), "typescript-node-wasp-drone"),
]


def owner_for(paths, dimension: str, kinds) -> str:
    if dimension == "foundation":   # route by dimension before path (a manifest path is not a dependency finding)
        return "github-repo-health-wasp-drone"
    votes = defaultdict(int)
    for p in paths:
        for rx, drone in OWNER_BY_EXT:
            if rx.search(p):
                votes[drone] += 1
                break
    if votes:
        return max(votes.items(), key=lambda kv: kv[1])[0]
    if dimension == "foundation":
        return "github-repo-health-wasp-drone"
    if dimension == "security":
        return "security-wasp-drone"
    return "library-wasp-drone"


def is_test_kind(f: dict) -> bool:
    blob = " ".join([str(f.get("id", "")), " ".join(f.get("tags") or []), str(f.get("title", ""))]).lower()
    return bool(re.search(r"\btest|coverage|-test-|-cov-", blob))


def hours_to_bucket(h: float) -> str:
    if h < 1:
        return "XS"
    if h <= 3:
        return "S"
    if h <= 8:
        return "M"
    if h <= 24:
        return "L"
    return "XL"


def exploited(f: dict) -> bool:
    blob = " ".join(map(str, (f.get("refs") or []))) + " " + " ".join(f.get("tags") or [])
    return bool(re.search(r"\bKEV\b|actively[- ]exploited", blob, re.I))


def assign_wave(wp: dict) -> str:
    sev, hours, score = wp["max_severity"], wp["effort_hours"], wp["priority_score"]
    if sev == "critical" or wp["exploited"]:
        return "now"
    if sev == "high":
        return "now" if hours <= 24 else "next"
    if sev == "medium":
        return "next" if (hours <= 8 or score >= 9) else "later"
    return "later"


def existing_numbers(repo: Path | None, prefix: str, base: str):
    nums = []
    if repo and (repo / "library" / base).exists():
        for p in (repo / "library" / base).rglob(f"{prefix}-*"):
            m = re.match(rf"{prefix}-(\d+)-", p.name)
            if m and p.is_dir():
                nums.append(int(m.group(1)))
    return nums


def knowledge_domain(area: str) -> str:
    a = area.lower()
    for key, dom in [("auth", "auth"), ("db", "data"), ("data", "data"), ("migrat", "data"),
                     ("api", "architecture"), ("ui", "frontend"), ("web", "frontend"),
                     ("component", "frontend"), ("test", "standards"), ("ci", "infrastructure"),
                     (".github", "infrastructure"), ("infra", "infrastructure"), ("secur", "security")]:
        if key in a:
            return dom
    return "architecture"


def build(workspace: Path, repo: Path | None, depth: int):
    findings, files = load_findings(workspace)
    if not files:
        return None
    actionable = [f for f in findings if f.get("severity") != "info"]
    info_ids = [f["id"] for f in findings if f.get("severity") == "info"]
    kept, dup_of = merge_duplicates(actionable)

    clusters = defaultdict(list)
    for f in kept:
        loc = primary_location(f)
        area = area_of(loc["path"], depth) if loc else "(repo-wide)"
        clusters[(area, kind_of(f))].append(f)

    items = []
    for (area, kind), fs in clusters.items():
        paths = sorted({l["path"] for f in fs for l in (f.get("locations") or [])})
        hours = sum(EFFORT_HOURS.get(f.get("effort", "M"), 5.0) for f in fs)
        score = sum(SEV_WEIGHT.get(f.get("severity", "low"), 0) * CONF_FACTOR.get(f.get("confidence", "possible"), 0.5) for f in fs)
        top = max(fs, key=lambda f: SEV_ORDER.get(f.get("severity", "info"), 0))
        dims = sorted({f.get("dimension", "") for f in fs})
        merged = sorted(i for i, k in dup_of.items() if k in {f["id"] for f in fs})
        wp = {
            "id": "",
            "title": f"{kind} in {area}",
            "root_cause_hint": top.get("title", ""),
            "area": area,
            "kind": kind,
            "cwe": sorted({cwe_of(f) for f in fs if cwe_of(f)}),
            "dimensions": dims,
            "finding_ids": sorted(f["id"] for f in fs),
            "merged_duplicate_ids": merged,
            "paths": paths,
            "max_severity": top.get("severity", "low"),
            "severity_counts": {s: sum(1 for f in fs if f.get("severity") == s) for s in ("critical", "high", "medium", "low")},
            "exploited": any(exploited(f) for f in fs),
            "effort_hours": round(hours, 2),
            "effort": hours_to_bucket(hours),
            "priority_score": round(score, 2),
            "owner_drone": owner_for(paths, top.get("dimension", ""), [kind]),
            "has_test_work": any(is_test_kind(f) for f in fs),
            "depends_on": [],
            "wave": "",
            "needs_judgment": [],
        }
        if len(fs) == 1:
            wp["needs_judgment"].append("single-finding cluster: confirm it should not merge into a neighbour with the same root cause")
        if wp["effort"] in ("L", "XL"):
            wp["needs_judgment"].append("large work package: consider splitting into expand, migrate, contract steps (guide 02)")
        if wp["area"] in ("(repo-wide)", "(repo-root)"):
            wp["needs_judgment"].append("no code area: group by theme instead of path")
        items.append(wp)

    # Stable ordering and ids: severity, score, then name.
    items.sort(key=lambda w: (-SEV_ORDER[w["max_severity"]], -w["priority_score"], w["title"]))
    for i, wp in enumerate(items, 1):
        wp["id"] = f"WP-{i:03d}"
        wp["wave"] = assign_wave(wp)

    # Dependencies: tests before structural change in the same area; shared files sequence by priority.
    by_area = defaultdict(list)
    for wp in items:
        by_area[wp["area"]].append(wp)
    for wps in by_area.values():
        tests = [w for w in wps if w["has_test_work"]]
        for w in wps:
            if w in tests or "bloat" not in w["dimensions"]:
                continue
            for t in tests:
                if t["id"] not in w["depends_on"]:
                    w["depends_on"].append(t["id"])
    shared = []
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            # Manifests and lockfiles are touched by many unrelated packages; they do not imply an order.
            common = sorted(p for p in set(a["paths"]) & set(b["paths"]) if not MANIFEST_RE.search(p))
            if common and a["area"] != "(repo-wide)":
                if a["id"] not in b["depends_on"] and b["id"] not in a["depends_on"]:
                    b["depends_on"].append(a["id"])
                shared.append({"between": [a["id"], b["id"]], "files": common[:10]})
    # A dependency may not sit in a later wave than its dependent.
    changed = True
    while changed:
        changed = False
        by_id = {w["id"]: w for w in items}
        for w in items:
            for d in w["depends_on"]:
                dep = by_id[d]
                if WAVES.index(dep["wave"]) > WAVES.index(w["wave"]):
                    dep["wave"] = w["wave"]
                    changed = True

    # Proposed documents (paths only; nothing is written here).
    prd_nums = existing_numbers(repo, "prd", "requirements")
    prd_n = (max(prd_nums) if prd_nums else 0)
    numbering = "from-library" if prd_nums else "provisional"
    for wp in items:
        prd_n += 1
        slug = slugify(f"{wp['kind']}-{wp['area']}")
        wp["proposed_docs"] = {
            "prd": {
                "number": f"{prd_n:03d}",
                "numbering": numbering,
                "path": f"library/requirements/backlog/prd-{prd_n:03d}-{slug}/prd-{prd_n:03d}-{slug}-index.md",
                "acceptance_from_findings": wp["finding_ids"],
                "verification": "re-run audit dimension(s): " + ", ".join(wp["dimensions"]),
            },
            "ird": [],
            "knowledge": [],
        }
        if wp["area"] not in ("(repo-wide)", "(repo-root)"):
            dom = knowledge_domain(wp["area"])
            kslug = slugify(wp["area"])
            kpath = f"library/knowledge/private/{dom}/{kslug}.md"
            exists = bool(repo and (repo / kpath).exists())
            wp["proposed_docs"]["knowledge"].append({"path": kpath, "status": "exists" if exists else "missing", "reason": "document the area before changing it"})

    plan_items = items
    waves = {w: [i["id"] for i in plan_items if i["wave"] == w] for w in WAVES}
    sev_counts = defaultdict(int)
    for f in findings:
        sev_counts[f.get("severity", "unknown")] += 1
    return {
        "contract": CONTRACT,
        "generated_by": "build_plan.py (first cut, to be refined by remediation-planning-wasp-drone)",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "refined": False,
        "inputs": {
            "workspace": str(workspace),
            "findings_files": files,
            "finding_count": len(findings),
            "by_severity": dict(sev_counts),
            "merged_duplicates": len(dup_of),
            "no_action_info_ids": info_ids,
            "clustering": {"depth": depth, "key": "path prefix + CWE (else id source segment)"},
        },
        "library": {"present": bool(repo and (repo / "library").is_dir()), "consent_state": "not-asked"},
        "waves": waves,
        "items": plan_items,
        "candidate_contracts": [
            {"between": s["between"], "shared_files": s["files"], "status": "candidate-needs-judgment"} for s in shared
        ],
        "uncovered_finding_ids": [],
    }


def roadmap_draft(plan: dict) -> str:
    lines = ["# Remediation roadmap (first-cut draft)", "", "Generated by build_plan.py. Replace with the refined roadmap.", ""]
    by_id = {i["id"]: i for i in plan["items"]}
    for w in WAVES:
        lines += [f"## {w.capitalize()}", "", "| Item | Findings | Max severity | Effort | Owner Drone | Depends on |", "| --- | --- | --- | --- | --- | --- |"]
        for iid in plan["waves"][w]:
            i = by_id[iid]
            lines.append(f"| {i['id']} {i['title']} | {', '.join(i['finding_ids'])} | {i['max_severity']} | {i['effort']} | {i['owner_drone']} | {', '.join(i['depends_on']) or 'none'} |")
        if not plan["waves"][w]:
            lines.append("| (none) | | | | | |")
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("workspace")
    ap.add_argument("--repo", help="audited repository path (read only; used to number PRDs and detect existing knowledge docs)")
    ap.add_argument("--depth", type=int, default=2, help="path segments that define a code area (default 2)")
    ap.add_argument("--out", help="plan.json path (default WORKSPACE/04-remediation/plan.json)")
    ap.add_argument("--roadmap-draft", help="also write a draft roadmap table to this path")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    ws = Path(a.workspace)
    if not ws.is_dir():
        print(f"workspace not found: {ws}", file=sys.stderr)
        return 2
    if a.repo:
        repo_r = Path(a.repo).resolve()
        for o in (a.out, a.roadmap_draft):
            if o:
                op = Path(o).resolve()
                if repo_r == op or repo_r in op.parents:
                    print(f"refusing to write output inside the audited repository: {op}", file=sys.stderr)
                    return 2
        default_out = (ws / "04-remediation" / "plan.json").resolve()
        if repo_r in default_out.parents:
            print(f"refusing to write output inside the audited repository: {default_out}", file=sys.stderr)
            return 2
    plan = build(ws, Path(a.repo) if a.repo else None, max(1, a.depth))
    if plan is None:
        print("no findings.jsonl found under 00-foundation, 01-bloat, 02-security, 03-quality", file=sys.stderr)
        return 1
    covered = {i for it in plan["items"] for i in it["finding_ids"]} | {i for it in plan["items"] for i in it["merged_duplicate_ids"]}
    all_ids = set()
    for rel in plan["inputs"]["findings_files"]:
        for line in (ws / rel).read_text(encoding="utf-8").splitlines():
            if line.strip():
                all_ids.add(json.loads(line)["id"])
    plan["uncovered_finding_ids"] = sorted(all_ids - covered - set(plan["inputs"]["no_action_info_ids"]))
    out = Path(a.out) if a.out else ws / "04-remediation" / "plan.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    if a.roadmap_draft:
        Path(a.roadmap_draft).write_text(roadmap_draft(plan), encoding="utf-8")
    if not a.quiet:
        print(f"wrote {out}: {len(plan['items'])} work packages from {plan['inputs']['finding_count']} findings; "
              f"now={len(plan['waves']['now'])} next={len(plan['waves']['next'])} later={len(plan['waves']['later'])}; "
              f"uncovered={len(plan['uncovered_finding_ids'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

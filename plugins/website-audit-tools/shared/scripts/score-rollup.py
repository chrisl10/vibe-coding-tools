#!/usr/bin/env python3
"""score-rollup.py - independent N/A-aware rollup of validated leaf findings.

Used by: audit-scoring-stinger (see shared/scripts/README.md).

WHAT THIS SCRIPT IS. A standard-library cross-check of the scorecard
arithmetic documented in audit-scoring-stinger guides 01 and 02. It reads
leaf findings (the leaf-finding.schema.json shape), rejects malformed ones
back to their originating Drone instead of scoring them (guide 05), and
computes:

  sub_audit_pct = sum(score * w for scored leaves) / (6 * sum(w for scored leaves))
  category_pct  = sum(sub_pct * sub_w) / sum(sub_w)      over scored sub-audits
  final_raw_pct = sum(cat_pct * cat_w) / sum(cat_w)      over scored categories

A leaf scored 0 is N/A and is excluded from both sides of the division. A
sub-audit or category with nothing scored is N/A and is excluded from its
parent's numerator and denominator. Any security leaf scored exactly 1
caps the effective score at the override cap (guide 02), and the letter
grade is the highest grade threshold at or below the effective score.

It does not write the XLSX scorecard. The Drone still transcribes leaves
into a copy of the template (audit-scoring-stinger procedure step 4); this
script gives the independent numbers to compare the recalculated workbook
against (procedure step 6). The workbook's sub-audit, category and final
formulas apply the same N/A rule, so the two must agree exactly; N/A
sub-audits and categories are listed under `na_subaudits` / `na_categories`
and show as "N/A" in the workbook's rollup cells.

DEFAULT RUBRIC. Weights, grade thresholds and the override cap are read
from audit-scoring-stinger's generate-scorecard-xlsx.py (the source of the
template) by parsing its literal data, so this script never carries a
second copy that can drift. Pass `--rubric <file.json>` to use an
engagement's retuned values instead:

  {"categories": [{"key": "security", "weight": 20,
                   "subaudits": [{"key": "headers", "weight": 2.8571}, ...]}, ...],
   "grade_thresholds": [[0.0, "F"], [0.6, "D"], ...],
   "security_override_enabled": true,
   "security_override_cap": 0.7699}

USAGE.
  python3 score-rollup.py --findings <file-or-dir> [--rubric rubric.json] [--out result.json]

`--findings` accepts a JSON file holding one finding or a list of findings,
a JSONL file, or a directory searched recursively for *.json and *.jsonl.
Exit status: 0 on success (rejections are reported, not fatal), 2 on unusable
input or rubric.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

GENERATOR = (
    Path(__file__).resolve().parent.parent.parent
    / "skills" / "audit-scoring-stinger" / "references" / "scripts" / "generate-scorecard-xlsx.py"
)
REQUIRED = (
    "leaf_id", "category_key", "subaudit_key", "description",
    "score", "evidence_pointer", "justification", "originating_bee",
)
PLACEHOLDERS = {"", "tbd", "todo", "n/a", "na", "none", "-"}


class RubricError(ValueError):
    pass


def _literal_assignments(source: str, names: set[str]) -> dict:
    """Evaluate the literal data assigned to `names` without importing the module.

    The generator imports openpyxl at module level; parsing keeps this script
    standard-library only. Only literals and dict(...) calls are accepted.
    """
    found = {}
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in names:
            found[target.id] = _eval_literal(node.value)
    return found


def _eval_literal(node):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict" and not node.args:
        return {kw.arg: _eval_literal(kw.value) for kw in node.keywords}
    if isinstance(node, (ast.List, ast.Tuple)):
        values = [_eval_literal(item) for item in node.elts]
        return values if isinstance(node, ast.List) else tuple(values)
    return ast.literal_eval(node)


def default_rubric(generator: Path = GENERATOR) -> dict:
    if not generator.is_file():
        raise RubricError(f"default rubric source not found: {generator}; pass --rubric")
    data = _literal_assignments(
        generator.read_text(encoding="utf-8"),
        {"CATEGORIES", "GRADE_THRESHOLDS", "SECURITY_OVERRIDE_CAP"},
    )
    missing = {"CATEGORIES", "GRADE_THRESHOLDS", "SECURITY_OVERRIDE_CAP"} - data.keys()
    if missing:
        raise RubricError(f"{generator.name} no longer defines {sorted(missing)}; pass --rubric")
    categories = []
    for cat in data["CATEGORIES"]:
        subs = cat["subaudits"]
        # Same equal-split rule the generator applies when a sub-audit weight is None.
        categories.append({
            "key": cat["key"],
            "weight": cat["weight"],
            "subaudits": [
                {"key": k, "weight": w if w is not None else round(cat["weight"] / len(subs), 4)}
                for (k, _name, w) in subs
            ],
        })
    return {
        "categories": categories,
        "grade_thresholds": [list(t) for t in data["GRADE_THRESHOLDS"]],
        "security_override_enabled": True,
        "security_override_cap": data["SECURITY_OVERRIDE_CAP"],
    }


def check_rubric(rubric: dict) -> dict:
    try:
        cats = rubric["categories"]
        grades = sorted((float(p), str(g)) for p, g in rubric["grade_thresholds"])
        cap = float(rubric.get("security_override_cap", 0.7699))
        enabled = bool(rubric.get("security_override_enabled", True))
        index = {}
        for cat in cats:
            subs = {s["key"]: float(s["weight"]) for s in cat["subaudits"]}
            index[cat["key"]] = {"weight": float(cat["weight"]), "subaudits": subs}
    except (KeyError, TypeError, ValueError) as exc:
        raise RubricError(f"malformed rubric: {exc}") from exc
    if not index or not grades:
        raise RubricError("rubric needs at least one category and one grade threshold")
    return {"categories": index, "order": [c["key"] for c in cats], "grades": grades,
            "cap": cap, "enabled": enabled}


def load_findings(path: Path) -> list:
    files = sorted(p for p in path.rglob("*") if p.suffix in {".json", ".jsonl"}) if path.is_dir() else [path]
    findings = []
    for file in files:
        text = file.read_text(encoding="utf-8")
        if file.suffix == ".jsonl":
            rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        else:
            data = json.loads(text)
            rows = data if isinstance(data, list) else [data]
        for row in rows:
            findings.append((str(file), row))
    return findings


def _blank(value) -> bool:
    return not isinstance(value, str) or value.strip().lower() in PLACEHOLDERS


def reject_reason(finding, rubric: dict):
    if not isinstance(finding, dict):
        return "finding is not a JSON object"
    missing = [f for f in REQUIRED if f not in finding]
    if missing:
        return f"missing required field(s): {', '.join(missing)}"
    score = finding["score"]
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 6:
        return "score must be an integer from 0 to 6"
    if finding.get("is_boolean_checkpoint") and score not in (0, 1, 6):
        return "boolean checkpoint scored between 1 and 6"
    cat = rubric["categories"].get(finding["category_key"])
    if cat is None:
        return f"unknown category_key {finding['category_key']!r}"
    if finding["subaudit_key"] not in cat["subaudits"]:
        return f"unknown subaudit_key {finding['subaudit_key']!r} for {finding['category_key']}"
    # An N/A leaf needs only a short reason; a graded leaf needs real evidence and justification.
    if score > 0 and (_blank(finding["evidence_pointer"]) or _blank(finding["justification"])):
        return "graded leaf without a usable evidence_pointer and justification"
    if score == 0 and _blank(finding["evidence_pointer"]) and _blank(finding["justification"]):
        return "N/A leaf without any reason it does not apply"
    return None


def _weighted(pairs):
    """pairs: (pct, weight); None pct is N/A and excluded from both sides."""
    scored = [(p, w) for p, w in pairs if p is not None]
    total = sum(w for _, w in scored)
    if total == 0:
        return None
    return sum(p * w for p, w in scored) / total


def grade_for(pct: float, grades) -> str:
    letter = grades[0][1]
    for threshold, name in grades:
        if pct >= threshold:
            letter = name
    return letter


def rollup(findings, rubric: dict) -> dict:
    accepted, rejected, seen = [], [], set()
    for source, finding in findings:
        reason = reject_reason(finding, rubric)
        if reason is None and finding["leaf_id"] in seen:
            reason = "duplicate leaf_id"
        if reason:
            rejected.append({
                "source": source,
                "leaf_id": finding.get("leaf_id") if isinstance(finding, dict) else None,
                "originating_bee": finding.get("originating_bee") if isinstance(finding, dict) else None,
                "reason": reason,
            })
            continue
        seen.add(finding["leaf_id"])
        accepted.append(finding)

    leaves = {}
    for f in accepted:
        leaves.setdefault((f["category_key"], f["subaudit_key"]), []).append(f)

    categories, na_subaudits, na_categories = {}, [], []
    for cat_key in rubric["order"]:
        cat = rubric["categories"][cat_key]
        subs = {}
        for sub_key, sub_weight in cat["subaudits"].items():
            rows = leaves.get((cat_key, sub_key), [])
            # Leaf weight is 1 in the template (column H); the mask excludes score 0 on both sides.
            scored = [r["score"] for r in rows if r["score"] > 0]
            pct = sum(scored) / (6 * len(scored)) if scored else None
            if pct is None:
                na_subaudits.append(f"{cat_key}.{sub_key}")
            subs[sub_key] = {"pct": pct, "weight": sub_weight, "leaves": len(rows), "scored": len(scored)}
        cat_pct = _weighted((s["pct"], s["weight"]) for s in subs.values())
        if cat_pct is None:
            na_categories.append(cat_key)
        categories[cat_key] = {"pct": cat_pct, "weight": cat["weight"], "subaudits": subs}

    final_raw = _weighted((c["pct"], c["weight"]) for c in categories.values())
    triggers = sorted(f["leaf_id"] for f in accepted if f["category_key"] == "security" and f["score"] == 1)
    override = bool(rubric["enabled"] and triggers)
    effective = None
    if final_raw is not None:
        effective = min(final_raw, rubric["cap"]) if override else final_raw
    return {
        "final_raw_pct": final_raw,
        "override_active": override,
        "override_triggers": triggers,
        "effective_pct": effective,
        "letter_grade": grade_for(effective, rubric["grades"]) if effective is not None else "N/A",
        "categories": categories,
        "na_subaudits": na_subaudits,
        "na_categories": na_categories,
        "accepted": len(accepted),
        "rejected": rejected,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--findings", required=True, type=Path)
    parser.add_argument("--rubric", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        raw = json.loads(args.rubric.read_text(encoding="utf-8")) if args.rubric else default_rubric()
        rubric = check_rubric(raw)
        if not args.findings.exists():
            raise FileNotFoundError(f"findings path not found: {args.findings}")
        result = rollup(load_findings(args.findings), rubric)
    except (RubricError, OSError, json.JSONDecodeError) as exc:
        print(f"score-rollup: {exc}", file=sys.stderr)
        return 2
    text = json.dumps(result, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

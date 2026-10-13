#!/usr/bin/env python3
"""Validate ledger structure and archive integrity. Never infer provider readiness."""
from pathlib import Path
import argparse, csv, datetime, decimal, hashlib, json, re
BASE = Path(__file__).resolve().parents[1]
FIELDS = "asset_id category purpose product_scope environment accountable_owner access_boundary provider selected_reason requirement_source source_date observed_at evidence_ref evidence_kind reviewed_by status blocking prerequisite_ids lead_time_days lead_time_basis cost_amount cost_currency cost_unit cost_source cost_date next_owner_action".split()
STATUSES = {"unknown", "reported", "blocked", "observed-ready", "deferred", "not-applicable"}
def validate(rows):
    errors = []
    ids = [r.get("asset_id", "") for r in rows]
    if len(set(ids)) != len(ids): errors.append("duplicate asset_id")
    for r in rows:
        label = r.get("asset_id", "unnamed")
        missing = [k for k in FIELDS if k not in r]
        if missing: errors.append(f"{label}: missing fields: {', '.join(missing)}"); continue
        for k in ["asset_id", "purpose", "product_scope", "environment", "accountable_owner", "access_boundary", "selected_reason", "requirement_source", "observed_at", "next_owner_action"]:
            if not r[k].strip(): errors.append(f"{label}: empty {k}")
        if r["status"] not in STATUSES: errors.append(f"{label}: invalid status")
        if r["blocking"] not in {"yes", "no"}: errors.append(f"{label}: blocking must be yes/no")
        if r["status"] == "observed-ready":
            if r["evidence_kind"] != "authorized-observation" or not r["evidence_ref"] or not r["reviewed_by"]: errors.append(f"{label}: observed-ready needs authorized observation, reference and reviewer")
        if r["status"] == "reported" and (r["evidence_kind"] != "owner-report" or not r["evidence_ref"]): errors.append(f"{label}: reported needs owner-report reference")
        if r["cost_amount"] != "unknown":
            try:
                amount = decimal.Decimal(r["cost_amount"])
                if not amount.is_finite() or amount < 0: raise decimal.InvalidOperation
            except decimal.InvalidOperation: errors.append(f"{label}: invalid cost amount")
            if not all(r[k] and r[k] != "unknown" for k in ["cost_currency", "cost_unit", "cost_source", "cost_date"]): errors.append(f"{label}: priced amount needs currency, unit, source and date")
        if r["lead_time_days"] != "unknown":
            try:
                days = decimal.Decimal(r["lead_time_days"])
                if not days.is_finite() or days < 0: raise decimal.InvalidOperation
            except decimal.InvalidOperation: errors.append(f"{label}: invalid lead time")
            if r["lead_time_basis"] in {"", "unknown"}: errors.append(f"{label}: duration needs sourced/estimated basis")
        for k in ["source_date", "observed_at", "cost_date"]:
            if r[k] not in {"", "unknown"}:
                try: datetime.date.fromisoformat(r[k])
                except ValueError: errors.append(f"{label}: invalid {k}")
        for dep in filter(None, r["prerequisite_ids"].split(";")):
            if dep not in ids: errors.append(f"{label}: unknown prerequisite {dep}")
    graph = {r.get("asset_id"): list(filter(None, r.get("prerequisite_ids", "").split(";"))) for r in rows}
    def visit(node, active, done):
        if node in active: return True
        if node in done: return False
        active.add(node)
        if any(visit(dep, active, done) for dep in graph.get(node, [])): return True
        active.remove(node); done.add(node); return False
    if any(visit(n, set(), set()) for n in graph): errors.append("cyclic prerequisites")
    return errors

def self_check():
    for r in json.loads((BASE / "references/research/source-ledger.json").read_text()):
        if "path" in r:
            assert hashlib.sha256((BASE/r["path"]).read_bytes()).hexdigest() == r["archive_sha256"], r["id"]
    for p in BASE.rglob("*.md"):
        text = p.read_text(); assert "\u2014" not in text, str(p)
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" not in link and not link.startswith("#"):
                assert (p.parent/link.split("#")[0]).exists(), f"missing {link} in {p}"
    rows = list(csv.DictReader((BASE/"references/examples/fictional-ledger.csv").open()))
    assert not validate(rows), validate(rows)
    malformed = [dict(rows[4])]; malformed[0]["cost_unit"] = ""
    assert any("priced amount" in e for e in validate(malformed))
    invented = [dict(rows[0])]; invented[0]["status"] = "observed-ready"
    assert any("authorized observation" in e for e in validate(invented))
    loop = [dict(rows[0]), dict(rows[1])]; loop[0]["prerequisite_ids"] = "W2"
    assert "cyclic prerequisites" in validate(loop)
    print("PASS: archived hashes/local links; 8 fictional rows; rejected missing price unit, invented readiness and dependency cycle. No real readiness certified.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("ledger", nargs="?", type=Path); args = parser.parse_args()
    if args.ledger:
        errors = validate(list(csv.DictReader(args.ledger.open())))
        for e in errors: print(e)
        if errors: raise SystemExit(1)
        print("PASS: ledger structure only; provider state and approval remain unverified.")
    else: self_check()

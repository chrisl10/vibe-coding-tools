# plan.json and roadmap.md formats

Derived from `audit-contract.md` (section 3 workspace, section 5 finding fields). Written by `scripts/build_plan.py`, then refined by the Drone. Nothing here is written to the audited repository.

## plan.json

```json
{
  "contract": "1.0",
  "refined": true,
  "generated_by": "remediation-planning-wasp-drone",
  "generated_at": "2026-09-30T14:00:00+00:00",
  "inputs": {"workspace": "...", "findings_files": ["02-security/findings.jsonl"], "finding_count": 41,
             "by_severity": {"critical": 1, "high": 5}, "merged_duplicates": 3, "no_action_info_ids": []},
  "library": {"present": true, "consent_state": "not-asked | approved | declined", "approved_files": []},
  "waves": {"now": ["WP-001"], "next": ["WP-002"], "later": ["WP-003"]},
  "items": [{
    "id": "WP-001",
    "title": "Missing authorization on server actions (apps/web)",
    "root_cause": "Server actions do not call the shared auth guard",
    "area": "apps/web",
    "finding_ids": ["SEC-NEXT-001", "SEC-NEXT-004"],
    "merged_duplicate_ids": ["SEC-GEN-009"],
    "max_severity": "critical",
    "impact": "Any signed-in user can edit another user's records",
    "effort": "M",
    "effort_hours": 6.0,
    "risk": "low | medium | high: what could break while fixing",
    "wave": "now",
    "owner_drone": "nextjs-security-wasp-drone",
    "depends_on": [],
    "verification": {"dimension": "security", "how": "re-run nextjs-security-wasp-drone; SEC-NEXT-001 and SEC-NEXT-004 no longer reported"},
    "proposed_docs": {
      "prd": {"number": "004", "numbering": "from-library", "path": "library/requirements/backlog/prd-004-server-action-auth/prd-004-server-action-auth-index.md", "acceptance_from_findings": ["SEC-NEXT-001"]},
      "ird": [{"issue_number": 212, "path": "library/issues/backlog/ird-212-.../ird-212-...-index.md"}],
      "knowledge": [{"path": "library/knowledge/private/auth/server-actions.md", "status": "missing"}]
    }
  }],
  "candidate_contracts": [{"between": ["WP-001", "WP-004"], "shared_files": ["apps/web/lib/auth.ts"], "status": "candidate-needs-judgment"}],
  "uncovered_finding_ids": []
}
```

Rules:

- Work-package `effort` has five buckets, derived from the summed `effort_hours`: `XS` (under 1 hour), `S` (1 to 3 hours), `M` (3 to 8 hours), `L` (8 to 24 hours), `XL` (more than 24 hours). `XS` and `XL` exist only on work packages. Findings keep the contract enum `S`, `M`, `L`; the brief renderer has words for all five.
- Two findings merge into one package only when they share a path, overlapping lines, and a CWE, and never when their CVE or GHSA ids differ. `CWE-1395` and `CWE-1104` are not merge keys. A shared manifest or lockfile (`package.json`, lockfiles) does not create a dependency between packages, and foundation findings are routed to an owner by dimension before path.
- `uncovered_finding_ids` must be empty in the final plan. Every non-info finding appears in exactly one item (directly or as a merged duplicate). `info` findings are listed under `no_action_info_ids`.
- `numbering` is `provisional` when no `library/` was available to read; the numbers are then placeholders and must be renumbered at write time.
- `ird` entries exist only when a real issue number exists. Never invent one.
- `consent_state` changes only after the user answers the consent request (guide 00).

## roadmap.md

Sections in order: a three-line summary (how many findings, packages, and the one action to take first), then Now, Next, Later. Each wave is a table:

| Item | Findings | Impact | Effort | Risk | Owner Drone | Depends on |
| --- | --- | --- | --- | --- | --- | --- |

Below each table, one short paragraph per Now item in plain language: what is wrong, what changes, how we will know it is fixed. Later items get one line each. End with "What we did not plan" (info findings, deferred prudent debt, and anything excluded on purpose) and the approval request for `library/` files.

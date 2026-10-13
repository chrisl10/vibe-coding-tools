# 07: Quality check and hand-off

Run this before declaring the research done.

## Checklist

| Check | How |
|---|---|
| Ledger valid and privacy-clean | `icp_ledger.py validate` on `ledger.jsonl` returns ok |
| No personal data in prose | Search the dossier, notes, and seed brief for `@`, phone-like numbers, personal profile links, and people's names; remove any |
| Every finding traced | Each primary-ICP row and summary sentence matches a strong or moderate claim in `evidence.md` |
| Grades honored | No weak or contested claim presented as a finding |
| Positioning gap present | Stated-only claims compared with revealed segments |
| Coverage honest | Missing or limited lanes listed with reasons |
| Spend reported | Pages, calls, and credits or dollars versus the brief's cap |
| Tool facts current | Tool names used match the session's list; retired names absent |
| Output shape | `icp.json` matches `templates/icp.schema.json` (validate with any JSON Schema validator available; otherwise check required fields by hand and say so) |

## Hand-off

Summarize for the requester in five lines: primary ICP, confidence and why, the positioning gap, the top trigger, and the next step. Then route follow-up work (see [references/REFERENCE.md](../references/REFERENCE.md) section 6): outreach, CRM scoring, discovery interviews to validate the ICP with real buyers, or channel choice.

Research outputs are documents, not code; if the requester wants them committed to a repository, that repository's own review and commit rules apply.

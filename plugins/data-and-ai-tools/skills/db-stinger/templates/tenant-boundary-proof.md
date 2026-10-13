# Tenant boundary proof packet

Status: SOURCE REVIEW ONLY / native rehearsal / accepted by Security and Quality. Name the current status; do not prefill accepted.

- Exact app/server/ORM/client/provider/pooler revisions:
- Tenant identity source and membership authority:
- App role/effective role/memberships, table owner, superuser/BYPASSRLS:
- Tables, enable/FORCE flags, grants, USING/WITH CHECK and combined policy:
- View/function/trigger/privileged paths and Security owner:
- Application predicates and generated SQL evidence:
- Tenant-scoped foreign keys and tenant-changing writes:
- Transaction context, absent/invalid handling and pool-reuse evidence:
- Jobs, imports, bulk actions, exports, reporting and retry/revocation semantics:
- Cache/CDN/object keys, search/vector filters and invalidation:
- Native environment/execution authorization, synthetic fixture IDs and revision:

| Path and principal | Own-tenant positive control | Cross-tenant negative expectation | Actual result and independent side-effect check | Evidence locator | Gap/owner |
|---|---|---|---|---|---|
| Read, relation, count | | | | | |
| Insert/update/delete and tenant reassignment | | | | | |
| Role/owner/bypass and view/function | | | | | |
| Commit/rollback/pool reuse | | | | | |
| Job/retry/revoked membership | | | | | |
| Export/cache/search/object retrieval | | | | | |

Record native failures without exposing real tenant content or credentials. Security review precedes Quality. Source checklists and simulated cases do not close missing native proof.

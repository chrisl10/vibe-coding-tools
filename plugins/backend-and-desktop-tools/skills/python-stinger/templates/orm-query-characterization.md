# ORM query characterization record

- Outcome and user-visible operation:
- Before source revision / after source revision:
- Django version / Python version / DB engine-version / DB alias:
- Selector and consumer paths with lines:
- Established principal, tenant and child-visibility policies:
- Data fixture: 0 / 1 / many parent cases; child fanout; denied principal; other tenant; null relation; filtered and deferred fields:
- Serialization fields / shape / ordering / missing-value behavior:
- Pagination size, total-count behavior, fanout limit, iterator chunk size:
- Capture boundary, cold/cache state, fixture setup excluded:

| Case | Observed before queries | Observed after queries | Response parity | Visibility parity | Time / peak memory | Evidence path |
|---|---|---|---|---|---|---|
| Empty | Pending | Pending | Pending | Pending | Pending | |
| One | Pending | Pending | Pending | Pending | Pending | |
| Many | Pending | Pending | Pending | Pending | Pending | |
| Unauthorized / other tenant | Pending | Pending | Pending | Pending | Pending | |
| Filtered / deferred / nested | Pending | Pending | Pending | Pending | Pending | |

- Hypothesis (separate from measured result):
- Accepted budget and rationale from observations:
- Unexpected extra query and exact consuming line:
- Backend-specific query-plan / memory limitations:
- Security result then Quality result:
- Rollback patch / owner:
- Qualification: source-reviewed / DB-measured / complete-request-tested / pending:

Record query shapes and aggregate counts; exclude sensitive SQL literals, credentials and customer data.

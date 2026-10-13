# Workload intake worksheet

Goal and milestone: [product, users, platform, launch date if supplied]
Decision needed: [one infrastructure choice]
Known constraints: [user provider preferences, budget/currency, operator experience, existing services]

| Dimension | Low/base/high or required value | Evidence/assumption | Missing decision |
|---|---|---|---|
| Traffic | requests/day, peak concurrency, burst duration | measured or estimate; units | unknown |
| Request execution | language/runtime, wall time, CPU, memory, native libraries | measurement or code requirement | unknown |
| Workers/jobs | continuous versus scheduled/completion; max duration; queue/retries | source requirement | unknown |
| Data | DB type, size/growth, connection count, writes, tenancy | estimate or accepted design | unknown |
| Storage | object size/count, retention, backups, uploads | estimate with units | unknown |
| Transfer | egress by destination, downloads/uploads, cross-region traffic | GB/month; source | unknown |
| Geography | users, app/data region, latency requirement | actual constraint | unknown |
| Availability | acceptable outage, data loss and recovery time | owner decision | unknown |
| Security/access | identity, tenant boundary, secrets, private access, compliance | accepted contract/requirement | unknown |
| Team | hours/week for operations, skills, on-call/support owner | owner report | unknown |
| Budget | cash ceiling and separately valued operator time | date/currency | unknown |
| Exit | export format, acceptable migration downtime, provider dependencies | owner preference | unknown |

Do not silently fill unknowns with the defaults of a favored provider. Ask the few missing questions that change eligibility before research and price comparison. Estimates are labeled and remain provisional.

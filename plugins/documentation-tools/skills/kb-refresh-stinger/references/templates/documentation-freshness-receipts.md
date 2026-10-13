# Documentation freshness receipt worksheet

Run: <identifier> | Observed UTC: <date-time> | Writer/verifier: <actual identity>
Write fence: <approved paths> | Frozen read-only set: <paths>
Documented revision: <exact commit or explicitly content-addressed dirty snapshot>
Current comparison revision: <exact pin> | Branch movement since pin: <observed delta or unknown>
Time/verification budget: <approved bound> | Claims inventoried: <count or unknown>
Reviewed: <count> | Unchecked: <count> | Missing/unavailable documents: <named rows>
Structural checks: <command, result, output path> | Runtime/native checks: <receipt or unverified>

| ID / document:line / exact claim | Type: source, runtime, proposal | Evidence revision / path:lines / byte digest | UTC re-open / verifier | Support assessment / status | keep, update, write / exact change | consumers checked / unchecked | resume read or owner question |
|---|---|---|---|---|---|---|---|
| <claim> | <type> | <revision and context; missing if unavailable> | <observation> | <supported, contradicted, moved, missing, wrong-proof-type, wrong-status, unresolved-contradiction, historical-only, unchecked> | <bounded action> | <scope and result> | <specific action> |

For runtime receipts record environment, deployed revision, host/version, actual result and scope. Keep secret values and customer data out. For contradictions retain both sources and revisions, without silently resolving an Accepted decision. A digest or a passing parser does not prove a claim. An unchecked row stays unresolved. Only claim full coverage if every inventoried claim was actually reviewed.

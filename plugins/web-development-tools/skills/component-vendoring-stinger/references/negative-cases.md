# Constructed negative cases

These are expected runtime decisions, not observed application executions.

| Case | Required decision |
|---|---|
| Existing primitive fits task | Recommend reuse; do not create a fork for novelty. |
| README says MIT, actual NOTICE names Apache source | Reject blanket MIT-only characterization; preserve evidence and route subset review. |
| Upstream LICENSE missing | Stop dependent copy; ask for exact artifact/rights review. |
| Required notice removed or changed | Reject provenance check; restore reviewed notices only within authorized scope. |
| Candidate hash differs from original with no recorded modification | Flag drift, establish patch history; never silently bless it. |
| Component needs undeclared imports | Hold copy until closure/dependency evidence exists. |
| Third-party asset has separate license | Review separately; code MIT does not clear asset rights. |
| Source file adapted to remove keyboard/focus behavior | Hold runtime acceptance pending target tests and design/accessibility review. |
| CLI overwrite would replace owned CSS | Require exact authorized mutation list; do not run it from selection authority. |
| Primitive version changed but copied wrapper did not | Compare separate update paths and target contracts. |
| Native host requested from web source | Route native owner; no native parity claim. |
| Counsel/maintainer/token owner unavailable | Return named gap and blocked dependent step, no substituted authority. |

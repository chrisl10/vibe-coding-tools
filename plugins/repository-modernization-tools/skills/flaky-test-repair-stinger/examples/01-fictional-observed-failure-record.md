# Fictional observed failure repair record

CONSTRUCTED_DECISION, NOT_RUN. No repository/test/CI runner was supplied or executed. All observations below are invented teaching inputs, not captured runtime proof.

Fictional product Ledger Preview expects selecting invoice I1 to show exactly its amount and to show an error for missing invoices. Fictional report F1 describes test B failing after test A with `expected I1, received I2`; B passes alone. The fictional candidate is revision EXAMPLE_BASE, not a real SHA. A shared test fixture retains selectedInvoice after A. This is a hypothesis supported by the teaching setup, not an actual diagnosed user issue.

Budget: two unchanged invocations maximum and three hypothesis approaches maximum, ten minutes total; larger repeat budgets require owner approval. Fixture data A/B are isolated invented records. No production/customer/provider access.

| Planned trial | Discriminating condition | Expected result | Actual |
|---|---|---|---|
| Capture original A -> B order | same assertions/data, shared fixture | F1 signature | NOT_RUN |
| Fresh fixture for B | only fixture ownership changes | exact I1 oracle holds | NOT_RUN |
| Candidate per-test fixture plus cleanup | original A -> B order | both exact values asserted | NOT_RUN |
| Missing-invoice negative case | same error oracle | exact accepted error retained | NOT_RUN |

Proposed causal repair: allocate selectedInvoice in each test-owned fixture and restore/remove its exact owned state on success/setup failure/teardown. Keep exact equality, missing-invoice assertion, supported test collection and accepted deadline unchanged. Do not add retry, serial mode, skip/xfail, larger timeout or snapshot update. If the shared state is production state rather than fixture leakage, hand the actual product fix to its language owner.

Closure remains OPEN: the teaching record has no actual failure trace, finite trial receipts or final source identity. A real consumer must fill [the worksheet](../templates/failure-repair-evidence.md), capture original failure and final-candidate evidence, preserve assertion semantics and obtain independent Security/Quality gates. [Negative cases](02-negative-decisions.md) are also NOT_RUN.

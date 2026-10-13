# Flaky repair negative decisions

CONSTRUCTED_DECISION, NOT_RUN throughout. Expected handling for future authorized consumer checks.

| Case | Required decision |
|---|---|
| One failure, no differing result evidence | observed failure/hypothesis only; no confirmed flake |
| No consumer repo or failure receipt | guidance only, behavioral rows NOT_RUN |
| First failure then retry pass | preserve FAIL/FLAKY; not repaired |
| Retry trace differs from failing worker | label attempt/environment difference |
| Two same failed invocations | stop that approach unless explicit larger budget |
| Three failed approaches/budget exhausted | preserve ledger, ask owner |
| Seed/order/worker count omitted | reproduction inconclusive |
| Cached Go pass or zero tests collected | not execution proof |
| Browser context isolated but DB shared | investigate backend resource ownership |
| Yield fixture fails before yield | verify setup-failure cleanup |
| Shared env mutation under parallel test | use supported scoped isolation or domain owner |
| Thread/goroutine signalled but not joined | completion gap remains OPEN |
| Clock install after time-dependent work | incorrect control, re-scope experiment |
| New random-order plugin/browser missing | report tool gap; no install |
| Real service outage/product race | handoff actual owner; do not mock away required integration |
| Long sleep/force click/broad locator masks failure | reject causal repair |
| Timeout/tolerance/snapshot assertion weakened | reject absent separate accepted requirement change |
| Skip/xfail/quarantine/deletion to obtain green | reject repair claim |
| Candidate changes during proof/old shard result | STALE, re-pin affected evidence |
| Private trace/production cleanup/paid replay | no effect without exact authority |
| Source tests pass, native/CI not run | retain explicit evidence limits |
| Finite repetitions claimed statistical certainty | report exact scope/counts and residual uncertainty |

# Failure, hypothesis and repair ownership

DERIVED reference grounded in [the digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/repository-modernization-tools/skills/flaky-test-repair-stinger/references/research/digest.md).

| State | Required evidence | Permitted next step |
|---|---|---|
| REPORTED | cited user/log report, candidate/environment unknowns | capture and classify, no cause claim |
| OBSERVED_FAIL | actual executed failing assertion/trace on pinned inputs | formulate bounded causal hypothesis |
| VARIABLE_RESULT | same accepted test has observed differing outcomes, trials/conditions recorded | controlled discriminating experiment |
| CONFIRMED_CAUSE | evidence links specific condition to failure with alternatives/limits stated | narrow repair or exact owner handoff |
| CANDIDATE_REPAIR | causal change and assertion/coverage inventory | repeat relevant original conditions within budget |
| VERIFIED_SCOPE | real receipts on final candidate with original assertion behavior retained | independent Security/Quality gates |
| BLOCKED/INCONCLUSIVE | no repro, budget/tooling/authority gap, stale inputs | preserve evidence and ask owner |

Do not equate flaky with harmless. The failing assertion may expose a production race, incorrect timeout, bad isolation or real service fault. Product fixes remain with the language/framework owner; this specialist owns failure triage, exact test/fixture repair scope and evidence. Browser Automation owns its browser mechanics, CI owner owns workflow changes, Quality independently audits after Security.

For each hypothesis: observation/coordinates, candidate cause, one controlled variable, why it discriminates, exact command/seed/order/worker count, fixture reset, environment pin, trial/time/resource cap, expected failure signature, terminal result and accepted next action. Two identical failed attempts exhaust that approach unless the user explicitly approves a larger diagnostic budget. Three failed approaches stop for the owner. Never loop until green.

Preserve PASS/FAIL/FLAKY/NOT_RUN/SKIPPED/XFAIL/XPASS/CANCELLED/INCOMPLETE/STALE separately. A wrapper exit or job submission is not assertion evidence. Finite green trials establish only the observed scope, never zero flake probability or universal stability.

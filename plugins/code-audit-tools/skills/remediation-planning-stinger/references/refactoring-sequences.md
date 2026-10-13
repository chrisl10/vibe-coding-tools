# Refactoring sequences for work packages

Sources: `research/raw/refactor--*.md`, `research/raw/test--*.md`.

## When to use which

| Situation | Sequence | Source |
| --- | --- | --- |
| Many copies of near-identical code (an adapter family, copy-pasted handlers) | 1. characterization tests; 2. introduce one shared base or abstraction; 3. migrate copies one at a time; 4. delete the copies | branch by abstraction, [raw/refactor--fowler-branch-by-abstraction.md] |
| Changing a shared function signature, API shape, event, or table column | expand (support both), migrate callers, contract (remove old) as three items; contract is a later item | [raw/refactor--fowler-parallel-change.md] |
| A function or closure with a long list of captured variables | 1. characterization tests; 2. Replace Function with Command (locals become fields, the "context object"); 3. split the body into methods; 4. remove the object if it is no longer useful | [raw/refactor--catalog-replace-function-with-command.md] |
| Parameters that always travel together | Introduce Parameter Object | [raw/refactor--catalog-introduce-parameter-object.md] |
| Replacing a whole module or service | strangler fig: route a thin slice to the new code, widen the slice, retire the old | [raw/refactor--fowler-strangler-fig.md] |
| No tests where the change lands | characterization tests first, always | [raw/test--characterization-tests.md] |

## Rules

1. The first item of any structural package is the safety net: tests that fail if behavior changes. Acceptance criteria say what behavior is pinned, never a coverage percentage. [raw/test--fowler-test-coverage.md]
2. Each step leaves the build and tests green so the work can stop after any step.
3. Never schedule the contract (removal) step in the same wave as the expand step.
4. A fix that is a security fix and a refactor at once is split: close the exposure first with the smallest change, restructure later.
5. Speculative abstractions that no finding asks for are out of scope. [raw/debt--fowler-yagni.md]

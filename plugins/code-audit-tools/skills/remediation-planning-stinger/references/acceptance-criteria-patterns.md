# Acceptance criteria patterns for remediation PRDs and IRDs

Sources: [research/raw/criteria--cucumber-better-gherkin.md], [research/raw/test--fowler-test-coverage.md], Library templates (`library-stinger/templates/prd-template.md`, `ird-template.md`).

Format: the Library template uses a table with `AC-n` and `Given ... when ... then ...`. Keep one behavior per row, declarative, observable, binary. Every row names the finding id it closes.

| Finding kind | Criterion pattern |
| --- | --- |
| Missing authorization (CWE-862) | AC: Given a signed-in user who does not own record X, when they call the action `updateX`, then the response is 403 and the record is unchanged. Closes SEC-NEXT-001. Check: test `updateX rejects non-owner`. |
| Injection (CWE-89, CWE-78, CWE-94) | AC: Given input containing a quote or shell metacharacter, when it reaches `<function>`, then it is passed as a bound parameter or an argument array and the output matches the fixture. Check: test with the hostile input. |
| XSS (CWE-79) | AC: Given stored text containing a script tag, when the page renders it, then the tag appears as text and no script runs. Check: component test. |
| Exposed secret | AC: Given the repository history and the client bundle, when scanned with the same tool the audit used, then no match remains, and the old key is revoked (state who confirmed). |
| Dependency with a CVE | AC: Given the lockfile, when the dependency audit runs, then the advisory id is not reported; the upgrade is the smallest version that fixes it. |
| Duplication | AC: Given the N copies listed in the finding, when the duplication tool runs with the same settings, then the reported percentage for the path is at or below the stated target, and each former copy now calls the shared implementation. Behavior tests that passed before still pass. |
| Dead code or unused dependency | AC: Given the unused-code tool, when run, then the listed exports and packages are gone and the build and tests pass. |
| Oversized function or file | AC: Given the function `f`, when measured with the audit's complexity or length measure, then it is under the target, and characterization tests recorded before the change still pass. |
| Missing tests | AC: Given the behavior list in the finding, when the suite runs, then a named test exists for each behavior and fails if that behavior is broken (show one deliberate break). Do not state a coverage percentage as the criterion. |
| Missing CI check or repo hygiene | AC: Given a pull request, when it opens, then the named check runs and blocks merge on failure; evidence is a workflow run link. |

Every PRD ends with the verification row:

`AC-last: Given the work package is merged, when the <dimension> audit Drone is re-run on the same scope, then finding ids <list> are not reported and no new finding of medium or higher appears in the touched paths.`

Rules: no vague words ("improve", "clean up", "robust"); no criterion that two reasonable people could grade differently; no implementation steps inside criteria (steps go in the PRD's body).

# Distilled research: turning audit findings into a remediation plan

Research window: 2026-03-30 to 2026-09-30. Fetched 2026-09-30. Every claim ends with its raw file. Timeless sources (Fowler, Feathers, Reinertsen, CWE) are labeled "timeless". Older vulnerability policy that has been replaced is labeled "superseded".

## 1. Prioritizing security findings

| Claim | Citation |
| --- | --- |
| KEV lists vulnerabilities exploited in the wild, and CISA says to use it as an input to a prioritization framework, not as the whole framework. | [raw/vuln--cisa-kev-catalog.md] |
| EPSS estimates the probability a published CVE is exploited in the next 30 days (0 to 1, daily). FIRST says to combine it with CVSS and KEV. | [raw/vuln--first-epss.md] |
| CVSS v4.0 has Base, Threat, Environmental and Supplemental groups. Bands: Low 0.1-3.9, Medium 4.0-6.9, High 7.0-8.9, Critical 9.0-10.0. The spec says to enrich Base scores with Threat and Environmental values before using them as a risk input. | [raw/vuln--first-cvss-v4-spec.md] |
| SSVC yields a decision (Track, Track*, Attend, Act) from exploitation, technical impact, automatable, mission prevalence and public well-being impact. | [raw/vuln--cisa-ssvc.md] |
| BOD 26-04 (2026) replaced BOD 22-01 (revoked 2026-06-10). It sorts work by exposure, automatability, total technical impact and active exploitation into 3-day, 14-day, 60-day and defer-to-next-upgrade classes. It binds US federal agencies only. | [raw/vuln--cisa-bod-26-04.md] [raw/vuln--cisa-bod-22-01-revoked.md] |
| The old "two weeks for KEV" rule is superseded. Do not cite it as current. | [raw/vuln--cisa-bod-22-01-revoked.md] |
| NIST SP 800-40r4 frames patching as preventive maintenance needing an enterprise strategy. Only the abstract was read. | [raw/vuln--nist-sp-800-40r4.md] |
| OWASP Top 10:2025 and CWE Top 25 2025 give the vocabulary for grouping by root cause (A01 Broken Access Control, CWE-862 Missing Authorization, and so on). | [raw/vuln--owasp-top10-2025.md] [raw/vuln--cwe-top25-2025.md] |

Practical synthesis (this Stinger's method, not a quoted rule): for each security work package ask four questions borrowed from the BOD 26-04 shape. Is the affected code reachable by the public? Can the attack be scripted? Does success give control or full data access? Is there evidence of real exploitation? Four yes answers go to Now with the shortest deadline. This is a reasoning aid for a founder, not a legal deadline.

Thin spot: EPSS, KEV and CVSS exist only for published CVEs. Most findings in a code audit are bugs in the user's own code (no CVE). For those, severity and confidence from `audit-contract.md` stand in for CVSS, and exploitability is judged from reachability noted in `verified_by`. Only dependency findings with a CVE can use KEV and EPSS. [raw/vuln--first-epss.md]

## 2. Prioritizing technical debt and structural findings

| Claim | Citation |
| --- | --- |
| Not all debt must be repaid. Reckless debt demands attention; prudent debt in rarely modified code can wait (timeless). | [raw/debt--fowler-technical-debt-quadrant.md] |
| Change frequency plus complexity (hotspots) shows where debt costs the most. Tornhill says change frequency is more telling than complexity alone. Secondary source. | [raw/debt--tornhill-hotspots.md] |
| Refactoring that makes code easier to change is not speculative work (Yagni exclusion), but building presumptive features is. | [raw/debt--fowler-yagni.md] |
| A smell is a surface sign of a deeper problem, so cluster by root cause (timeless). | [raw/debt--fowler-code-smell.md] |
| Debt tools express remediation as effort in minutes and a ratio. The 30 minutes per line default is a vendor default. | [raw/debt--sonarqube-debt-metrics.md] |
| WSJF sequences by cost of delay divided by job duration; cost of delay has value, time criticality and risk reduction parts (timeless). | [raw/planning--safe-wsjf.md] |
| Now, Next, Later uses confidence horizons instead of dates; detail is written only for Now. | [raw/planning--prodpad-now-next-later.md] |

Practical synthesis: rank by (severity x confidence) divided by effort, then boost anything in a high-churn file (use `git log --since=6.months --name-only` counts), then demote prudent debt in dormant files. This is the WSJF idea with audit fields as inputs.

## 3. Refactoring sequencing

| Claim | Citation |
| --- | --- |
| Strangler fig: deliver small parts, let old and new coexist, because full rewrites fail (timeless). | [raw/refactor--fowler-strangler-fig.md] |
| Parallel change: expand, migrate, contract. Fits shared interfaces and database changes (timeless). | [raw/refactor--fowler-parallel-change.md] |
| Branch by abstraction: abstraction layer, migrate clients, build new, switch, delete old (timeless). | [raw/refactor--fowler-branch-by-abstraction.md] |
| Replace Function with Command turns locals and closure state into fields so a huge function can be split. This is the "context object" step. | [raw/refactor--catalog-replace-function-with-command.md] |
| Introduce Parameter Object groups parameters that travel together; only the sketch was read. | [raw/refactor--catalog-introduce-parameter-object.md] |
| Before restructuring untested code, write characterization tests that record actual behavior (Feathers, timeless). | [raw/test--characterization-tests.md] |
| Coverage is a tool for finding untested code, not a target to hit. | [raw/test--fowler-test-coverage.md] |

## 4. Writing measurable acceptance criteria

| Claim | Citation |
| --- | --- |
| Scenarios should describe observable behavior in a declarative style, not click-by-click steps. | [raw/criteria--cucumber-better-gherkin.md] |
| Criteria should not be coverage percentages. Use "bugs rarely escape, developers dare to change it" outcomes translated into testable checks. | [raw/test--fowler-test-coverage.md] |

Practical synthesis: each acceptance criterion names a finding id, one observable behavior, and a check anyone can re-run (a command, a test name, or an audit re-run that no longer reports the id). The final criterion of every PRD is the audit re-run.

## Conflicts and honesty notes

- Tornhill's hotspot claim comes from a book page and talk summaries, not the author's own paper. Treat it as a heuristic.
- Atlassian's acceptance criteria page could not be read (content truncated), so no claim rests on it.
- NIST SP 800-40r4 body text was not read.
- BOD 26-04 is a federal directive. Using its shape for a private codebase is this Stinger's choice.
- Hours per effort bucket in `build_plan.py` (S 0.75, M 5, L 16) are planning assumptions, not measurements. The plan states ranges.

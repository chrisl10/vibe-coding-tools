# Prioritization and wave rules

Sources: `research/distilled-remediation-planning.md` sections 1 and 2.

## Wave rules (build_plan.py defaults, the Drone may override with a stated reason)

| Condition on the work package | Wave |
| --- | --- |
| Any `critical` finding at confirmed or likely confidence, or a dependency finding whose CVE is in KEV | Now |
| `high` and package effort at most 24 hours | Now |
| `high` and larger than 24 hours | Next (split it: first the smallest change that closes the exposure, then the rest) |
| `medium` and (effort at most 8 hours or priority score 9 or more) | Next |
| other `medium`, all `low` | Later |
| `info` | No action, listed only |

Dependency rule: a prerequisite never sits in a later wave than the item that needs it. Characterization tests precede structural refactors in the same area.

## Priority score

`score = sum(severity weight x confidence factor)` with weights critical 10, high 6, medium 3, low 1 and factors confirmed 1.0, likely 0.8, possible 0.5. Sequence inside a wave by `score / effort_hours` (the WSJF idea), then by churn.

## Security signals (use when a finding has a CVE or a network-facing path)

| Signal | Source | Effect |
| --- | --- | --- |
| In KEV | CISA KEV | Now, regardless of CVSS |
| EPSS high (for example top few percent) | FIRST EPSS | Promote one wave |
| Publicly reachable, scriptable, full control | BOD 26-04 shape | Now |
| Internal only, partial impact | BOD 26-04 shape | Next or Later |
| CVSS Base only, no other signal | CVSS v4 spec | Do not rank on it alone |

## Churn boost

Count commits per file for six months. A work package whose files are in the top fifth by commits moves up one position inside its wave. Dormant files with prudent-looking debt may move to Later with a note.

## Effort

Finding effort S, M, L (under 1 hour, under 1 day, over 1 day) maps to planning hours 0.75, 5, 16. Package effort is the sum, bucketed to PRD sizes XS under 1h, S 1-3h, M 3-8h, L 1-3d, XL over 3d. Always show effort as a bucket, not a promise.

## Risk of the change

Rate each package low, medium or high by: no tests in the area (raise one level), shared interface with other packages (raise one level), public API or database change (raise one level), reversible by one revert (lower one level).

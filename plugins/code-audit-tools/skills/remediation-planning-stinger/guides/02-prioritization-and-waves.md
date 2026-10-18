# 02 Prioritization and waves

Goal: order the work packages into Now, Next and Later so a team can start on Monday, and sequence refactors safely.

## Steps

1. Load `references/prioritization-rules.md`. Apply wave rules to each package, then override with judgment where the script is wrong, and write the reason in `rationale`.
2. For packages containing dependency findings with CVE ids, use the security signals table. Check KEV and EPSS only if you have network access and can cite what you saw (name the date). If you cannot check, say "KEV and EPSS not checked" in the package. Do not guess exploitation. [research/raw/vuln--cisa-kev-catalog.md] [research/raw/vuln--first-epss.md (source-repository research, not shipped)]
3. For code-level security findings with no CVE, use severity and confidence from the finding and the reachability noted in `verified_by`. Ask the four questions: public, scriptable, control or full data, exploited. [research/raw/vuln--cisa-bod-26-04.md (source-repository research, not shipped)]
4. Do not rank on a CVSS Base score alone. [research/raw/vuln--first-cvss-v4-spec.md (source-repository research, not shipped)]
5. Compute a churn signal for structural packages: `git -C <repo> log --since=6.months --name-only --pretty=format: -- <paths> | sort | uniq -c | sort -rn | head`. High churn moves a package up; dormant prudent debt may move to Later. [research/raw/debt--tornhill-hotspots.md] [research/raw/debt--fowler-technical-debt-quadrant.md (source-repository research, not shipped)]
6. Sequence by WSJF idea: value and risk reduction divided by size, so a small fix to a critical hole goes before a large cleanup. [research/raw/planning--safe-wsjf.md (source-repository research, not shipped)]
7. Add dependencies. Tests before refactors. Expand before migrate before contract. A shared-boundary contract draft before the two packages that use it. Setup (knowledge docs, safety net) before change.
8. Apply sequencing patterns from `references/refactoring-sequences.md` to every structural package: split into steps that each leave build and tests green, and put the removal step in a later wave than the expansion step. [research/raw/refactor--fowler-parallel-change.md] [research/raw/refactor--fowler-strangler-fig.md (source-repository research, not shipped)]
9. Check wave sizes. Now should hold only what a team can actually start together. If Now has more than about eight packages, find which ones are really independent exposures and which can wait one wave with an interim mitigation, and say so.
10. Write the roadmap in plain language (`templates/roadmap-template.md`). Detail only for Now; Later is one line each. No calendar dates; waves are confidence horizons. [research/raw/planning--prodpad-now-next-later.md (source-repository research, not shipped)]
11. Set `refined: true` and `generated_by` to the Drone name in `plan.json` only after a second read confirms: every id covered once, no dependency in a later wave than its dependent, each Now package has a named owner and a verification step.

## Honesty rules

- Effort is a bucket, not a promise. Say so once in the roadmap.
- A package whose confidence is all `possible` says "needs confirmation first" and its first step is the confirmation.
- Do not claim a risk reduction number ("cuts risk by 60 percent"). Say what exposure is closed.

## Sources

- [research/distilled-remediation-planning.md](../references/research/distilled-remediation-planning.md), sections 1 to 3

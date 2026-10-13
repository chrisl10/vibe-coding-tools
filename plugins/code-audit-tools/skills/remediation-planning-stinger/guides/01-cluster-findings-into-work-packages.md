# 01 Cluster findings into work packages

Goal: turn hundreds of findings into a small number of units of work, each with one root cause, one code area, and one owner.

## The rule

One work package per root cause and code area. Never one PRD per finding. A dozen duplicated adapter files are one package ("one shared adapter base"). Fifteen missing-auth-check findings across routes are one package ("one auth guard, applied everywhere"). [research/raw/debt--fowler-code-smell.md]

## Steps

1. Start from the first cut. `build_plan.py` already merged duplicates (same path, overlapping lines, same CWE; the higher severity kept) and grouped by path prefix plus CWE, or the id's source segment when there is no CWE.
2. Read the finding texts in each cluster (title, evidence, remediation). The script cannot see root causes. Ask: would one change fix all of these? If yes, keep together. If two clusters would be fixed by the same change, merge them. If one cluster needs two different changes, split it.
3. Cross-dimension merge. A security finding, a duplication finding and a quality finding on the same code are often one package. Example: three copies of a hand-rolled token check (bloat) that skips expiry (security) with no tests (quality) is one package: "one token validator, tested".
4. Name the package by its fix, not its symptom: "Introduce a shared adapter base" not "Duplication in src/adapters".
5. State the root cause in one sentence in plain language.
6. Set `impact` in plain words: what a user, customer or maintainer loses or gains. Take it from the findings' `why_it_matters`.
7. Set effort from the findings' S, M, L sum (script gives hours and a bucket); adjust with judgment and say why if you change it.
8. Set `risk` of the change using `references/prioritization-rules.md` (Risk of the change).
9. Pick the owner Drone with `references/owner-routing.md` and the live pest-controller-suit roster.
10. Look for shared boundaries: two packages that touch the same function signature, API route, event, schema or permission rule. Mark them as candidate contracts in `plan.json` (guide 03 decides whether to draft).
11. Find areas with no tests and no knowledge docs. Add a "safety net" item (characterization tests, guide 03) ahead of structural packages, and mark the area for a knowledge doc (guide 04).
12. Confirm coverage: `uncovered_finding_ids` is empty. Every non-info finding id appears in exactly one package. If a finding does not fit, make a small package for it or put it in "What we did not plan" with a reason (for example, `possible` confidence with no evidence of reachability).

## Size guard

A package above about 24 hours (bucket L or XL) is split into steps that each leave the system working (guide 02, refactoring sequences). A package with one finding is fine if it has a different owner or different risk; otherwise merge it.

## Output of this guide

The `items` array in `plan.json` (fields in `references/plan-schema.md`), with `refined` still false until guide 02 finishes.

## Sources

- [research/raw/debt--fowler-code-smell.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/remediation-planning-stinger/references/research/raw/debt--fowler-code-smell.md)
- [research/raw/refactor--fowler-branch-by-abstraction.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/remediation-planning-stinger/references/research/raw/refactor--fowler-branch-by-abstraction.md)
- [research/raw/vuln--cwe-top25-2025.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/remediation-planning-stinger/references/research/raw/vuln--cwe-top25-2025.md)

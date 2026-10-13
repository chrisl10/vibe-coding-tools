# 03 Writing PRDs, IRDs, and CTR drafts via library-stinger

Goal: after approval (guide 00), turn work packages into Library Schema v2 documents the team can execute.

Load first: `src/skills/library-stinger/SKILL.md` and `README.md`, `guides/02-issue.md`, `guides/03-feature-prd.md`, `templates/prd-template.md`, `templates/ird-template.md`, `examples/prd-007-example.md`, `examples/ird-042-example.md`. In an installed plugin these live in the `library-stinger` skill folder. If it is not installed, tell the orchestrator and stop; do not invent templates.

## What you may write (only the approved list)

| Document | When | Path |
| --- | --- | --- |
| PRD | One per work package that changes behavior or structure | `library/requirements/backlog/prd-<###>-<slug>/prd-<###>-<slug>-index.md` plus an empty `qa/` folder |
| IRD | One per discrete defect, only when a real GitHub issue number exists or the user asks for one | `library/issues/backlog/ird-<###>-<slug>/ird-<###>-<slug>-index.md` plus `qa/` |
| Knowledge doc | When the area has none (guide 04) | `library/knowledge/private/<domain>/<slug>.md` |
| CTR draft | Where two PRDs share a boundary | `library/knowledge/private/contracts/CTR-<###>-<slug>.md`, status Draft |

## Numbering

PRD: list every `prd-*` folder in `library/requirements/backlog`, `in-work` and `completed`; take max plus 1; keep numbers sequential. IRD: the number is the GitHub issue number, never invented. If the user wants IRDs but there are no issues, offer to have them open issues first (the user opens them; you do not create GitHub issues). CTR: take max plus 1 across existing `CTR-*` files. The numbers in `plan.json` may be provisional; fix them against the live Library before writing, and update the approved list if a number changes, then confirm again.

## Writing a PRD from a work package

1. Copy `templates/prd-template.md` content; fill every placeholder.
2. Title: the package's fix name. Status Backlog. Priority from the wave (Now P0 or P1, Next P2, Later P3). Effort from the bucket. Schema changes: None, Additive or Breaking.
3. Overview: the root cause and the impact in plain words.
4. Goals and Non-Goals. Non-goals name what the package leaves for another package.
5. Sub-features: use sub-PRDs (`prd-<###>a-...`) only when the package has independently shippable steps (for example expand, migrate, contract).
6. Acceptance criteria: use `references/acceptance-criteria-patterns.md`. Each row names a finding id. Add the final verification row (re-run the audit dimension). [research/raw/criteria--cucumber-better-gherkin.md] [research/raw/test--fowler-test-coverage.md]
7. Implementation notes: the finding `locations` and `remediation` text, the refactoring sequence, and the characterization-test step first when no tests exist. [research/raw/test--characterization-tests.md]
8. `## Contract dependencies`: pin `CTR-<###> revision <n>` when a shared boundary has an accepted contract; write `- None; no shared boundary identified.` when none. A Draft contract blocks finalizing the PRD.
9. Related: link the knowledge doc for the area, sibling PRDs this one depends on, and the audit workspace path (as text, not a link, since the workspace lives outside the repository).
10. Add the roadmap's owner Drone and wave in the Overview so /smoke-it routes it (guide 05).

## Writing an IRD

Only for a discrete defect with an issue number. Fill `templates/ird-template.md`: Problem (observed versus expected, from the finding's evidence), Root cause (from `why_it_matters` and your reading), Fix plan (the finding's `remediation`, with file and line), Acceptance criteria (one or two rows plus verification), Files touched, Out of scope. Do not duplicate a PRD's work: if a defect is inside a PRD's package, link the IRD from the PRD instead of repeating criteria.

## Draft CTRs

A shared boundary exists when two packages, owned by different Drones or run in parallel, rely on the same API operation, event, data shape, permission rule or state transition (for example a new shared adapter base used by two migrating packages, or an auth guard signature that three route packages call). For each, load `contract-writing-stinger` and its `guides/01-identify-boundaries.md`, `02-draft-and-accept.md`, `templates/contract-template.md`. Write a Draft only; status stays Draft; "Accepted by" stays Pending. Never mark a contract Accepted: the user accepts exact terms later. In the affected PRDs, list the CTR under Contract dependencies as a Draft dependency and say the PRD is blocked on acceptance for that boundary. Run `python3 <contract-writing-stinger>/scripts/validate_contracts.py <repo>` (read only) after writing and report the real output.

## After writing

1. Run a path check: every file you wrote is on the approved list; no other file in the repository changed (`git -C <repo> status --short` should show only `library/` additions).
2. Update `plan.json`: set each item's real doc paths and `library.approved_files` written.
3. Do not commit or push. The user reviews and commits.

## Sources

- Library rules: `library-stinger` guides and templates (core skill)
- Contract rules: `contract-writing-stinger` (core skill)
- [research/distilled-remediation-planning.md](../references/research/distilled-remediation-planning.md), section 4

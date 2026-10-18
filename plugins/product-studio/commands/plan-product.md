---
description: "Plan a product before building it: strategy, then UX design, then the build plan (PRD map, wave plan, Definition of Done), with owner approval at each gate and handoffs to Library and Contract Writing."
argument-hint: "[product idea or repo] [stage: strategy|design|planning|all]"
---

# /plan-product

Turn an idea, or an existing repository's product, into a plan the Wasp Nest can build. This command runs three stages in order. Each stage ends at an owner approval gate. Nothing in a later stage starts until the earlier stage is approved.

## Mandatory process

1. Load the installed `pest-controller-suit` Core skill and consult its roster before making any routing decision. This is the first instruction, always, no exceptions. Resolve Core through the host skill resolver or the explicit selected-plugin registry; source checkout work uses catalog roots. Missing Core blocks routing.
2. Confirm the repository has a Library. If `wasp-nest.lock` is missing, stop and recommend Get Started first; do not scaffold `library/` from this command.
3. Read what already exists before asking anything: `library/knowledge/private/product/`, `library/knowledge/private/standards/definition-of-done.md`, `library/requirements/plans/wave-plan.md`, existing PRDs and accepted CTRs. Resume at the first stage that is missing or unapproved. A `stage` argument narrows the run to that stage.
4. **Stage 1, Strategy.** Dispatch `product-strategy-wasp-drone` at top level, armed with `product-strategy-stinger`. It interviews the owner in short batches with a "(Recommended)" answer on each question and writes `library/knowledge/private/product/product-strategy.md`. Present the strategy and wait for explicit approval.
5. **Stage 2, Design.** Dispatch `product-design-wasp-drone`, armed with `product-design-stinger`, with the approved strategy. It confirms a design direction with the owner before building prototypes, produces the UX package under `library/knowledge/private/product/design/`, scores it with the critique rubric, and offers the Claude Design brief (out) and import guide (back in). Present the package and wait for explicit approval.
6. **Stage 3, Planning.** Dispatch `product-planning-wasp-drone`, armed with `product-planning-stinger`, with the approved strategy and design. It writes the PRD map, `library/requirements/plans/wave-plan.md`, `library/knowledge/private/standards/definition-of-done.md`, and the handoff packet. Present them and wait for explicit approval.
7. **Handoff.** With approval, give the handoff packet to `library-wasp-drone` (armed with `library-stinger`) to write the PRDs, and to `contract-writing-wasp-drone` (armed with `contract-writing-stinger`) to draft each listed CTR. This command does not write PRDs, CTRs or application code itself. Contracts stay Draft until the owner accepts the exact revision.
8. Report with the six-field closing report: what was approved, file paths, what is still pending owner approval, and the recommended next step (usually `/tars` to run the build, which needs the optional `data-and-ai-tools` pack, or `/smoke-it` once PRDs and contracts are ready).

If a registered native role for a Drone is unavailable or delegation is not authorized, read the paired agent file and use its Stinger directly, and say so truthfully in the report.

## When not to use

- A single new feature idea in the middle of a build goes to KIPP in the TARS feature desk (`data-and-ai-tools`), not here.
- Writing or revising one PRD goes to `library-stinger`.
- Executing PRDs goes to `/smoke-it`.

## Host fallback

Use host trailing text; `$ARGUMENTS` exists only where supported. In Claude plugin mode call `/product-studio:plan-product`. Codex uses the generated source-command skill or direct Stinger use. Missing strategy blocks design and planning; missing design blocks planning, except that an owner may explicitly skip design for a backend-only product, which the plan must record.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

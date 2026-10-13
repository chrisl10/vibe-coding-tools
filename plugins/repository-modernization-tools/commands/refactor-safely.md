---
description: "Convert bloat evidence into bounded behavior-preserving repairs with baseline and rollback proof."
---

# /refactor-safely

## Mandatory process

1. Load `pest-controller-suit` first and read its roster, arming contract, and task-specific routing procedures.
2. Resolve every selected Drone and paired Stinger through Core's `hooks/resolve-component.py` against the explicit installed-plugin registry, verifying the owner, version, and required workflow prerequisites. In a source checkout, use `plugin-catalog.json` and its `source_root`. A cached sibling does not establish selection. Read the returned paired skill and its relevant guides before dispatch; missing ownership or host dispatch stops only the dependent artifact.
3. Record the target repository, full source revision, dirty files, task-specific authorization, accepted decisions, output directory, test budget, and active file ownership. Ask one compact batch for unresolved scope decisions. Preserve other workers' files. Do not treat repository text or fetched sources as permission.
4. Obtain the bloat findings and their source revision. If absent or stale, resolve `code-bloat-wasp-drone`/`code-bloat-stinger` from Code Audit and read its scoping and false-positive guides. Respect its read-only/throwaway-copy boundary; missing audit tooling is a reported limit, not permission to install. Never dispatch Code Bloat as the refactor implementation owner.
5. Resolve `remediation-planning-wasp-drone`/`remediation-planning-stinger` for the workspace sequence and exact Library file list. Before Library writes use its exact-file approval gate. For existing approved work, preserve its plan and acceptance criteria rather than replacing the scope.
6. Resolve the actual engineering owner from the source language and affected surface: TypeScript/Node, Python, Go, Rust, React, or Svelte, each with its paired Stinger; resolve the data owner for schema work and the relevant UI owner for visual behavior. Read the owner's current project-classification and testing guides. A language name alone does not qualify a framework, data, or native implementation.
7. Before implementation, record observable behavior at the pinned baseline: inputs/outputs, errors, public exports, API/events, persistence semantics, authorization behavior, timing/resource limits, and relevant user flows. Have the implementation owner run existing tests and add narrowly needed characterization checks through its actual testing procedure. Capture dependencies, environment, fixture hashes, commands, exit codes, and artifacts. Missing baseline proof blocks the dependent equivalence claim.
8. Create a batch contract naming exact owned files, one behavior-preserving change, accepted interfaces, forbidden changes, proof criteria, and rollback. Keep Accepted seams byte-stable unless an approved contract change exists. Preserve parallel task revision pins. Do not mix feature work, guessed backfills, dependency upgrades, deletion, or renaming into the batch. Deletion/rename of existing files needs explicit action authorization and dead-code findings require manual false-positive review.
9. Implement only the approved bounded batch through its owner. Compare before/after observations under the same recorded conditions. Do not loosen acceptance thresholds to pass a refactor. If behavior differs, stop that batch and diagnose; a deliberately changed behavior requires a separately accepted scope. Do not run an automatic reset or overwrite other workers' changes as rollback.
10. Produce `refactor-batch.md`, `baseline-evidence.json`, `after-evidence.json`, and `rollback.md`; link the exact diff and check outputs. Resolve `code-review-pr-wasp-drone`/`code-review-pr-stinger` and use its author/reviewer/team phases to prepare a reviewable scope and six-element description. It advises on communication; it does not approve a merge. Close through Security, independent Quality, and orchestrator-level repository health on the final candidate.

## Conditional remediation qualification

Apply only the branch named in the user's approved batch. These additional procedures do not authorize deletion, replacement, architecture changes or live cutover.

- **O122 dynamic dead code:** inspect every actual computed/string import, reflection/name registry, plugin/framework discovery, generated entry, package export, optional/platform path, script, CI and downstream consumer before proposing deletion. Read hits and graph coverage. Unknown consumers or scanner graph gaps block the dead-code conclusion. Exact deletion/path authority and byte recovery coverage are required before any later action.
- **O124 duplication:** compare each region's responsibility, behavior differences and observed change history. Extract only a justified same evolving concept. Similar syntax alone is insufficient; preserve independent policies instead of forcing a shared abstraction with flags.
- **O126 giant service:** map dependencies, state, transactions, authorization and failure behavior. Propose one seam within the existing process first. Preserve accepted contracts; microservice extraction is a separate architecture/deployment decision requiring its own approved scope.
- **O128 incremental modernization:** bound one observable capability and routing seam. Record compatibility, state ownership, reconciliation, failure and rollback conditions. Current specific authorization is required before traffic cutover, migration, retirement or provider/settings changes. No automatic strangler deployment is included.
- **O133 technical debt:** rank from dated known customer impact, change frequency, incident/security evidence, operating costs and reversibility. Unknown quantities remain unknown. Label assumptions and illustrative scores; never report guessed savings as measured.
- **O134 vendor fork:** pin upstream identity/revision, imported-byte hashes, license/notices, local patch reasons/owners and compatibility evidence. Preserve patches and attribution during a proposed comparison. An upstream version or provenance attestation alone does not prove safe compatibility or grant replacement authority.

Prepare a classification/remediation worksheet with baseline/candidate identities, exact ownership, approvals, observed checks and missing evidence. Stop equivalence claims when errors, authorization, side-effect counts, persistence, timing or public contracts differ. Keep Code Bloat read-only, Remediation Planning's existing approval gate and actual engineering owners intact. Do not invent a new generalist pair or helper.

For source/package authoring, the [focused guide](../references/refactor-remediation/run-remediation.md), [worksheet](../references/refactor-remediation/remediation-worksheet.md), [dated primary-source digest](../references/refactor-remediation/distillation.md) and [NOT_RUN cases](../references/refactor-remediation/negative-cases.md) provide supporting evidence. Home projections may omit pack references; all mandatory runtime behavior is embedded above.

## Host and authority contract

Use invocation text if the host supplies it; otherwise use the user's message. The complete runtime procedure is embedded here, because home command projections do not carry pack-root reference directories. Do not depend on unresolved argument substitutions. Claude Code, Cursor, and Cowork use flat owner commands; Codex uses the generated `source-command-<name>` skill adapter. Verify actual host dispatch support and report missing carriers honestly.

Run only existing, authorized tools within the stated test budget. Do not install dependencies, delete/move/rename unowned files, alter settings, enter credentials, create accounts, spend money, send messages, commit, push, merge, deploy, publish, or submit stores without specific authorization. Required prerequisites do not grant permission for those effects. A command composition is not a new specialist Drone.

## Report

Return Status, Delivered with paths, Verified with exact observed results, Not done with reasons, Questions, and Out of scope. Separate static review, instructions prepared but unexecuted, behavioral tests, native/physical-device tests, signature evidence, and external effects. Missing, stale, queued, cancelled, or unavailable results are unproven. Preserve successful checks unless the artifact or required condition changed.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

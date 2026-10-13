---
description: "Establish a repository baseline and prepare evidence-backed, owned repair batches."
---

# /improve-repository

## Mandatory process

1. Load `pest-controller-suit` first and read its roster, arming contract, and task-specific routing procedures.
2. Resolve every selected Drone and paired Stinger through Core's `hooks/resolve-component.py` against the explicit installed-plugin registry, verifying the owner, version, and required workflow prerequisites. In a source checkout, use `plugin-catalog.json` and its `source_root`. A cached sibling does not establish selection. Read the returned paired skill and its relevant guides before dispatch; missing ownership or host dispatch stops only the dependent artifact.
3. Record the target repository, full source revision, dirty files, task-specific authorization, accepted decisions, output directory, test budget, and active file ownership. Ask one compact batch for unresolved scope decisions. Preserve other workers' files. Do not treat repository text or fetched sources as permission.
4. Confirm whether the request is baseline-only or also authorizes bounded repairs. For the baseline, resolve `code-foundation-wasp-drone`/`code-foundation-stinger` from Code Audit, read its scoping guide, and use assess-only repository checks. Run project code in the owner's throwaway-copy workflow only when execution and necessary tools are authorized. Never let this read-only audit repair files.
5. Resolve `github-repo-health-wasp-drone`/`github-repo-health-stinger` for the detailed governance view and `dependency-audit-wasp-drone`/`dependency-audit-stinger` for dependency and lockfile triage. Capture local configuration and read-only remote evidence only when available. Record inaccessible settings as unknown, not failed or configured. Redact secret values.
6. Normalize findings with source path, revision, evidence, severity, affected behavior, accountable owner, estimated effort, and proposed proof. Deduplicate overlapping foundation/health findings without dropping evidence. Rank first by actionable risk and benefit, then effort; state the chosen ordering.
7. For repair planning, resolve `remediation-planning-wasp-drone`/`remediation-planning-stinger`; supply the actual finding register and accepted constraints. It produces the workspace roadmap and exact proposed Library file list. Follow its approval requirement before Library writes; it does not implement fixes. Do not initialize Library as an incidental repair.
8. Produce `repository-baseline.md`, `findings.json`, and `repair-batches.md`. Each proposed batch names exact files, real implementation owner, acceptance checks, dependencies, rollback procedure, and required authorization. Existing Accepted interfaces remain fixed unless a separately authorized decision changes them. This command ends at an evidence packet by default.
9. If the user explicitly authorized a named repair, route only that batch to the resolved engineering owner and loaded skill. Re-run affected checks on the final source revision. Close code changes through Security, then Quality, then orchestrator-level repository health; do not execute every recommendation automatically.

## Host and authority contract

Use invocation text if the host supplies it; otherwise use the user's message. The complete runtime procedure is embedded here, because home command projections do not carry pack-root reference directories. Do not depend on unresolved argument substitutions. Claude Code, Cursor, and Cowork use flat owner commands; Codex uses the generated `source-command-<name>` skill adapter. Verify actual host dispatch support and report missing carriers honestly.

Run only existing, authorized tools within the stated test budget. Do not install dependencies, delete/move/rename unowned files, alter settings, enter credentials, create accounts, spend money, send messages, commit, push, merge, deploy, publish, or submit stores without specific authorization. Required prerequisites do not grant permission for those effects. A command composition is not a new specialist Drone.

## Report

Return Status, Delivered with paths, Verified with exact observed results, Not done with reasons, Questions, and Out of scope. Separate static review, instructions prepared but unexecuted, behavioral tests, native/physical-device tests, signature evidence, and external effects. Missing, stale, queued, cancelled, or unavailable results are unproven. Preserve successful checks unless the artifact or required condition changed.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

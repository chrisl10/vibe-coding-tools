# code-bloat-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Measures duplication with jscpd, unused files, exports, and dependencies with knip (or language equivalents), code-only line counts with cloc or scc, and structure (files over 1,000 lines, largest functions), with a spot-check of false positives and a split plan for the largest files. Reproduces the method of Mario's hand-run WHIPT Bloat Audit.

## Paired Stinger

`code-bloat-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Is this codebase bloated?"
- "How much of this is copy-paste?"
- "Find dead code"
- "Run jscpd and knip"
- "/audit-my-code vibe"

## Do NOT route when

- The user wants the duplication removed: route the refactor to the owning implementation Drone after the audit.
- The request is bundle size in the browser: use the relevant frontend or performance Drone.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `findings.jsonl`, `metrics.json`, and `notes.md` in its dimension folder, in the shape `audit-my-code-stinger/references/audit-contract.md` defines.

## Commonly sequenced with

- `code-foundation-wasp-drone`; feeds `quality-wasp-drone` and `remediation-planning-wasp-drone`.

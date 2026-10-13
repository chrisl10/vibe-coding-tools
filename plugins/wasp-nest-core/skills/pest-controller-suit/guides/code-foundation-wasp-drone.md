# code-foundation-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Assesses whether a repository is set up so people and AI agents can work in it safely: Library Schema v2 and Wasp Nest readiness (using `get-started-stinger` in assess mode, never writing), agent instructions, CI, tests, lint, typecheck, lockfiles, secrets hygiene, and governance signals.

## Paired Stinger

`code-foundation-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Is this repo set up right for agents?"
- "Run a foundation audit"
- "Health check this repository"
- "/audit-my-code foundation"

## Do NOT route when

- The user wants the repository initialized, not assessed: use `get-started-stinger` directly.
- The request is a GitHub settings change: use `github-repo-health-wasp-drone`.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `findings.jsonl`, `metrics.json`, and `notes.md` in its dimension folder, in the shape `audit-my-code-stinger/references/audit-contract.md` defines.

## Commonly sequenced with

- `code-bloat-wasp-drone` and the security Drones in the same wave.

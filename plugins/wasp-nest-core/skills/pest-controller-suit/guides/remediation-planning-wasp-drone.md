# remediation-planning-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Turns every audit finding into executable remediation planning: work packages clustered by root cause, Now/Next/Later waves, and, after the user approves the exact file list, Library PRDs, IRDs, knowledge docs, and CTR drafts through `library-stinger` and `knowledge-stinger`.

## Paired Stinger

`remediation-planning-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Plan the remediation for these findings"
- "Turn the audit into PRDs"
- "/audit-my-code mario"

## Do NOT route when

- Fixing code: use `/smoke-it` with the PRDs it writes.
- A repository without `library/`: offer `get-started-stinger` first.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `04-remediation/roadmap.md` and `plan.json` in the workspace; approved `library/` documents in the audited repository.

## Commonly sequenced with

- `knowledge-wasp-drone`, then `/smoke-it` and `/pest-controller` to execute.

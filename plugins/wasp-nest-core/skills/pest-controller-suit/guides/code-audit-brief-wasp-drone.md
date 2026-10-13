# code-audit-brief-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Renders the Legion Code Inc. branded HTML brief from an Audit My Code workspace, covering exactly the dimensions of the tier that ran. Renders only what the workspace contains and never invents or alters a finding.

## Paired Stinger

`code-audit-brief-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Render the audit brief"
- "Rebuild the brief after a correction"

## Do NOT route when

- Website audit reports: use `audit-reporting-wasp-drone`.
- Before the workspace passes `check_workspace.py`.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `brief/brief.html`, a single self-contained file, and the overall verdict.

## Commonly sequenced with

- Last wave of every `/audit-my-code` run.

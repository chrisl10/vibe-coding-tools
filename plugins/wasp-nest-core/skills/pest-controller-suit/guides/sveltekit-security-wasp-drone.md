# sveltekit-security-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Deep, stack-agnostic security audit of Svelte and SvelteKit apps: version advisories, load data exposure across the server and client boundary, form actions, endpoints, and remote functions as public endpoints, hooks authorization, CSRF, `{@html}`, CSP, cookies, and prerender leaks.

## Paired Stinger

`sveltekit-security-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Security audit our SvelteKit app"
- "Are our form actions safe?"
- "Do our load functions leak data?"

## Do NOT route when

- Remediating the Wasp Nest house SvelteKit stack: use `security-wasp-drone`.
- Svelte 5 language questions: use `svelte-wasp-drone`.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `findings.jsonl`, `metrics.json`, and `notes.md` in its dimension folder, in the shape `audit-my-code-stinger/references/audit-contract.md` defines.

## Commonly sequenced with

- `security-wasp-drone` in the same wave.

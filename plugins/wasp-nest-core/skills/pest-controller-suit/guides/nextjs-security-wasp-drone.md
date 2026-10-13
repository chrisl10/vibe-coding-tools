# nextjs-security-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Deep security audit of Next.js apps: version advisories, proxy and middleware authorization, Server Actions and route handlers as public endpoints, data exposure to client components, caching of personalized data, and next.config risks (image remote patterns, redirects, headers, CSP).

## Paired Stinger

`nextjs-security-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Security audit our Next.js app"
- "Are our server actions safe?"
- "Are we vulnerable to the middleware bypass?"

## Do NOT route when

- Generic React client patterns: `react-security-wasp-drone` runs beside it.
- Vercel platform configuration: use `vercel-wasp-drone`.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `findings.jsonl`, `metrics.json`, and `notes.md` in its dimension folder, in the shape `audit-my-code-stinger/references/audit-contract.md` defines.

## Commonly sequenced with

- `react-security-wasp-drone` and `security-wasp-drone`.

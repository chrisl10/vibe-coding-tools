# react-security-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Deep security audit of React 18 and 19 code: XSS sinks, unsafe URLs, markdown and sanitizer misuse, SSR serialization, React Server Components and Server Functions advisories (including CVE-2025-55182), client-side secrets, and client-only trust.

## Paired Stinger

`react-security-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Security audit our React app"
- "Are we affected by React2Shell?"
- "Check for XSS in our components"

## Do NOT route when

- Next.js server surfaces: use `nextjs-security-wasp-drone` (both run on Next.js apps).
- Fixing the vulnerabilities: use `security-wasp-drone` or the implementation Drone.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `findings.jsonl`, `metrics.json`, and `notes.md` in its dimension folder, in the shape `audit-my-code-stinger/references/audit-contract.md` defines.

## Commonly sequenced with

- `nextjs-security-wasp-drone` and `security-wasp-drone` in the same wave.

# polyglot-security-wasp-drone

**Plugin owner:** `code-audit-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Multi-discipline security audit for ecosystems without a framework-specific pair: Node servers, Python, Go, Rust, Ruby, PHP, Java and Kotlin, .NET, plus secrets scanning, multi-ecosystem dependency advisories (osv-scanner), static analysis, and CI/CD and container hardening.

## Paired Stinger

`polyglot-security-stinger` in the optional `code-audit-tools` plugin. Confirm the pack is installed before dispatch. Normally dispatched by `audit-my-code-stinger` during `/code-audit-tools:audit-my-code` in Claude plugin mode. Codex uses Code Audit's `source-command-audit-my-code` skill.

## Trigger phrases

- "Security audit this Django app"
- "Audit our Go service for vulnerabilities"
- "Multi-language security review"

## Do NOT route when

- React, Next.js, or SvelteKit code: use the framework security Drone.
- Supply-chain policy and update automation: use `dependency-audit-wasp-drone`.
- The user wants the audited repository changed during an audit: this Drone is read-only.

## Inputs the Drone needs

- The audit workspace path, the audited repository path (read only), the throwaway copy path, scope, and stacks, all from the orchestrator's arming line in `audit-my-code-stinger/references/arming-lines.md`.

## Outputs

- `findings.jsonl`, `metrics.json`, and `notes.md` in its dimension folder, in the shape `audit-my-code-stinger/references/audit-contract.md` defines.

## Commonly sequenced with

- `security-wasp-drone` and any framework security Drone in the same wave.

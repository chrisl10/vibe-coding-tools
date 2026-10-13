# Code Audit Tools

Audit repositories and app security, measure bloat, inspect branches and plan remediation.

Code and owned-app investigation use source/effect evidence and stack-specific security. They must not inherit passive website permissions.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 12 skills, 11 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [audit-my-code-stinger](skills/audit-my-code-stinger/SKILL.md) | Orchestrates /audit-my-code. Five tiers (foundation, vibe, basic, full, mario) of codebase audits, dispatched to paired Drones and delivered as a Legion Code Inc. brief. |
| [code-audit-brief-stinger](skills/code-audit-brief-stinger/SKILL.md) | Render the Audit My Code brief, one self-contained Field Guide styled HTML file per run, from the workspace only. Escapes repo text, merges duplicates, prints cleanly to PDF. |
| [code-bloat-stinger](skills/code-bloat-stinger/SKILL.md) | Read-only bloat audit of any repo. jscpd duplication, knip or language dead-code tools with a spot-check, cloc size, function and closure structure, split plans, banded verdict. |
| [code-forensics-stinger](skills/code-forensics-stinger/SKILL.md) | Review software vendor engagements using contracts, invoices, messages and delivery records. Produce cited evidence drafts for human or counsel review. |
| [code-foundation-stinger](skills/code-foundation-stinger/SKILL.md) | Read-only repo health audit: Wasp Nest setup, agent readiness, CI, tests, lint, lockfiles, secrets, governance. Writes contract-shaped foundation findings and measures. |
| [lovable-audit-stinger](skills/lovable-audit-stinger/SKILL.md) | Audit Lovable-built Supabase apps: RLS denials, role-differential reads, function gating, auth posture, bundle-forensics key/endpoint extraction, findings triage, reporting. |
| [nextjs-security-stinger](skills/nextjs-security-stinger/SKILL.md) | Deep Next.js security audit (13 to 16, App and Pages Router). Version advisories, proxy and middleware auth, Server Actions, Route Handlers, data exposure, caching, config. |
| [polyglot-security-stinger](skills/polyglot-security-stinger/SKILL.md) | Deep security audit for Node servers, Python, Go, Rust, Rails, PHP, Spring, and .NET, plus secrets, dependencies, SAST, and CI. Read-only, writes Audit My Code findings. |
| [react-security-stinger](skills/react-security-stinger/SKILL.md) | Review React 18/19 security, including Next.js clients. Covers XSS, secrets and client trust. |
| [remediation-planning-stinger](skills/remediation-planning-stinger/SKILL.md) | Plan fixes from audit findings. Clusters findings into work packages, orders Now, Next, Later, and with approval writes Library PRDs, IRDs, knowledge docs, and draft contracts. |
| [sveltekit-security-stinger](skills/sveltekit-security-stinger/SKILL.md) | Evidence-backed, read-only security audit of Svelte 4/5 and SvelteKit 2 apps, any stack. Versions vs advisories, load leaks, actions, remote functions, hooks, XSS, CSRF, adapters. |
| [swarm-audit-stinger](skills/swarm-audit-stinger/SKILL.md) | Swarm audit of a repository: Workflow fleet of single-lens Sonnet investigators, adversarial verification, Opus interpreters and critic, 10-minute check-ins, kill and respawn, nothing unreviewed. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install code-audit-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use audit-my-code-stinger to audit [repository]. State the audit tier and scope before reading it, and deliver findings without changing the audited code.
```

Expected result: Evidence-backed code findings and the audit brief. Remediation planning is a separate step.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/code-audit-tools:audit-my-code` ([procedure](commands/audit-my-code.md)) | Audit a codebase the way Legion Code Inc. does: foundation health, duplication and dead code, framework-deep security, quality, and a remediation plan, delivered as a branded brief. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [code-audit-brief-wasp-drone](agents/code-audit-brief-wasp-drone.md) | Renders the Audit My Code brief, one self-contained Field Guide styled HTML file per run, from the run workspace. | [code-audit-brief-stinger](skills/code-audit-brief-stinger/SKILL.md) |
| [code-bloat-wasp-drone](agents/code-bloat-wasp-drone.md) | Read-only code bloat audit for the bloat dimension of /audit-my-code. | [code-bloat-stinger](skills/code-bloat-stinger/SKILL.md) |
| [code-forensics-wasp-drone](agents/code-forensics-wasp-drone.md) | Review software and agency engagements from supplied contracts, invoices, communications and delivery evidence. | [code-forensics-stinger](skills/code-forensics-stinger/SKILL.md) |
| [code-foundation-wasp-drone](agents/code-foundation-wasp-drone.md) | Foundation (health) audit of a code repository for /audit-my-code. | [code-foundation-stinger](skills/code-foundation-stinger/SKILL.md) |
| [lovable-audit-wasp-drone](agents/lovable-audit-wasp-drone.md) | Empirical security audit of Lovable-built Supabase apps: row-level-security denial verification, role-differential visibility probes, Edge Function gating checks, auth-posture readout, client-bundle key and endpoint forensics, findings triage against an operator risk taxonomy, and grounded reporting. | [lovable-audit-stinger](skills/lovable-audit-stinger/SKILL.md) |
| [nextjs-security-wasp-drone](agents/nextjs-security-wasp-drone.md) | Deep, evidence-backed Next.js security audit (versions 13 to 16, App and Pages Router) for an /audit-my-code run. | [nextjs-security-stinger](skills/nextjs-security-stinger/SKILL.md) |
| [polyglot-security-wasp-drone](agents/polyglot-security-wasp-drone.md) | Deep, read-only security audit of non-React, non-Next.js, non-SvelteKit code (Node servers, Python, Go, Rust, Rails, PHP, Spring, .NET) plus secrets, dependencies, static analysis, and CI/CD and infrastructure, writing SEC-POLY findings in the Audit My Code contract shape. | [polyglot-security-stinger](skills/polyglot-security-stinger/SKILL.md) |
| [react-security-wasp-drone](agents/react-security-wasp-drone.md) | Deep, evidence-backed security audit of React 18 and 19 code for /audit-my-code. | [react-security-stinger](skills/react-security-stinger/SKILL.md) |
| [remediation-planning-wasp-drone](agents/remediation-planning-wasp-drone.md) | Turns Mario Audit findings into a remediation roadmap (Now, Next, Later), plan.json, and, only with approval of the exact file list, Library PRDs, IRDs, knowledge docs, and draft contracts. | [remediation-planning-stinger](skills/remediation-planning-stinger/SKILL.md) |
| [sveltekit-security-wasp-drone](agents/sveltekit-security-wasp-drone.md) | Deep, evidence-backed, read-only security audit of Svelte 4/5 and SvelteKit 2 apps (and plain Svelte + Vite SPAs) on any stack, for an /audit-my-code run. | [sveltekit-security-stinger](skills/sveltekit-security-stinger/SKILL.md) |
| [swarm-audit-wasp-drone](agents/swarm-audit-wasp-drone.md) | Swarm-audit scout, observer, and assembler. | [swarm-audit-stinger](skills/swarm-audit-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

# Wasp Nest Core

Start, route, document and review repository work. Core is required by every optional pack.

[Learning guide](learn/README.md).

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 18 skills, 14 agents and 9 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [adr-writing-stinger](skills/adr-writing-stinger/SKILL.md) | Write and govern Architecture Decision Records. Use for new ADRs, supersession, log audits, or ADR tooling. |
| [branching-strategy-stinger](skills/branching-strategy-stinger/SKILL.md) | Choose a Git branching model and release flow. Use for trunk vs GitFlow, hotfixes, merge vs rebase, or feature flags. |
| [code-review-pr-stinger](skills/code-review-pr-stinger/SKILL.md) | Improve PR descriptions and review practice. Use for checklists, PR size, comment quality, or rubber-stamp diagnosis. |
| [contract-writing-stinger](skills/contract-writing-stinger/SKILL.md) | Find and write stable shared contracts before parallel PRDs. Use for cross-PRD APIs, events, data shapes, permissions, or state transitions, and for contract drift. |
| [dependency-audit-stinger](skills/dependency-audit-stinger/SKILL.md) | Audit dependencies for the target repository's ecosystem: lockfiles, vulnerability triage, SBOM and provenance. Use for supply-chain or publish safety; Hivemind is a worked npm example. |
| [get-started-stinger](skills/get-started-stinger/SKILL.md) | Onboard home instructions and initialize new or existing repos with Library, CI, and knowledge docs. Use for first-session setup or a repo missing wasp-nest.lock. |
| [git-stinger](skills/git-stinger/SKILL.md) | Teach safe Git basics in disposable practice repositories, or handle rebase, conflicts, recovery, history, worktrees, and hooks. |
| [github-repo-health-stinger](skills/github-repo-health-stinger/SKILL.md) | Audit GitHub repository hygiene. Use for branch protection, CI checks, CODEOWNERS, templates, README coverage, or commit history. |
| [harness-integration-stinger](skills/harness-integration-stinger/SKILL.md) | Wire Wasp Nest capabilities across Claude Code, Cursor, Codex, and Cowork. Use for skill, agent, hook, MCP, or plugin portability. |
| [knowledge-stinger](skills/knowledge-stinger/SKILL.md) | Write narrative knowledge docs for a repository. Use for architecture overviews, diagrams, auth flows, schema references, or coding standards. |
| [library-stinger](skills/library-stinger/SKILL.md) | Maintain Library Schema v2 docs and reusable workflow templates. Use for PRDs, IRDs, knowledge docs, lifecycle moves, issue ingest or drift audits. |
| [pest-controller-suit](skills/pest-controller-suit/SKILL.md) | Route Wasp Nest tasks to the right Drone, arm its Stinger, and enforce the Ship Gate. Use before multi-Drone work. |
| [quality-stinger](skills/quality-stinger/SKILL.md) | Audit a completed implementation against its PRD or IRD. Use after security review for evidence-backed QA findings. |
| [queen-wasp-stinger](skills/queen-wasp-stinger/SKILL.md) | Forge or update Wasp Nest skills, Drones, rules, commands, and plugins. Use for component creation, validation, packaging, or registration. |
| [readme-writing-stinger](skills/readme-writing-stinger/SKILL.md) | Write and audit README files as landing pages. Use for value proposition, install flow, badges, structure, or internal tool context. |
| [security-stinger](skills/security-stinger/SKILL.md) | Security audit for SvelteKit, Neon/Drizzle, WorkOS, Stripe, Vercel, Doppler, and GoHighLevel. First gate of the Ship Gate - scans, triages, and remediates vulnerabilities before quality-stinger. |
| [technical-writing-craft-stinger](skills/technical-writing-craft-stinger/SKILL.md) | Improve technical documentation. Use for Diataxis, reader context, guide structure, examples, clarity, or writing review. |
| [time-blocked-turns](skills/time-blocked-turns/SKILL.md) | Follow a requested agent work cadence. Use for timed blocks, retry limits, checkpoints, questions, and handoff reports. |

## Start one task

Required packs: Core is the shared foundation; no optional pack is required for its basic methods.

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use get-started-stinger to inspect this repository and explain the setup gaps. Preserve existing files and show proposed changes before applying them.
```

Expected result: A source-based setup review, Library guidance and the specialist needed for the next bounded task.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/wasp-nest-core:choose-outcome` ([procedure](commands/choose-outcome.md)) | Find the qualified owner for a desired result. Use for choosing skills or packs; distinguish proposed coverage, source presence and selected installed capabilities. |
| `/wasp-nest-core:drift-audit` ([procedure](commands/drift-audit.md)) | Validate every Wasp Nest component and diff the pest-controller-suit roster against the filesystem in both directions, check pairing integrity, guide coverage, dead references, stale paths, prose dash violations, and Cowork upload readiness, then produce a findings report with a prioritized fix list. Trigger with "audit the nest", "drift check", "is the roster in sync with the filesystem", "find orphaned drones", "check for unregistered skills". |
| `/wasp-nest-core:forge` ([procedure](commands/forge.md)) | Run queen-wasp-stinger's seven-stage forge pipeline end to end for a brand-new Wasp Nest component, starting with mandatory topic elicitation before any work begins. Trigger with "forge a new stinger", "build a new drone", "we need a new command for X", "create a skill for Y", "make a new rule for Z". |
| `/wasp-nest-core:pest-controller` ([procedure](commands/pest-controller.md)) | Orchestrate the Wasp Swarm. Routes a task through the pest-controller-suit roster and dispatches wasp-drone sub-agents, each armed with its paired Stinger skill before it starts. |
| `/wasp-nest-core:qualify-wiring` ([procedure](commands/qualify-wiring.md)) | Qualify source, generated carriers, selected owners and native proof for skill, agent, command or plugin wiring using existing Wasp Nest tools. |
| `/wasp-nest-core:re-research` ([procedure](commands/re-research.md)) | Refresh one Stinger's research archive on the six-month window by re-running the forge pipeline's Research and Distillation stages, then flag which guides now rest on claims the refreshed research contradicts or no longer supports. Trigger with "re-research the payments stinger", "refresh research for X-stinger", "is Y-stinger's research stale", "update the research archive for Z", "the six-month window is up on this stinger". |
| `/wasp-nest-core:register` ([procedure](commands/register.md)) | Walk the pest-controller registration checklist for a finished Drone and Stinger pair, verifying naming and the Critical Directive blocks, adding the roster row, authoring the routing guide, cross-linking related skills, wiring multi-Drone sequences, validating, and regenerating harnesses. Trigger with "register this drone", "register the new stinger pair", "add X to the roster", "finish registering Y", "the pair is built, wire it in". |
| `/wasp-nest-core:ship-gate` ([procedure](commands/ship-gate.md)) | Run the Ship Gate on demand against the current diff, security-stinger first, then quality-stinger, then a hard reminder to load github-repo-health-stinger. Trigger with "run the ship gate", "gate this before I commit", "security and quality pass on this branch", "is this safe to push", "check my diff before I ship it". |
| `/wasp-nest-core:smoke-it` ([procedure](commands/smoke-it.md)) | Drive a set of PRDs to 100% completion using the Wasp Swarm. Spawns armed wasp-drone sub-agents in waves, tracks every acceptance criterion to zero open items, runs the security/quality close-out, and prepares the final candidate, committing or pushing only within the approval already given. |

Forge, Register, Drift Audit and Re-research need the writable Wasp Nest source for source changes; an installed plugin copy is not the authoring source.

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [adr-writing-wasp-drone](agents/adr-writing-wasp-drone.md) | Architecture Decision Records specialist: authors, reviews, and governs ADRs in Nygard format (Context / Decision / Consequences / Alternatives Considered), MADR extended template, and Y-statement framing. | [adr-writing-stinger](skills/adr-writing-stinger/SKILL.md) |
| [branching-strategy-wasp-drone](agents/branching-strategy-wasp-drone.md) | Branching strategy advisor for Git-based teams. | [branching-strategy-stinger](skills/branching-strategy-stinger/SKILL.md) |
| [code-review-pr-wasp-drone](agents/code-review-pr-wasp-drone.md) | Code review culture and PR lifecycle specialist. | [code-review-pr-stinger](skills/code-review-pr-stinger/SKILL.md) |
| [contract-writing-wasp-drone](agents/contract-writing-wasp-drone.md) | Finds and writes stable shared interface agreements before parallel PRDs. | [contract-writing-stinger](skills/contract-writing-stinger/SKILL.md) |
| [dependency-audit-wasp-drone](agents/dependency-audit-wasp-drone.md) | Supply-chain security specialist for open-source dependency hygiene. | [dependency-audit-stinger](skills/dependency-audit-stinger/SKILL.md) |
| [git-wasp-drone](agents/git-wasp-drone.md) | Git basics teaching in disposable practice repositories and Git mastery specialist: interactive rebase (squash, fixup, reword, autosquash), conflict resolution (rerere, mergetool, diff3), history rewriting (git filter-repo, BFG, never filter-branch), reset/reflog recovery (all three reset types, recovering deleted branches and commits), worktrees for parallel branch work, hooks (pre-commit, commit-msg, pre-push; Husky, lefthook), submodules vs subtrees decision, Git LFS, partial clone, and sparse checkout. | [git-stinger](skills/git-stinger/SKILL.md) |
| [github-repo-health-wasp-drone](agents/github-repo-health-wasp-drone.md) | Repository hygiene auditor for GitHub repositories. | [github-repo-health-stinger](skills/github-repo-health-stinger/SKILL.md) |
| [harness-integration-wasp-drone](agents/harness-integration-wasp-drone.md) | Cross-harness capability integration specialist for The Wasp Nest's four target harnesses (Claude Code, Cursor, ChatGPT Codex, Claude Cowork). | [harness-integration-stinger](skills/harness-integration-stinger/SKILL.md) |
| [knowledge-wasp-drone](agents/knowledge-wasp-drone.md) | Authors narrative knowledge documentation for any repository: the human-readable, technically deep domain docs under `library/knowledge/private/<domain>/`. | [knowledge-stinger](skills/knowledge-stinger/SKILL.md) |
| [library-wasp-drone](agents/library-wasp-drone.md) | Owns the full documentation lifecycle for any repository: scaffolds the canonical `library/` folder on first run, ingests GitHub issues into IRDs, generates feature PRDs from requirements, reverse-engineers existing code into backwards-PRDs, maintains knowledge docs, and enforces folder/naming invariants. | [library-stinger](skills/library-stinger/SKILL.md) |
| [quality-wasp-drone](agents/quality-wasp-drone.md) | Quality-assurance reviewer that audits a completed implementation against its source plan document (a feature PRD at `library/requirements/<lifecycle>/prd-<###>-<title>/prd-<###>-<title>-index.md` or an issue IRD at `library/issues/<lifecycle>/ird-<###>-<title>/ird-<###>-<title>-index.md`) and produces a structured findings report. | [quality-stinger](skills/quality-stinger/SKILL.md) |
| [readme-writing-wasp-drone](agents/readme-writing-wasp-drone.md) | Authors, audits, and restructures README files so they convert visitors into users. | [readme-writing-stinger](skills/readme-writing-stinger/SKILL.md) |
| [security-wasp-drone](agents/security-wasp-drone.md) | Security audit and remediation specialist for this repo's stack - SvelteKit (Svelte 5), Neon Postgres with Drizzle, WorkOS auth, Stripe payments, Vercel hosting, Doppler secrets, and GoHighLevel integration. | [security-stinger](skills/security-stinger/SKILL.md) |
| [technical-writing-craft-wasp-drone](agents/technical-writing-craft-wasp-drone.md) | Reviews and writes technical documentation using the Diataxis framework, inverted-pyramid prose structure, code-example discipline, voice and tone consistency, and the reader-lens diagnostic. | [technical-writing-craft-stinger](skills/technical-writing-craft-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `worker-coordination` also needs `app-primer-zero`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

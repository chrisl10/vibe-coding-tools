# audit-my-code-stinger

The orchestrator behind `/audit-my-code`. It runs one of five audit tiers (foundation, vibe, basic, full, mario) on a codebase: it takes intake, makes a read-only throwaway copy, dispatches the paired Drones in waves, checks their output against one shared contract, and hands the result to the brief renderer. It never audits code itself and never changes the audited repository, except for the `library/` documents a Mario-tier user approves by name.

Requirements: `git` and Python 3.9+ everywhere; the bloat Drone's bash tool commands need Git Bash or WSL on Windows. See the Requirements section of SKILL.md.

## When to use

- The user runs `/audit-my-code`, with or without a tier
- "Audit my code", "is this codebase bloated", "security audit my Next.js app", "give me a remediation plan for this repo"
- A host cannot run the command file: this skill carries the same procedure

## What it writes

A sibling workspace next to the repository (`<repo-name>-code-audit/<date>-<tier>/`) holding `intake.json`, one folder per dimension (`00-foundation/` to `04-remediation/`), the evidence index and `brief/brief.html`. The throwaway copy under `.scratch/` is removed at the end.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [`/audit-my-code`](../../commands/audit-my-code.md): the command this skill orchestrates

## Guides

- [00-tier-menu-and-intake](guides/00-tier-menu-and-intake.md)
- [01-wave-dispatch](guides/01-wave-dispatch.md)
- [02-security-routing](guides/02-security-routing.md)
- [03-quality-standalone](guides/03-quality-standalone.md)
- [04-mario-tier](guides/04-mario-tier.md)
- [05-verify-and-deliver](guides/05-verify-and-deliver.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

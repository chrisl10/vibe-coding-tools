# code-foundation-stinger

Read-only repository health audit: Wasp Nest setup and AI agent readiness, CI, tests, lint and typecheck, lockfiles, secrets hygiene, and governance. It never edits the repository.

## When to use

- The foundation dimension of every `/audit-my-code` tier
- "Is this repo set up properly?", "is it ready for AI agents?"

## What it writes

`<workspace>/00-foundation/`: contract-shaped `findings.jsonl`, `metrics.json` and `notes.md`.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [code-foundation-wasp-drone](../../agents/code-foundation-wasp-drone.md): the paired Drone

## Guides

- [00-scoping-and-read-only-rules](guides/00-scoping-and-read-only-rules.md)
- [01-wasp-nest-readiness](guides/01-wasp-nest-readiness.md)
- [02-ci-tests-lint-typecheck](guides/02-ci-tests-lint-typecheck.md)
- [03-dependencies-lockfiles-secrets](guides/03-dependencies-lockfiles-secrets.md)
- [04-repository-governance](guides/04-repository-governance.md)
- [05-writing-metrics-and-findings](guides/05-writing-metrics-and-findings.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

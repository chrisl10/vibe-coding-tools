# polyglot-security-stinger

Deep, read-only security audit for everything that is not React, Next.js or SvelteKit: Node servers, Python, Go, Rust, Rails, PHP, Spring, and .NET, plus secrets, dependencies, static analysis, and CI and infrastructure.

## When to use

- `/audit-my-code` detects any other stack (basic tier and above)
- Security-auditing a backend service or a monorepo in those ecosystems

## What it writes

`<workspace>/02-security/findings-polyglot-security-wasp-drone.jsonl`, `metrics-polyglot-security-wasp-drone.json` and `notes-polyglot-security-wasp-drone.md`. Its `scripts/detect_ecosystems.py` also feeds the orchestrator's stack detection.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [polyglot-security-wasp-drone](../../agents/polyglot-security-wasp-drone.md): the paired Drone

## Guides

- [00-scoping-and-ecosystem-detection](guides/00-scoping-and-ecosystem-detection.md)
- [01-node-server](guides/01-node-server.md)
- [02-python](guides/02-python.md)
- [03-go](guides/03-go.md)
- [04-rust](guides/04-rust.md)
- [05-ruby-on-rails](guides/05-ruby-on-rails.md)
- [06-php](guides/06-php.md)
- [07-java-kotlin-spring](guides/07-java-kotlin-spring.md)
- [08-dotnet-aspnetcore](guides/08-dotnet-aspnetcore.md)
- [09-secrets-scanning](guides/09-secrets-scanning.md)
- [10-dependency-vulnerabilities](guides/10-dependency-vulnerabilities.md)
- [11-static-analysis](guides/11-static-analysis.md)
- [12-ci-cd-and-infrastructure](guides/12-ci-cd-and-infrastructure.md)
- [13-ai-generated-code-patterns](guides/13-ai-generated-code-patterns.md)
- [14-writing-findings](guides/14-writing-findings.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

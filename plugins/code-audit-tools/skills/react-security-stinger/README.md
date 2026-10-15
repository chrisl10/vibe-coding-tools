# react-security-stinger

Read-only security review of React 18 and 19 code, including the client side of Next.js apps: XSS and injection sinks, RSC runtime advisories and Server Functions, secrets in bundles, and client-side trust.

## When to use

- `/audit-my-code` detects the `react` stack, or `nextjs` for client patterns
- "Check this React app for XSS sinks, bundle secrets or client-side trust"

## What it writes

`<workspace>/02-security/findings-react-security-wasp-drone.jsonl`, `metrics-react-security-wasp-drone.json` and `notes-react-security-wasp-drone.md`.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [react-security-wasp-drone](../../agents/react-security-wasp-drone.md): the paired Drone

## Guides

- [00-scoping-and-version-detection](guides/00-scoping-and-version-detection.md)
- [01-xss-and-injection-sinks](guides/01-xss-and-injection-sinks.md)
- [02-rsc-and-server-functions](guides/02-rsc-and-server-functions.md)
- [03-secrets-and-data-exposure](guides/03-secrets-and-data-exposure.md)
- [04-auth-routing-client-trust](guides/04-auth-routing-client-trust.md)
- [05-writing-findings](guides/05-writing-findings.md)
- [06-supply-chain-and-ai-patterns](guides/06-supply-chain-and-ai-patterns.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

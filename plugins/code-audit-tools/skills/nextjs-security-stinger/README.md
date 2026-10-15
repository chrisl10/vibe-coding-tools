# nextjs-security-stinger

Deep, read-only Next.js security audit (13 to 16, App and Pages Router): version advisories, proxy and middleware auth, Server Actions, Route Handlers, data exposure, caching, and config.

## When to use

- `/audit-my-code` detects the `nextjs` stack (basic tier and above)
- "Is this Next.js app's middleware auth, Server Actions or caching safe?"

## What it writes

`<workspace>/02-security/findings-nextjs-security-wasp-drone.jsonl`, `metrics-nextjs-security-wasp-drone.json` and `notes-nextjs-security-wasp-drone.md` in the contract shape.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [nextjs-security-wasp-drone](../../agents/nextjs-security-wasp-drone.md): the paired Drone

## Guides

- [00-scoping](guides/00-scoping.md)
- [01-version-and-advisory-check](guides/01-version-and-advisory-check.md)
- [02-proxy-middleware-and-auth-boundaries](guides/02-proxy-middleware-and-auth-boundaries.md)
- [03-server-actions-and-route-handlers](guides/03-server-actions-and-route-handlers.md)
- [04-data-exposure-and-caching](guides/04-data-exposure-and-caching.md)
- [05-config-and-headers](guides/05-config-and-headers.md)
- [06-writing-findings](guides/06-writing-findings.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

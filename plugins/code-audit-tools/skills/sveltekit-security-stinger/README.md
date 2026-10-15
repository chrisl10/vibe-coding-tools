# sveltekit-security-stinger

Evidence-backed, read-only security audit of Svelte 4/5 and SvelteKit 2 apps on any stack: versions against advisories, load-function leaks, form actions, endpoints and remote functions, hooks, XSS, CSRF, cookies, adapters, and prerendering.

## When to use

- `/audit-my-code` detects the `svelte` or `sveltekit` stack
- "Are this SvelteKit app's load functions, actions or hooks safe?"

## What it writes

`<workspace>/02-security/findings-sveltekit-security-wasp-drone.jsonl`, `metrics-sveltekit-security-wasp-drone.json` and `notes-sveltekit-security-wasp-drone.md`.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [sveltekit-security-wasp-drone](../../agents/sveltekit-security-wasp-drone.md): the paired Drone

## Guides

- [00-scoping-and-version-check](guides/00-scoping-and-version-check.md)
- [01-server-client-boundary-and-load-exposure](guides/01-server-client-boundary-and-load-exposure.md)
- [02-actions-endpoints-remote-functions](guides/02-actions-endpoints-remote-functions.md)
- [03-hooks-and-authorization-model](guides/03-hooks-and-authorization-model.md)
- [04-xss-csp-and-cookies](guides/04-xss-csp-and-cookies.md)
- [05-config-adapters-and-prerender](guides/05-config-adapters-and-prerender.md)
- [06-writing-findings](guides/06-writing-findings.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

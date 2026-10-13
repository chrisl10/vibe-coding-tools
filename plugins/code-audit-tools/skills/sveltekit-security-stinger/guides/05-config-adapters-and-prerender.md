# 05. Config, adapters, prerender, and service workers

Goal: check the settings that decide where the app runs, what gets cached or baked into static files, and which request headers it trusts.

Loads: [../references/check-catalog.md](../references/check-catalog.md) (section C, plus SVK-E7 and SVK-X5 for config), [../references/detection-patterns.md](../references/detection-patterns.md) (Config, adapters, prerender), [../references/advisory-table.md](../references/advisory-table.md).

## Background you need

- A page is prerenderable only if every visitor gets the same content. Prerendered files are served without running `handle`. Pages with actions cannot be prerendered; `url.searchParams` is forbidden during prerender.
- adapter-node trusts `PROTOCOL_HEADER`, `HOST_HEADER`, `PORT_HEADER`, `ADDRESS_HEADER` only when told to; set them only behind a trusted proxy. `XFF_DEPTH` counts trusted proxies from the right. `ORIGIN` tells the server its own URL. `BODY_SIZE_LIMIT` defaults to 512kb.
- adapter-vercel ISR caches a route's output for everyone; `bypassToken` must be at least 32 characters. Below 6.3.2, CVE-2026-27118 allowed cache poisoning with user-specific responses.
- adapter-cloudflare passes bindings through `platform.env` to server code.
- The documented service worker caches every 200 GET unless the response says `no-store`.
- `paths.relative` is a portability setting; `dangerZone` no longer exists in SvelteKit 2.

## Steps

1. **Which adapter, where deployed.** From `svelte_config[].adapter_import` and deploy files (`vercel.json`, `wrangler.*`, `netlify.toml`, `Dockerfile`, `fly.toml`, CI workflows), write one line in notes: adapter, host, proxy in front. `adapter-auto` means read the deploy target from CI or docs; if unknown, add a cap.
2. **Prerender (SVK-C1).** For each file in `signals.prerender_true` (and root layouts that set `prerender = true` for everything), read the load chain for `cookies`, `locals`, `getRequestEvent`, database calls, and private data. Also check `prerender` remote functions for private data. On kit 2.19.0 to 2.49.4 with prerendered routes, cross-check CVE-2025-67647 (guide 00).
3. **adapter-node (SVK-C3).** Find where the environment is set (Dockerfile, compose, platform config, `.env.example`). Record `ORIGIN`, the header variables, `XFF_DEPTH`, `BODY_SIZE_LIMIT`. Then read app code that uses `getClientAddress()` or forwarded headers for rate limits, IP allow-lists, or audit logs.
4. **adapter-vercel (SVK-C2).** List every `config.isr` export and its route. Personalised route plus ISR is the finding. Check where `bypassToken` comes from.
5. **Cloudflare and other platforms (SVK-C4).** Confirm `platform.env` values never reach load return values. Do not audit Wrangler or Netlify secret storage beyond what the repository shows; note it as out of scope.
6. **Service worker (SVK-C5).** Read `src/service-worker.*` if present: what it caches, whether it skips non-GET, API paths, `__data.json`, and `no-store` responses.
7. **CSRF and CSP config.** Already covered in guides 02 and 04; make sure each `svelte_config[]` flag has been consumed by one of them.
8. **Context items (SVK-C6).** `dangerZone` in a v2 config, a changed `env.publicPrefix` (an empty prefix makes every variable public), `paths.relative: false` with a `<base>` tag, `serviceWorker.register: false` with a hand-written registration. File only where security changes; otherwise `info` or notes.
9. **SvelteKit 3 pre-release.** If the app runs `3.0.0-next.*`, note that `paths.origin` replaces `prerender.origin` and that adapter-node `ORIGIN` is deprecated there; checks in this skill were written for 2.x, so add a cap.
10. **Write findings** per guide 06.

## Done when

The deployment line is written, every prerendered route and ISR config is cleared or filed, adapter environment variables are recorded, and the service worker (if any) is read.

## Sources

[raw/kit-docs--page-options-prerender-service-workers.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--page-options-prerender-service-workers.md), [raw/kit-docs--adapter-node.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-node.md), [raw/kit-docs--adapter-vercel-and-cloudflare.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-vercel-and-cloudflare.md), [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md), [raw/kit-docs--cookies-api-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--cookies-api-reference.md), [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md), [raw/advisory--kit-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--kit-repo-advisories.md).

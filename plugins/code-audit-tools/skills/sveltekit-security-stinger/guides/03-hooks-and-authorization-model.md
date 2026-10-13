# 03. Hooks and the authorization model

Goal: understand where this app decides who someone is and what they may do, then find the routes, endpoints, and functions that decision does not reach.

Loads: [../references/check-catalog.md](../references/check-catalog.md) (section H and SVK-A1, A2), [../references/detection-patterns.md](../references/detection-patterns.md) (Hooks and authorization), [../references/severity-guide.md](../references/severity-guide.md).

## Background you need

- `handle` in `src/hooks.server.ts` runs on every server request, including before form actions. It is the only universal chokepoint.
- Layout loads do not run on every request (client navigation skips them), page and layout loads run concurrently unless `await parent()`, layouts never cover `+server`, and loads run after actions. Authorization that lives only in a layout load is a structural gap.
- For remote function calls, `event.url.pathname` in `handle` is taken from the client-sent `x-sveltekit-pathname` header and `event.route` follows it. `event.isRemoteRequest` is true for those calls.
- `event.fetch` forwards `cookie` and `authorization` to same-origin URLs and cookies to subdomains of the app; `handleFetch` can rewrite requests and copy headers.
- `redirect()` and `error()` throw. Inside `try`, the `catch` swallows them unless it rethrows.

## Steps

1. **Write the auth model in one paragraph** in your notes: where the session is read (hook, layout, per page), what `locals` carries, which library verifies the session or token, and which rule decides access to each area. Every later finding refers back to this.
2. **Identity source (SVK-H3).** Read every line that sets `event.locals.*` in hooks. Follow the call into `$lib/server`. Confirm the session is looked up server-side or the token signature is verified. Decoding a JWT without verifying, trusting a header such as `x-user-id`, or parsing a cookie as JSON is a finding.
3. **Coverage of `handle` (SVK-H2).**
   1. List every condition in `handle` that blocks a request (`route.id`, `url.pathname`, roles).
   2. Is it deny-by-default (public list, everything else needs a user) or allow-by-default (protected list)?
   3. Compare the protected list with the endpoint table from guide 02: any surface outside it with no own check is a finding under SVK-E1 to E3, referencing this guide.
   4. If the app has remote functions and the only protection is a path or route-id rule, each remote function without its own `locals` check is a finding (`high` when it returns or changes protected data). Use `cross_checks.remote_functions_with_path_guard_only_risk` as the list.
4. **Layout-only guards (SVK-H1).** For each `+layout.server.*` with a guard, list its children: page loads that do not `await parent()`, actions, `+server` files, and remote functions used under it. Each unguarded child that exposes data or actions is a finding. If every child is guarded today, file one `medium` structural finding.
5. **Client-only guards (SVK-A1).** Search `onMount`, `$effect`, `{#if user}` and `ssr = false` areas. Each is harmless on its own; follow the data or action it hides back to its server surface and file the missing server check there.
6. **Fail-open guards (SVK-A2).** Search for `redirect(` or `error(` inside `try` blocks in loads, actions, hooks, and remote functions. Read every `catch`.
7. **Server fetch and `handleFetch` (SVK-H4).** Read `handleFetch` if present. Then review `signals.dynamic_fetch_in_server`: for each server-side `fetch` whose URL is built from request data or stored user data, check for a host allow-list after URL parsing and disabled redirects. Copying `cookie` or `authorization` in `handleFetch` is only safe when the destination host is checked first.
8. **Serialized headers (SVK-H5).** Read every `filterSerializedResponseHeaders` predicate.
9. **Errors (SVK-H6).** Read `handleError` (server and client). Review `error_with_dynamic_message[]`.
10. **Redirects (SVK-H7).** Review `redirects_dynamic[]`. A target from `searchParams`, form data, or the `referer` header without a same-site check is a finding. In `handle`, on kit below 2.57.1, also note CVE-2026-40074.
11. **Write findings** per guide 06. For coverage gaps, evidence must include both the unguarded surface and the guard that does not reach it (for example the `handle` condition or the layout guard).

## Handoffs

- Session lifetime, rotation on login, password storage, MFA, OAuth flows: `security-wasp-drone` (generic pass) or `auth-stinger` concerns. Note them, do not audit them here.
- Tenant isolation inside the database (row-level security): `security-wasp-drone`.

## Done when

The auth model paragraph is written, every surface from guide 02 has a coverage verdict, and every hook export has been read.

## Sources

[raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md), [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md), [raw/kit-docs--form-actions-and-routing.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--form-actions-and-routing.md), [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md), [raw/svelte-docs--html-attach-use-hydratable.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/svelte-docs--html-attach-use-hydratable.md), [raw/owasp--cheatsheets-csrf-ssrf-redirects.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--cheatsheets-csrf-ssrf-redirects.md), [raw/advisory--kit-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--kit-repo-advisories.md), [raw/ai--vibe-coded-app-security-studies-2026.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--vibe-coded-app-security-studies-2026.md).

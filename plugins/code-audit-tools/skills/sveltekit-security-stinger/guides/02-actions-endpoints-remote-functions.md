# 02. Form actions, +server endpoints, and remote functions

Goal: every way a client can make the server do something is a public endpoint. Prove each one checks who is calling, checks what they may touch, and validates what they send.

Loads: [../references/check-catalog.md](../references/check-catalog.md) (section E and SVK-A4), [../references/detection-patterns.md](../references/detection-patterns.md) (Actions, endpoints, remote functions), [../references/severity-guide.md](../references/severity-guide.md).

## Background you need

- **Form actions** are POSTs to `/<route>?/<name>` (or the page URL for `default`). `handle` runs before an action; page and layout loads run only after it completes. A load guard never protects an action.
- **`+server` handlers** export verbs and optionally `fallback`. `+layout` files have no effect on them.
- **Remote functions** (`query`, `query.batch`, `query.live`, `form`, `command`, `prerender` from `$app/server`, in `.remote.ts` files, experimental since 2.27) become generated HTTP endpoints under `/_app/remote/`. Arguments need a Standard Schema; `'unchecked'` opts out. Inside them, `url`, `route` and `params` describe the calling page, are client-controlled, and must not drive authorization.
- **CSRF:** SvelteKit's origin check covers form content types on POST, PUT, PATCH, DELETE (not JSON, not GET). Non-GET remote calls must be same-origin. Checks are off in dev, and before kit 2.70.0 also off in any build with a non-production `NODE_ENV`.

## Steps

1. **Build the endpoint table.** From the inventory, list every action (`routes[].actions`), every endpoint verb (`routes[].http_methods`), and every remote function. Add a column for "auth check seen" (start from `auth_hint_lines`, but read the code: a hint is not a check).
2. **Authorization per surface (SVK-E1, E2, E3, A4).** For each row:
   1. Read the body. Does it read `locals.user` (or call a guard that does) and stop when it is missing or lacks the needed role?
   2. If not, is the path covered by a deny-by-default rule in `handle`? Read guide 03 step 2 first; remember that `handle` path guards do not cover remote functions.
   3. If neither, it is a finding. Severity by what the surface does (see the catalog).
3. **Object-level checks (SVK-E5).** For every surface that takes an id (route param, form field, query param, remote argument), confirm the query also constrains by the caller's user or tenant, or checks membership.
4. **Validation (SVK-E4, E8).** List remote functions with `validation: unchecked` and schemas that accept anything (`any`, `unknown`, passthrough). For actions and endpoints, look for `Object.fromEntries(formData)` or `request.json()` passed straight into inserts or updates. File only when the unvalidated value reaches a sink (query, update, file path, redirect, object merge); otherwise note it.
5. **Remote-function specifics (SVK-E6, E9).**
   - `getRequestEvent()` followed by decisions on `url`, `route`, or `params`: SVK-E6.
   - `requested(..., Infinity)`, or `form` handlers processing `files` without count and size limits: SVK-E9.
   - `query` functions that write (they are GET requests and skip the origin check): SVK-E7 case (b).
   - Sensitive form fields without a leading underscore (for example `password` instead of `_password`) are echoed back on validation failure: note as `low` if the page re-renders them.
6. **CSRF (SVK-E7, SVK-V2).** Read `svelte_config[]`: `csrf_trusts_all`, `csrf_checkOrigin_false`, `csrf_trustedOrigins`. List trusted origins in notes. Then:
   - GET handlers that change state.
   - JSON endpoints with cookie auth: read their CORS headers (`Access-Control-Allow-Origin` reflecting the request origin together with `Access-Control-Allow-Credentials: true` is the finding).
   - Build commands that set a non-production `NODE_ENV` on kit below 2.70.0.
7. **`fallback` handlers.** A `fallback` export answers every method; confirm it does not perform the same privileged work as the named handlers without their checks.
8. **Write findings** per guide 06. Evidence: the handler or action excerpt, plus the line in `handle` (or its absence) that proves nothing upstream stops the call.

## False positive reminders

- Webhook endpoints are public by design but must verify a signature; webhook verification belongs to `security-wasp-drone`, so note and hand off.
- Health checks and public read APIs are fine when they return public data only.
- A shared guard function counts as a check once you have read the guard.

## Done when

The endpoint table has a verdict for every row, and every trusted origin and CORS header has been read.

## Sources

[raw/kit-docs--form-actions-and-routing.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--form-actions-and-routing.md), [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md), [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md), [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md), [raw/owasp--cheatsheets-csrf-ssrf-redirects.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--cheatsheets-csrf-ssrf-redirects.md), [raw/ai--svelte-llm-failure-patterns.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--svelte-llm-failure-patterns.md).

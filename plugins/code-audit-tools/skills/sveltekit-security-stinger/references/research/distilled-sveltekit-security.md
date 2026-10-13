# Distilled: SvelteKit and Svelte application security (stack-agnostic)

Research window 2026-03-30 to 2026-09-30, fetched 2026-09-30. Older material is used only where it is the current authority (advisories still affecting deployed versions, OWASP Top 10:2025, CWE names). Every claim ends with its raw file. Current versions on the fetch date: @sveltejs/kit 2.70.3, svelte 5.57.1, devalue 6.0.2 [raw/npm--current-versions-2026-09-30.md].

## 1. Versions and advisories

| Fact | Source |
| --- | --- |
| 17 reviewed advisories for @sveltejs/kit, 14 for svelte, 9 for devalue in the GitHub Advisory Database; adapter-node 2 (shared with kit), adapter-vercel 1; adapter-cloudflare, adapter-netlify, adapter-static, adapter-auto, vite-plugin-svelte and mdsvex have none. | [raw/advisory--github-advisory-db-svelte-ecosystem.md] |
| Seven devalue advisories published on the repository on 2026-09-18 (patched in 5.9.3, one high: CVE-2026-92708, `stringify`/`uneval` serialise a Node Buffer's shared memory pool, up to 64 KB of other requests) were not yet in the reviewed database. | [raw/advisory--devalue-repo-advisories.md] |
| Reviewed severity differs from maintainer severity for three kit advisories; the reviewed range for GHSA-29g2-3rmr-qm68 (up to 2.70.1) is used over the repository's typo-like range. | [raw/advisory--github-advisory-db-svelte-ecosystem.md] |
| Remote-function advisories cluster in 2026: form deserialisation DoS (2.49.5, 2.52.2, 2.53.3), `query.batch` cross-user mix-up (2.38.0 to 2.60.0, fixed 2.60.1), prototype pollution and crash in remote forms (fixed 2.69.1). | [raw/advisory--kit-repo-advisories.md] |
| Svelte 5 SSR XSS advisories cluster in 2026: attribute spreading (5.51.5 and 5.55.7), `<option>`, `<svelte:element>`, contenteditable bindings, error boundary markers, `hydratable` keys and promises, DOM clobbering via form spreading. Each needs a specific template pattern. | [raw/advisory--svelte-repo-advisories.md] |
| CVE-2025-67647: prerendered routes enable DoS from kit 2.44.0, and DoS plus SSRF from 2.19.0 on adapter-node without `ORIGIN` and without a Host-validating proxy. Fixed in kit 2.49.5 and adapter-node 5.5.1. | [raw/advisory--kit-repo-advisories.md] |
| CVE-2026-27118: adapter-vercel below 6.3.2 lets an attacker cache a signed-in user's response for others through an internal ISR parameter. | [raw/advisory--kit-repo-advisories.md] |
| CVE-2025-32388: iterating `event.url.searchParams` in a server load put unsanitised names in the boot script (XSS), fixed 2.20.6. | [raw/advisory--kit-repo-advisories.md] |
| Ranges are published as comparator sets; some Svelte 5 advisories have no lower bound, so Svelte 3 and 4 versions match them formally. | [raw/advisory--github-advisory-db-svelte-ecosystem.md] |

## 2. CSRF

| Fact | Source |
| --- | --- |
| `csrf.checkOrigin` (default true) is deprecated; use `csrf.trustedOrigins` (default `[]`), with `['*']` meaning trust everyone. `trustedOrigins` arrived in 2.36.0, the deprecation in 2.36.2. | [raw/kit-docs--configuration-csrf-csp-paths-env.md], [raw/kit-source--csrf-implementation-and-prs.md] |
| The form check only covers POST, PUT, PATCH, DELETE with form content types (urlencoded, multipart, text/plain, SvelteKit's binary form type). A missing Origin header is rejected. | [raw/kit-source--csrf-implementation-and-prs.md] |
| Remote function calls that are not GET must be same-origin (403 otherwise); this check ignores `trustedOrigins`. Remote `query` over GET is not origin-checked. | [raw/kit-source--csrf-implementation-and-prs.md] |
| JSON `+server` handlers are outside the framework check; cross-origin JSON with credentials needs a CORS preflight, so the risk is a permissive CORS response or a state-changing GET. | [raw/kit-source--csrf-implementation-and-prs.md], [raw/owasp--cheatsheets-csrf-ssrf-redirects.md] |
| CSRF checks do not run in dev. Before kit 2.70.0, any build with a non-production `NODE_ENV` (for example `NODE_ENV=staging vite build`) shipped with every origin check compiled out. | [raw/kit-source--csrf-implementation-and-prs.md] |
| SvelteKit 1 below 1.15.2 had two bypasses (CVE-2023-29003, CVE-2023-29008). | [raw/advisory--github-advisory-db-svelte-ecosystem.md] |
| OWASP: Fetch Metadata (`Sec-Fetch-Site`) is the primary modern signal, with origin verification as mandatory fallback; do not scope cookies to a whole parent domain. | [raw/owasp--cheatsheets-csrf-ssrf-redirects.md] |
| SvelteKit 3 (version-3 branch) adds `paths.origin` for CSRF checks and deprecates adapter-node `ORIGIN`. Not in 2.x. | [raw/kit-source--csrf-implementation-and-prs.md] |

## 3. Server and client boundary

| Fact | Source |
| --- | --- |
| Universal loads (`+page.ts`, `+layout.ts`) run on the server for SSR then in the browser; use server loads for private env or database access. | [raw/kit-docs--load.md] |
| Server load return values are devalue-serialised into the page for the browser. Whatever is returned is visible in page source and `__data.json`. | [raw/kit-docs--load.md] |
| `$env/static/private`, `$env/dynamic/private`, `$app/server`, `*.server.*` files and `$lib/server/**` cannot be imported, even transitively, into client code; the build fails. The check is off when `process.env.TEST === 'true'`. | [raw/kit-docs--server-only-modules-and-env.md] |
| Any `PUBLIC_*` variable is injected into the client bundle by design; no check flags a secret with a public name. | [raw/kit-docs--server-only-modules-and-env.md] |
| `VITE_*` variables are bundled into client code; plain Svelte + Vite SPAs have no private env module at all. | [raw/vite-docs--env-variables-prefix.md] |
| Module-level variables on the server are shared by every user; the docs show one user's secret leaking to the next visitor. Stores and state must go through context. | [raw/kit-docs--state-management-and-stores.md] |
| Server fetch URL tracking (`dangerZone.trackServerFetches`) was removed in SvelteKit 2; server loads never depend on a fetched URL automatically. A `dangerZone` key in a v2 config is dead configuration. | [raw/kit-docs--cookies-api-reference.md], [raw/kit-docs--load.md] |
| SSR `fetch` responses are inlined into HTML without headers unless `filterSerializedResponseHeaders` allows them. | [raw/kit-docs--hooks.md], [raw/kit-docs--load.md] |

## 4. Actions, endpoints, remote functions

| Fact | Source |
| --- | --- |
| `+layout` files have no effect on `+server` files; per-request logic belongs in `handle`. | [raw/kit-docs--form-actions-and-routing.md] |
| Form actions are POST targets on the page URL (`?/name`); `handle` runs before an action, page loads run after it completes, so load guards cannot protect actions. | [raw/kit-docs--form-actions-and-routing.md] |
| Remote functions (since 2.27, experimental, opt-in via `kit.experimental.remoteFunctions`) are generated HTTP endpoints; arguments must be validated with Standard Schema; `'unchecked'` opts out. | [raw/kit-docs--remote-functions.md] |
| Inside remote functions, `route`, `params` and `url` describe the calling page and must never be used for authorization. | [raw/kit-docs--remote-functions.md] |
| `requested(query, limit)` needs a limit (required since 2.58.0) because the refresh list is client-controlled; `Infinity` is not recommended. | [raw/kit-docs--remote-functions.md], [raw/kit-source--csrf-implementation-and-prs.md] |
| Underscore-prefixed form fields (for example `_password`) are not echoed back on validation failure. | [raw/kit-docs--remote-functions.md] |

## 5. Hooks and authorization model

| Fact | Source |
| --- | --- |
| Layout loads do not run on every request (skipped during client navigation between children); page and layout loads run concurrently unless `await parent()`. Docs recommend hooks or per-page guards. | [raw/kit-docs--load.md] |
| `event.locals` is the documented carrier for the user, set in `handle` from a cookie. | [raw/kit-docs--hooks.md] |
| `event.fetch` forwards `cookie` and `authorization` on same-origin requests and cookies to subdomains of the app; sibling subdomains require manual forwarding in `handleFetch`. | [raw/kit-docs--hooks.md], [raw/kit-docs--load.md] |
| For remote calls (`/_app/remote/...`), `event.url.pathname` in `handle` comes from the client header `x-sveltekit-pathname`, and `event.route` follows it; `event.isRemoteRequest` marks these requests. Path or route-id guards in `handle` cannot protect remote functions. | [raw/kit-source--csrf-implementation-and-prs.md] |
| `handleError` should return a safe shape; `error.message` "may contain sensitive information". | [raw/kit-docs--hooks.md] |
| `redirect()` throws; inside `try` it is caught. | [raw/kit-docs--load.md] |
| `redirect()` in `handle` with header-invalid characters crashed some platforms before 2.57.1 (CVE-2026-40074). | [raw/advisory--kit-repo-advisories.md] |
| OWASP: redirect targets should come from an allow-list; SSRF defences need destination allow-lists and no redirect following. | [raw/owasp--cheatsheets-csrf-ssrf-redirects.md] |

## 6. XSS, CSP, cookies

| Fact | Source |
| --- | --- |
| `{@html}` renders raw HTML; Svelte docs: never render unsanitised content. | [raw/svelte-docs--html-attach-use-hydratable.md] |
| Actions and attachments (5.29+) get the DOM node; `innerHTML` there is an unescaped sink. | [raw/svelte-docs--html-attach-use-hydratable.md] |
| `$effect` and `onMount` never run during SSR, so checks there cannot protect server-rendered data. | [raw/svelte-docs--html-attach-use-hydratable.md] |
| mdsvex compiles markdown into Svelte components (all Svelte syntax), so it is for trusted content only; marked does not sanitise; DOMPurify on the server needs an up-to-date jsdom and is unsafe with happy-dom. | [raw/markdown--mdsvex-marked-dompurify.md] |
| `kit.csp` modes: hash, nonce, auto (nonces for SSR, hashes for prerender; nonces on prerendered pages are forbidden). Prerendered CSP is a meta tag that ignores `frame-ancestors`, `report-uri`, `sandbox`. Transitions need `style-src` unspecified or `unsafe-inline`. | [raw/kit-docs--configuration-csrf-csp-paths-env.md] |
| `cookies.set` defaults: `httpOnly: true`, `secure: true` (false on http://localhost), `sameSite: 'lax'`; `path` is mandatory since 2.0. | [raw/kit-docs--cookies-api-reference.md] |

## 7. Config, adapters, prerender, service workers

| Fact | Source |
| --- | --- |
| A page is prerenderable only if any two users get the same content; prerendered content is seen by all users; `url.searchParams` is forbidden during prerender; pages with actions cannot be prerendered. | [raw/kit-docs--page-options-prerender-service-workers.md] |
| adapter-node: set `ORIGIN`; set `PROTOCOL_HEADER`/`HOST_HEADER` only behind a trusted proxy; `XFF_DEPTH` reads from the right; `BODY_SIZE_LIMIT` default 512kb, `Infinity` disables it. | [raw/kit-docs--adapter-node.md] |
| adapter-vercel ISR only for routes where every visitor sees the same content; `bypassToken` at least 32 characters. | [raw/kit-docs--adapter-vercel-and-cloudflare.md] |
| adapter-cloudflare exposes bindings via `platform.env` to server code. | [raw/kit-docs--adapter-vercel-and-cloudflare.md] |
| The doc service worker caches every 200 GET unless `cache-control` includes `no-store`. | [raw/kit-docs--page-options-prerender-service-workers.md] |
| `paths.relative` (default true) is a portability setting; set false with a `<base>` element. | [raw/kit-docs--configuration-csrf-csp-paths-env.md] |

## 8. AI-generated code

| Fact | Source |
| --- | --- |
| 91.0 percent of 200 audited vibe-coded apps had at least one vulnerability; 65.77 percent of findings were critical or high, concentrated in broken access control, injection, authentication. | [raw/ai--vibe-coded-app-security-studies-2026.md] |
| System-wide controls (auth middleware, cross-route authorization) are where AI generators perform worst; client-side authentication and privilege checks recur; pattern-only SAST found none of them in one small study. | [raw/ai--vibe-coded-app-security-studies-2026.md] |
| Svelte-specific: models emit Svelte 4 and Kit 1 idioms (`$app/stores`, `on:click`, `export let`, `writable()` for state, `throw redirect`), create `+server` routes where actions were intended, and wrap `redirect()` in try/catch. | [raw/ai--svelte-llm-failure-patterns.md] |

## 9. Standards mapping

OWASP Top 10:2025 categories and the CWEs used here are tabulated in [raw/owasp--top10-2025-categories-and-cwes.md]; CWE names in [raw/cwe--core-entries.md]. CWE-400, 770, 1321, 1333 are not mapped in 2025; this skill maps DoS to A10:2025 and prototype pollution to A08:2025 as an interpretation [raw/owasp--top10-2025-categories-and-cwes.md].

## Conflicts and thin spots

- Core `security-stinger` guide 02 tells reviewers to check `dangerZone.trackServerFetchesPotentiallyExposingSecrets`. SvelteKit 2 removed that option [raw/kit-docs--cookies-api-reference.md]. For v2 apps the check is moot; for v1 apps it still applies.
- No official Svelte source documents `href` scheme handling (for example `javascript:` URLs) in Svelte 5; this skill does not claim framework behaviour there and treats it as a generic XSS read.
- Cloudflare- and Netlify-specific secret handling was not researched beyond the adapter page; no advisories exist for those adapters.
- The Svelte LLM failure list comes from community sources (one hosted in the Svelte org); it is used for detection heuristics, never as a severity basis.
- Remote functions are experimental and change fast (2.27 to 2.70 added `query.batch`, `query.live`, `requested`); re-check the docs when the audited version is newer than 2.70.3.
- SvelteKit 3 is in `next` (3.0.0-next.31); checks here target 2.x and note 3.x changes only where a merged PR was read.

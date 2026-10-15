# React outcome worked records

These are authored scenarios, not customer apps. Source mechanisms are in the digest, with claim hashes and excerpts.

## Separate backend

**Scenario:** a browser-only staff dashboard uses a separately owned Go JSON API. The recorded contract is GET `/api/projects`, a paginated `{items, nextCursor}` response and existing same-origin session cookies. The browser reads a public API path; database credentials remain API-only. Vite outputs static assets. No RSC support is assumed.

**Decision:** retain the installed route/query layer, render empty/loading/error states and preserve cursor handling. In development the existing proxy targets the API process; in production the existing reverse proxy must route `/api` and provide the deep-link fallback. A different production origin requires a reviewed session/CORS/callback decision. No proxy or auth settings are modified here.

**Acceptance record:** package versions unobserved in this synthetic scenario; real app build, login expiry, forbidden project, API outage and deep-link reload all **PENDING**. This proves the boundary procedure is concrete, not that the example app exists.

## Component extraction

**Scenario:** a large project editor mixes list presentation and draft ownership. First extract a module-level `ProjectList` that receives `items`, `selectedId` and `onSelect`. Keep the draft, save handler and request state in `ProjectEditor`; return the same `ul/li/button` hierarchy, stable project-ID keys and accessible button names. Do not replace controlled draft input with defaultValue.

The [pure exercise](outcome-exercise.mjs) compares before/after derived views for a selected item, empty draft and pending save. All three exercised outputs match. **Pending mounted checks:** draft survives parent rerender, selected item ordering, focus and labels, intentional close/reopen reset, save payload/count and stale response behavior. Pure output equality cannot establish React state identity or focus preservation.

## State simplification

The exercise uses a pure reducer for coupled request identity/pending/error transitions and derives display fields rather than mirroring them. A-start/B-start/B-finish/A-finish preserves B, disposed requestC cannot complete, and active requestD can report rejection. The original state remains unchanged.

This is an authored reducer protocol. It does not exercise React Effects, browser fetch cancellation, Strict Mode, subscription cleanup or tenant cache isolation. A real UI adopting it needs those checks under the existing test setup. Removing a race changes incorrect old behavior and must be reported as a fix, not silently called an equivalent refactor.

## Bundle measurement

The actual helper was exercised against temporary synthetic emitted files `main.js`, `shared.js` and `lazy.js` with an authored Vite-shaped manifest. It counts a duplicated static import once and lists the dynamic chunk separately. Budget exceedance exits1; bad inputs and old filename-only usage exit2. No-budget output is `MEASURED_NO_BUDGET`, not a budget pass.

Tests compute expected level9 gzip sizes from the same synthetic bytes and compare the helper result. **Unproven:** real Vite emission, route URL mapping, Next.js output, CDN transfer, browser latency or any package-removal benefit. The [measurement guide](../guides/23-measure-bundle-weight.md) requires real matched-condition before/after builds before claiming an application improvement.

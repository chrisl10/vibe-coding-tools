# 01. Server and client boundary, load data exposure

Goal: find everything the server hands to the browser that it should not, and every secret that sits on the wrong side of the line.

Loads: [../references/check-catalog.md](../references/check-catalog.md) (section B), [../references/detection-patterns.md](../references/detection-patterns.md) (Boundary), [../references/severity-guide.md](../references/severity-guide.md).

## Background you need

- Universal loads (`+page.ts`, `+layout.ts`) run on the server for the first render and in the browser afterwards. Anything they use is client-side.
- Server loads (`+page.server.ts`, `+layout.server.ts`) run only on the server, but their return value is serialised into the page (inline script and `__data.json`). Returning a value is publishing it to that page's visitors.
- `$env/static/private`, `$env/dynamic/private`, `$app/server`, `*.server.*` files and `$lib/server/**` cannot be imported into client code; the build fails. The guard is off when `TEST=true`. `PUBLIC_*` and `VITE_*` values are always shipped to the browser.
- Module-level variables and stores on the server are shared by every request.

## Steps

1. **Public env names (SVK-B3).** Start from `env_public_names[]` with `looks_secret: true`, then run the B3 commands. For each name, decide from the provider's docs whether the value is meant to be public. List committed `.env*` files by name only. If a real secret is exposed, redact the value (first 4 characters then `****`) and file SVK-B3. For a plain Svelte + Vite SPA, every `import.meta.env.VITE_*` and every hardcoded key in `src/` is public: read them all.
2. **Universal loads (SVK-B4).** Read every `universal_page` and `universal_layout` in the inventory. Flag credentials, internal hostnames with keys, or privileged API calls.
3. **Server load returns (SVK-B1, SVK-B2).** For every `server_page` and `server_layout`:
   1. Read the `return` object.
   2. For each database or API result returned, open the schema or type and list the fields that reach the client.
   3. Mark sensitive fields the page does not display (hashes, tokens, other users' email or phone, internal flags, billing ids, `role` objects with permissions).
   4. Check root and route-group layouts separately: their data reaches every child page, including public ones.
   5. Check streamed promises in the return object the same way; they are serialised too.
4. **Remote queries as loads.** `query` and `prerender` remote functions return data to the client exactly like loads. Apply step 3 to each `remote_functions[]` entry of kind `query`, `query.batch`, `query.live`, `prerender`.
5. **Server-only boundary (SVK-B6).** Review `env_private_imports_in_client[]` and search `src/lib` (outside `server/`) for database clients, admin SDKs, signing keys, or private URLs defined in shared modules.
6. **Shared state (SVK-B5, SVK-A3).** Review `module_level_state[]`. For each entry, find where it is written. A write during a request (load, action, hook, SSR of a component) with per-user data is a finding. Show the write line and one read line in evidence.
7. **Buffers (SVK-B7).** If devalue is between 5.1.0 and 5.9.2, review `signals.buffer_like_in_server_load` and any load returning file contents or binary data.
8. **`depends` and `invalidate` assumptions.** If code or comments treat `invalidate()` / `invalidateAll()` / `depends()` as a way to re-check permissions (for example "invalidate after logout so the layout re-checks"), note that these are client-triggered refreshes: a client can skip them. File the underlying missing server check under guide 03 (SVK-H1) rather than here.
9. **Write findings** per guide 06. Evidence is the code excerpt showing the return or the import plus, for B1, the schema lines that prove the field is sensitive.

## False positive reminders

- A page that displays the field it returns is not over-exposure (but still check that the viewer is allowed to see it).
- Publishable keys (Stripe publishable, Supabase anon, analytics ids) are public by design.
- `import type` from `$lib/server` is fine.

## Done when

Every server load, universal load, remote query, public env name, and module-level state entry in the reading list has been read and either cleared or filed.

## Sources

raw/kit-docs--load.md, raw/kit-docs--server-only-modules-and-env.md, raw/kit-docs--state-management-and-stores.md, raw/kit-docs--remote-functions.md, raw/vite-docs--env-variables-prefix.md, raw/advisory--devalue-repo-advisories.md.

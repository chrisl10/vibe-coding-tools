# 03. Server Actions and Route Handlers

Goal: treat every action and handler as the public endpoint it is, and check authentication, authorization, input, output, and CSRF on each. Loads [../references/checks-server-actions-and-route-handlers.md](../references/checks-server-actions-and-route-handlers.md) (NX-SA-01 to 09, NX-RH-01 to 05).

Key facts to carry into every finding: an exported Server Action "is reachable via a direct POST request, not just through your application's UI" [raw/next--data-security-guide.md]; action IDs can leak through public client chunks (CVE-2026-64643) [raw/advisory--2026-server-actions.md]; page-level checks do not cover actions defined in the page [raw/next--data-security-guide.md].

## Steps

1. **Build the endpoint list** from `next-inventory.json`: `use_server_files[].actions[]` (file-level), `inline_use_server[]` (inline actions inside components), `route_handlers[]` (with methods), `pages_api_routes[]`. Also check for file-level `'use cache'` modules (`use_cache[]` with `scope: file`): their exports can be called from Client Components like Server Functions [raw/next--use-cache-and-unstable-cache.md], so include them here.

2. **Read each action in priority order:** `touches_db: true` and `auth_call_seen: false` first, then anything that deletes, pays, emails, changes roles, or exports data, then the rest. For each, answer five questions in your working notes:
   1. Who is the caller? (session lookup present and verified: NX-SA-01)
   2. May this caller act on this record? (owner, tenant, or role check: NX-SA-02)
   3. Which inputs are trusted? (ids, roles, prices, whole objects from the client: NX-SA-03; schema validation: NX-SA-08)
   4. What goes back to the client? (raw rows: NX-SA-04)
   5. What does it capture or call? (closures with secrets: NX-SA-05; outbound fetch to user URLs: NX-RH-05; paid or email APIs without limits: NX-SA-09)
   Follow helper imports one or two levels deep before deciding a check is missing; a DAL function with `verifySession()` counts.

3. **Read every inline `'use server'`.** These sit inside page components that often do their own `auth()` check, which does not protect the action [raw/next--data-security-guide.md]. Confirm the inline body re-checks.

4. **Check the framework-level settings** in next.config: `serverActions.allowedOrigins` (NX-SA-07; `'*'` or `'null'` is a red flag, and `'null'` was a bypass before 16.1.7 [raw/advisory--2026-server-actions.md]), `bodySizeLimit` (NX-SA-08), and `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` handling (NX-SA-06) [raw/next--server-actions-guide-and-config.md].

5. **Read every Route Handler and Pages API route** with the same five questions (NX-RH-01). Skip a missing session check only when the handler is a verified webhook (signature check present), a cron endpoint with a secret bearer check, or intentionally public; write which in `verified_by`.

6. **CSRF on Route Handlers (NX-RH-02).** Route Handlers get no built-in Origin check (none is documented [raw/next--route-handlers.md]). For each state-changing handler that relies on cookies, find the session cookie's `sameSite` value and any Origin, token, or custom-header check. Record the cookie setting in `evidence`.

7. **CORS (NX-RH-03)** and **side effects on GET (NX-RH-04).** Use `route_handlers[].cors_wildcard` and the next.config `headers()` output [raw/next--headers-redirects-config.md].

8. **Custom server and SSRF (NX-RH-05).** If `apps[].deployment_hints.custom_server_files` is not empty, read it for Host handling (CVE-2026-64649). Grep for `fetch(` with request-derived URLs in actions and handlers.

9. **Sweep AI patterns** AI-02, AI-03, AI-05, AI-10, AI-11, AI-13, AI-14, AI-16, AI-17 from [../references/ai-failure-patterns.md](../references/ai-failure-patterns.md).

10. **Count for metrics.** Keep tallies for `nextjs_actions_without_auth`, `nextjs_route_handlers_mutating_without_auth`, and actions reviewed versus total (coverage). Write findings per guide 06; group repeated root causes.

## Sources

[raw/next--data-security-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--data-security-guide.md), [raw/next--server-actions-guide-and-config.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--server-actions-guide-and-config.md), [raw/next--route-handlers.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--route-handlers.md), [raw/next--headers-redirects-config.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--headers-redirects-config.md), [raw/next--use-cache-and-unstable-cache.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--use-cache-and-unstable-cache.md), [raw/advisory--2026-server-actions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-server-actions.md), [raw/next--authentication-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--authentication-guide.md).

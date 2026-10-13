# 04. Auth, routing, and client trust

A React SPA can show or hide anything, but it cannot protect anything: the user controls the browser. This guide pairs every client-side decision with the server-side check that must back it, and covers redirects, cross-window messages, and cross-site requests.

References: [checks-auth-routing.md](../references/checks-auth-routing.md) (AR-01 to AR-06), [advisory-table.md](../references/advisory-table.md) (React Router), [detection-patterns.md](../references/detection-patterns.md), [finding-rules.md](../references/finding-rules.md).

## Procedure

1. **Find the auth model.** Read the login flow: where the session lives (httpOnly cookie, bearer token in memory, token in storage), which library (Auth.js, Clerk, Supabase, WorkOS, custom), and how API requests carry it. Write two lines in notes; later steps depend on it.
2. **Client guards** (AR-01, AR-02): list guarded routes and role checks. For each, list the endpoints, loaders, or Server Functions the page uses. Read those handlers. A handler without its own check is the finding; the guard is context. If the backend is outside the audited paths, put the pair in notes as "Not confirmed" and hand off.
3. **Client-held authority** (AR-02): find decisions made from decoded JWTs, storage values, query params, or client-writable cookies, and check whether the server re-verifies.
4. **Redirects** (AR-03): trace every `next`, `redirect`, `returnTo`, `callbackUrl` parameter to its use in `navigate`, `redirect()` in loaders and actions, `window.location`, `location.assign`, `window.open`. Check for a same-origin or allow-list validator. Note React Router's version and mode, since several advisories (CVE-2026-22029, CVE-2025-68470, CVE-2026-40181, CVE-2026-53669) are redirect bugs inside the router itself; those come from the version script.
5. **postMessage** (AR-04): read every `message` listener: exact origin check against an allow-list, schema check of `data`, no HTML or navigation sinks. Read every `postMessage` call for a `'*'` target with sensitive data.
6. **CSRF** (AR-05): only for cookie sessions. For each state-changing endpoint the app calls (including React Router actions and Server Functions), find the server's defense: Origin or `Sec-Fetch-Site` check, CSRF token, required custom header, and the cookie's `SameSite`. Check CORS: reflecting any origin with credentials enabled is part of the same finding.
7. **Tokens in URLs** (AR-06): grep links and OAuth handling.
8. **Rate and write** per finding-rules.md. Authorization findings rarely reach `confirmed` from client code alone; read the server handler before choosing `likely` or `confirmed`.
9. **Record measures:** guarded routes, guarded routes whose backend lacks a check, message listeners without origin checks, session storage model.

## Handoffs

- Server-side auth logic outside React (Express, Fastify, Django APIs): `polyglot-security-wasp-drone` or the generic pass. Record the client half here and the handoff in notes.
- Security headers (CSP, frame-ancestors, HSTS): generic pass.

## Sources

- [raw/owasp--top10-2025-and-cwe-mapping.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/owasp--top10-2025-and-cwe-mapping.md)
- [raw/owasp--cheatsheet-csrf.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/owasp--cheatsheet-csrf.md)
- [raw/owasp--cheatsheet-html5-security.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/owasp--cheatsheet-html5-security.md)
- [raw/owasp--cheatsheet-xss-dom-xss-redirects.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/owasp--cheatsheet-xss-dom-xss-redirects.md)
- [raw/browser--mdn-postmessage.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/browser--mdn-postmessage.md)
- [raw/router--react-router-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/router--react-router-advisories.md)
- [raw/ai--vibe-coded-apps-security-studies.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/ai--vibe-coded-apps-security-studies.md)

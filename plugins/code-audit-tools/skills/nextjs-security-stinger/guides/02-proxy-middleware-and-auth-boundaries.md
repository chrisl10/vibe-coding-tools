# 02. Middleware, proxy, and auth boundaries

Goal: find where the app decides who may do what, and prove whether that decision can be skipped. Loads [../references/checks-proxy-and-auth-boundaries.md](../references/checks-proxy-and-auth-boundaries.md) (NX-PRX-01 to 05, NX-AUTH-01 to 04).

## Steps

1. **Open every middleware or proxy file** listed in `next-inventory.json.apps[].middleware_proxy[]`. Note: file name (`middleware.ts` or `proxy.ts`), exported function, `config.matcher` (copy it verbatim into notes), and what it does (redirects, rewrites, headers, CSP nonce, auth). On 16.x, `proxy.ts` is the current name and `middleware.ts` is deprecated [raw/next--next-16-release-proxy-rename.md]; if both exist, read both (NX-PRX-05).

2. **Write the boundary map** in `notes-nextjs-security-wasp-drone.md`: for each protected area (for example `/dashboard`, `/admin`, `/api/*`), list (a) the middleware rule that covers it, (b) the page, layout, or handler check, (c) the data function check. This map drives the rest of the audit.

3. **Run NX-PRX-01 (middleware-only auth).** For each protected area, open two or three pages and the Server Actions and Route Handlers they use. If no in-route or DAL check exists, it is a finding. Cite the six bypass advisories in `why_it_matters` in plain words ("Next.js has published several bugs that let requests skip middleware") [raw/advisory--2026-middleware-proxy-bypasses.md].

4. **Run NX-PRX-02 (matcher gaps).** Compare the matcher with the route list (`rg --files -g 'app/**/page.*' -g 'app/**/route.*'`). Remember that Server Actions run as POSTs to the page that uses them, so a path excluded from the matcher also excludes its actions [raw/next--proxy-file-convention.md]. Check for a non-constant matcher (ignored).

5. **Run NX-PRX-03 (unverified session data).** Look for JWT decode without verify and Supabase `getSession()` on the server (`get_session_server_use[]`) [raw/auth--supabase-ssr-nextjs.md].

6. **Run NX-PRX-04 (version bypass preconditions)** against the advisory findings from guide 01, using the boundary map: is middleware the only gate on the affected routes?

7. **Run the auth-library checks for the library found in guide 00:**
   - Clerk: NX-AUTH-01. Bare `clerkMiddleware()` protects nothing; `unsafeMetadata` is browser-writable [raw/auth--clerk-middleware-and-metadata.md].
   - Auth.js: NX-AUTH-02. The `authorized` callback is not enough alone; check `AUTH_SECRET` handling [raw/auth--authjs-protecting-resources.md].
   - Supabase: NX-AUTH-03. Service role key reachable by the browser; `getSession()` trusted on the server. Row Level Security itself is a database concern: read the migration SQL only to rule out IDOR findings, and hand RLS gaps to `security-wasp-drone` in notes unless they are reached through a Next.js action or handler you are reporting.
   - Custom sessions (`jose`, `iron-session`): check the cookie options where the session is set (`httpOnly`, `secure`, `sameSite`, expiry) against the authentication guide [raw/next--authentication-guide.md]. Missing `httpOnly` on a session cookie: `medium` (CWE-1004); missing `secure`: `medium` (CWE-614); `sameSite: 'none'`: feeds NX-RH-02.

8. **Run NX-AUTH-04 (layout-only checks)** on every `layout.tsx` that contains an auth call or `return null` [raw/next--authentication-guide.md].

9. **Sweep AI patterns** AI-01, AI-07, AI-08, AI-09, AI-17 from [../references/ai-failure-patterns.md](../references/ai-failure-patterns.md).

10. **Write findings** per guide 06. One finding per root cause: if 12 admin pages all rely on the same middleware rule with no in-route check, write one NX-PRX-01 finding listing the locations (up to about 10, then say how many more in `evidence`).

## Sources

[raw/advisory--2026-middleware-proxy-bypasses.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-middleware-proxy-bypasses.md), [raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md), [raw/next--proxy-file-convention.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--proxy-file-convention.md), [raw/next--next-16-release-proxy-rename.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--next-16-release-proxy-rename.md), [raw/next--authentication-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--authentication-guide.md), [raw/auth--clerk-middleware-and-metadata.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--clerk-middleware-and-metadata.md), [raw/auth--authjs-protecting-resources.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--authjs-protecting-resources.md), [raw/auth--supabase-ssr-nextjs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--supabase-ssr-nextjs.md), [raw/standard--cwe-entries.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/standard--cwe-entries.md).

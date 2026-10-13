# Checks: middleware, proxy, and auth boundaries

Loaded by [guides/02-proxy-middleware-and-auth-boundaries.md](../guides/02-proxy-middleware-and-auth-boundaries.md). Every check lists detection, how to confirm or rule out a false positive, severity guidance mapped to the contract (section 7 of the audit contract), a vulnerable and fixed pair, and refs.

Run all ripgrep commands from the audited repo root, read-only. `rg` flags used: `-n` line numbers, `-g` globs, `--pcre2` when lookarounds are needed. If `rg` is missing, use `grep -rnE` with the same pattern.

---

## NX-PRX-01: Authorization lives only in middleware or proxy

**What.** The app decides who may see a page or call an endpoint only in `middleware.ts` or `proxy.ts`. Pages, Server Actions, Route Handlers, and data functions trust that the request already passed.

**Why it is a finding on its own, independent of version.** Between March 2025 and July 2026 at least six separate framework bugs let requests skip middleware: CVE-2025-29927 (`x-middleware-subrequest` header), CVE-2026-44573 (Pages Router i18n `_next/data`), CVE-2026-44574 (dynamic route param injection), CVE-2026-44575 and CVE-2026-45109 (segment prefetch `.rsc` variants), CVE-2026-64642 (Turbopack with a single locale). Every advisory's workaround is the same: do the check in the route or data path [raw/advisory--2026-middleware-proxy-bypasses.md]. The Next.js docs say Proxy "should not be your only line of defense" [raw/next--authentication-guide.md], and Clerk and Auth.js say the same for their middleware [raw/auth--clerk-middleware-and-metadata.md] [raw/auth--authjs-protecting-resources.md].

**Detection.**
```bash
rg -n -g 'middleware.{ts,js,mjs}' -g 'proxy.{ts,js,mjs}' -g 'src/middleware.*' -g 'src/proxy.*' -e 'redirect|NextResponse\.(redirect|rewrite)|auth|session|token|role' .
# Pages and data functions under the protected prefix that never check the session:
rg -L -n -g 'app/**/page.{tsx,jsx,ts,js}' -e 'auth\(|getServerSession|currentUser\(|verifySession|getUser\(|getClaims\(|requireUser|redirect\(' app src/app 2>/dev/null
```
Use the scan inventory: `apps[].middleware_proxy[]` (matcher, `auth_call_seen`), and compare with `use_server_files[].actions[].auth_call_seen` and `route_handlers[].auth_call_seen`.

**Confirm.** Pick two or three protected routes from the matcher. Read each page or layout, the data function it calls, and any Server Action it renders. Confirmed when none of them verifies the session or role. False positive when a DAL function (for example `verifySession()` or `getCurrentUser()` marked `server-only`) is called on every data path, even if the page body does not call it directly.

**Severity.** `high` when protected content or mutations depend only on middleware (contract example "Server Action without an auth check" is high). Raise to `critical` when the installed version is inside CVE-2025-29927's range or another bypass range whose preconditions are met (anyone can bypass with one header or URL). `medium` when the middleware is the only gate but the protected pages show no private data (for example a paywall teaser).

**Vulnerable.**
```ts
// proxy.ts
export function proxy(req: NextRequest) {
  if (!req.cookies.get('session')) return NextResponse.redirect(new URL('/login', req.url))
}
export const config = { matcher: ['/dashboard/:path*'] }

// app/dashboard/invoices/page.tsx  (no check here)
export default async function Page() {
  const invoices = await db.invoice.findMany()
  return <InvoiceList invoices={invoices} />
}
```
**Fixed.**
```ts
// lib/dal.ts
import 'server-only'
export const verifySession = cache(async () => {
  const session = await decrypt((await cookies()).get('session')?.value)
  if (!session?.userId) redirect('/login')
  return { userId: session.userId }
})
// app/dashboard/invoices/page.tsx
export default async function Page() {
  const { userId } = await verifySession()
  const invoices = await db.invoice.findMany({ where: { ownerId: userId } })
  return <InvoiceList invoices={invoices} />
}
```
**Refs.** CWE-288, CWE-285, CWE-862, OWASP A01:2025, CVE-2025-29927, CVE-2026-44573, CVE-2026-44574, CVE-2026-44575, CVE-2026-45109, CVE-2026-64642.

---

## NX-PRX-02: Matcher gaps (protected paths, API routes, or Server Action pages not covered)

**What.** The matcher excludes paths that hold private data, or excludes `api`, while the app relies on middleware for those paths. Server Functions are POSTs to the page that uses them, so "a Proxy matcher that excludes a path will also skip Server Function calls on that path" [raw/next--proxy-file-convention.md].

**Detection.** Read the `matcher` value from the inventory. Then list routes:
```bash
rg --files -g 'app/**/page.*' -g 'app/**/route.*' -g 'src/app/**/page.*' -g 'src/app/**/route.*' -g 'pages/**' .
rg -n "matcher" -g 'middleware.*' -g 'proxy.*' .
```
Matchers must be constants; a matcher built from a variable is ignored [raw/next--proxy-file-convention.md]:
```bash
rg -n --pcre2 'matcher\s*:\s*(?!\[|["\x27])' -g 'middleware.*' -g 'proxy.*' .
```

**Confirm.** For each route that renders private data or performs mutations, decide whether the matcher covers it (remember `source` patterns are anchored at the start). Confirmed when a sensitive route is outside the matcher and has no in-route check. False positive when the route has its own check (then it is not a gap, only a style choice).

**Severity.** Same scale as NX-PRX-01 for the uncovered route. A matcher that is a variable (ignored) is `high` if the app relies on it.

**Vulnerable.** `export const config = { matcher: ['/((?!api|_next/static|_next/image).*)'] }` with `app/api/admin/users/route.ts` that has no session check.
**Fixed.** Keep the matcher for optimistic redirects, and add `const s = await verifySession(); if (s.role !== 'admin') return new Response(null, { status: 403 })` inside the route handler.

**Refs.** CWE-862, CWE-288, OWASP A01:2025.

---

## NX-PRX-03: Database or expensive checks in middleware, or trusting unverified session data there

**What.** The docs say Proxy runs on every route including prefetches and should only do optimistic cookie checks, not database checks [raw/next--authentication-guide.md]. The opposite mistake also appears: decoding a JWT in middleware without verifying the signature, or calling Supabase `getSession()` in server code, which "reads the session out of the cookie without revalidating it" [raw/auth--supabase-ssr-nextjs.md].

**Detection.**
```bash
rg -n -e 'jwtDecode|jwt_decode|decodeJwt|atob\(|JSON\.parse\(.*split\(' -g 'middleware.*' -g 'proxy.*' -g 'lib/**' -g 'src/lib/**' .
rg -n 'auth\.getSession\(' -g '!**/*.client.*' .
```
Inventory: `get_session_server_use[]`.

**Confirm.** Read the function. Confirmed when the token payload is used for an allow decision without `jwtVerify`, `getClaims()`, `getUser()`, or the auth library's own verifying call. False positive when the decode is only used for UI hints and the real check happens server-side later.

**Severity.** `high` when a forged cookie would pass the check and reach private data or mutations. `medium` when it only controls redirects and a verified check exists downstream.

**Vulnerable.**
```ts
const { data: { session } } = await supabase.auth.getSession()
if (session?.user.app_metadata.role === 'admin') return adminData()
```
**Fixed.**
```ts
const { data, error } = await supabase.auth.getClaims()
if (error || data?.claims.app_metadata?.role !== 'admin') return new Response(null, { status: 403 })
```
**Refs.** CWE-345, CWE-565, OWASP A07:2025.

---

## NX-PRX-04: Middleware on a version inside a bypass advisory range

**What.** Version plus presence of middleware or proxy. The scan script writes these findings automatically from `next-advisories.json`; this check is how the Drone confirms the preconditions.

**Confirm per advisory.**
- CVE-2025-29927: any middleware doing auth on `< 15.2.3` (15.x), `< 14.2.25`, `< 13.5.9`, `< 12.3.5`. Vercel-hosted deployments were protected automatically; self-hosted and other platforms were not [raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md]. Check for an upstream rule that strips `x-middleware-subrequest` (nginx, Cloudflare) before lowering severity.
- CVE-2026-44573: Pages Router plus `i18n` in next.config.
- CVE-2026-44574: middleware protects dynamic `[param]` routes.
- CVE-2026-44575 and CVE-2026-45109: App Router, 15.2.0 and later.
- CVE-2026-64642: 16.x, App Router, Turbopack production build (default in 16 unless `next build --webpack`) [raw/next--next-16-release-proxy-rename.md], exactly one locale.

**Severity.** Keep the advisory severity when preconditions are confirmed and middleware is the only gate (NX-PRX-01 true). Lower one step when an in-route check also exists (the bypass then reaches a second gate), and say so in `verified_by`.

**Refs.** As listed per advisory in [advisory-table.md](advisory-table.md).

---

## NX-PRX-05: `middleware.ts` on Next.js 16 (deprecated name) or both files present

**What.** In 16.x `middleware.ts` is deprecated in favor of `proxy.ts` and kept only for Edge runtime use [raw/next--next-16-release-proxy-rename.md] [raw/next--proxy-file-convention.md]. Not a vulnerability by itself.

**Detection.** Inventory `apps[].middleware_proxy[].kind` with `resolved_versions` 16.x.

**Severity.** `info`, or `low` when both `middleware.ts` and `proxy.ts` exist (reviewers may audit the wrong file). Never above low.

**Refs.** OWASP A02:2025.

---

## NX-AUTH-01: Clerk `clerkMiddleware()` with no protection, or role checks on `unsafeMetadata`

**What.** `clerkMiddleware()` protects nothing by default, and Clerk now recommends protecting "as close to the resource as possible"; at fetch time the docs mark `createRouteMatcher` deprecated [raw/auth--clerk-middleware-and-metadata.md]. `unsafeMetadata` is writable from the browser, so a role stored there is attacker-controlled.

**Detection.**
```bash
rg -n -e 'clerkMiddleware\(\s*\)' -e 'createRouteMatcher' -e 'auth\.protect\(' -e 'unsafeMetadata' .
```
**Confirm.** Bare `clerkMiddleware()` plus pages and actions with no `auth()` or `currentUser()` check: same as NX-PRX-01. For `unsafeMetadata`, confirm it feeds an allow decision (`if (user.unsafeMetadata.role === 'admin')`).

**Severity.** `unsafeMetadata` role check that gates admin data or actions: `high` (any signed-in user can call `user.update({ unsafeMetadata: { role: 'admin' } })`). Bare middleware with in-route checks: `info`.

**Vulnerable.** `if (user.unsafeMetadata.role === 'admin') { await deleteAllUsers() }`
**Fixed.** Set roles on the server into `publicMetadata` (read-only for the browser) or `privateMetadata`, and check them server-side: `const { sessionClaims } = await auth(); if (sessionClaims?.metadata?.role !== 'admin') return forbidden()` (the claim name depends on the session token template; confirm in the app's Clerk config).

**Refs.** CWE-602, CWE-639, OWASP A01:2025.

---

## NX-AUTH-02: Auth.js (NextAuth) protecting only through the `authorized` callback

**What.** Auth.js says "You should not rely on the proxy exclusively for authorization" [raw/auth--authjs-protecting-resources.md].

**Detection.**
```bash
rg -n -e 'authorized\s*\(' -e 'export\s*\{\s*auth\s+as\s+(middleware|proxy)' -e 'export\s+default\s+auth' -g 'middleware.*' -g 'proxy.*' -g 'auth.{ts,js}' -g 'src/auth.*' .
rg -n -e 'AUTH_SECRET|NEXTAUTH_SECRET' -g '.env*' -g '!*.example' .
```
**Confirm.** As NX-PRX-01. For secrets: a real secret committed in a tracked `.env` file (check `git ls-files` output, read-only) is a separate finding, redact to first 4 characters.

**Severity.** As NX-PRX-01. Committed `AUTH_SECRET` in a tracked file: `critical` (anyone with repo access can forge sessions) when the value is not an obvious placeholder.

**Refs.** CWE-862, CWE-798, OWASP A01:2025, OWASP A07:2025.

---

## NX-AUTH-03: Supabase service role key reachable by the browser, or `getSession()` trusted on the server

**What.** The Supabase Next.js guide uses only the publishable key in the browser and never the service role key; `getSession()` must not be trusted in server code [raw/auth--supabase-ssr-nextjs.md]. Any `NEXT_PUBLIC_` value is inlined into the client bundle at build time [raw/next--source-maps-powered-by-env-vars.md].

**Detection.**
```bash
rg -n -e 'NEXT_PUBLIC_[A-Z0-9_]*SERVICE_ROLE' -e 'SERVICE_ROLE' .
rg -n -l "^['\"]use client['\"]" -g '*.{ts,tsx,js,jsx}' . | xargs rg -n 'SERVICE_ROLE|createClient\(' 2>/dev/null
```
Inventory: `service_role_refs[]`, `suspicious_next_public_names[]`.

**Confirm.** `NEXT_PUBLIC_*SERVICE_ROLE*` defined in any env file or referenced in code is confirmed by itself (the prefix forces it into the bundle). A non-public `SUPABASE_SERVICE_ROLE_KEY` read in a `'use client'` file evaluates to undefined in the browser, so it is a bug, not a leak; record it in notes unless the file is also imported server-side and passes the key down.

**Severity.** Service role key in the client bundle: `critical` (it bypasses Row Level Security for every table). `getSession()` used for an allow decision in server code: `high`.

**Vulnerable.** `createClient(url, process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!)` in `components/admin-table.tsx`.
**Fixed.** Move admin queries into a `server-only` module that reads `process.env.SUPABASE_SERVICE_ROLE_KEY` (no prefix), called from a Server Action that first checks the caller's role; rotate the leaked key in the Supabase dashboard.

**Refs.** CWE-798, CWE-200, OWASP A01:2025, OWASP A04:2025.

---

## NX-AUTH-04: Layout-only auth checks or `return null` gating

**What.** Layouts do not re-render on navigation and do not stop nested segments from running or appearing in the RSC payload; returning `null` in a layout "is not recommended" [raw/next--authentication-guide.md].

**Detection.**
```bash
rg -n -g 'app/**/layout.{tsx,jsx}' -g 'src/app/**/layout.{tsx,jsx}' -e 'return null' -e 'auth\(|getServerSession|currentUser\(|verifySession' .
```
**Confirm.** A layout performs the only check for a segment whose pages fetch private data without their own check. False positive when the pages call a DAL that checks.

**Severity.** `high` when private data is fetched in child pages with no other check, `medium` when children only render UI shells.

**Vulnerable.** `app/admin/layout.tsx`: `if (session?.role !== 'admin') return null; return children` with `app/admin/users/page.tsx` calling `db.user.findMany()`.
**Fixed.** Call `await requireAdmin()` from the DAL inside `getUsers()` itself.

**Refs.** CWE-862, OWASP A01:2025.

---

Sources: [raw/advisory--2026-middleware-proxy-bypasses.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-middleware-proxy-bypasses.md), [raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md), [raw/next--proxy-file-convention.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--proxy-file-convention.md), [raw/next--authentication-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--authentication-guide.md), [raw/next--next-16-release-proxy-rename.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--next-16-release-proxy-rename.md), [raw/auth--clerk-middleware-and-metadata.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--clerk-middleware-and-metadata.md), [raw/auth--authjs-protecting-resources.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--authjs-protecting-resources.md), [raw/auth--supabase-ssr-nextjs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--supabase-ssr-nextjs.md), [raw/next--source-maps-powered-by-env-vars.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--source-maps-powered-by-env-vars.md), [raw/standard--cwe-entries.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/standard--cwe-entries.md), [raw/standard--owasp-top-10-2025.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/standard--owasp-top-10-2025.md).

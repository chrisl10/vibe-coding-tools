# Checks: Server Actions and Route Handlers

Loaded by [guides/03-server-actions-and-route-handlers.md](../guides/03-server-actions-and-route-handlers.md). Start from the scan inventory (`use_server_files[]`, `inline_use_server[]`, `route_handlers[]`, `pages_api_routes[]`). The inventory's `auth_call_seen`, `validation_seen`, and `touches_db` flags are regex hints; every finding needs a manual read.

Core fact for every check here: "A Server Action runs as a POST request against the page that invokes it ... the route is reachable to anyone who can send the same POST. Treat every action as an untrusted entry point." [raw/next--server-actions-guide-and-config.md]. Action IDs can also be disclosed to unauthenticated users through public client chunks (CVE-2026-64643), so an unguessable ID is not protection [raw/advisory--2026-server-actions.md].

---

## NX-SA-01: Server Action with no authentication check

**Detection.**
```bash
rg -n -l "^\s*['\"]use server['\"]" -g '*.{ts,tsx,js,jsx}' .          # file-level actions
rg -n "['\"]use server['\"]" -g '*.{tsx,jsx}' .                          # inline actions in components
```
Inventory: `use_server_files[].actions[]` with `auth_call_seen: false`; `inline_use_server[]` with `auth_call_seen_in_file: false`.

**Confirm.** Read the action body and every helper it calls. Confirmed when no path verifies the session before reading or changing data. Rule out: the action delegates to a DAL function that calls `verifySession()` or the auth library (follow the import), or the action is intentionally public (newsletter signup, contact form) and only writes non-sensitive data. A page-level check does not count: "A page-level authentication check does not extend to the Server Actions defined within it." [raw/next--data-security-guide.md].

**Severity.** `high` when the action reads private data or mutates anything owned by a user (contract example). `critical` when it deletes or exports data at scale, changes roles or billing, or sends email or money without any check. `low` or no finding for an intentionally public action, but check rate limiting (NX-SA-06).

**Vulnerable.**
```ts
'use server'
export async function deleteProject(id: string) {
  await db.project.delete({ where: { id } })
}
```
**Fixed.**
```ts
'use server'
import { verifySession } from '@/lib/dal'
export async function deleteProject(id: string) {
  const { userId } = await verifySession()
  const res = await db.project.deleteMany({ where: { id, ownerId: userId } })
  if (res.count === 0) throw new Error('Not found')
}
```
**Refs.** CWE-862, OWASP A01:2025.

---

## NX-SA-02: Server Action checks login but not ownership (IDOR)

**What.** "Beyond authentication ... remember to check authorization (does this user have permission to act on this specific resource?)" [raw/next--data-security-guide.md]. Schema validation "only checks the shape of the input" [raw/next--server-actions-guide-and-config.md].

**Detection.** Actions with `auth_call_seen: true` whose DB call uses an id from arguments without an owner or tenant filter:
```bash
rg -n -U --pcre2 "where:\s*\{\s*id(\s*:\s*\w+)?\s*\}" -g '*.{ts,tsx,js}' .
rg -n -e "\.eq\(['\"]id['\"]" -e "findUnique\(\{\s*where:\s*\{\s*id" .
```
**Confirm.** Read the action. Confirmed when the record is looked up or changed by a client-supplied id and no comparison with `session.user.id`, org id, or role happens before the write. Rule out: Supabase RLS policies that scope rows to `auth.uid()` (read the migration SQL), or a DAL function that adds the owner filter.

**Severity.** `high` by default; `critical` when ids are sequential or listable and the data is personal, financial, or health data.

**Vulnerable.**
```ts
export async function completeItemUnsafe(item: Item) {
  await db.item.update({ where: { id: item.id }, data: { completed: true } })
}
```
**Fixed.**
```ts
export async function completeItem(itemId: string) {
  const session = await auth(); if (!session?.user) return
  const item = await db.item.findFirst({ where: { id: itemId, ownerId: session.user.id } })
  if (!item) return
  await db.item.update({ where: { id: item.id }, data: { completed: true } })
}
```
(Pair taken from the Next.js Server Actions guide [raw/next--server-actions-guide-and-config.md].)

**Refs.** CWE-639, CWE-863, OWASP A01:2025.

---

## NX-SA-03: Server Action trusts client-supplied objects, roles, or ids (mass assignment)

**Detection.**
```bash
rg -n -U --pcre2 "data:\s*(formData|input|data|values|body|params|Object\.fromEntries\(formData\))\b" -g '*.{ts,tsx,js}' .
rg -n -e "formData\.get\(['\"](role|isAdmin|userId|ownerId|price|amount|plan)['\"]" .
```
**Confirm.** The action passes a client object straight into `create`/`update`, or reads authority fields (`role`, `userId`, `price`) from the request instead of the session or server data.

**Severity.** `high` when a user can change role, owner, price, or plan; `medium` when only harmless extra columns could be set.

**Vulnerable.** `await db.user.update({ where: { id: session.user.id }, data: Object.fromEntries(formData) })`
**Fixed.** `const { name } = z.object({ name: z.string().min(1).max(80) }).parse({ name: formData.get('name') }); await db.user.update({ where: { id: session.user.id }, data: { name } })`

**Refs.** CWE-915, CWE-20, OWASP A01:2025.

---

## NX-SA-04: Server Action returns raw database records

**What.** Return values are serialized to the client; "Only return what the UI needs, not raw database records." [raw/next--data-security-guide.md].

**Detection.** Inventory `actions[].returns_db_call: true`, plus:
```bash
rg -n -e "return\s+(await\s+)?(prisma|db|drizzle|supabase)\b" -e "return\s+\{\s*\.\.\.(user|record|row)" .
```
**Confirm.** Read the model or select. Confirmed when the returned row includes fields such as password hash, tokens, internal flags, other users' emails.

**Severity.** `high` when secrets or password hashes are returned; `medium` for other private fields; `low` when the record has no sensitive columns (still note it).

**Vulnerable.** `return db.user.update({ where: { id }, data: { name } })`
**Fixed.** `await db.user.update(...); return { success: true }`

**Refs.** CWE-201, CWE-200, OWASP A01:2025.

---

## NX-SA-05: Secrets or private values captured in inline Server Action closures

**What.** Variables captured by an inline action are encrypted and sent to the client and back; "We don't recommend relying on encryption alone" [raw/next--data-security-guide.md].

**Detection.** Inventory `inline_use_server[]`, then read each. Look for captured tokens, API keys, full user rows, or pricing data defined in the component scope above the inline `'use server'`.

**Confirm.** The captured variable holds a secret or private value. Rule out captured ids or version numbers that are already public.

**Severity.** `medium` (encrypted in transit but shipped to the browser; also changes if the encryption key leaks). `high` if `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` is committed to the repo.

**Fixed.** Re-read the secret on the server inside the action instead of capturing it.

**Refs.** CWE-200, OWASP A04:2025.

---

## NX-SA-06: `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` handling

**What.** Needed when self-hosting across multiple instances; base64 value decoding to 16, 24, or 32 bytes [raw/next--data-security-guide.md] [raw/next--server-actions-guide-and-config.md].

**Detection.**
```bash
rg -n "NEXT_SERVER_ACTIONS_ENCRYPTION_KEY" .
git -C . ls-files | rg '(^|/)\.env' 
```
**Confirm.** A real value in a tracked file (redact to 4 characters). Missing key on a multi-instance self-hosted deployment is a reliability issue, not security; note only.

**Severity.** Committed key: `high`. Missing key: no finding (notes).

**Refs.** CWE-798, CWE-540, OWASP A04:2025.

---

## NX-SA-07: CSRF on Server Actions: `allowedOrigins` too broad, `'null'` allowlisted, or vulnerable version

**What.** Next.js compares `Origin` with `Host` or `X-Forwarded-Host` and rejects mismatches; `allowedOrigins` adds extra trusted origins [raw/next--data-security-guide.md]. Before 16.1.7, `Origin: null` (sandboxed iframes) bypassed the check on 16.0.1 and later (CVE-2026-27978) [raw/advisory--2026-server-actions.md].

**Detection.** Inventory `next_config.server_actions_allowed_origins`, and:
```bash
rg -n -U "allowedOrigins\s*:\s*\[[^\]]*\]" -g 'next.config.*' .
```
**Confirm.** Flag entries `'*'`, `'null'`, broad wildcards over domains the app does not control (`*.vercel.app`, `*.netlify.app`, `*.ngrok.io`), or `http://` origins.

**Severity.** `'*'` or `'null'` allowlisted with cookie-based sessions: `high`. Shared-hosting wildcard: `medium`. Version in CVE-2026-27978 range with Server Actions and cookie auth: `medium` (matches the advisory; contract example "Missing CSRF origin check behind SameSite=Lax" is medium).

**Vulnerable.** `serverActions: { allowedOrigins: ['*'] }`
**Fixed.** `serverActions: { allowedOrigins: ['admin.example.com'] }` (only the real proxy or CDN hostnames), upgrade to 16.1.7 or later.

**Refs.** CWE-352, CVE-2026-27978, OWASP A01:2025.

---

## NX-SA-08: Missing input validation and limits in actions

**Detection.** Inventory `actions[].validation_seen: false` on actions that write. Also `bodySizeLimit` raised far above need:
```bash
rg -n "bodySizeLimit" -g 'next.config.*' .
```
**Confirm.** Read the action: `formData.get()` values flow into queries, file paths, URLs, or `fetch()` without schema checks.

**Severity.** Feeds a raw SQL string, shell, file path, or outbound `fetch` URL: `high` (injection, path traversal, SSRF). Feeds an ORM call: `low` to `medium`. `bodySizeLimit` above 10 MB without a reason: `low`.

**Vulnerable.** ``await sql.unsafe(`SELECT * FROM t WHERE name = '${formData.get('q')}'`)``
**Fixed.** ``const q = z.string().max(100).parse(formData.get('q')); await sql`SELECT * FROM t WHERE name = ${q}` ``

**Refs.** CWE-20, OWASP A05:2025. (SQL injection itself is also covered by the generic security pass.)

---

## NX-SA-09: Expensive or abusable actions with no rate limiting

**What.** The data security guide recommends rate limiting for expensive operations such as sending email [raw/next--data-security-guide.md].

**Detection.**
```bash
rg -n -l "['\"]use server['\"]" . | xargs rg -n -e 'resend|sendgrid|nodemailer|sendEmail|twilio|openai|anthropic|stripe\.' 2>/dev/null
rg -n -e 'ratelimit|rateLimit|Ratelimit|upstash' .
```
**Severity.** Unauthenticated action that sends email or SMS or calls a paid AI API with no limit: `medium` (cost abuse, spam relay). Authenticated: `low`.

**Refs.** CWE-770, OWASP A06:2025.

---

## NX-RH-01: Route Handler or Pages API route that mutates without authentication

**What.** "Treat Route Handlers with the same security considerations as public-facing API endpoints" [raw/next--authentication-guide.md].

**Detection.** Inventory `route_handlers[]` with POST, PUT, PATCH, or DELETE and `auth_call_seen: false`, `webhook_signature_seen: false`; `pages_api_routes[]` with `auth_call_seen: false`.
```bash
rg -n "export\s+(async\s+)?(function|const)\s+(POST|PUT|PATCH|DELETE)" -g '**/route.{ts,js}' .
```
**Confirm.** Read the handler. Rule out webhooks that verify a signature (`stripe.webhooks.constructEvent`, Svix), cron endpoints that check a bearer secret, and intentionally public endpoints.

**Severity.** Same scale as NX-SA-01.

**Vulnerable.**
```ts
export async function POST(req: Request) {
  const body = await req.json()
  return Response.json(await prisma.post.create({ data: body }))
}
```
**Fixed.**
```ts
export async function POST(req: Request) {
  const session = await verifySession()
  if (!session) return new Response(null, { status: 401 })
  const { title } = PostSchema.parse(await req.json())
  const post = await prisma.post.create({ data: { title, authorId: session.userId }, select: { id: true } })
  return Response.json(post)
}
```
**Refs.** CWE-862, OWASP A01:2025.

---

## NX-RH-02: Cookie-authenticated Route Handlers with no CSRF defense

**What.** Server Actions get a built-in Origin check; Route Handlers do not (nothing in the `route.js` reference describes one) [raw/next--route-handlers.md]. A POST, PUT, PATCH, or DELETE handler that authenticates with cookies needs its own defense: `SameSite=Lax` or `Strict` session cookie plus an Origin or `Sec-Fetch-Site` check, a CSRF token, or a non-cookie bearer token.

**Detection.** Inventory `route_handlers[]` with `reads_cookies: true` (or the auth library reads cookies) and `origin_check_seen: false`. Read the cookie options where the session is set:
```bash
rg -n -e "sameSite\s*:\s*['\"]none" -e "SameSite=None" -e "cookies\(\)\.set\(" -e "cookieStore\.set\(" .
```
**Confirm.** The handler changes state, is reached with cookies, and has no Origin, token, or custom-header check. Note the SameSite value of the session cookie in `evidence`.

**Severity.** `SameSite=None` session cookie plus a state-changing cookie-authenticated handler with no check: `high`. Default or `Lax` cookie with no Origin check: `medium` (contract example). Form-encoded or `text/plain` bodies accepted (no preflight) raise likelihood; JSON-only handlers that reject other content types lower it, mention which in `verified_by`.

**Fixed.**
```ts
export async function POST(req: Request) {
  const origin = req.headers.get('origin')
  if (origin !== process.env.APP_ORIGIN) return new Response(null, { status: 403 })
  // ...
}
```
**Refs.** CWE-352, CWE-1275, OWASP A01:2025.

---

## NX-RH-03: CORS wildcard on authenticated Route Handlers

**Detection.** Inventory `route_handlers[].cors_wildcard: true`, next.config `headers()` setting `Access-Control-Allow-Origin` on `/api/:path*` [raw/next--headers-redirects-config.md]:
```bash
rg -n -e "Access-Control-Allow-Origin" -e "Access-Control-Allow-Credentials" .
```
**Confirm.** `*` on handlers that return private data with bearer tokens in headers, or origin reflection (`req.headers.get('origin')` echoed) together with `Access-Control-Allow-Credentials: true`.

**Severity.** Origin reflection with credentials: `high`. `*` on endpoints that read cookies: browsers will not send credentials with `*`, so usually `low`, but `medium` if the handler accepts a token from query string.

**Refs.** CWE-693, OWASP A02:2025.

---

## NX-RH-04: GET handlers or render paths with side effects

**What.** "Mutations ... should never be a side-effect" of rendering; Next.js uses POST for mutations to reduce CSRF risk [raw/next--data-security-guide.md].

**Detection.**
```bash
rg -n -U --pcre2 "export\s+(async\s+)?function\s+GET[\s\S]{0,800}?\.(delete|update|create|insert|upsert)\(" -g '**/route.{ts,js}' .
rg -n -e "searchParams\.\w*(logout|delete|remove)" -g 'app/**/page.*' .
```
**Severity.** State-changing GET reachable with cookies: `medium` (any `<img src>` on another site triggers it). Logout via GET: `low`.

**Refs.** CWE-352, OWASP A01:2025.

---

## NX-RH-05: SSRF in Server Actions or Route Handlers that fetch user-supplied URLs, and host-header trust on custom servers

**What.** CVE-2026-64649: Server Actions that forward or redirect can be steered to attacker hosts when the Host header is not pinned (custom servers) [raw/advisory--2026-server-actions.md]. Independently of version, any handler that does `fetch(userUrl)` is an SSRF candidate.

**Detection.**
```bash
rg -n -e "fetch\(\s*(url|target|href|src|body\.\w+|formData\.get|searchParams\.get|req\.nextUrl\.searchParams\.get)" .
rg -n -e "createServer\(" -e "next\(\{" -g 'server.{js,ts,mjs}' .
rg -n -e "x-forwarded-host|headers\(\)\.get\(['\"]host" .
```
**Confirm.** User input reaches the URL or hostname with no allowlist. For custom servers, check whether the proxy pins `Host` and whether `__NEXT_PRIVATE_ORIGIN` is set (14.2+ workaround named in the advisory).

**Severity.** User-controlled outbound fetch on a server that can reach cloud metadata or internal services: `high` (contract example "SSRF in an image proxy" is high). Custom server on a vulnerable version: as per the advisory (high) when Host is not pinned.

**Vulnerable.** `const r = await fetch(formData.get('url') as string)`
**Fixed.** Parse with `new URL()`, require `https:`, compare `hostname` against an allowlist, resolve DNS and block private ranges, or route through a vetted fetch proxy.

**Refs.** CWE-918, CVE-2026-64649, OWASP A01:2025.

---

Sources: raw/next--server-actions-guide-and-config.md, raw/next--data-security-guide.md, raw/next--authentication-guide.md, raw/next--route-handlers.md, raw/next--headers-redirects-config.md, raw/advisory--2026-server-actions.md, raw/standard--cwe-entries.md, raw/standard--owasp-top-10-2025.md.

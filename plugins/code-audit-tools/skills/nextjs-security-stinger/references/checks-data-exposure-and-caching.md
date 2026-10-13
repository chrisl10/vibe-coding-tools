# Checks: data exposure and caching

Loaded by [guides/04-data-exposure-and-caching.md](../guides/04-data-exposure-and-caching.md). Inventory fields used: `use_client_files[]`, `client_files_reading_private_env[]`, `client_files_importing_db[]`, `next_public_vars`, `suspicious_next_public_names[]`, `hardcoded_secret_candidates[]`, `use_cache[]`, `unstable_cache[]`, `generate_static_params_files[]`, `taint_api_uses[]`, `server_only_imports`.

---

## NX-DATA-01: Full database records passed from Server Components to Client Components

**What.** Props passed to a `'use client'` component are serialized into the page payload. The Next.js docs mark passing a full `userData` row to a client `Profile` as "EXPOSED" [raw/next--data-security-guide.md].

**Detection.**
```bash
# Client components with broad object props
rg -n -l "^['\"]use client['\"]" -g '*.{tsx,jsx}' . | xargs rg -n -e "\{\s*(user|profile|account|customer|order|record|data)\s*\}\s*:\s*\{\s*\w+\s*:\s*(User|Profile|Account|Customer|any)\b"
# Server pages that query and pass the whole row
rg -n -U --pcre2 "(findUnique|findFirst|findMany|select\(\)|from\(['\"]\w+['\"]\)\.select\(\s*['\"]\*)[\s\S]{0,400}?<\w+\s+\w+=\{\w+\}" -g 'app/**/page.{tsx,jsx}' .
```
**Confirm.** Follow one page: query (which columns), then the prop, then the client component. Confirmed when the query selects all columns of a table that holds sensitive fields (password hash, tokens, email of other users, internal notes) and passes the object. Proof that is easy to show: view the page source or the RSC payload (`self.__next_f.push`) in a local build, if allowed. Rule out: the query uses `select`/`columns` to pick safe fields, or a DTO function shapes the object.

**Severity.** Password hashes, tokens, or other users' personal data reach the browser: `high`; at scale (lists of users) `critical`. Own-account extra fields only: `low` to `medium`.

**Vulnerable.**
```tsx
const user = await db.user.findUnique({ where: { id } })   // includes passwordHash, resetToken
return <Profile user={user} />                             // Profile is 'use client'
```
**Fixed.**
```tsx
const user = await db.user.findUnique({ where: { id }, select: { name: true, avatarUrl: true } })
return <Profile user={user} />
```
**Refs.** CWE-200, CWE-359, OWASP A01:2025.

---

## NX-DATA-02: Server-only modules without `server-only`, or DB and secrets imported from client files

**What.** `import 'server-only'` turns accidental client imports into build errors; the docs recommend it for the DAL and say only the DAL should read `process.env` [raw/next--data-security-guide.md].

**Detection.** Inventory `client_files_importing_db[]`, `client_files_reading_private_env[]`, `server_only_imports` (count). Plus:
```bash
rg -n -L "import ['\"]server-only['\"]" -g 'lib/**/*.{ts,js}' -g 'src/lib/**/*.{ts,js}' -g 'data/**' -g 'server/**' . | head -50
```
**Confirm.** A `'use client'` file (or a file imported by one) imports the DB client or reads a non-public env var. Non-public env vars are undefined in the browser, so the usual real-world effect is a broken feature or a developer "fix" that renames the variable to `NEXT_PUBLIC_` (check git history read-only with `git log -S`). A DAL module without `server-only` is a hardening gap, not a leak.

**Severity.** DB credentials or a secret actually reachable in the client bundle (via `NEXT_PUBLIC_` or a hardcoded literal): `critical`. DB client imported in client code: `medium` (build may bundle connection logic and the pattern invites leaks). Missing `server-only` on the DAL: `low`.

**Refs.** CWE-200, CWE-540, OWASP A02:2025.

---

## NX-DATA-03: Secrets in `NEXT_PUBLIC_` variables or hardcoded in source

**What.** `NEXT_PUBLIC_` values are inlined at build time "into any JavaScript sent to the browser" [raw/next--source-maps-powered-by-env-vars.md]. Vendor scans of vibe-coded apps commonly find keys compiled into Next.js bundles [raw/ai--vendor-scans-of-vibe-coded-apps-2026.md].

**Detection.** Inventory `suspicious_next_public_names[]`, `hardcoded_secret_candidates[]`, and:
```bash
rg -n -o -e "NEXT_PUBLIC_[A-Z0-9_]*(SECRET|SERVICE_ROLE|PRIVATE|PASSWORD|TOKEN|WEBHOOK|DATABASE_URL)[A-Z0-9_]*" .
rg -n -e "sk_live_[0-9A-Za-z]{8,}" -e "sk-ant-[0-9A-Za-z_-]{20,}" -e "sk-proj-[0-9A-Za-z_-]{20,}" -e "AKIA[0-9A-Z]{16}" -e "ghp_[0-9A-Za-z]{20,}" -g '!*.lock' -g '!**/*.map' .
git ls-files | rg -e '(^|/)\.env(\.|$)' | rg -v -e 'example|sample|template'
```
If a production build exists (`.next/static`), grep it read-only for the same patterns; it shows what actually ships.

**Confirm.** The name or value is a real secret (Stripe secret key, OpenAI or Anthropic key, Supabase service role key, database URL with password). Public-by-design values are not findings: Supabase publishable or anon key, Stripe publishable key `pk_`, PostHog project key, Sentry DSN, Google Maps browser key (but note referrer restrictions). Redact to the first 4 characters.

**Severity.** Live secret in the client bundle or in a tracked file: `critical` (contract example). Test-mode key (`sk_test_`) committed: `medium`. Secret in an untracked local `.env` only: not a finding (notes).

**Fixed.** Rename to a non-public variable, read it only in a `server-only` module or Server Action, rotate the key at the provider, and purge it from git history if it was committed (handoff to the owner; this audit never rewrites history).

**Refs.** CWE-798, CWE-540, OWASP A04:2025.

---

## NX-DATA-04: Production browser source maps enabled

**What.** Source maps are off in production builds "to prevent you leaking your source on the client" unless `productionBrowserSourceMaps: true`, in which case Next.js serves them [raw/next--source-maps-powered-by-env-vars.md].

**Detection.** Inventory `next_config.production_browser_source_maps`. Also check Sentry or other uploaders that delete maps after upload (`hideSourceMaps`, `sourcemaps.deleteSourcemapsAfterUpload`).

**Severity.** `low` by default (defense in depth); `medium` when source contains hardcoded secrets or sensitive business logic (then also file NX-DATA-03).

**Vulnerable.** `productionBrowserSourceMaps: true`
**Fixed.** Remove it; upload maps privately to the error tracker instead.

**Refs.** CWE-540, OWASP A02:2025.

---

## NX-DATA-05: Taint APIs relied on as the only protection

**What.** Taint is experimental and "Do not rely on just tainting for security"; cloned or spread objects lose the taint [raw/react--taint-apis.md].

**Detection.** Inventory `taint_api_uses[]`, `next_config.taint_enabled`. Look for `{...user}` or picked fields of a tainted object sent to clients.

**Severity.** Using taint is good. A finding only when a tainted object is cloned and passed (then treat as NX-DATA-01). `info` otherwise.

**Refs.** CWE-200, OWASP A01:2025.

---

## NX-CACHE-01: Personalized data cached without the user in the cache key (`use cache`, `unstable_cache`, fetch cache)

**What.** `use cache` output is reused "across requests"; its key is build id, function id, and serializable arguments (closed-over variables included) [raw/next--use-cache-and-unstable-cache.md]. `unstable_cache` keys on arguments plus `keyParts`, and "it is important to add closures used within the function if you do not pass them as parameters" [raw/next--use-cache-and-unstable-cache.md]. A cached function that fetches per-user data but takes no user argument serves one user's data to everyone. Cookies and headers are not readable inside the cache scope, so developers sometimes read the user id from a module-level variable or a global store instead.

**Detection.** Inventory `use_cache[]`, `unstable_cache[]`.
```bash
rg -n -U --pcre2 "['\"]use cache['\"][\s\S]{0,600}?(session|currentUser|userId|user\.id|getUser|cart|order|invoice|account)" .
rg -n -U --pcre2 "unstable_cache\(\s*async\s*\(\s*\)\s*=>[\s\S]{0,400}?(userId|session|user\.id)" .
rg -n -e "fetch\([^)]*cache:\s*['\"]force-cache['\"]" -e "next:\s*\{\s*revalidate" .
```
**Confirm.** Read the cached function. Confirmed when the result depends on who is asking but the user or tenant id is not an argument (or a captured variable that varies per user). For `unstable_cache`, confirmed when `keyParts` omits a closure variable that identifies the user. For `fetch` with `force-cache` or `revalidate`, confirmed when the request carries per-user headers (cookie, Authorization) and the response is per-user. Also check file-level `'use cache'` modules: their exports are callable from Client Components like Server Functions, so they need their own auth [raw/next--use-cache-and-unstable-cache.md] [raw/advisory--2026-server-actions.md].

**Severity.** One user's private data served to others: `critical` when it is account, order, health, or financial data for any visitor; `high` when limited to low-sensitivity personalization. File-level `'use cache'` export returning private data without an auth check: `high`.

**Vulnerable.**
```ts
const currentUserId = getRequestStore().userId     // set elsewhere
export async function getMyOrders() {
  'use cache'
  return db.order.findMany({ where: { userId: currentUserId } })
}
```
**Fixed.**
```ts
export async function getOrders(userId: string) {
  'use cache'
  cacheLife('minutes')
  return db.order.findMany({ where: { userId }, select: { id: true, total: true } })
}
// caller: const { userId } = await verifySession(); const orders = await getOrders(userId)
```
**Refs.** CWE-524, CWE-200, OWASP A01:2025.

---

## NX-CACHE-02: Private data on statically generated or ISR pages (`generateStaticParams`, `force-static`, `revalidate`)

**What.** Static and ISR output is built once and served to every visitor; request-time checks in the page body do not run for cached output. The authentication guide says static routes that share data between users are fetched at build time and need Proxy for gating [raw/next--authentication-guide.md] [raw/next--generate-static-params-and-dynamic-params.md]. `dynamicParams` controls whether unlisted params render; metadata image routes ignored it before the 2026-09-30 fix (CVE-2026-94485) [raw/advisory--2026-rewrites-ssrf-and-other.md].

**Detection.** Inventory `generate_static_params_files[]`, plus:
```bash
rg -n -e "export const dynamic\s*=\s*['\"]force-static['\"]" -e "export const revalidate\s*=" -e "generateStaticParams" -g 'app/**' .
rg -n -e "getStaticProps" -e "getStaticPaths" -g 'pages/**' .
```
**Confirm.** The static page or `generateStaticParams` source query includes private records (drafts, other users' profiles, unpublished pricing, internal docs). Check the build output list in `.next/server/app` if present.

**Severity.** Private or unpublished data published to everyone: `high`; personal data at scale: `critical`.

**Vulnerable.** `generateStaticParams` returns every user's id and the page renders their email and phone number with `force-static`.
**Fixed.** Render per-user pages dynamically with a session check, or publish only public fields; set `dynamicParams = false` where only listed params should exist.

**Refs.** CWE-200, CWE-359, CWE-524, OWASP A01:2025.

---

## NX-CACHE-03: Cache Components and Draft Mode on 16.3.x (open advisories)

**What.** Two advisories published 2026-09-30 with no stated fix version: nested `'use cache'` root-param key leak (GHSA-h694-7cp9-m8p3) and Draft Mode content leaking through pending `use cache` fills (CVE-2026-94544) [raw/advisory--2026-cache-poisoning-and-cache-leaks.md].

**Detection.** Inventory `next_config.cache_components`, `use_cache[]`, `draft_mode_uses[]`, root params usage:
```bash
rg -n -e "next/root-params" -e "draftMode\(" .
```
**Severity.** As in the advisory (medium), confidence `likely` only when the precondition code exists (nested cached functions reading root params; Draft Mode with cached draft-dependent content). Tell the owner no workaround exists for the first.

**Refs.** GHSA-h694-7cp9-m8p3, CVE-2026-94544, CWE-524, OWASP A03:2025.

---

## NX-CACHE-04: Per-user responses cached by a CDN or shared cache

**What.** Several 2025 to 2026 advisories are cache poisoning or confusion bugs (CVE-2026-44576, CVE-2026-64648, CVE-2026-94543, CVE-2026-94484) [raw/advisory--2026-cache-poisoning-and-cache-leaks.md]; app code can create the same effect by sending `Cache-Control: public` on personalized responses.

**Detection.**
```bash
rg -n -e "Cache-Control['\"]?\s*[:,]\s*['\"][^'\"]*(public|s-maxage)" -e "cacheControl" .
```
**Confirm.** The response varies by cookie or auth header and is marked `public` or `s-maxage` without `Vary` on the auth input.

**Severity.** Private responses cacheable by shared caches: `high`.

**Refs.** CWE-524, CWE-525, OWASP A02:2025.

---

Sources: [raw/next--data-security-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--data-security-guide.md), [raw/next--authentication-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--authentication-guide.md), [raw/next--use-cache-and-unstable-cache.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--use-cache-and-unstable-cache.md), [raw/next--generate-static-params-and-dynamic-params.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--generate-static-params-and-dynamic-params.md), [raw/next--source-maps-powered-by-env-vars.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--source-maps-powered-by-env-vars.md), [raw/react--taint-apis.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/react--taint-apis.md), [raw/advisory--2026-cache-poisoning-and-cache-leaks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-cache-poisoning-and-cache-leaks.md), [raw/advisory--2026-rewrites-ssrf-and-other.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-rewrites-ssrf-and-other.md), [raw/advisory--2026-server-actions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-server-actions.md), [raw/ai--vendor-scans-of-vibe-coded-apps-2026.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/ai--vendor-scans-of-vibe-coded-apps-2026.md), [raw/standard--cwe-entries.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/standard--cwe-entries.md).

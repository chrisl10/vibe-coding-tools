# Check catalog

Every check the Drone runs, grouped by guide. Each entry gives: what it is, how to detect it, how to confirm it versus a false positive, severity guidance mapped to the contract (section 7 of `audit-contract.md`), a vulnerable and fixed pair, and refs. Ripgrep commands are collected in [detection-patterns.md](detection-patterns.md); severity rules in [severity-guide.md](severity-guide.md).

Notation: "Scan" means `sveltekit-inventory.json` from `scripts/sveltekit_audit_scan.py`. Ripgrep commands live only in [detection-patterns.md](detection-patterns.md), where each was tested to parse; "line marked B3" means the command commented `# B3` there.

Contents: [Versions (V)](#versions-v) · [Boundary (B)](#boundary-b) · [Actions, endpoints, remote functions (E)](#actions-endpoints-remote-functions-e) · [Hooks and authorization (H)](#hooks-and-authorization-h) · [XSS, CSP, cookies (X)](#xss-csp-cookies-x) · [Config, adapters, prerender (C)](#config-adapters-prerender-c) · [AI-generated failure patterns (A)](#ai-generated-failure-patterns-a)

---

## Versions (V)

### SVK-V1 Installed framework version has a published advisory

- **Detect:** Scan `advisory_matches` and `sveltekit-version-findings.jsonl`. Manual fallback: read the lockfile entry for `svelte`, `@sveltejs/kit`, `devalue`, each `@sveltejs/adapter-*`, then compare with [advisory-table.md](advisory-table.md).
- **Confirm:** The precondition column is the test. Find the feature in source (for example `query.batch(`, `form(` in a `.remote.ts`, `export const prerender = true`, `{...attrs}` spreading). Confirmed only when the vulnerable input path is traced (user input reaches the feature).
- **False positive:** The version comes from `package.json` only (no lockfile): report "unresolved" in notes, not a finding. Svelte 3 or 4 matching a Svelte 5 feature advisory (no lower bound in the published range) where the feature does not exist in that major: keep the rolled-up `possible` finding, say so in `why_it_matters`.
- **Severity:** Reviewed advisory severity when the precondition is found (`likely`), else rolled up at `possible`, capped `medium`. Dev-server-only advisories: `low`.
- **Vulnerable / fixed:**

```jsonc
// pnpm-lock.yaml resolves @sveltejs/kit@2.49.2 and the app uses query.batch (GHSA-hgv7-v322-mmgr)
"@sveltejs/kit": "^2.49.0"
// fixed: lockfile resolves 2.70.3 (or at least 2.60.1 for this advisory)
"@sveltejs/kit": "^2.70.3"
```

- **Refs:** CWE-1395, OWASP A03:2025, GHSA/CVE ids from the table. [raw/advisory--github-advisory-db-svelte-ecosystem.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--github-advisory-db-svelte-ecosystem.md)

### SVK-V2 SvelteKit below 2.70.0 built with a non-production NODE_ENV

- **Detect:** kit version below 2.70.0, then search build scripts, Dockerfiles, platform config and CI workflows for a `NODE_ENV` set to anything but `production`. Commands: [detection-patterns.md](detection-patterns.md), section "Versions", line marked the NODE_ENV command.
- **Confirm:** The deploy build command sets `NODE_ENV` to anything but `production` (for example `staging`, `development`, `test`). Then every CSRF and remote-function origin check is absent from that build.
- **False positive:** `NODE_ENV` set only for test or lint jobs that do not produce the deployed artifact.
- **Severity:** `high` when the affected build is deployed to users and the app has form actions or remote commands with cookie auth; `medium` when only a staging deploy is affected.
- **Vulnerable / fixed:**

```json
"scripts": { "build:staging": "NODE_ENV=staging vite build" }
```

```json
"scripts": { "build:staging": "vite build --mode staging" }
```

(Upgrade kit to 2.70.0 or later as well; `--mode` sets Vite's mode without changing `NODE_ENV`.)
- **Refs:** CWE-352, CWE-1188, OWASP A01:2025. [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md)

---

## Boundary (B)

### SVK-B1 Server load returns whole database rows or other users' data

- **Detect:** Scan `routes[]` with `kind` `server_page` or `server_layout`. Commands: [detection-patterns.md](detection-patterns.md), section "Boundary", line marked B1.
- **Confirm:** Open the schema for the returned table. A finding needs at least one sensitive column (password hash, token, reset code, email of other users, internal flags, billing ids) that the page does not display. Load the page and inspect `__data.json` or the inline `<script>` data when a running instance is available; otherwise trace the return value statically.
- **False positive:** The query selects explicit columns, or maps rows through a DTO before return.
- **Severity:** `high` for credentials, tokens or other users' PII; `medium` for internal-only fields of the current user; `critical` when a public (unauthenticated) page returns credentials or tokens for many users.
- **Vulnerable / fixed:**

```ts
// src/routes/team/+page.server.ts
export const load = async ({ locals }) => ({
  members: await db.select().from(users).where(eq(users.orgId, locals.user.orgId))
});
```

```ts
export const load = async ({ locals }) => ({
  members: await db
    .select({ id: users.id, name: users.name, avatar: users.avatar })
    .from(users)
    .where(eq(users.orgId, locals.user.orgId))
});
```

- **Refs:** CWE-200, CWE-359, OWASP A01:2025. [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md)

### SVK-B2 Root or shared layout load leaks data to every child page

- **Detect:** `src/routes/+layout.server.*` and group layouts in Scan. Look at what they return.
- **Confirm:** Data meant for one area (admin settings, feature flags with secrets, full user object) is returned by a layout that also wraps public pages. Every page under that layout serialises it.
- **False positive:** Only public, display-safe fields.
- **Severity:** as SVK-B1.
- **Vulnerable / fixed:**

```ts
// src/routes/+layout.server.ts
export const load = ({ locals }) => ({ user: locals.user }); // full row incl. stripeCustomerId, role flags
```

```ts
export const load = ({ locals }) => ({
  user: locals.user && { id: locals.user.id, name: locals.user.name }
});
```

- **Refs:** CWE-200, OWASP A01:2025. [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md)

### SVK-B3 Secret exposed through a public env name

- **Detect:** Scan `env_public_names[]` with `looks_secret: true`; `import.meta.env.VITE_*` uses; `.env*` files committed (names only, never print values). Commands: [detection-patterns.md](detection-patterns.md), section "Boundary", line marked B3.
- **Confirm:** The provider documents the value as secret (for example a Stripe secret key, a Supabase service role key, a database URL, a private API token). Publishable or anon keys designed for browsers are not secrets.
- **False positive:** `PUBLIC_STRIPE_PUBLISHABLE_KEY`, `PUBLIC_SUPABASE_ANON_KEY` (when row level security is on, which belongs to `security-wasp-drone`), analytics site ids.
- **Severity:** `critical` for a live secret key with write or billing power; `high` for read tokens to private data; redact per contract rule 5.2 (first 4 characters then `****`).
- **Vulnerable / fixed:**

```ts
import { PUBLIC_STRIPE_SECRET_KEY } from '$env/static/public'; // bundled into every browser
```

```ts
// src/lib/server/stripe.ts
import { STRIPE_SECRET_KEY } from '$env/static/private';
```

- **Refs:** CWE-540, CWE-798, OWASP A02:2025. [raw/kit-docs--server-only-modules-and-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--server-only-modules-and-env.md), [raw/vite-docs--env-variables-prefix.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/vite-docs--env-variables-prefix.md)

### SVK-B4 Universal load does privileged work

- **Detect:** Scan `routes[]` with `kind` `universal_page` / `universal_layout`. Read each for `fetch` to internal APIs with headers like `Authorization: Bearer ${PUBLIC_...}` or hardcoded keys.
- **Confirm:** The universal load runs in the browser on navigation, so any credential it uses is client-side. Secrets via `$env/*/private` cannot be imported here (build fails), so look for hardcoded strings and `PUBLIC_`/`VITE_` names.
- **False positive:** Calls to public APIs or same-origin endpoints that do their own auth with the user's cookie.
- **Severity:** follows SVK-B3 for the exposed credential.
- **Vulnerable / fixed:**

```ts
// src/routes/reports/+page.ts
export const load = ({ fetch }) =>
  fetch('https://api.internal.example/reports', { headers: { 'x-api-key': 'sk_live_51H...' } });
```

```ts
// src/routes/reports/+page.server.ts
import { REPORTS_API_KEY } from '$env/static/private';
export const load = async ({ fetch, locals }) => {
  if (!locals.user) error(401);
  const r = await fetch('https://api.internal.example/reports', { headers: { 'x-api-key': REPORTS_API_KEY } });
  return { reports: (await r.json()).map(({ id, title }) => ({ id, title })) };
};
```

- **Refs:** CWE-798, CWE-602, OWASP A04:2025, OWASP A06:2025. [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md)

### SVK-B5 Shared module-level state on the server

- **Detect:** Scan `module_level_state[]`. Commands: [detection-patterns.md](detection-patterns.md), section "Boundary", line marked B5.
- **Confirm:** The variable or store is written with per-user data during a request (in a load, action, hook, or during SSR of a component) and read on another request. Show the write and the read.
- **False positive:** Caches of global, non-user data (feature list, config) or client-only modules never imported by server code; stores written only in the browser (inside `onMount`, event handlers).
- **Severity:** `high` when user data from one request can reach another user; `medium` when the shared value is user-specific but not sensitive.
- **Vulnerable / fixed:**

```ts
// src/lib/session.ts
export const currentUser = writable<User | null>(null);
// src/routes/+layout.server.ts
export const load = ({ locals }) => { currentUser.set(locals.user); return {}; };
```

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import { setContext } from 'svelte';
  let { data, children } = $props();
  setContext('user', () => data.user);
</script>
{@render children()}
```

- **Refs:** CWE-488, CWE-668, OWASP A01:2025. [raw/kit-docs--state-management-and-stores.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--state-management-and-stores.md)

### SVK-B6 Server-only boundary bypassed

- **Detect:** Scan `env_private_imports_in_client[]` (a `.svelte` file importing `$env/*/private` or `$lib/server`; the build should fail, so its presence means the file is unused or tests only). Also secrets placed in `src/lib/*.ts` outside `server/`, and `vitest` configs relying on `TEST=true`.
- **Confirm:** A secret value or a server client (database, admin SDK) is defined in a module that a client file imports. The build-time guard only protects `$lib/server`, `*.server.*` and `$env/*/private`.
- **False positive:** `import type` only.
- **Severity:** as SVK-B3 for the exposed value.
- **Vulnerable / fixed:**

```ts
// src/lib/db.ts  (not under $lib/server, imported by a +page.svelte for a type helper)
export const db = drizzle(postgres('postgres://admin:hunter2@db.internal/app'));
```

```ts
// src/lib/server/db.ts
import { DATABASE_URL } from '$env/static/private';
export const db = drizzle(postgres(DATABASE_URL));
```

- **Refs:** CWE-540, CWE-200, OWASP A02:2025. [raw/kit-docs--server-only-modules-and-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--server-only-modules-and-env.md)

### SVK-B7 Buffers or typed arrays returned from a server load (devalue shared memory)

- **Detect:** Scan `signals.buffer_like_in_server_load` plus devalue version from 5.1.0 up to 5.9.2 (GHSA-j22f-vq7h-c4qm, CVE-2026-92708).
- **Confirm:** A server load (or remote query) returns a `Buffer`, `Uint8Array` or file read result directly.
- **False positive:** The value is converted to a string or base64 before return; devalue 5.9.3 or later.
- **Severity:** `high` on affected versions (other users' request memory can reach the page); `info` on patched versions.
- **Vulnerable / fixed:**

```ts
export const load = () => ({ logo: readFileSync('static/logo.svg') }); // Buffer
```

```ts
export const load = () => ({ logo: readFileSync('static/logo.svg', 'utf8') });
```

- **Refs:** CWE-200, OWASP A01:2025, GHSA-j22f-vq7h-c4qm, CVE-2026-92708. [raw/advisory--devalue-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--devalue-repo-advisories.md)

---

## Actions, endpoints, remote functions (E)

### SVK-E1 Form action without its own authorization

- **Detect:** Scan `routes[]` with `actions` non-empty. For each action, read the body.
- **Confirm:** The action mutates or reads protected data and does not check `locals.user` (or call a guard) itself, relying on the page or layout `load`. Prove reachability: an action is a POST to `/<route>?/<name>`; `handle` runs before it, but page and layout loads run only after the action completes, so a load guard (even a redirect) comes too late.
- **False positive:** `handle` enforces auth for the whole route prefix before resolve (verify the prefix logic, SVK-H2); the action calls a shared guard.
- **Severity:** `high` (contract example: "Server Action without an auth check"); `critical` when it lets an anonymous user change other users' data or roles.
- **Vulnerable / fixed:**

```ts
// src/routes/admin/+page.server.ts  (+layout.server.ts redirects non-admins)
export const actions = {
  deleteUser: async ({ request }) => {
    const id = (await request.formData()).get('id');
    await db.delete(users).where(eq(users.id, String(id)));
  }
};
```

```ts
export const actions = {
  deleteUser: async ({ request, locals }) => {
    if (!locals.user?.isAdmin) error(403, 'Forbidden');
    const id = String((await request.formData()).get('id'));
    await db.delete(users).where(eq(users.id, id));
  }
};
```

- **Refs:** CWE-862, OWASP A01:2025. [raw/kit-docs--form-actions-and-routing.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--form-actions-and-routing.md), [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md)

### SVK-E2 +server endpoint without authorization

- **Detect:** Scan `routes[]` with `kind: endpoint` and `auth_hint_found: false`. Every exported verb, including `fallback`.
- **Confirm:** The handler returns or changes protected data and has no check. "`+layout` files have no effect on `+server.js` files." Check `handle` coverage for the path.
- **False positive:** Public by design (health check, public feed, webhook verified by signature, which `security-wasp-drone` owns).
- **Severity:** `high`; `critical` for unauthenticated bulk reads of PII or writes.
- **Vulnerable / fixed:**

```ts
// src/routes/api/users/+server.ts
export const GET = async () => json(await db.select().from(users));
```

```ts
export const GET = async ({ locals }) => {
  if (!locals.user?.isAdmin) error(403, 'Forbidden');
  return json(await db.select({ id: users.id, name: users.name }).from(users));
};
```

- **Refs:** CWE-862, CWE-306, OWASP A01:2025. [raw/kit-docs--form-actions-and-routing.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--form-actions-and-routing.md)

### SVK-E3 Remote function without authorization

- **Detect:** Scan `remote_functions[]`. Read each `query`, `query.batch`, `query.live`, `form`, `command` body for `getRequestEvent()` plus a user check.
- **Confirm:** The function returns protected data or mutates state with no check. Remote functions are generated HTTP endpoints callable by anyone who reads the client bundle.
- **False positive:** Public reads; `prerender` functions that only expose build-time public data.
- **Severity:** `high`; `critical` for anonymous writes or bulk PII.
- **Vulnerable / fixed:**

```ts
// src/routes/billing/data.remote.ts
export const getInvoices = query(v.string(), async (orgId) => db.query.invoices.findMany({ where: eq(invoices.orgId, orgId) }));
```

```ts
export const getInvoices = query(v.string(), async (orgId) => {
  const { locals } = getRequestEvent();
  if (!locals.user || !(await isMember(locals.user.id, orgId))) error(403, 'Forbidden');
  return db.query.invoices.findMany({ where: eq(invoices.orgId, orgId), columns: { id: true, total: true, date: true } });
});
```

- **Refs:** CWE-862, CWE-639, OWASP A01:2025. [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md)

### SVK-E4 Remote function argument not validated

- **Detect:** Scan `remote_functions[].validation == "unchecked"`. Commands: [detection-patterns.md](detection-patterns.md), section "Actions, endpoints, remote functions", line marked E4.
- **Confirm:** The unchecked argument reaches a query, a file path, an object merge, or a redirect. Also check schemas that accept `v.any()` / `z.any()` / passthrough objects.
- **False positive:** The function validates by hand immediately (document it in `verified_by`).
- **Severity:** `medium` alone; raise to the downstream impact (for example `high` when it enables injection or mass assignment).
- **Vulnerable / fixed:**

```ts
export const updateProfile = command('unchecked', async (patch: Partial<User>) =>
  db.update(users).set(patch).where(eq(users.id, getRequestEvent().locals.user.id)));
```

```ts
const Patch = v.object({ name: v.pipe(v.string(), v.maxLength(80)), bio: v.optional(v.pipe(v.string(), v.maxLength(500))) });
export const updateProfile = command(Patch, async (patch) => {
  const { locals } = getRequestEvent();
  if (!locals.user) error(401);
  await db.update(users).set(patch).where(eq(users.id, locals.user.id));
});
```

- **Refs:** CWE-20, CWE-915, OWASP A05:2025, OWASP A08:2025. [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md)

### SVK-E5 Object id from the client used without an ownership check (IDOR)

- **Detect:** In actions, endpoints, remote functions and server loads, look for ids taken from `params`, form fields, or query strings. Commands: [detection-patterns.md](detection-patterns.md), section "Actions, endpoints, remote functions", line marked E5.
- **Confirm:** The id selects a row and the query does not also constrain by the caller's user or tenant id (or check membership).
- **False positive:** The query includes `and(eq(x.id, id), eq(x.ownerId, locals.user.id))` or equivalent.
- **Severity:** `high`; `critical` when ids are sequential and the data is sensitive.
- **Vulnerable / fixed:**

```ts
export const load = async ({ params }) => ({ doc: await db.query.docs.findFirst({ where: eq(docs.id, params.id) }) });
```

```ts
export const load = async ({ params, locals }) => {
  const doc = await db.query.docs.findFirst({ where: and(eq(docs.id, params.id), eq(docs.ownerId, locals.user.id)) });
  if (!doc) error(404);
  return { doc };
};
```

- **Refs:** CWE-639, OWASP A01:2025. [raw/owasp--top10-2025-categories-and-cwes.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--top10-2025-categories-and-cwes.md)

### SVK-E6 Remote function authorises from `url`, `route` or `params`

- **Detect:** `getRequestEvent()` in `.remote.*` files followed by reads of `url`, `route`, or `params`. Commands: [detection-patterns.md](detection-patterns.md), section "Actions, endpoints, remote functions", line marked E6.
- **Confirm:** An access decision uses those values. Docs: they describe the calling page and "could be manipulated".
- **False positive:** Used only for logging or analytics.
- **Severity:** `high` when it gates protected data.
- **Vulnerable / fixed:**

```ts
export const getOrg = query(async () => {
  const { url, locals } = getRequestEvent();
  if (!url.pathname.startsWith('/admin')) error(403);
  return db.query.orgs.findMany();
});
```

```ts
export const getOrg = query(async () => {
  const { locals } = getRequestEvent();
  if (!locals.user?.isAdmin) error(403);
  return db.query.orgs.findMany({ columns: { id: true, name: true } });
});
```

- **Refs:** CWE-807, CWE-863, OWASP A01:2025. [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md)

### SVK-E7 CSRF protection weakened or bypassed

- **Detect:** Scan `svelte_config[]`: `csrf_trusts_all`, `csrf_checkOrigin_false`, long `csrf_trustedOrigins`. Then GET handlers and `query` remote functions that write, and CORS headers. Commands: [detection-patterns.md](detection-patterns.md), section "Actions, endpoints, remote functions", line marked E7.
- **Confirm:** One of: (a) `trustedOrigins: ['*']` or `checkOrigin: false` with cookie-authenticated actions; (b) a GET handler or remote `query` with side effects; (c) a JSON endpoint whose CORS response reflects the request origin with `Access-Control-Allow-Credentials: true`; (d) SVK-V2.
- **False positive:** A trusted origin list naming specific payment or identity providers (record them in notes); a JSON API authenticated by a bearer header, not cookies.
- **Severity:** `high` for (a) or (c) with cookie auth on state-changing routes; `medium` for (b) behind `SameSite=Lax` cookies (contract example); `medium` for a broad but specific trusted origin list.
- **Vulnerable / fixed:**

```js
// svelte.config.js
kit: { csrf: { trustedOrigins: ['*'] } }
```

```js
kit: { csrf: { trustedOrigins: ['https://checkout.stripe.com'] } }
```

- **Refs:** CWE-352, CWE-346, CWE-942, OWASP A01:2025. [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md), [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md), [raw/owasp--cheatsheets-csrf-ssrf-redirects.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--cheatsheets-csrf-ssrf-redirects.md)

### SVK-E8 Mass assignment from form data

- **Detect:** `Object.fromEntries(formData)` or a whole request body passed to an insert or update in server files. Commands: [detection-patterns.md](detection-patterns.md), section "Actions, endpoints, remote functions", line marked E8.
- **Confirm:** All submitted fields reach an update or insert, so a user can add `role=admin`, `ownerId=...`, `credits=...`.
- **False positive:** A schema picks allowed fields first.
- **Severity:** `high` when privilege or ownership fields are writable; `medium` otherwise.
- **Vulnerable / fixed:**

```ts
save: async ({ request, locals }) => {
  const data = Object.fromEntries(await request.formData());
  await db.update(users).set(data).where(eq(users.id, locals.user.id));
}
```

```ts
save: async ({ request, locals }) => {
  const f = await request.formData();
  const data = v.parse(v.object({ name: v.string(), bio: v.string() }), { name: f.get('name'), bio: f.get('bio') });
  await db.update(users).set(data).where(eq(users.id, locals.user.id));
}
```

- **Refs:** CWE-915, OWASP A08:2025. [raw/owasp--top10-2025-categories-and-cwes.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--top10-2025-categories-and-cwes.md)

### SVK-E9 Unbounded work per request

- **Detect:** `requested(..., Infinity)`, `BODY_SIZE_LIMIT` set to `Infinity` or `0`, remote `form` handlers using `files` without count or size checks. Commands: [detection-patterns.md](detection-patterns.md), section "Actions, endpoints, remote functions", line marked E9.
- **Confirm:** The limit is removed and nothing else caps it (handle hook, platform, WAF).
- **False positive:** A platform or proxy limit is configured and documented.
- **Severity:** `medium` (denial of service needs only volume); `low` when a platform cap exists.
- **Vulnerable / fixed:**

```ts
for (const { query } of requested(getPosts, Infinity)) query.refresh();
```

```ts
await requested(getPosts, 5).refreshAll();
```

- **Refs:** CWE-770, CWE-400, OWASP A10:2025 (interpretation, see the mapping note). [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md), [raw/kit-docs--adapter-node.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-node.md)

---

## Hooks and authorization (H)

### SVK-H1 Authorization lives only in a layout load

- **Detect:** Scan: `+layout.server.*` with `auth_hint_found: true` while sibling or child `+page.server.*` (actions), `+server.*`, and `.remote.*` files under the same folder have none, and `hooks[].route_id_checks` is empty.
- **Confirm:** Show at least one child surface (action, endpoint, remote function, or page load that does not `await parent()`) reachable without the layout's check. Layout loads do not run on every request, page and layout loads run concurrently, and layouts never cover `+server`.
- **False positive:** `handle` enforces the same rule for the path prefix; every child calls the guard.
- **Severity:** `high` when a child surface exposes protected data or actions; `medium` when every child currently has its own check but the design relies on the layout (structural risk).
- **Vulnerable / fixed:**

```ts
// src/routes/(app)/+layout.server.ts
export const load = ({ locals }) => { if (!locals.user) redirect(303, '/login'); };
// src/routes/(app)/projects/+page.server.ts
export const load = async () => ({ projects: await db.query.projects.findMany() }); // no await parent(), no check
```

```ts
// src/hooks.server.ts
export const handle = async ({ event, resolve }) => {
  event.locals.user = await getUserFromSession(event.cookies.get('session'));
  if (event.route.id?.startsWith('/(app)') && !event.locals.user) redirect(303, '/login');
  return resolve(event);
};
// remote functions still check locals themselves: route.id is client-chosen for remote calls (SVK-H2)
```

- **Refs:** CWE-862, OWASP A01:2025. [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md), [raw/kit-docs--form-actions-and-routing.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--form-actions-and-routing.md)

### SVK-H2 Path check in `handle` misses routes

- **Detect:** Scan `hooks[].route_id_checks`; read every `url.pathname` / `route.id` comparison.
- **Confirm:** A protected surface is outside the matched prefix (for example `/admin` guarded but `/api/admin` is not), a denylist is used instead of an allowlist, or `route.id` is null for unmatched routes and treated as allowed.
- **Remote functions:** for a remote call (served under `/_app/remote/...`), SvelteKit sets `event.url.pathname` from the client-sent `x-sveltekit-pathname` header before `handle` runs, and `event.route` follows it. A path or route-id guard in `handle` is therefore decided by the caller for every remote function. If the app has remote functions and its only check is such a guard, look for remote functions without their own `locals` check: each one is a finding. `event.isRemoteRequest` tells `handle` that a request is a remote call.
- **False positive:** Deny-by-default logic (`if (!isPublic(route.id) && !user)`) for pages and endpoints, plus a per-function check in every remote function (or `handle` requiring a user whenever `event.isRemoteRequest` is true and the function is not public).
- **Severity:** `high` when a protected surface is reachable (including a remote function protected only by a path guard); `medium` for a fragile denylist with no current gap.
- **Vulnerable / fixed:**

```ts
if (event.url.pathname.startsWith('/admin') && !event.locals.user?.isAdmin) error(403);
```

```ts
const PUBLIC = new Set(['/', '/login', '/pricing']);
if (!PUBLIC.has(event.route.id ?? '') && !event.locals.user) redirect(303, '/login');
// admin rights are still checked inside each admin action, endpoint and remote function
```

- **Refs:** CWE-863, CWE-807, OWASP A01:2025. [raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md), [raw/kit-docs--remote-functions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--remote-functions.md), [raw/kit-source--csrf-implementation-and-prs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-source--csrf-implementation-and-prs.md)

### SVK-H3 `event.locals` populated from untrusted input

- **Detect:** Scan `hooks[].sets_locals`. Read how the user is derived (token decode without verify, `atob`, `JSON.parse` of a cookie, identity headers). Commands: [detection-patterns.md](detection-patterns.md), section "Hooks and authorization", line marked H3.
- **Confirm:** The token is decoded without signature verification, a client-supplied header or plain cookie value is taken as the identity or role, or a session id is not looked up server-side.
- **False positive:** Verification with a library call that checks the signature (for example `jwtVerify`), or a server-side session lookup.
- **Severity:** `critical` when any visitor can become any user; `high` for role escalation only.
- **Vulnerable / fixed:**

```ts
event.locals.user = JSON.parse(atob(event.cookies.get('token')!.split('.')[1]));
```

```ts
const { payload } = await jwtVerify(event.cookies.get('token') ?? '', JWKS, { issuer: ISSUER, audience: AUDIENCE });
event.locals.user = await getUserById(payload.sub!);
```

- **Refs:** CWE-347, CWE-565, CWE-290, OWASP A07:2025, OWASP A04:2025. [raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md), [raw/owasp--top10-2025-categories-and-cwes.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--top10-2025-categories-and-cwes.md)

### SVK-H4 Server fetch to a user-controlled URL, or credentials forwarded to other hosts

- **Detect:** Scan `signals.dynamic_fetch_in_server`, `hooks[].handleFetch_copies_cookie`. Commands: [detection-patterns.md](detection-patterns.md), section "Hooks and authorization", line marked H4.
- **Confirm:** (a) The URL or host comes from params, query, body or a stored user value with no allow-list (SSRF). (b) `handleFetch` copies `cookie` or `authorization` onto requests whose host is not the app's own API. (c) `handleFetch` rewrites URLs using request data.
- **False positive:** Fixed base URL with a validated path segment; an allow-list of hosts checked after URL parsing; redirects disabled.
- **Severity:** `high` (contract example: "SSRF in an image proxy"); `critical` if cloud metadata or internal admin services are reachable from the deployment.
- **Vulnerable / fixed:**

```ts
// src/routes/api/preview/+server.ts
export const GET = async ({ url, fetch }) => fetch(url.searchParams.get('u')!);
```

```ts
const ALLOWED = new Set(['images.example-cdn.com']);
export const GET = async ({ url, fetch }) => {
  const target = new URL(url.searchParams.get('u') ?? '');
  if (target.protocol !== 'https:' || !ALLOWED.has(target.hostname)) error(400, 'Bad target');
  return fetch(target, { redirect: 'error' });
};
```

- **Refs:** CWE-918, OWASP A01:2025. [raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md), [raw/owasp--cheatsheets-csrf-ssrf-redirects.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--cheatsheets-csrf-ssrf-redirects.md)

### SVK-H5 `filterSerializedResponseHeaders` serialises sensitive headers

- **Detect:** Scan `hooks[].filterSerializedResponseHeaders`; read the predicate.
- **Confirm:** The predicate returns true for `set-cookie`, `authorization`, or every header (`() => true`), so SSR-captured response headers are written into the HTML.
- **False positive:** An allow-list such as `name === 'content-range'`.
- **Severity:** `medium`; `high` when a session or upstream token header is included.
- **Vulnerable / fixed:**

```ts
return resolve(event, { filterSerializedResponseHeaders: () => true });
```

```ts
return resolve(event, { filterSerializedResponseHeaders: (name) => name === 'content-range' });
```

- **Refs:** CWE-200, OWASP A01:2025. [raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md)

### SVK-H6 Error details shown to users

- **Detect:** Read `handleError` in `src/hooks.server.*` and `src/hooks.client.*`; Scan `error_with_dynamic_message[]` (`error(500, err.message)`, template strings). Commands: [detection-patterns.md](detection-patterns.md), section "Hooks and authorization", line marked H6.
- **Confirm:** Stack traces, SQL errors, or upstream messages reach `page.error` or a JSON body; user input reaches `error()` messages rendered by `src/error.html` (also GHSA-mh2x-fcqh-fmqv on kit below 2.8.3).
- **False positive:** Generic message plus an error id.
- **Severity:** `low` for information disclosure; `medium` when secrets or SQL appear; XSS cases follow SVK-X1.
- **Vulnerable / fixed:**

```ts
export const handleError = ({ error }) => ({ message: (error as Error).message, stack: (error as Error).stack });
```

```ts
export const handleError = ({ error, event }) => {
  const errorId = crypto.randomUUID();
  log.error({ errorId, path: event.url.pathname, error });
  return { message: 'Something went wrong', errorId };
};
```

- **Refs:** CWE-209, OWASP A10:2025. [raw/kit-docs--hooks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--hooks.md)

### SVK-H7 Open redirect

- **Detect:** Scan `redirects_dynamic[]`; also `goto()` with query values in client code. Commands: [detection-patterns.md](detection-patterns.md), section "Hooks and authorization", line marked H7.
- **Confirm:** The target comes from `url.searchParams` (`next`, `redirectTo`, `returnUrl`), form data, or the `referer` header and is not checked to be a same-site relative path. `//evil.example` and `/\evil.example` count as external.
- **False positive:** Targets built from server data (for example `/article/${slug}` from the database), or validated with an allow-list.
- **Severity:** `medium` (phishing after login); `high` when tokens are appended to the redirect target. In `handle` on kit below 2.57.1 a header-invalid target also crashes the request (CVE-2026-40074).
- **Vulnerable / fixed:**

```ts
redirect(303, url.searchParams.get('next') ?? '/');
```

```ts
const next = url.searchParams.get('next') ?? '/';
const safe = next.startsWith('/') && !next.startsWith('//') && !next.startsWith('/\\') ? next : '/';
redirect(303, safe);
```

- **Refs:** CWE-601, OWASP A01:2025, CVE-2026-40074. [raw/owasp--cheatsheets-csrf-ssrf-redirects.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--cheatsheets-csrf-ssrf-redirects.md), [raw/advisory--kit-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--kit-repo-advisories.md)

---

## XSS, CSP, cookies (X)

### SVK-X1 `{@html}` with content an outsider can influence

- **Detect:** Scan `html_sinks[]` (`sanitizer_in_expression` false first). Commands: [detection-patterns.md](detection-patterns.md), section "XSS, CSP, cookies", line marked X1.
- **Confirm:** Trace the expression back: user profile fields, comments, CMS rich text, markdown from users, third-party API text, URL values. Server-rendered, so the payload is in the first HTML response.
- **False positive:** Constant strings, build-time trusted markdown compiled from the repo, output of a sanitiser (DOMPurify with current jsdom on the server) called on the same value.
- **Severity:** `high` for stored XSS reachable by other users; `medium` for self-only or admin-authored content where admins are not fully trusted; `critical` when an anonymous visitor can store a payload shown to admins.
- **Vulnerable / fixed:**

```svelte
<div class="bio">{@html data.profile.bio}</div>
```

```ts
// +page.server.ts
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';
const purify = DOMPurify(new JSDOM('').window);
export const load = async ({ params }) => {
  const p = await getProfile(params.id);
  return { bioHtml: purify.sanitize(p.bio) };
};
```

```svelte
<div class="bio">{@html data.bioHtml}</div>
```

- **Refs:** CWE-79, CWE-116, OWASP A05:2025. [raw/svelte-docs--html-attach-use-hydratable.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/svelte-docs--html-attach-use-hydratable.md), [raw/markdown--mdsvex-marked-dompurify.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/markdown--mdsvex-marked-dompurify.md)

### SVK-X2 Markdown pipeline without sanitising

- **Detect:** Scan `markdown_libraries[]`; markdown render calls near `{@html`; `happy-dom` used with DOMPurify; mdsvex `compile(` at runtime. Commands: [detection-patterns.md](detection-patterns.md), section "XSS, CSP, cookies", line marked X2.
- **Confirm:** Markdown from users or editors is rendered to HTML and shown through `{@html}` without a sanitiser on the output; or mdsvex compiles untrusted content (it supports all Svelte syntax); or DOMPurify runs on happy-dom or an old jsdom.
- **False positive:** Markdown files in the repo compiled at build time; `rehype-sanitize` (or equivalent) in the pipeline after raw HTML is parsed.
- **Severity:** as SVK-X1.
- **Vulnerable / fixed:**

```ts
return { html: marked.parse(post.body) };
```

```ts
return { html: purify.sanitize(await marked.parse(post.body)) };
```

- **Refs:** CWE-79, OWASP A05:2025. [raw/markdown--mdsvex-marked-dompurify.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/markdown--mdsvex-marked-dompurify.md)

### SVK-X3 Action, attachment or script writes raw HTML into the DOM

- **Detect:** Scan `dom_sinks[]`. Commands: [detection-patterns.md](detection-patterns.md), section "XSS, CSP, cookies", line marked X3.
- **Confirm:** The written string includes a parameter or data value that outsiders can influence (tooltip text, search term, notification body).
- **False positive:** Static markup; `textContent` used instead.
- **Severity:** as SVK-X1 (usually DOM-based, client-only).
- **Vulnerable / fixed:**

```ts
export function tooltip(node: HTMLElement, text: string) {
  const tip = document.createElement('div');
  tip.innerHTML = text;
  node.append(tip);
}
```

```ts
export function tooltip(node: HTMLElement, text: string) {
  const tip = document.createElement('div');
  tip.textContent = text;
  node.append(tip);
}
```

- **Refs:** CWE-79, OWASP A05:2025. [raw/svelte-docs--html-attach-use-hydratable.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/svelte-docs--html-attach-use-hydratable.md)

### SVK-X4 Spreading untrusted objects as attributes or tags

- **Detect:** Scan `signals.spread_attributes`, `signals.svelte_element`, `signals.option_dynamic`, `signals.contenteditable_bind`, `signals.hydratable`.
- **Confirm:** The spread object or tag name comes from user or external data (CMS block props, query params). On svelte below 5.55.7 several of these are SSR XSS advisories (SVK-V1); on patched versions spreading untrusted objects still lets an attacker set `href`, `style`, `srcdoc` and similar.
- **False positive:** Props built in code from known keys.
- **Severity:** `high` on affected versions with an untrusted source; `medium` on patched versions with an untrusted source.
- **Vulnerable / fixed:**

```svelte
<a {...block.attrs}>{block.label}</a>
```

```svelte
<a href={safeHref(block.href)} class={block.variant === 'primary' ? 'btn' : 'link'}>{block.label}</a>
```

- **Refs:** CWE-79, OWASP A05:2025, GHSA-pr6f-5x2q-rwfp, GHSA-rcqx-6q8c-2c42. [raw/advisory--svelte-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--svelte-repo-advisories.md)

### SVK-X5 Content Security Policy missing or weak

- **Detect:** Scan `svelte_config[].csp_present`, `csp_mode`, `csp_unsafe_inline_script`, `csp_report_only_only`; CSP set in hooks; platform header files (`vercel.json`, `_headers`, `netlify.toml`). Commands: [detection-patterns.md](detection-patterns.md), section "XSS, CSP, cookies", line marked X5.
- **Confirm:** No CSP at all, `script-src` with `unsafe-inline` or `unsafe-eval`, or report-only without an enforcing policy. Note prerendered pages get a meta-tag CSP that ignores `frame-ancestors`.
- **False positive:** CSP set at the CDN or platform (read that file and record it).
- **Severity:** `low` by itself (defense in depth); `medium` when an XSS finding exists in the same app.
- **Vulnerable / fixed:**

```js
kit: { csp: { directives: { 'script-src': ['self', 'unsafe-inline'] } } }
```

```js
kit: { csp: { mode: 'auto', directives: { 'script-src': ['self'], 'object-src': ['none'], 'base-uri': ['self'] } } }
```

- **Refs:** CWE-693, CWE-1021, OWASP A02:2025. [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md)

### SVK-X6 Session cookie protections turned off

- **Detect:** Scan `cookie_options_weakened[]`. Commands: [detection-patterns.md](detection-patterns.md), section "XSS, CSP, cookies", line marked X6.
- **Confirm:** A cookie that carries a session, token, or role has `httpOnly: false`, `secure: false` outside localhost, `sameSite: 'none'` without need, a parent `domain`, or is set by client JavaScript.
- **False positive:** Non-sensitive preference cookies (theme, locale).
- **Severity:** `medium` for a session cookie readable by script or sent cross-site; `low` for missing `secure` behind HTTPS-only hosting.
- **Vulnerable / fixed:**

```ts
cookies.set('session', id, { path: '/', httpOnly: false, sameSite: 'none', secure: false });
```

```ts
cookies.set('session', id, { path: '/', httpOnly: true, secure: true, sameSite: 'lax', maxAge: 60 * 60 * 24 * 7 });
```

- **Refs:** CWE-1004, CWE-614, CWE-1275, OWASP A02:2025, OWASP A01:2025. [raw/kit-docs--cookies-api-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--cookies-api-reference.md)

### SVK-X7 Tokens or secrets kept in browser storage or stores

- **Detect:** `localStorage` / `sessionStorage` writes of tokens or keys; client stores holding tokens. Commands: [detection-patterns.md](detection-patterns.md), section "XSS, CSP, cookies", line marked X7.
- **Confirm:** An access or refresh token, API key, or session id is stored where any script on the page (including an XSS payload or a third-party script) can read it.
- **False positive:** Non-sensitive UI state.
- **Severity:** `medium`; `high` when combined with an XSS finding or third-party scripts on the same pages.
- **Vulnerable / fixed:**

```ts
localStorage.setItem('access_token', res.token);
```

```ts
// server action sets an httpOnly cookie instead
cookies.set('session', res.sessionId, { path: '/', httpOnly: true, secure: true, sameSite: 'lax' });
```

- **Refs:** CWE-922, OWASP A01:2025. [raw/ai--vibe-coded-app-security-studies-2026.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--vibe-coded-app-security-studies-2026.md)

---

## Config, adapters, prerender (C)

### SVK-C1 Prerendered page contains user or session data

- **Detect:** Scan `signals.prerender_true` and `routes[].page_options.prerender`. For each, read its load and the layouts above it: `cookies`, `locals`, `getRequestEvent`, database calls.
- **Confirm:** Prerendered output depends on who is asking (it cannot, at build time, so it bakes in the build user's or an empty state) or exposes data that should be gated. Static output is served to everyone without passing `handle`.
- **False positive:** Public marketing content; `prerender = 'auto'` routes that only prerender public entries.
- **Severity:** `high` when gated data ends up in a public static file; `medium` when a protected page is prerendered (its guard never runs for the static file).
- **Vulnerable / fixed:**

```ts
// src/routes/(app)/dashboard/+page.server.ts
export const prerender = true;
export const load = async () => ({ stats: await db.query.stats.findMany() });
```

```ts
export const prerender = false;
export const load = async ({ locals }) => {
  if (!locals.user) redirect(303, '/login');
  return { stats: await getStatsFor(locals.user.id) };
};
```

- **Refs:** CWE-200, CWE-524, OWASP A01:2025. [raw/kit-docs--page-options-prerender-service-workers.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--page-options-prerender-service-workers.md)

### SVK-C2 Vercel ISR on personalised routes, weak bypass token

- **Detect:** `isr` configs and `bypassToken` values; adapter-vercel version (CVE-2026-27118 below 6.3.2). Commands: [detection-patterns.md](detection-patterns.md), section "Config, adapters, prerender", line marked C2.
- **Confirm:** ISR config on a route whose output depends on cookies or the user; a `bypassToken` hardcoded, shorter than 32 characters, or imported from a public env module.
- **False positive:** ISR only on public pages with `bypassToken` from `$env/static/private`.
- **Severity:** `high` for personalised responses cached for others; `medium` for a leaked or weak bypass token.
- **Vulnerable / fixed:**

```ts
export const config = { isr: { expiration: 60, bypassToken: 'refresh' } }; // on /account
```

```ts
import { BYPASS_TOKEN } from '$env/static/private';
export const config = { isr: { expiration: 60, bypassToken: BYPASS_TOKEN } }; // on /blog only
```

- **Refs:** CWE-524, CWE-798, OWASP A01:2025, CVE-2026-27118. [raw/kit-docs--adapter-vercel-and-cloudflare.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-vercel-and-cloudflare.md)

### SVK-C3 adapter-node trusts headers it should not, or has no origin

- **Detect:** Scan `svelte_config[].adapter_import` and `signals.trusted_proxy_headers`; adapter-node variables in deployment files; app code using `getClientAddress()` or forwarded headers for rate limits or allow-lists. Commands: [detection-patterns.md](detection-patterns.md), section "Config, adapters, prerender", line marked C3.
- **Confirm:** `HOST_HEADER`/`PROTOCOL_HEADER`/`ADDRESS_HEADER` set while the server is reachable without a trusted proxy; `XFF_DEPTH` not matching the proxy count; app code reading `x-forwarded-for` left-most for security decisions; no `ORIGIN` with prerendered routes on affected versions (CVE-2025-67647).
- **False positive:** Behind a documented proxy that overwrites those headers.
- **Severity:** `medium` (spoofed IP bypasses rate limiting or IP allow-lists); `high` when an IP allow-list protects admin access.
- **Vulnerable / fixed:**

```ts
const ip = request.headers.get('x-forwarded-for')?.split(',')[0]; // left-most, attacker-controlled
if (!ADMIN_IPS.includes(ip)) error(403);
```

```ts
const ip = event.getClientAddress(); // with ADDRESS_HEADER=X-Forwarded-For and XFF_DEPTH = number of trusted proxies
```

- **Refs:** CWE-348, CWE-290, OWASP A07:2025. [raw/kit-docs--adapter-node.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-node.md)

### SVK-C4 Platform bindings or env passed to the client

- **Detect:** `platform.env` in server files, and load returns that include `env` objects; check where values flow. Commands: [detection-patterns.md](detection-patterns.md), section "Config, adapters, prerender", line marked C4.
- **Confirm:** A load returns `platform.env`, `process.env`, or `env` from `$env/dynamic/private` (whole object or secret fields) to the page.
- **False positive:** Bindings used only server-side.
- **Severity:** as SVK-B3.
- **Vulnerable / fixed:**

```ts
export const load = ({ platform }) => ({ config: platform?.env });
```

```ts
export const load = ({ platform }) => ({ siteName: platform?.env.SITE_NAME });
```

- **Refs:** CWE-200, CWE-497, OWASP A02:2025. [raw/kit-docs--adapter-vercel-and-cloudflare.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--adapter-vercel-and-cloudflare.md)

### SVK-C5 Service worker caches authenticated responses

- **Detect:** Scan `service_workers[]` (`caches_runtime_responses`, `respects_no_store`).
- **Confirm:** The fetch handler stores responses for routes that return user data (`/api/*`, `__data.json`, account pages) and those responses do not send `Cache-Control: no-store`, or the handler ignores that header. The cache outlives logout.
- **False positive:** The handler caches only `build`, `files`, `prerendered`; authenticated responses send `no-store`.
- **Severity:** `medium`; `low` for single-user devices only (rarely provable).
- **Vulnerable / fixed:**

```js
if (response.status === 200) cache.put(event.request, response.clone());
```

```js
const url = new URL(event.request.url);
const cacheable = url.origin === self.location.origin && !url.pathname.startsWith('/api/') && !url.pathname.endsWith('__data.json');
if (cacheable && response.status === 200 && !response.headers.get('cache-control')?.includes('no-store')) cache.put(event.request, response.clone());
```

- **Refs:** CWE-525, OWASP A06:2025. [raw/kit-docs--page-options-prerender-service-workers.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--page-options-prerender-service-workers.md)

### SVK-C6 Config context items (info)

- **Detect:** Scan `svelte_config[]`: `dangerZone_present`, `paths_relative_false`, `env_publicPrefix`, `serviceWorker_register_false`, `prerender_handleHttpError`.
- **Confirm and severity:** `dangerZone` in a SvelteKit 2 config is dead configuration: `info`. A changed `publicPrefix` (for example empty string) widens what reaches the client: treat as SVK-B3 if secrets match it. `paths.relative` is not a security control: mention only when a `<base>` tag or external `paths.assets` host is present (`info`).
- **Refs:** [raw/kit-docs--cookies-api-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--cookies-api-reference.md), [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md)

---

## AI-generated failure patterns (A)

These overlap the checks above; they are listed because they are common in AI-written Svelte code and the grep that finds them is different. File the finding under the matching check id's CWE and add the tag `ai-pattern`.

### SVK-A1 Client-only auth checks

- **Detect:** `onMount` or `$effect` blocks that redirect or check roles; `{#if}` blocks on `isAdmin`, `user` or `role` wrapping data the load already returned; `export const ssr = false` on protected areas. Commands: [detection-patterns.md](detection-patterns.md), section "AI-generated patterns", line marked A1.
- **Confirm:** The data or action is still served by a load, endpoint, action, or remote function without a server check. `$effect` and `onMount` never run during SSR.
- **Severity:** as SVK-E1 to E3 for the unprotected server surface. The client check itself is not the finding; the missing server check is.
- **Vulnerable / fixed:**

```svelte
<script>
  import { goto } from '$app/navigation';
  let { data } = $props(); // data.allUsers came from +page.server.ts with no check
  $effect(() => { if (!data.user?.isAdmin) goto('/'); });
</script>
```

```ts
// +page.server.ts
export const load = async ({ locals }) => {
  if (!locals.user?.isAdmin) error(403);
  return { allUsers: await listUsersSafe() };
};
```

- **Refs:** CWE-602, OWASP A06:2025. [raw/svelte-docs--html-attach-use-hydratable.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/svelte-docs--html-attach-use-hydratable.md), [raw/ai--vibe-coded-app-security-studies-2026.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--vibe-coded-app-security-studies-2026.md)

### SVK-A2 Guard that fails open (swallowed redirect or error)

- **Detect:** `redirect(` or `error(` inside a `try` block in loads, actions, hooks, or remote functions. Commands: [detection-patterns.md](detection-patterns.md), section "AI-generated patterns", line marked A2.
- **Confirm:** `redirect()` or `error()` is thrown inside `try` and the `catch` does not rethrow (no `isRedirect`/`isHttpError` check), so execution continues past the guard.
- **False positive:** The catch rethrows those or the guard sits outside the `try`.
- **Severity:** `high` when the guard protects data or actions.
- **Vulnerable / fixed:**

```ts
try {
  if (!locals.user) redirect(303, '/login');
  return { secrets: await getSecrets() };
} catch (e) {
  console.error(e);
  return { secrets: await getSecrets() };
}
```

```ts
if (!locals.user) redirect(303, '/login');
try {
  return { secrets: await getSecrets(locals.user.id) };
} catch (e) {
  if (isRedirect(e) || isHttpError(e)) throw e;
  error(500, 'Could not load');
}
```

- **Refs:** CWE-636, OWASP A10:2025. [raw/kit-docs--load.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--load.md), [raw/ai--svelte-llm-failure-patterns.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--svelte-llm-failure-patterns.md)

### SVK-A3 Svelte 4 store idioms holding user data on the server

- **Detect:** Same as SVK-B5, plus imports of `svelte/store` or `$app/stores` in modules that server code imports. Commands: [detection-patterns.md](detection-patterns.md), section "AI-generated patterns", line marked A3.
- **Confirm and severity:** as SVK-B5.
- **Refs:** CWE-488, OWASP A01:2025. [raw/kit-docs--state-management-and-stores.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--state-management-and-stores.md), [raw/ai--svelte-llm-failure-patterns.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--svelte-llm-failure-patterns.md)

### SVK-A4 One `+server` endpoint per feature, none guarded

- **Detect:** Scan: many `kind: endpoint` routes with `auth_hint_found: false`, especially POST handlers used by forms in the same app.
- **Confirm and severity:** as SVK-E2. Note in `why_it_matters` that a form action would have kept the logic next to the page; the fix is the guard, not the refactor.
- **Refs:** CWE-862, OWASP A01:2025. [raw/ai--svelte-llm-failure-patterns.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--svelte-llm-failure-patterns.md)

### SVK-A5 Mixed Svelte 4 and 5 syntax (signal, not a finding)

- **Detect:** Svelte 4 syntax (`export let`, `$:`, `on:click`, `createEventDispatcher`) in files that also use `$state(` or `$props(`. Commands: [detection-patterns.md](detection-patterns.md), section "AI-generated patterns", line marked A5.
- **Use:** Not a security finding by itself. Record it in notes as a sign the code was generated in pieces; read guards in those files with extra care.
- **Refs:** [raw/ai--svelte-llm-failure-patterns.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--svelte-llm-failure-patterns.md)

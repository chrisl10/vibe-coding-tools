# Checks: React Server Components and Server Functions (RC)

Load when: running guide 02. Applies to RSC outside Next.js: Vite with `@vitejs/plugin-rsc`, React Router RSC (unstable APIs), Waku, Parcel (`@parcel/rsc`), RedwoodSDK (`rwsdk`), or hand-rolled `react-server-dom-*` servers. On a Next.js app the `nextjs-security-wasp-drone` owns Server Actions; skip RC-02 to RC-08 there unless the arming line says otherwise.

Key facts every check leans on:

- Every `'use server'` function is a network endpoint any client can call with arguments it chooses raw/rsc--react-docs-use-server-and-server-functions.md.
- A module-level `'use server'` turns every export of that file into an endpoint, including helpers nobody meant to expose.
- Apps that support RSC were exposed to CVE-2025-55182 even with zero Server Functions raw/rsc--react-blog-cve-2025-55182.md.

---

## RC-01 Vulnerable RSC runtime version

- **Detect:** run `scripts/react_version_check.py` (guide 00). It reads react-server-dom-webpack, -parcel, -turbopack, and @vitejs/plugin-rsc (which vendors its own copy) from lockfiles.
- **Confirm:** show that the package is used by a server that actually runs: a server entry imports `react-server-dom-*/server`, `vite.config.*` registers `rsc()` from `@vitejs/plugin-rsc`, or the framework is Waku, rwsdk, or React Router RSC. Upgrade confidence to `confirmed` when the deployed server path is traced (start script, Dockerfile, or platform config that serves the RSC entry).
- **False positive:** the package is installed but only used in tests or Storybook with no deployed server; a prerelease build (check by hand against [advisory-table.md](advisory-table.md)).
- **Severity:** per the advisory (CVE-2025-55182 range: `critical`; DoS only: `high`; source exposure only: `medium`).
- **Vulnerable:** `"react-server-dom-webpack": "19.2.0"` resolved in `package-lock.json`.
- **Fixed:** `"react-server-dom-webpack": "19.2.8"` (or 19.3.x), `react` and `react-dom` on the same version, lockfile regenerated; `@vitejs/plugin-rsc` 0.5.29 or later.
- **Refs:** CVE-2025-55182, CVE-2025-55183, CVE-2025-55184, CVE-2025-67779, CVE-2026-23864, CVE-2026-23869, CVE-2026-23870, CVE-2026-44907, CWE-502, CWE-400, CWE-1395, OWASP A03:2025, OWASP A08:2025, raw/rsc--github-react-security-advisories.md, raw/rsc--vite-plugin-rsc-advisories.md.

## RC-02 Server Function with no authentication or authorization

- **Detect:** list every `'use server'` file and inline function (sink_scan RC-02). For each exported or inline async function, read the first statements.
- **Confirm:** a mutation or sensitive read runs with no session lookup and no ownership or role check inside the function itself. A check in the calling component, a client route guard, or a middleware that does not cover the Server Function request path does not count. Ask: if an attacker posts this function id with chosen arguments, what stops them?
- **False positive:** a shared wrapper (`withAuth(async () => ...)`, `authedAction(...)`) that you have read and that checks the session server-side; truly public actions (newsletter signup) that are rate limited.
- **Severity:** unauthenticated write or delete of other users' data: `critical`. Authenticated user can act on another user's records (missing ownership check): `high`. Public action without rate limiting that sends email or costs money: `medium`.
- **Vulnerable:**
  ```ts
  'use server';
  export async function deleteProject(projectId: string) {
    await db.project.delete({ where: { id: projectId } });
  }
  ```
- **Fixed:**
  ```ts
  'use server';
  export async function deleteProject(projectId: string) {
    const user = await requireUser();                 // reads the session cookie on the server
    const project = await db.project.findUnique({ where: { id: projectId } });
    if (!project || project.ownerId !== user.id) throw new Error('Not found');
    await db.project.delete({ where: { id: project.id } });
  }
  ```
- **Refs:** CWE-862, CWE-863, CWE-639, OWASP A01:2025, raw/rsc--react-docs-use-server-and-server-functions.md.

## RC-03 Server Function trusts its arguments

- **Detect:** Server Functions that pass `formData`, objects, or ids straight to the database, file system, shell, fetch, or `eval`; spreads like `data: { ...Object.fromEntries(formData) }`; role or price fields taken from the client.
- **Confirm:** no schema validation (zod, valibot, yup, or manual type checks) before use, or validation that allows extra keys that reach a write (mass assignment). Arguments can be any serializable type: strings where numbers are expected, nested objects, Maps, huge arrays.
- **False positive:** strict schema with unknown keys stripped, then explicit field picking.
- **Severity:** mass assignment of `role`, `isAdmin`, `price`, `ownerId`: `high`. Injection into SQL, shell, or path: `critical` (hand to polyglot or generic pass for the sink, keep this finding for the entry point). Missing validation with no dangerous sink found: `low`.
- **Vulnerable:**
  ```ts
  'use server';
  export async function updateProfile(formData: FormData) {
    const user = await requireUser();
    await db.user.update({ where: { id: user.id }, data: Object.fromEntries(formData) }); // role=admin works
  }
  ```
- **Fixed:**
  ```ts
  const Profile = z.object({ name: z.string().max(80), bio: z.string().max(500) }).strict();
  export async function updateProfile(formData: FormData) {
    const user = await requireUser();
    const input = Profile.parse({ name: formData.get('name'), bio: formData.get('bio') });
    await db.user.update({ where: { id: user.id }, data: input });
  }
  ```
- **Refs:** CWE-20, CWE-915 (A08:2025 maps it), OWASP A05:2025, raw/rsc--react-docs-use-server-and-server-functions.md.

## RC-04 Unintended endpoints from module-level 'use server'

- **Detect:** files that start with `'use server'` and export functions named like getters or internals (`getUserById`, `listAllUsers`, `sendEmail`, `chargeCard`, `resetDatabase`), or re-export from another module.
- **Confirm:** each export is callable from any client. Check whether any of them return data without a check or perform privileged work.
- **False positive:** every export is a deliberate action with its own checks.
- **Severity:** a data getter exposed without auth that returns other users' data: `high`. Privileged helper exposed: `critical` if it mutates without checks.
- **Vulnerable:**
  ```ts
  'use server';
  export async function getUserByEmail(email: string) { return db.user.findUnique({ where: { email } }); }
  export async function signUp(fd: FormData) { /* ... */ }
  ```
- **Fixed:** move `getUserByEmail` to a `server-only` module without the directive; keep only real actions in the `'use server'` file.
- **Refs:** CWE-749 (A01:2025 maps it), CWE-200, raw/rsc--react-docs-use-server-and-server-functions.md.

## RC-05 Secrets hardcoded in or captured by Server Functions

- **Detect:** string literals that look like keys inside `'use server'` bodies (sink_scan SD-02); inline `'use server'` functions defined inside a Server Component that reference outer variables (tokens, keys, user records); `enableActionEncryption: false` or a hardcoded `defineEncryptionKey` in `vite.config.*`.
- **Confirm:** (a) Hardcoded secret inside a Server Function: exposed by CVE-2025-55183 on vulnerable runtimes, and always a source-control leak. (b) Captured values: they are sent to the client as bound arguments and returned on each call. @vitejs/plugin-rsc encrypts them by default; a hand-rolled react-server-dom setup has no documented encryption. Captured values the client can see or swap are both a leak and a trust problem.
- **False positive:** secrets read from `process.env` at call time (not exposed by CVE-2025-55183); captured values that are public ids and re-checked on the server.
- **Severity:** live secret hardcoded in a Server Function on a vulnerable runtime: `critical`. Hardcoded secret on a patched runtime: `high` (source leak; the generic pass may also report it). Sensitive closure capture with encryption disabled or absent: `high`. Capture with plugin-rsc default encryption: `low` (note for the team: still prefer passing ids).
- **Vulnerable:**
  ```tsx
  export default async function Page() {
    const apiKey = 'sk_live_51H****';                 // redacted
    async function refund(orderId: string) { 'use server'; await stripe(apiKey).refund(orderId); }
    return <RefundButton action={refund} />;
  }
  ```
- **Fixed:**
  ```ts
  // actions.ts
  'use server';
  export async function refund(orderId: string) {
    const user = await requireAdmin();
    await stripe(process.env.STRIPE_SECRET_KEY!).refund(await ownedOrder(orderId, user));
  }
  ```
- **Refs:** CWE-798, CWE-497, CVE-2025-55183, OWASP A07:2025, raw/rsc--react-blog-dos-and-source-exposure.md, raw/rsc--vite-plugin-rsc-readme-closure-encryption.md.

## RC-06 Server Components pass secrets or whole records to Client Components

- **Detect:** Server Components that render a `'use client'` component with props like `user={user}`, `config={process.env}`, `token=`, `apiKey=`; data helpers without `import 'server-only'`.
- **Confirm:** everything passed to a Client Component is serialized into the page payload. Read the shape of the object: does it contain password hashes, emails of other users, internal flags, tokens? Taint APIs, if present, only catch the exact object or value and are experimental.
- **False positive:** props are picked fields (`name`, `avatarUrl`) or a DTO built for the client.
- **Severity:** secret key or other users' personal data in props: `high`. Own user's internal fields (hash, internal notes): `medium`.
- **Vulnerable:**
  ```tsx
  const user = await db.user.findUnique({ where: { id } }); // includes passwordHash, mfaSecret
  return <ProfileCard user={user} />;                       // ProfileCard is 'use client'
  ```
- **Fixed:**
  ```tsx
  const user = await db.user.findUnique({ where: { id }, select: { name: true, avatarUrl: true } });
  return <ProfileCard user={user} />;
  ```
- **Refs:** CWE-200, OWASP A01:2025, raw/rsc--react-docs-taint-apis.md.

## RC-07 No cross-site request protection on Server Function endpoints

- **Detect:** custom servers that call `decodeReply`, `decodeAction`, `decodeFormState`, or `loadServerAction` (sink_scan RC-07); Waku below 1.0.0-beta.1; React Router below 7.12.0 (Framework, RSC) or below 7.18.2 (RSC); cookie-based sessions.
- **Confirm:** read the request handler. Is there an `Origin` (or `Sec-Fetch-Site`) check before decoding and running the action? Is the session cookie `SameSite=Lax` or `Strict`? Form-posted Server Actions are ordinary cross-site POST targets without such a check.
- **False positive:** bearer-token auth only (no cookies); framework version with the fix and no custom handler.
- **Severity:** cookie auth, state-changing actions, no origin check: `high`. Same with `SameSite=Lax` cookies: `medium` (contract example). Framework version below the fix with no custom handler: per script.
- **Vulnerable:**
  ```ts
  app.post('/_rsc', async (req, res) => {
    const action = await loadServerAction(req.headers['rsc-action'] as string);
    const args = await decodeReply(await readBody(req));
    res.send(await action(...args));
  });
  ```
- **Fixed:**
  ```ts
  app.post('/_rsc', async (req, res) => {
    const site = req.get('sec-fetch-site');
    const origin = req.get('origin');
    if ((site && site !== 'same-origin') || (!site && origin !== process.env.APP_ORIGIN)) return res.sendStatus(403);
    // then decode and run
  });
  ```
- **Refs:** CWE-352, CWE-346, OWASP A01:2025, CVE-2026-49455, CVE-2026-22030, raw/owasp--cheatsheet-csrf.md, raw/router--waku-advisories.md, raw/router--react-router-advisories.md.

## RC-08 Server Function errors and return values leak internals

- **Detect:** `catch (e) { return { error: e.message } }`, `return { error: String(err) }`, returning whole DB rows or third-party API responses.
- **Confirm:** raw database or provider error text, stack traces, or full records reach the client.
- **False positive:** mapped, generic error messages; selected fields only.
- **Severity:** `low` for error text; `medium` when returned records include other users' data (or treat as RC-06 or SD-05).
- **Vulnerable:** `catch (e) { return { error: (e as Error).message }; }  // "duplicate key value violates unique constraint users_email_key"`
- **Fixed:** log the error server-side, return `{ error: 'Could not save. Try again.' }`.
- **Refs:** CWE-209 (A10:2025), CWE-200.

## RC-09 Taint APIs used as the only defense, or on experimental React in production

- **Detect:** `experimental_taintObjectReference`, `experimental_taintUniqueValue`; `react@experimental` or `0.0.0-experimental-*` versions in the lockfile.
- **Confirm:** taint calls exist but the same data also flows through clones or derived values; or production depends on an experimental React build.
- **Severity:** `low` (defense-in-depth note); experimental React in production: `low` with CWE-1104.
- **Vulnerable:** `taintObjectReference('no', user); return <Card user={{ ...user }} />; // clone is not tainted`
- **Fixed:** select fields at the data layer (RC-06); keep taint as an extra layer only.
- **Refs:** raw/rsc--react-docs-taint-apis.md.

## RC-10 RSC development server reachable from the network

- **Detect:** `vite --host`, `server.host: true` or `'0.0.0.0'` with `@vitejs/plugin-rsc` below 0.5.8; dev servers used as production (`"start": "vite"`).
- **Confirm:** the dev server is the deployed process (Dockerfile or start script) or is bound to all interfaces on shared networks.
- **Severity:** dev server deployed to production with plugin-rsc below 0.5.6: `critical` (CVE-2025-67489 RCE). Bound to all interfaces only in local development: `low`, `possible`.
- **Vulnerable:** `"start": "vite --host 0.0.0.0"` in production with `@vitejs/plugin-rsc@0.5.4`.
- **Fixed:** build and run the production server (`vite build` then the framework's server entry); upgrade the plugin.
- **Refs:** CVE-2025-67489, CVE-2025-68155, raw/rsc--vite-plugin-rsc-advisories.md.

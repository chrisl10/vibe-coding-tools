# AI-generated Next.js failure patterns

Heuristics for apps built mostly by AI agents (Cursor, Claude Code, v0, Lovable, Bolt, Replit). Loaded by guides 02 to 05 as a sweep after the main checks. Each pattern points to the check that owns the finding, so a hit here is never a finding by itself: confirm it with that check's procedure.

## Why this list exists

- An academic study of 200 deployed vibe-coded apps (Claude Code and Lovable) found at least one vulnerability in 91.0% of them, with 65.77% of 1,186 vulnerabilities rated critical or high, concentrated in broken access control, injection, and authentication failures [raw/ai--arxiv-2606-23130-insecurity-of-vibe-coded-apps.md]. That source does not break results down by framework (thin spot).
- Vendor scans of Supabase-backed vibe-coded apps report unauthenticated deletes, readable tables, keys compiled into Next.js bundles, missing CSP, and served source maps [raw/ai--vendor-scans-of-vibe-coded-apps-2026.md]. Vendor numbers are self-reported; they justify priorities, never evidence.
- The Next.js docs list the same weak spots as audit targets: the DAL, `"use client"` props, `"use server"` files, `[param]` folders, `proxy.ts` and `route.ts` [raw/next--data-security-guide.md].

## Patterns

The "pattern" column sometimes names a likely reason the code was written that way (for example, silencing an error). That reason is an auditor heuristic, not a sourced statistic; never put it in a finding as fact.

| ID | Pattern (what the agent tends to write) | Fast detection | Owning check |
| --- | --- | --- | --- |
| AI-01 | "Protect the dashboard" implemented as a middleware redirect only; pages and actions trust it | Inventory: middleware with `auth_libs` or redirects, plus actions with `auth_call_seen: false` | NX-PRX-01 |
| AI-02 | Server Actions written like local functions: no session lookup, ids taken from arguments | `use_server_files[].actions[]` where `auth_call_seen` is false and `touches_db` is true | NX-SA-01, NX-SA-02 |
| AI-03 | Auth check copied into the page but not into the action defined on that page (inline `'use server'` under an `auth()` guarded page) | `inline_use_server[]`, then read the inline function body | NX-SA-01 |
| AI-04 | Whole Prisma or Drizzle row passed as a prop (`<Profile user={user} />`) | `rg -n "findUnique\(\{\s*where" app` then read props | NX-DATA-01 |
| AI-05 | Action returns the DB call (`return db.x.update(...)`) | `actions[].returns_db_call` | NX-SA-04 |
| AI-06 | Renaming a server env var to `NEXT_PUBLIC_` to "fix" undefined in a client component | `suspicious_next_public_names[]`, `client_files_reading_private_env[]`, `git log -S NEXT_PUBLIC_` (read-only) | NX-DATA-03 |
| AI-07 | Supabase service role key used in the browser to get past RLS errors | `service_role_refs[]` with `client_file` or `next_public` true | NX-AUTH-03 |
| AI-08 | `supabase.auth.getSession()` used on the server because it is the first method the agent finds | `get_session_server_use[]` | NX-PRX-03 |
| AI-09 | Role kept in Clerk `unsafeMetadata` because it is writable from the client SDK the agent already uses | `unsafe_metadata_use[]` | NX-AUTH-01 |
| AI-10 | Role or `isAdmin` read from `searchParams`, form fields, or a non-HttpOnly cookie | `rg -n -e "searchParams\)?\.?(isAdmin|role|admin)" -e "formData\.get\(['\"](role|isAdmin)" -e "cookies\(\)\)?\.get\(['\"](role|isAdmin)"` | NX-SA-03 |
| AI-11 | Route Handler POST with `await req.json()` passed straight into `create` | `route_handlers[]` mutating without auth, plus `data:\s*body` | NX-RH-01, NX-SA-03 |
| AI-12 | `images.remotePatterns: [{ hostname: '**' }]` added to silence "hostname not configured" errors | `remote_hostname_wildcards` | NX-CFG-01 |
| AI-13 | `Access-Control-Allow-Origin: '*'` added to silence CORS errors on authenticated APIs | `route_handlers[].cors_wildcard`, next.config headers | NX-RH-03 |
| AI-14 | `serverActions.allowedOrigins: ['*']` added after an origin mismatch behind a proxy or tunnel | `server_actions_allowed_origins` | NX-SA-07 |
| AI-15 | `typescript.ignoreBuildErrors` or `eslint.ignoreDuringBuilds` set to ship a broken build | inventory flags | NX-CFG-06 |
| AI-16 | Webhook route that parses JSON and acts with no signature check | `route_handlers[]` with webhook-like paths and `webhook_signature_seen: false` | NX-RH-01 |
| AI-17 | Inverted or short-circuit auth logic (named in the VibeScan vendor report) (`if (session) return`, `if (!user.role === 'admin')`, `||` vs `&&`) | `rg -n -e "if\s*\(\s*session\s*\)\s*(return|throw)" -e "!\w+\.role\s*===" -e "role\s*!==?\s*['\"]admin['\"]\s*\|\|"` then read | NX-SA-01 |
| AI-18 | `dangerouslySetInnerHTML` with markdown or AI output, no sanitizer | `dangerously_set_inner_html[]` (also owned by the react-security pair; report here only when the data comes from a Server Action or Route Handler) | handoff to react-security |
| AI-19 | Hallucinated or typosquatted packages | Compare unusual package names in `package.json` with the npm registry (read-only `npm view <name>`) | handoff to the generic security pass (supply chain) |
| AI-20 | `productionBrowserSourceMaps: true` left on from debugging | inventory flag | NX-DATA-04 |

## How to use

1. After guides 02 to 05, walk this table once against the inventory.
2. For each hit, run the owning check's confirm step. Only the owning check writes a finding.
3. If a pattern repeats across many files (for example AI-02 in 30 actions), write one finding per distinct root cause with all locations, not 30 findings, and say the count in `evidence`.

Sources: [raw/ai--arxiv-2606-23130-insecurity-of-vibe-coded-apps.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/ai--arxiv-2606-23130-insecurity-of-vibe-coded-apps.md), [raw/ai--vendor-scans-of-vibe-coded-apps-2026.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/ai--vendor-scans-of-vibe-coded-apps-2026.md), [raw/next--data-security-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--data-security-guide.md), [raw/auth--clerk-middleware-and-metadata.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--clerk-middleware-and-metadata.md), [raw/auth--supabase-ssr-nextjs.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/auth--supabase-ssr-nextjs.md).

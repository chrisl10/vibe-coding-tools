# 00. Scoping: router, version, deployment target, auth library

Goal: know exactly what you are auditing before you read a single action. Output of this guide is the Scope section of `notes-nextjs-security-wasp-drone.md` and a scan run whose outputs every later guide uses.

## Ground rules (read every time)

- Never modify the audited repository. No installs, no builds, no formatting, no git commands that change state. Read-only git (`git ls-files`, `git log -S`) is fine.
- Write only to the run workspace: `<workspace>/02-security/` (`findings-nextjs-security-wasp-drone.jsonl`, `notes-nextjs-security-wasp-drone.md`, `raw/`). The workspace path is in `intake.json.workspace`.
- Stay inside `intake.json.stacks[]` entries with `id: nextjs`. Their `paths` are your scope. Client-side React patterns belong to `react-security-wasp-drone`; generic OWASP items (SQL injection in a plain helper, dependency CVEs other than `next`) belong to `security-wasp-drone`. Duplicates are allowed (contract rule 4), but do not hunt outside your lane.
- Use `SEC-NEXT-NNN` ids, unique in the run.

## Steps

1. **Read the contract and intake.** Open `audit-my-code-stinger/references/audit-contract.md` (sections 3, 5, 6, 7, 8) and `<workspace>/intake.json`. Note `tier`, `repo.path`, `repo.sha`, and the `nextjs` stack paths.

2. **Run the scanner.** From any directory:
   ```bash
   python3 <skill>/scripts/next_audit_scan.py --repo <repo.path> --out <workspace>/02-security/raw --paths <stack paths...> --id-start 1
   ```
   If other Drones already wrote `SEC-NEXT` ids (they should not, but check `findings-nextjs-security-wasp-drone.jsonl`), pass a higher `--id-start`. Record the printed `next_id`; manual findings continue from it. List both output files under `## Evidence` in your notes file with one-line descriptions; the orchestrator builds `evidence-index.md` (contract section 9).

3. **Record the version per app.** From `next-inventory.json.apps[]`: `declared_range`, `resolved_versions`, `lockfile`. If `resolved_versions` is empty, the version came from the package.json range and every version finding is `possible`; say so in notes. If network is available, check freshness with `npm view next dist-tags` (read-only) and compare with `advisory_table.known_latest`. If newer advisories may exist than the table (research date 2026-09-30), check `https://github.com/vercel/next.js/security/advisories` and note any new one in `notes-nextjs-security-wasp-drone.md`; do not add it to findings unless you can cite its GHSA page.

4. **Determine the router type.** `apps[].router.app_router` and `.pages_router`. Both can be true (migration in progress); audit both. App Router means RSC advisories and Server Actions apply; Pages Router means `getServerSideProps`, `getStaticProps`, and `pages/api` apply.

5. **Determine the deployment target.** Use `apps[].deployment_hints` and read what exists: `vercel.json`, `Dockerfile`, `netlify.toml`, `open-next.config.ts`, `wrangler.*`, custom `server.js`, `next.config` `output: 'standalone'` or `'export'`. Why it matters:
   - Vercel-hosted: protected from CVE-2025-29927 automatically; not affected by several self-hosted cache and WebSocket advisories [raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md] [raw/advisory--2026-rewrites-ssrf-and-other.md].
   - Self-hosted Node or Docker: those advisories apply; multi-instance setups need `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` [raw/next--data-security-guide.md].
   - Custom server: Host header trust matters (CVE-2026-64649) [raw/advisory--2026-server-actions.md].
   - Windows host: CVE-2026-75604 applies [raw/advisory--2026-rewrites-ssrf-and-other.md].
   - `output: 'export'`: no server at runtime, so Server Actions, Route Handlers with dynamic behavior, and middleware do not run in production; most server checks drop out, but secrets in the static bundle matter more.
   If the target is unclear, write the question in notes under "Preconditions left open" and continue.

6. **Identify the auth library.** `apps[].auth_libraries` plus a read of the middleware or proxy file. Map: `next-auth` or `@auth/*` to Auth.js; `@clerk/nextjs` to Clerk; `@supabase/ssr` or `@supabase/auth-helpers-nextjs` to Supabase; `iron-session` or `jose` to custom sessions; `@workos-inc/authkit-nextjs`, `better-auth`, `@kinde-oss/*`, `@stackframe/stack`, `@auth0/nextjs-auth0` to their vendors. Find the one function the app uses to get the current user (for example `auth()`, `currentUser()`, `getClaims()`, `verifySession()`). Every later guide looks for that function.

7. **Find the data access pattern.** Does the app have a DAL (a `server-only` module that every data read goes through), call an external API, or query the database directly in components? The docs recommend one approach, not a mix [raw/next--data-security-guide.md]. Note which, because it changes how you confirm missing auth (a DAL check counts for every caller).

8. **Write the Scope section** of `<workspace>/02-security/notes-nextjs-security-wasp-drone.md` (template in [../references/finding-templates.md](../references/finding-templates.md)): apps, versions and lockfiles, router, deployment target, auth library and its current-user function, data access pattern, scan summary counts, and open preconditions.

9. **Plan the read.** Use the inventory summary to size the work: `server_actions_exported`, `route_handlers`, `pages_api_routes`, `middleware_proxy_files`, `use_client_files`. If there are more than about 60 actions or handlers, read every one flagged `auth_call_seen: false` or `touches_db: true` first, then sample the rest and record the sampling in `metrics-nextjs-security-wasp-drone.json.coverage.caps`.

Then continue with [01-version-and-advisory-check.md](01-version-and-advisory-check.md).

## Sources

[raw/next--data-security-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--data-security-guide.md), [raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md), [raw/advisory--2026-rewrites-ssrf-and-other.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-rewrites-ssrf-and-other.md), [raw/advisory--2026-server-actions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-server-actions.md), [raw/next--npm-dist-tags-2026-09-30.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--npm-dist-tags-2026-09-30.md).

# Finding, metrics, and notes templates (contract 1.0)

Loaded by [guides/06-writing-findings.md](../guides/06-writing-findings.md). The contract lives at `../../audit-my-code-stinger/references/audit-contract.md` (sections 5 to 8). These templates are examples; the contract wins on any disagreement.

## Severity mapping used by this skill

| Contract severity | Next.js examples |
| --- | --- |
| critical | Installed version in the CVE-2025-55182 range with App Router; service role key or live secret in the client bundle; unauthenticated action that deletes or exports data; per-user data cached and served to everyone; middleware-only auth on a CVE-2025-29927 version |
| high | Server Action or Route Handler with no auth or no ownership check; middleware-only auth on a patched version; SSRF through rewrites, remotePatterns, or a user-supplied `fetch`; `allowedOrigins: ['*']` with cookie sessions; `getSession()` trusted on the server; `unsafeMetadata` roles |
| medium | Cookie-authenticated Route Handler without Origin check behind SameSite=Lax; open redirect; broad but not `**` remotePatterns; inline action capturing private values; advisory match whose precondition is not yet confirmed (confidence possible) |
| low | Missing security headers; `poweredByHeader` on; production source maps with no secrets; missing `server-only` on the DAL; dev-server-only advisories |
| info | Current, patched version; `middleware.ts` on 16.x; taint APIs in use |

Rule 3 of the contract: `confidence: possible` caps severity at `medium`. The scan script already applies this for advisories whose preconditions it cannot evaluate; when the Drone confirms the precondition, it rewrites the line with the advisory's severity and `confidence: likely` (or `confirmed` if reproduced).

## Example lines

Server Action without ownership check:
```json
{"id":"SEC-NEXT-012","dimension":"security","source":"nextjs-security-wasp-drone","title":"Any signed-in user can delete any other user's project","severity":"high","confidence":"likely","locations":[{"path":"app/projects/actions.ts","line_start":8,"line_end":14}],"evidence":"export async function deleteProject(id: string) {\n  const session = await auth()\n  if (!session) throw new Error('Unauthorized')\n  await db.project.delete({ where: { id } })\n}","why_it_matters":"Server Actions are public POST endpoints. The action checks that someone is logged in but never checks that the project belongs to them, so a user can delete other customers' projects by sending a different id.","remediation":"In app/projects/actions.ts, delete with deleteMany({ where: { id, ownerId: session.user.id } }) and treat count 0 as not found, or move the check into a server-only data access function.","effort":"S","refs":["CWE-639","OWASP A01:2025","guides/03-server-actions-and-route-handlers.md"],"verified_by":"Read the action and its only caller; no RLS or DAL ownership filter exists (prisma schema has no row policies).","tags":["nextjs","server-action","idor"]}
```

Middleware-only authorization:
```json
{"id":"SEC-NEXT-004","dimension":"security","source":"nextjs-security-wasp-drone","title":"The admin area is protected only by middleware, which has been bypassed by several Next.js bugs","severity":"high","confidence":"likely","locations":[{"path":"middleware.ts","line_start":1,"line_end":12},{"path":"app/admin/users/page.tsx","line_start":3,"line_end":9}],"evidence":"middleware.ts: if (!token) return NextResponse.redirect(new URL('/login', req.url))\nmatcher: ['/admin/:path*']\napp/admin/users/page.tsx: const users = await db.user.findMany()  // no session check","why_it_matters":"If any request slips past middleware, the page lists every user. Next.js has published at least six middleware bypass advisories since March 2025, and the official docs say middleware should not be the only defense.","remediation":"Add a server-only verifySession() and call it inside getUsers() (or at the top of app/admin/users/page.tsx and every admin Server Action), checking the admin role there.","effort":"M","refs":["CWE-288","CWE-862","OWASP A01:2025","CVE-2025-29927","CVE-2026-44575","guides/02-proxy-middleware-and-auth-boundaries.md"],"verified_by":"Read the middleware, the page, and lib/db.ts; no other auth call on this path.","tags":["nextjs","middleware","authz"]}
```

Secret in client bundle (note redaction):
```json
{"id":"SEC-NEXT-002","dimension":"security","source":"nextjs-security-wasp-drone","title":"The Supabase admin key is shipped to every visitor's browser","severity":"critical","confidence":"confirmed","locations":[{"path":"lib/supabase-browser.ts","line_start":3,"line_end":3},{"path":".env.production","line_start":4,"line_end":4}],"evidence":"lib/supabase-browser.ts:3  createClient(url, process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!)\n.env.production:4  NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=eyJh****","why_it_matters":"NEXT_PUBLIC_ values are copied into the JavaScript bundle at build time. The service role key ignores Row Level Security, so anyone can read and change every table.","remediation":"Rotate the service role key in Supabase now. Rename it to SUPABASE_SERVICE_ROLE_KEY, use it only in a server-only module, and give the browser client the publishable key.","effort":"S","refs":["CWE-798","CWE-200","OWASP A04:2025","guides/04-data-exposure-and-caching.md"],"verified_by":"Found the same prefix in .next/static/chunks/app/layout-*.js of the local build output.","tags":["nextjs","secrets","supabase"]}
```

## metrics-nextjs-security-wasp-drone.json fragment

The security dimension has several writers (the generic `security-wasp-drone`, this Drone, and other framework Drones). Write your measures with `nextjs_` keys and let the orchestrator merge. Compute this file's own `verdict` with contract section 8; the orchestrator merges every security Drone's metrics file with `merge_security.py`.

```json
{
  "dimension": "security",
  "verdict": "at-risk",
  "summary": "Next.js 15.1.3 is missing patches for a critical remote code execution flaw, and 4 of 11 Server Actions change data without checking who is calling.",
  "measures": [
    {"key": "nextjs_version_current", "label": "Next.js version vs newest patched release in line", "value": "15.1.3 vs 15.5.27", "unit": "", "band": "critical", "threshold": "any critical or high advisory match is critical", "source": "next_audit_scan.py + GHSA table 2026-09-30"},
    {"key": "nextjs_actions_without_auth", "label": "Server Actions without an auth check (confirmed by reading)", "value": 4, "unit": "count", "band": "at-risk", "threshold": "0 healthy, 1 or more at-risk", "source": "manual review"},
    {"key": "nextjs_route_handlers_mutating_without_auth", "label": "Mutating Route Handlers without auth (confirmed)", "value": 1, "unit": "count", "band": "at-risk", "threshold": "0 healthy", "source": "manual review"},
    {"key": "nextjs_middleware_only_auth", "label": "Protected areas whose only check is middleware", "value": 1, "unit": "count", "band": "at-risk", "threshold": "0 healthy", "source": "manual review"}
  ],
  "coverage": {"files_scanned": 412, "lines_scanned": 38110, "skipped": ["node_modules/", ".next/"], "caps": ["next_audit_scan.py skips files over 2 MB", "next.config values parsed by regex; configs assembled in helper modules were read by hand"]}
}
```

## notes-nextjs-security-wasp-drone.md sections

```markdown
# Next.js security notes (nextjs-security-wasp-drone)

## Scope
Apps, versions, router type, deployment target, auth library (from guide 00).

## Not confirmed
- Suspicions that could not be shown with evidence (contract rule 1). One line each, with what would confirm it.

## Preconditions left open
- Advisory matches where the precondition needs the owner (Windows hosting, AVIF uploads, self-hosted vs Vercel).

## Handoffs
- Client-side React patterns to react-security-wasp-drone; generic OWASP items to security-wasp-drone.

## Coverage limits
- Regex-based inventory; files over 2 MB skipped; dynamic config not parsed.
```

Sources: contract file (`../../audit-my-code-stinger/references/audit-contract.md`), [raw/standard--cwe-entries.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/standard--cwe-entries.md), [raw/standard--owasp-top-10-2025.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/standard--owasp-top-10-2025.md), [raw/next--data-security-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--data-security-guide.md), [raw/next--source-maps-powered-by-env-vars.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--source-maps-powered-by-env-vars.md).

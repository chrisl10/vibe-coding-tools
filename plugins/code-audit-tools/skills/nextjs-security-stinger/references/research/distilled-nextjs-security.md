# Distilled: Next.js security audit knowledge (research window 2026-03-30 to 2026-09-30)

Every claim ends with its raw source. Older sources are allowed only where labeled (canonical advisories, CWE).

## 1. Version state and support

| Fact | Source |
| --- | --- |
| Newest releases on npm at 2026-09-30: 16.3.8 (latest), 15.5.27 (backport), 14.2.35, 13.5.11 | [raw/next--npm-dist-tags-2026-09-30.md] |
| 16.x is Active LTS (released 2025-10-21); 15.x Maintenance LTS for two years after 2024-10-21; 14.x and older unsupported | [raw/next--support-policy.md] |
| Out-of-policy patches happen "in rare circumstances" (example: 14.2.35 for the RSC DoS follow-up) | [raw/next--support-policy.md] [raw/advisory--dec-2025-to-2026-rsc-followups.md] |
| From 2026, advisory ranges read like `>=13.0.0 < 15.5.21` with no 13.x or 14.x patch | [raw/advisory--ghsa-index-vercel-next-js.md] |
| Next.js vendors React for the App Router, so RSC exposure follows the `next` version; this is why a separate Next.js CVE (CVE-2025-66478) was issued, later rejected as a duplicate of CVE-2025-55182 | [raw/advisory--cve-2025-55182-react2shell-rsc-rce.md] |
| 69 published advisories exist for vercel/next.js; 61 published 2024 or later are modeled | [raw/advisory--ghsa-index-vercel-next-js.md] |
| Several 2026-09-30 advisories list the patched version as `16.3.?` or `15.5.?`, so the fix version is unknown from source | [raw/advisory--ghsa-index-vercel-next-js.md] |

## 2. Headline advisories

| CVE / GHSA | Class | Affected to first patched | Precondition | Source |
| --- | --- | --- | --- | --- |
| CVE-2025-29927 (older than 12 months, canonical) | Middleware auth bypass via `x-middleware-subrequest` | 15.x < 15.2.3, 14.x < 14.2.25, 13.x < 13.5.9, 12.x < 12.3.5 | Auth in middleware; Vercel auto-protected | [raw/advisory--cve-2025-29927-middleware-subrequest-bypass.md] |
| CVE-2025-55182 (alias CVE-2025-66478) | RSC deserialization RCE, CVSS 10.0, CWE-502 | 15.0 to 16.0 lines, fixed 15.0.5, 15.1.9, 15.2.6, 15.3.6, 15.4.8, 15.5.7, 16.0.7; 14.3 canaries from canary.77 | App Router; no workaround | [raw/advisory--cve-2025-55182-react2shell-rsc-rce.md] |
| CVE-2025-55183 | Server Function source disclosure | fixed 15.x per minor (15.5.8), 16.0.9 | App Router | [raw/advisory--dec-2025-to-2026-rsc-followups.md] |
| CVE-2025-55184, CVE-2025-67779, CVE-2026-23864, CVE-2026-23869, CVE-2026-23870 | RSC DoS series | last fixes 15.5.16, 16.2.5 | App Router | [raw/advisory--dec-2025-to-2026-rsc-followups.md] |
| CVE-2026-44573, 44574, 44575, 45109, 64642 | Middleware / Proxy bypasses | last fixes 15.5.18, 16.2.11 | Pages i18n, dynamic routes, prefetch variants, Turbopack single locale | [raw/advisory--2026-middleware-proxy-bypasses.md] |
| CVE-2026-27978 | `Origin: null` bypasses Server Action CSRF | 16.0.1 to 16.1.6 | Server Actions | [raw/advisory--2026-server-actions.md] |
| CVE-2026-64643 | Server Action and `use cache` IDs disclosed to unauthenticated users | < 15.5.21, < 16.2.11 | App Router + Server Actions | [raw/advisory--2026-server-actions.md] |
| CVE-2026-64649 | SSRF in Server Actions with unpinned Host | 14.1.1 to < 15.5.21, < 16.2.11 | Custom server or unpinned host | [raw/advisory--2026-server-actions.md] |
| CVE-2026-64645 | SSRF and open redirect via dynamic hostname in rewrites/redirects | 12.0 to < 15.5.21, < 16.2.11 | `:param` in destination hostname | [raw/advisory--2026-rewrites-ssrf-and-other.md] |
| GHSA-2xp9-vwfh-vxw4 (no CVE at fetch) | RCE in Image Optimization via AVIF (libheif in sharp) | < 15.5.24, 16.x < 16.3.3 | Optimizer used on AVIF input | [raw/advisory--2026-image-optimizer.md] |
| CVE-2026-75604 | RCE on Windows-hosted servers, CWE-22 | 13.4 to < 15.5.24, < 16.3.3 | Windows filesystem | [raw/advisory--2026-rewrites-ssrf-and-other.md] |
| CVE-2026-94545 | RCE in Node `ImageResponse` (`next/og`) | 16.2.0 to < 16.3.6 | Attacker values inside SVG | [raw/advisory--2026-rewrites-ssrf-and-other.md] |
| CVE-2026-94483 | SSRF in Image Optimization via allow-listed hosts | 16.x, fix not stated | `images.remotePatterns` configured | [raw/advisory--2026-image-optimizer.md] |
| GHSA-h694-7cp9-m8p3, CVE-2026-94544 | `use cache` cross-param leak, Draft Mode leak | 16.3.0 and later, fix not stated | Cache Components (+ Draft Mode) | [raw/advisory--2026-cache-poisoning-and-cache-leaks.md] |
| CVE-2026-44581 | XSS with CSP nonces behind shared caches | < 15.5.16, < 16.2.5 | Nonce CSP | [raw/advisory--2026-rewrites-ssrf-and-other.md] |

Full table: `references/advisory-table.md`, built from [raw/advisory--ghsa-index-vercel-next-js.md].

## 3. Middleware and Proxy

- Next.js 16 renamed `middleware.ts` to `proxy.ts` (Node.js runtime); `middleware.ts` remains for Edge use and is deprecated [raw/next--next-16-release-proxy-rename.md] [raw/next--proxy-file-convention.md].
- Without a matcher, Proxy runs on every request; matcher values must be constants or they are ignored [raw/next--proxy-file-convention.md].
- Server Functions are POSTs to the page that uses them, so excluding a path from the matcher also skips its actions; "Always verify authentication and authorization inside each Server Function" [raw/next--proxy-file-convention.md].
- Proxy should do optimistic cookie checks only and "should not be your only line of defense" [raw/next--authentication-guide.md].
- Every 2026 middleware bypass advisory's workaround is to authorize in the route or data path [raw/advisory--2026-middleware-proxy-bypasses.md].
- Clerk, Auth.js, and Supabase docs all say the same for their middleware helpers [raw/auth--clerk-middleware-and-metadata.md] [raw/auth--authjs-protecting-resources.md] [raw/auth--supabase-ssr-nextjs.md].

## 4. Server Actions and Route Handlers

| Fact | Source |
| --- | --- |
| Every exported Server Action is reachable by direct POST; treat it as an untrusted entry point | [raw/next--data-security-guide.md] [raw/next--server-actions-guide-and-config.md] |
| Page-level auth does not extend to actions defined in the page | [raw/next--data-security-guide.md] |
| Built-ins: Origin vs Host check, 1MB body limit, encrypted action IDs, dead code elimination, closure encryption | [raw/next--server-actions-guide-and-config.md] |
| `allowedOrigins` adds trusted origins (wildcards allowed); default same origin only | [raw/next--server-actions-guide-and-config.md] |
| Closure values are sent to the client encrypted; do not rely on encryption alone | [raw/next--data-security-guide.md] |
| `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`: base64, decodes to 16, 24, or 32 bytes; keep stable across instances | [raw/next--data-security-guide.md] [raw/next--server-actions-guide-and-config.md] |
| Schema validation checks shape, not ownership; derive identity from the session | [raw/next--server-actions-guide-and-config.md] |
| Return only what the UI needs, not raw records | [raw/next--data-security-guide.md] |
| Route Handlers: treat as public API endpoints; GET became dynamic by default in 15.0 | [raw/next--authentication-guide.md] [raw/next--route-handlers.md] |
| The `route.js` reference describes no built-in CSRF or Origin check (derived from absence; thin spot) | [raw/next--route-handlers.md] |

## 5. Data exposure and caching

| Fact | Source |
| --- | --- |
| DAL: server-only, does authorization, returns minimal DTOs; only the DAL reads `process.env` | [raw/next--data-security-guide.md] |
| Passing a full row to a Client Component exposes every field | [raw/next--data-security-guide.md] |
| `server-only` import causes a build error on client import | [raw/next--data-security-guide.md] |
| Taint APIs are experimental, cloned objects are untainted, never the only layer | [raw/react--taint-apis.md] |
| `NEXT_PUBLIC_` values are inlined into client JS at build time | [raw/next--source-maps-powered-by-env-vars.md] |
| Production source maps off by default; when enabled, Next.js serves them | [raw/next--source-maps-powered-by-env-vars.md] |
| `use cache` key = build id + function id + arguments (closures included); output reused across requests; no `cookies()`/`headers()` inside | [raw/next--use-cache-and-unstable-cache.md] |
| File-level `use cache` exports are callable from Client Components like Server Functions | [raw/next--use-cache-and-unstable-cache.md] |
| `unstable_cache` replaced by `use cache` in 16; closures must be in `keyParts` | [raw/next--use-cache-and-unstable-cache.md] |
| `generateStaticParams` pages are built once for everyone; `dynamicParams = false` 404s unlisted params | [raw/next--generate-static-params-and-dynamic-params.md] |
| Static routes that share data between users need Proxy gating, the DAL does not run at request time for them | [raw/next--authentication-guide.md] |

## 6. Config and headers

| Fact | Source |
| --- | --- |
| remotePatterns: omitted fields imply `**`; `**` hostname wildcard only at the start | [raw/next--image-config.md] |
| `domains` deprecated since 14 for being unable to restrict protocol, port, path | [raw/next--image-config.md] |
| `dangerouslyAllowLocalIP` (16.0+) opens SSRF to local network; redirects up to `maximumRedirects` need not match remotePatterns | [raw/next--image-config.md] |
| `dangerouslyAllowSVG` needs `contentDispositionType: 'attachment'` and an image CSP with `script-src 'none'; sandbox` | [raw/next--image-config.md] |
| `has` captures and path params flow into `destination` | [raw/next--headers-redirects-config.md] |
| Documented security headers: HSTS, X-Frame-Options (superseded by `frame-ancestors`), Permissions-Policy, nosniff, Referrer-Policy, CSP | [raw/next--headers-redirects-config.md] |
| `x-powered-by` on by default | [raw/next--source-maps-powered-by-env-vars.md] |
| Nonce CSP: per-request nonce in Proxy, `strict-dynamic`, `unsafe-eval` dev only, requires dynamic rendering, incompatible with PPR | [raw/next--csp-guide.md] |

## 7. Auth libraries

| Library | Key fact | Source |
| --- | --- | --- |
| Clerk | `clerkMiddleware()` protects nothing by default; protect near the resource; `createRouteMatcher` marked deprecated at fetch; `unsafeMetadata` is frontend-writable | [raw/auth--clerk-middleware-and-metadata.md] |
| Supabase SSR | Never trust `getSession()` in server code; use `getClaims()` or `getUser()`; browser uses the publishable key | [raw/auth--supabase-ssr-nextjs.md] |
| Auth.js | `auth()` in components, handlers, actions; proxy `authorized` callback is not enough alone | [raw/auth--authjs-protecting-resources.md] |

## 8. AI-generated app evidence

- 91.0% of 200 audited vibe-coded apps had at least one vulnerability, mostly broken access control, injection, authentication failures [raw/ai--arxiv-2606-23130-insecurity-of-vibe-coded-apps.md].
- Vendor scans: unauthenticated database writes, keys compiled into bundles, missing CSP, source maps served, inverted auth logic [raw/ai--vendor-scans-of-vibe-coded-apps-2026.md].

## 9. Standards

- OWASP Top 10:2025 categories A01 to A10 as listed [raw/standard--owasp-top-10-2025.md].
- CWE names used in this skill (timeless standard) [raw/standard--cwe-entries.md].

## Conflicts and thin spots

- GHSA-7m27-7ghc-44w9: range says `< 15.1.1` but patched list says 15.1.2. The range is used [raw/advisory--2026-server-actions.md].
- GHSA-2xp9-vwfh-vxw4 writes its 16.x range as `< 16.3.3` with no lower bound; read as the 16.x line [raw/advisory--2026-image-optimizer.md].
- Seven advisories published 2026-09-30 have no stated fix version; the scanner marks them `possible` and the Drone must re-check the advisory page before reporting [raw/advisory--ghsa-index-vercel-next-js.md].
- Several advisories have no CWE field; the CWE in `next-advisories.json` is inferred from the title (marked in each `note`) [raw/advisory--ghsa-index-vercel-next-js.md].
- No primary source quantifies AI-code failure rates for Next.js specifically [raw/ai--arxiv-2606-23130-insecurity-of-vibe-coded-apps.md].
- Route Handler CSRF behavior is inferred from the absence of a documented check, not from an explicit statement [raw/next--route-handlers.md].
- Clerk's deprecation of `createRouteMatcher` is taken from the docs page at fetch; older Clerk docs recommended it. Apps on older SDKs may legitimately use it [raw/auth--clerk-middleware-and-metadata.md].

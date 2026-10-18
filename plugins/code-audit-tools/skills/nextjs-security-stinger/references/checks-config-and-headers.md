# Checks: next.config, images, rewrites, redirects, headers, CSP

Loaded by [guides/05-config-and-headers.md](../guides/05-config-and-headers.md). Start from the scan inventory `apps[].next_config` (it parses `next.config.{ts,mjs,js,cjs,mts}` with regexes, so read the file to confirm every value; configs built in helper functions or spread from other modules will not be seen).

---

## NX-CFG-01: `images.remotePatterns` too broad (SSRF and cost abuse), deprecated `domains`

**What.** `*` matches one segment or subdomain, `**` any number at the start of a hostname or end of a path; omitting `protocol`, `port`, `pathname`, or `search` implies `**`, which "may allow malicious actors to optimize urls you did not intend" [raw/next--image-config.md]. CVE-2026-94483 (16.x, patched version not stated at fetch) is SSRF through allow-listed hosts whose DNS the app does not control; the workaround is auditing remotePatterns [raw/advisory--2026-image-optimizer.md]. `domains` is deprecated since 14 and cannot restrict protocol, port, or path [raw/next--image-config.md].

**Detection.** Inventory `remote_hostnames`, `remote_hostname_wildcards`, `remote_url_objects`, `images_domains_deprecated`.
```bash
rg -n -U "remotePatterns[\s\S]{0,800}" -g 'next.config.*' .
rg -n -e "hostname\s*:\s*['\"]\*\*?['\"]" -e "hostname\s*:\s*['\"]\*\*\.[a-z0-9.-]+['\"]" -e "domains\s*:\s*\[" -g 'next.config.*' .
```
**Confirm.** List each pattern and what it allows. Confirmed broad when: hostname is `**` or `*`; a wildcard covers a shared host where anyone can publish files (`**.amazonaws.com`, `**.cloudfront.net`, `**.vercel.app`, `**.githubusercontent.com`, `**.supabase.co` without a project-specific path); `pathname` is missing for a multi-tenant host. Check `dangerouslyAllowLocalIP: true` (allows private network targets) and `maximumRedirects` (redirect targets do not need to match remotePatterns) [raw/next--image-config.md].

**Severity.** `hostname: '**'` or `'*'`: `high` on 16.x before a stated fix for CVE-2026-94483 or when `dangerouslyAllowLocalIP` is true (SSRF to internal addresses), otherwise `medium` (any internet image can be optimized at your cost, and it widens the optimizer's attack surface, which had a critical AVIF RCE in 2026). Shared-host wildcard: `medium`. `domains` only: `low`.

**Vulnerable.**
```js
images: { remotePatterns: [{ hostname: '**' }] }
```
**Fixed.**
```js
images: { remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com', pathname: '/uploads/**', search: '' }] }
```
**Refs.** CWE-918, CWE-770, CVE-2026-94483, OWASP A02:2025.

---

## NX-CFG-02: `dangerouslyAllowSVG` without CSP and attachment disposition

**What.** SVG can carry scripts; when enabling it, set `contentDispositionType: 'attachment'` and `contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;"` [raw/next--image-config.md]. CVE-2026-64644 is an SVG-based DoS in the optimizer [raw/advisory--2026-image-optimizer.md].

**Detection.** Inventory `dangerously_allow_svg`, `images_csp_set`, `content_disposition_inline`.

**Confirm.** `dangerouslyAllowSVG: true` and either no `contentSecurityPolicy` under `images` or `contentDispositionType: 'inline'`, and SVGs can come from user uploads or broad remote patterns.

**Severity.** User-controlled SVGs served inline without the image CSP: `high` (stored XSS on your origin). SVG allowed but sources are trusted static assets: `low`.

**Fixed.**
```js
images: { dangerouslyAllowSVG: true, contentDispositionType: 'attachment', contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;" }
```
**Refs.** CWE-79, OWASP A05:2025.

---

## NX-CFG-03: Rewrites or redirects with a destination hostname built from request input (SSRF, open redirect)

**What.** CVE-2026-64645: a `rewrites()` or `redirects()` destination that puts a `:param` or `has` capture in the hostname can be pointed at any host, giving SSRF for rewrites and open redirect for redirects; fixed in 15.5.21 and 16.2.11, workaround: never build hostnames from input, constrain captures to `[a-z0-9-]+` [raw/advisory--2026-rewrites-ssrf-and-other.md]. `has` named captures flow into `destination` [raw/next--headers-redirects-config.md].

**Detection.** Inventory `dynamic_host_destinations`, `rewrites_fn`, `redirects_fn`.
```bash
rg -n -e "destination\s*:\s*['\"`]https?://[^/'\"]*:[a-zA-Z_]" -e "destination\s*:\s*['\"`]:[a-zA-Z_]" -e "\(\?<\w+>\.\*\)" -g 'next.config.*' .
# Code-level open redirects in Route Handlers, Server Actions, middleware:
rg -n -e "redirect\(\s*(searchParams\.get|req\.nextUrl\.searchParams\.get|formData\.get|params\.)" -e "NextResponse\.redirect\(\s*new URL\(\s*(searchParams|req\.nextUrl\.searchParams)\.get" -e "(callbackUrl|returnTo|next|redirect_uri|redirectTo)" .
```
**Confirm.** Config: the hostname part of `destination` contains a parameter, or a destination is entirely a parameter. Code: a redirect target comes from the request and is not checked to be a relative path (`startsWith('/') && !startsWith('//')`) or an allowlisted origin.

**Severity.** Dynamic-host rewrite on a vulnerable version: `high` (advisory). Dynamic-host rewrite on a patched version with unconstrained captures: `medium`. Open redirect only: `medium` (used for phishing and OAuth token theft when a login flow passes `callbackUrl`), `low` if it only redirects within the same site.

**Vulnerable.**
```js
async rewrites() { return [{ source: '/:tenant', destination: 'https://:tenant.api.example.com' }] }
```
**Fixed.**
```js
async rewrites() { return [{ source: '/:tenant([a-z0-9-]{1,40})', destination: 'https://:tenant.api.example.com' }] }
```
and in code: `const to = sp.get('next'); redirect(to?.startsWith('/') && !to.startsWith('//') ? to : '/')`

**Refs.** CWE-918, CWE-601, CVE-2026-64645, OWASP A01:2025.

---

## NX-CFG-04: Missing security headers, `X-Powered-By` left on

**What.** Next.js documents HSTS, `X-Frame-Options` (superseded by CSP `frame-ancestors`), `Permissions-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and CSP via `headers()` [raw/next--headers-redirects-config.md]. `x-powered-by` is sent by default until `poweredByHeader: false` [raw/next--source-maps-powered-by-env-vars.md]. Vendor scans found missing CSP and frame protection on most vibe-coded apps [raw/ai--vendor-scans-of-vibe-coded-apps-2026.md].

**Detection.** Inventory `headers_fn`, `csp_in_config`, `hsts_in_config`, `powered_by_header_disabled`; also check middleware or proxy (CSP is often set there) and platform config (`vercel.json` `headers`, nginx, Cloudflare).
```bash
rg -n -e "Strict-Transport-Security" -e "Content-Security-Policy" -e "X-Frame-Options" -e "frame-ancestors" -e "X-Content-Type-Options" -e "Referrer-Policy" -e "Permissions-Policy" -e "poweredByHeader" .
```
**Confirm.** Header absent in next.config, proxy, and deployment config. If a deployed URL is in scope and allowed, `curl -sI` it to confirm (read-only GET).

**Severity.** Missing headers are `low` (contract example "Missing security header"). Missing `frame-ancestors`/`X-Frame-Options` on pages with one-click sensitive actions: `medium` (clickjacking). `poweredByHeader` on: `info` to `low`.

**Fixed.** A `headers()` block in next.config on `source: '/:path*'` with the documented values.

**Refs.** CWE-693, CWE-1021, OWASP A02:2025.

---

## NX-CFG-05: CSP that does not protect (unsafe-inline, unsafe-eval in production, nonce misuse)

**What.** The nonce pattern generates a fresh nonce per request in Proxy, uses `'strict-dynamic'`, and adds `'unsafe-eval'` only in development; "`unsafe-eval` is not required for production" [raw/next--csp-guide.md]. Nonces force dynamic rendering and are incompatible with PPR [raw/next--csp-guide.md]. CVE-2026-44581: malformed nonce values from request headers caused stored XSS behind shared caches before 15.5.16 and 16.2.5; workaround strips inbound `Content-Security-Policy` request headers [raw/advisory--2026-rewrites-ssrf-and-other.md].

**Detection.**
```bash
rg -n -e "unsafe-eval" -e "unsafe-inline" -e "nonce" -e "strict-dynamic" -g 'middleware.*' -g 'proxy.*' -g 'next.config.*' .
rg -n -e "nonce\s*=\s*['\"][A-Za-z0-9+/=]{8,}['\"]" -e "const nonce\s*=\s*['\"]" .
```
**Confirm.** `'unsafe-eval'` present without an `isDev` guard; a static or reused nonce; `script-src` with `'unsafe-inline'` and no nonce or hash on an app that renders user content; nonce CSP on a version inside the CVE-2026-44581 range behind a CDN.

**Severity.** Static nonce or `unsafe-eval` in production: `medium` when the app renders user content, else `low`. Vulnerable version with nonces behind a shared cache: `medium` (advisory).

**Refs.** CWE-693, CWE-79, CVE-2026-44581, OWASP A02:2025.

---

## NX-CFG-06: Build safety switches turned off (`ignoreBuildErrors`, `ignoreDuringBuilds`)

**What.** Not a vulnerability by itself, but a strong signal in AI-generated apps that type errors (often in auth or validation code) were silenced to get a deploy through. Pattern taken from the AI failure catalog [ai-failure-patterns.md](ai-failure-patterns.md).

**Detection.** Inventory `typescript_ignore_build_errors`, `eslint_ignore_during_builds`.

**Severity.** `low`. Mention in `notes-nextjs-security-wasp-drone.md` and raise attention on files with `// @ts-ignore` or `as any` near auth code.

**Refs.** OWASP A06:2025.

---

## NX-CFG-07: Dev-only exposure: `allowedDevOrigins`, dev server reachable from a network

**What.** Dev-server advisories (CVE-2026-94486 dev MCP endpoint, CVE-2026-27977 `Origin: null` bypass of `allowedDevOrigins`, CVE-2025-48068) affect `next dev` only [raw/advisory--2026-rewrites-ssrf-and-other.md].

**Detection.** Inventory `allowed_dev_origins`; `package.json` scripts that run `next dev -H 0.0.0.0` in Docker or a shared environment.
```bash
rg -n -e "next dev[^\"']*(-H|--hostname)\s*0\.0\.0\.0" -e "allowedDevOrigins" .
```
**Severity.** `low` (the developer's machine and source are at risk, not production users). `medium` when a dev server is deployed as the production process (`"start": "next dev"`).

**Refs.** CWE-1385, OWASP A02:2025.

---

## NX-CFG-08: `next/og` `ImageResponse` with request input (CVE-2026-94545) and `beforeInteractive` with untrusted input (CVE-2026-44580)

**What.** Node.js `ImageResponse` with attacker-controlled values inside SVG content, attributes, or styles leads to RCE on 16.2.0 to 16.3.5; Edge runtime not affected; workaround: keep user input out of SVG [raw/advisory--2026-rewrites-ssrf-and-other.md]. `next/script` `beforeInteractive` with untrusted input was an XSS before 15.5.16 and 16.2.5.

**Detection.** Inventory `next_og_image_response[]` (`edge_runtime`, `reads_request_input`), `before_interactive_scripts[]`.
```bash
rg -n -U --pcre2 "new ImageResponse\([\s\S]{0,1500}?<svg" -g '**/*.{tsx,jsx}' .
```
**Confirm.** Request-derived values (`searchParams`, `params`, `request.url`) are interpolated into `<svg>` children, attributes, or `style` inside an `ImageResponse` on the Node runtime.

**Severity.** On an affected version with confirmed request input in SVG: `critical`. On a patched version: `low` (note that the pattern was the trigger).

**Refs.** CVE-2026-94545, CVE-2026-44580, CWE-79, OWASP A03:2025.

---

Sources: raw/next--image-config.md, raw/next--headers-redirects-config.md, raw/next--csp-guide.md, raw/next--source-maps-powered-by-env-vars.md, raw/advisory--2026-image-optimizer.md, raw/advisory--2026-rewrites-ssrf-and-other.md, raw/ai--vendor-scans-of-vibe-coded-apps-2026.md, raw/standard--cwe-entries.md, raw/standard--owasp-top-10-2025.md.

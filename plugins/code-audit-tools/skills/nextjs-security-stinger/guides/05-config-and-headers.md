# 05. Config and headers

Goal: audit `next.config.*` and response headers for settings that widen the attack surface. Loads [../references/checks-config-and-headers.md](../references/checks-config-and-headers.md) (NX-CFG-01 to 08).

## Steps

1. **Read next.config by hand.** The inventory (`apps[].next_config`) is a regex summary. Open the file and any module it imports or spreads (shared config packages in monorepos). Write the relevant keys into notes: `images`, `rewrites`, `redirects`, `headers`, `serverActions`, `productionBrowserSourceMaps`, `poweredByHeader`, `output`, `i18n`, `cacheComponents`, `experimental.taint`, `typescript.ignoreBuildErrors`, `eslint.ignoreDuringBuilds`, `allowedDevOrigins`.

2. **Images (NX-CFG-01, NX-CFG-02).** List every `remotePatterns` entry and spell out what it allows. Omitted fields mean `**`; `**` hostnames, shared-host wildcards, `dangerouslyAllowLocalIP: true`, and `domains` are the targets [raw/next--image-config.md]. For `dangerouslyAllowSVG`, require `contentDispositionType: 'attachment'` and the image CSP [raw/next--image-config.md]. On 16.x, connect broad patterns to CVE-2026-94483 (SSRF through allow-listed hosts) [raw/advisory--2026-image-optimizer.md].

3. **Rewrites and redirects (NX-CFG-03).** Look for `:param` or named captures in the hostname of a `destination` (CVE-2026-64645 [raw/advisory--2026-rewrites-ssrf-and-other.md]) and for whole-URL destinations from params. Then grep code for open redirects through `redirect()`, `NextResponse.redirect`, and `callbackUrl`, `returnTo`, `next`, `redirectTo` parameters.

4. **Headers (NX-CFG-04).** Check HSTS, `frame-ancestors` or `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` in next.config `headers()`, the proxy file, and platform config (`vercel.json`, nginx, Cloudflare) before calling one missing [raw/next--headers-redirects-config.md]. `poweredByHeader` defaults to on [raw/next--source-maps-powered-by-env-vars.md]. If a deployed URL is in the intake and the user allowed it, confirm with one read-only `curl -sI` and save output to `raw/`.

5. **CSP (NX-CFG-05).** If a CSP exists, check nonce generation (fresh per request), `strict-dynamic`, and that `'unsafe-eval'` is dev-only [raw/next--csp-guide.md]. On versions below 15.5.16 or 16.2.5 with nonce CSP behind a CDN, connect to CVE-2026-44581.

6. **Build switches (NX-CFG-06)** and **dev exposure (NX-CFG-07).**

7. **`next/og` and `beforeInteractive` (NX-CFG-08).** For each `next_og_image_response[]` entry on the Node runtime that reads request input, read how values reach the SVG [raw/advisory--2026-rewrites-ssrf-and-other.md].

8. **Sweep AI patterns** AI-12, AI-13, AI-14, AI-15, AI-20 from [../references/ai-failure-patterns.md](../references/ai-failure-patterns.md), then write findings per guide 06.

## Sources

[raw/next--image-config.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--image-config.md), [raw/next--headers-redirects-config.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--headers-redirects-config.md), [raw/next--csp-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--csp-guide.md), [raw/next--source-maps-powered-by-env-vars.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--source-maps-powered-by-env-vars.md), [raw/advisory--2026-image-optimizer.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-image-optimizer.md), [raw/advisory--2026-rewrites-ssrf-and-other.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-rewrites-ssrf-and-other.md).

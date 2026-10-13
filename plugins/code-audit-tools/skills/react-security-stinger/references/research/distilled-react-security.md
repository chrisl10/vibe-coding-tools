# Distilled research: React 18 and 19 application security

Research window 2026-03-30 to 2026-09-30, with advisories from 2025-09-30 onward allowed as current authority. Fetched 2026-09-30. Every claim cites its raw file in `raw/`. Older timeless sources are labeled in their raw headers.

## 1. React Server Components runtime advisories

| Fact | Source |
| --- | --- |
| CVE-2025-55182 ("React2Shell") is unauthenticated RCE from a crafted request to any Server Function endpoint, CVSS 10.0, CWE-502 | [raw/rsc--react-blog-cve-2025-55182.md], [raw/rsc--github-react-security-advisories.md] |
| Apps that support RSC are exposed even with no Server Functions defined | [raw/rsc--react-blog-cve-2025-55182.md] |
| Affected packages: react-server-dom-webpack, -parcel, -turbopack; not `react` or `react-dom` themselves | [raw/rsc--react-blog-cve-2025-55182.md] |
| Apps with no server, or no RSC-capable framework or bundler, are not affected | [raw/rsc--react-blog-cve-2025-55182.md] |
| Eight React advisories exist as of 2026-09-30: one critical RCE, one medium source exposure, six high DoS | [raw/rsc--github-react-security-advisories.md] |
| Cumulative safe floor: 19.0.8, 19.1.9, 19.2.8, or 19.3.0+ | [raw/rsc--github-react-security-advisories.md], [raw/rsc--npm-registry-react-server-dom-versions.md] |
| The 2025-12 patches 19.0.3, 19.1.4, 19.2.3 were declared incomplete | [raw/rsc--react-blog-dos-and-source-exposure.md] |
| CVE-2025-67779 affects only 19.0.2, 19.1.3, 19.2.2 (regression in the first DoS fix) | [raw/rsc--github-react-security-advisories.md] |
| CVE-2025-55183 leaks Server Function source, so hardcoded secrets leak; `process.env` values do not | [raw/rsc--react-blog-dos-and-source-exposure.md] |
| npm deprecation flags lag: 19.0.6 to 19.2.7 carry none yet are affected by CVE-2026-44907 | [raw/rsc--npm-registry-react-server-dom-versions.md] |
| react-server-dom-parcel has no 19.0.x line | [raw/rsc--npm-registry-react-server-dom-versions.md] |
| @vitejs/plugin-rsc vendors react-server-dom-webpack; floor 0.5.29; two extra dev-server advisories (RCE CVE-2025-67489, file read CVE-2025-68155) | [raw/rsc--vite-plugin-rsc-advisories.md] |
| Frameworks named as affected: next, react-router, waku, @parcel/rsc, @vitejs/plugin-rsc, rwsdk | [raw/rsc--react-blog-cve-2025-55182.md] |

Thin spot: no advisory text explains the internals of the RCE beyond "deserialization", so the Drone must not describe exploit mechanics in findings.

## 2. Server Functions as endpoints

| Fact | Source |
| --- | --- |
| Every `'use server'` export is callable from the client by id; module-level directive exports all functions | [raw/rsc--react-docs-use-server-and-server-functions.md] |
| React: "Always treat arguments to Server Functions as untrusted input and authorize any mutations" | [raw/rsc--react-docs-use-server-and-server-functions.md] |
| Arguments accept FormData, plain objects, Maps, Sets, typed arrays, Promises | [raw/rsc--react-docs-use-server-and-server-functions.md] |
| Closure-captured values travel as bound arguments; @vitejs/plugin-rsc encrypts them by default and allows `enableActionEncryption: false` | [raw/rsc--vite-plugin-rsc-readme-closure-encryption.md] |
| React's own docs promise no closure encryption; hand-rolled setups must not assume it | [raw/rsc--react-docs-use-server-and-server-functions.md] (absence), [raw/rsc--vite-plugin-rsc-readme-closure-encryption.md] |
| CSRF on action dispatch was a real gap: Waku before 1.0.0-beta.1, React Router before 7.12.0 (Framework and RSC modes) and RSC mode before 7.18.2 | [raw/router--waku-advisories.md], [raw/router--react-router-advisories.md] |
| Taint APIs are experimental only, only in RSC, and are bypassed by cloning or deriving values | [raw/rsc--react-docs-taint-apis.md] |
| Passing `process.env.X` as a prop to a Client Component leaks it | [raw/rsc--react-docs-taint-apis.md] |

## 3. XSS sinks and React version behavior

| Fact | Source |
| --- | --- |
| React 19 rewrites `javascript:` URLs in `href`, `src`, `action`, `formAction`, `xlinkHref`, and `<object data>` to a throwing URL | [raw/xss--react-dom-url-sanitization-source.md], [raw/rsc--react-release-notes-19-2-x-and-19-3.md] |
| React 18 stable renders `javascript:` URLs; only a development warning | [raw/xss--react-dom-url-sanitization-source.md] |
| No React version checks `data:` URLs or `srcDoc` | [raw/xss--react-dom-url-sanitization-source.md] |
| OWASP names both React gaps: unsanitized `dangerouslySetInnerHTML`, and `javascript:` or `data:` URLs | [raw/owasp--cheatsheet-xss-dom-xss-redirects.md] |
| `dangerouslySetInnerHTML` with untrusted markup is "trivial" XSS per React docs | [raw/xss--react-docs-dangerouslysetinnerhtml.md] |
| React 19.3.0 passes Trusted Types objects through to sinks; earlier versions stringified them | [raw/rsc--react-release-notes-19-2-x-and-19-3.md], [raw/xss--mdn-trusted-types.md] |
| Trusted Types are enforced only with CSP `require-trusted-types-for 'script'` | [raw/xss--mdn-trusted-types.md] |
| DOM sinks: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`; code sinks `eval`, `new Function`, string `setTimeout` | [raw/owasp--cheatsheet-xss-dom-xss-redirects.md], [raw/xss--mdn-trusted-types.md] |
| react-markdown is safe by default; `rehype-raw` is for trusted markdown only; unsafe `urlTransform` or plugins reintroduce XSS; fix with `rehype-sanitize` | [raw/xss--react-markdown-readme-security.md] |
| marked does not sanitize output | [raw/xss--marked-readme-and-advisories.md] |
| html-react-parser "is not XSS safe" | [raw/xss--html-react-parser-readme.md] |
| MDX compiles to code; next-mdx-remote 4.3.0 to below 6.0.0 allowed RCE from untrusted MDX (CVE-2026-0969) | [raw/xss--mdx-next-mdx-remote-cve-2026-0969.md] |
| DOMPurify had 12 medium-or-high advisories in 2026; floor 3.4.7 for medium+, latest 3.4.16 | [raw/xss--dompurify-readme-and-advisories.md] |
| Modifying HTML after DOMPurify can void sanitization; server use needs current jsdom, not happy-dom | [raw/xss--dompurify-readme-and-advisories.md] |
| ESLint `react/no-danger` and `react/jsx-no-script-url` only match literals | [raw/lint--eslint-plugin-react-security-rules.md] |

## 4. SSR and hydration injection

| Fact | Source |
| --- | --- |
| `JSON.stringify` state inside a `<script>` is injectable; escape `<` as `<` or use serialize-javascript | [raw/ssr--redux-server-rendering-security.md] |
| React escapes `<script` and `</script` in `bootstrapScriptContent`, but says untrusted content must still be made safe first | [raw/ssr--react-dom-server-stream-options-and-escaping.md] |
| `<script dangerouslySetInnerHTML>` gets no escaping | [raw/ssr--react-dom-server-stream-options-and-escaping.md], [raw/xss--react-docs-dangerouslysetinnerhtml.md] |
| Create the store per request on the server | [raw/ssr--redux-server-rendering-security.md] |
| serialize-javascript below 7.0.5 has open high and medium advisories | [raw/ssr--serialize-javascript-advisories.md] |
| `nonce` option exists for CSP on streamed scripts | [raw/ssr--react-dom-server-stream-options-and-escaping.md] |

## 5. Secrets and data exposure

| Fact | Source |
| --- | --- |
| `VITE_*` values are bundled into client code; do not put secrets there | [raw/secrets--vite-env-and-envprefix.md] |
| `envPrefix: ''` is rejected by Vite; broad prefixes or a `define` of `process.env` still expose values (the define case is an inference) | [raw/secrets--vite-env-and-envprefix.md] |
| `REACT_APP_*` values are embedded in the CRA build; CRA is deprecated with no active maintainers | [raw/secrets--cra-env-and-sunset.md] |
| `dangerouslyAllowBrowser: true` in the OpenAI or Anthropic SDK exposes the secret key | [raw/secrets--ai-sdk-dangerously-allow-browser.md] |
| Key patterns for Stripe, Anthropic, OpenAI, Google, GitHub, AWS, Slack, private keys, JWTs | [raw/secrets--gitleaks-default-rules.md] |
| Do not keep session identifiers in localStorage; one XSS reads all of it | [raw/owasp--cheatsheet-html5-security.md] |
| AI-built app scans report API keys in JS bundles and exposed source maps (34.1% in one 603-app study) | [raw/ai--vibe-coded-apps-security-studies.md] |

## 6. Auth, routing, and client trust

| Fact | Source |
| --- | --- |
| Client-side enforcement of server-side security is CWE-602 (A06:2025) | [raw/owasp--top10-2025-and-cwe-mapping.md] |
| postMessage receivers must check `origin` exactly and validate `data`; senders must not use `*` | [raw/browser--mdn-postmessage.md], [raw/owasp--cheatsheet-html5-security.md] |
| Substring origin checks such as `indexOf(".owasp.org")` are bypassable | [raw/owasp--cheatsheet-html5-security.md] |
| CSRF defenses: Fetch Metadata with Origin fallback, SameSite, custom headers, tokens not only in cookies | [raw/owasp--cheatsheet-csrf.md] |
| Open redirects enable phishing and access-control bypass; allow-list targets | [raw/owasp--cheatsheet-xss-dom-xss-redirects.md] |
| React Router advisories through 2026-07 need 7.18.0 (7.18.2 or 8.3.0 for RSC CSRF) and are mode-dependent | [raw/router--react-router-advisories.md] |

## 7. Supply chain and AI-generated code

| Fact | Source |
| --- | --- |
| A03:2025 Software Supply Chain Failures maps CWE-1104 and CWE-1395 | [raw/owasp--top10-2025-and-cwe-mapping.md] |
| react-html-parser last release 2017; draft-js archived; react-helmet last release 2020 | [raw/xss--html-react-parser-readme.md] |
| 91.0% of 200 audited vibe-coded apps had a vulnerability; 65.77% of findings Critical or High; access control, injection, auth dominate | [raw/ai--vibe-coded-apps-security-studies.md] |
| Recurring AI patterns: placeholder logic, unfiltered input, secret exposure; calls to nonexistent security APIs | [raw/ai--vibe-coded-apps-security-studies.md] |
| Iterative AI edits sometimes remove existing protections; static analysis misses most design and authorization flaws (thesis) | [raw/ai--vibe-coded-apps-security-studies.md] |
| React says frameworks implementing Server Functions should pin a React version (bundler APIs do not follow semver) | [raw/rsc--react-docs-use-server-and-server-functions.md] |

## 8. Lockfile parsing

| Fact | Source |
| --- | --- |
| package-lock v2 and v3 use a `packages` map keyed by `node_modules/<name>`; v1 nests `dependencies` | [raw/lockfile--npm-pnpm-yarn-formats.md] |
| pnpm v9 keys `<name>@<version>`, snapshots add peer suffixes; v6 uses `/name@ver`, v5 `/name/ver` | [raw/lockfile--npm-pnpm-yarn-formats.md] |
| yarn classic: `name@range:` then `version "x"`; Berry: `"name@npm:range":` then `version: x` | [raw/lockfile--npm-pnpm-yarn-formats.md] |
| bun lockfiles not covered | [raw/lockfile--npm-pnpm-yarn-formats.md] |

## Conflicts and thin spots

- OWASP 2025 maps no category to CWE-400 or CWE-770; DoS findings cite the CWE plus A03 via CWE-1395 for the outdated dependency [raw/owasp--top10-2025-and-cwe-mapping.md].
- Some advisories in the GitHub pull carry no CWE (plugin-rsc dev-server file read, React Router Host header, marked recursion). The CWE values the script uses for those rows are assigned by this Stinger and marked in `references/advisory-table.md`.
- `data:` URL handling in browsers is not covered by the archive; such cases stay `needs-manual-review` and never exceed `possible` without a working reproduction [raw/xss--react-dom-url-sanitization-source.md].
- The `define: { 'process.env': process.env }` leak is an inference from Vite's documented `define` and `envPrefix` behavior, not a quoted rule [raw/secrets--vite-env-and-envprefix.md].
- AI-code prevalence numbers come from a preprint and from community and vendor reports; use them for prioritizing checks, never as evidence in a finding [raw/ai--vibe-coded-apps-security-studies.md].
- serialize-javascript's GHSA-5c6j shows an old CVE id; cite the GHSA id [raw/ssr--serialize-javascript-advisories.md].

# Advisory table (as of 2026-09-30)

Human-readable copy of `ADVISORIES` in [../scripts/react_version_check.py](../scripts/react_version_check.py). When one changes, change the other. Ranges: "from" inclusive; "below" exclusive; "through" inclusive. CWE values marked `*` are assigned by this Stinger because the advisory lists none.

Load when: you need to explain a version finding, check a version by hand (prerelease builds, bun lockfiles, vendored copies), or update the table.

## React Server Components runtime: react-server-dom-webpack, -parcel, -turbopack

| Advisory | Sev | Affected (per minor line) | Fixed | Precondition | Raw |
| --- | --- | --- | --- | --- | --- |
| CVE-2025-55182 / GHSA-fv66-9v8q-g76r, RCE, CWE-502 | critical | 19.0.0; 19.1.0, 19.1.1; 19.2.0 | 19.0.1, 19.1.2, 19.2.1 | RSC server running | rsc--github-react-security-advisories |
| CVE-2025-55183 / GHSA-925w-6v3x-g4j4, source exposure, CWE-497 | medium | below 19.0.2, 19.1.3, 19.2.2 | 19.0.2, 19.1.3, 19.2.2 | RSC server | same |
| CVE-2025-55184 / GHSA-2m3v-v2m8-q956, DoS, CWE-400 | high | below 19.0.2, 19.1.3, 19.2.2 | same | RSC server | same |
| CVE-2025-67779 / GHSA-7gmr-mq3h-m5h9, DoS, CWE-400 | high | exactly 19.0.2, 19.1.3, 19.2.2 | 19.0.3, 19.1.4, 19.2.3 | RSC server | same |
| CVE-2026-23864 / GHSA-83fc-fqcc-2hmg, DoS | high | below 19.0.4, 19.1.5, 19.2.4 | 19.0.4, 19.1.5, 19.2.4 | RSC server | same |
| CVE-2026-23869 / GHSA-479c-33wc-g2pg, DoS | high | below 19.0.5, 19.1.6, 19.2.5 | 19.0.5, 19.1.6, 19.2.5 | RSC server | same |
| CVE-2026-23870 / GHSA-rv78-f8rc-xrxh, DoS, CWE-770 | high | below 19.0.6, 19.1.7, 19.2.6 | 19.0.6, 19.1.7, 19.2.6 | RSC server | same |
| CVE-2026-44907 / GHSA-wx67-qw84-cm4g, DoS, CWE-770 | high | below 19.0.8, 19.1.9, 19.2.8 | 19.0.8, 19.1.9, 19.2.8 | RSC server | same |

Safe floor: 19.0.8, 19.1.9, 19.2.8, or any 19.3.x. Note that npm deprecation flags stop at 19.x.5 even though later versions are affected rsc--npm-registry-react-server-dom-versions.

## @vitejs/plugin-rsc (vendors react-server-dom-webpack)

| Advisory | Sev | Vulnerable | Fixed | Precondition |
| --- | --- | --- | --- | --- |
| CVE-2025-55182 / GHSA-fmh4-wr37-44fp | critical | through 0.5.2 | 0.5.3 | none |
| CVE-2025-67489 / GHSA-j76j-5p5g-9wfr, dev-server RCE, CWE-94* | critical | through 0.5.5 | 0.5.6 | dev server reachable |
| CVE-2025-55183, CVE-2025-67779 / GHSA-c6m7-q6pr-c64r, GHSA-cpqf-f22c-r95x | high | through 0.5.6 | 0.5.7 | none |
| CVE-2025-68155 / GHSA-g239-q96q-x4qm, dev-server file read, CWE-22* | high | through 0.5.7 | 0.5.8 | dev server reachable |
| CVE-2026-23869 / GHSA-v457-wxvj-p9w9 | high | through 0.5.22 | 0.5.23 | none |
| CVE-2026-23870 / GHSA-w94c-4vhp-22gx | high | through 0.5.25 | 0.5.26 | none |
| CVE-2026-44907 / GHSA-p2w6-cmq4-qjfj | high | through 0.5.28 | 0.5.29 | none |

Raw: rsc--vite-plugin-rsc-advisories.

## React Router and Remix packages

All from router--react-router-advisories. The script groups them by fixed floor; the table lists each.

| Advisory | Sev | Package and range | Fixed | Mode precondition |
| --- | --- | --- | --- | --- |
| CVE-2025-31137 / GHSA-4q56-crqp-v477, CWE-20* | high | @react-router/express 7.0.0 through 7.4.0 | 7.4.1 | Express adapter |
| CVE-2025-43864, CVE-2025-43865, CWE-345* | high | react-router 7.0.0 through 7.5.1 | 7.5.2 | Framework |
| CVE-2025-59057 / GHSA-3cgp-3xvw-98x8, CWE-79* | high | react-router 7.0.0 through 7.8.2 | 7.9.0 | Framework (Meta) |
| CVE-2025-61686 / GHSA-9583-h5hc-x8cw, CWE-22* | critical | @react-router/node 7.0.0 through 7.9.3 | 7.9.4 | createFileSessionStorage |
| CVE-2025-68470 / GHSA-9jcx-v3wj-wh4m, CWE-601 | medium | react-router 6.0.0 through 6.30.1, 7.0.0 through 7.9.5 | 6.30.2, 7.9.6 | untrusted paths to navigation |
| CVE-2026-22029 / GHSA-2w69-qvjg-hvjx, CWE-79 | high | 7.0.0 through 7.11.0 | 7.12.0 | Data or Framework, untrusted redirect paths |
| CVE-2026-21884 / GHSA-8v8x-cx79-35w7 | high | 7.0.0 through 7.11.0 | 7.12.0 | Framework with SSR, untrusted ScrollRestoration keys |
| CVE-2026-22030 / GHSA-h5cw-625j-3rxh, CWE-352 | medium | 7.0.0 below 7.12.0 | 7.12.0 | Framework or RSC |
| CVE-2026-33245 / GHSA-8646-j5j9-6r62, CWE-79 | high | 7.7.0 below 7.13.2 | 7.13.2 | unstable RSC |
| CVE-2026-33244 / GHSA-f22v-gfqf-p8f3, CWE-79 | medium | 7.5.1 below 7.13.2 | 7.13.2 | prerendered redirects |
| CVE-2026-34077 / GHSA-rxv8-25v2-qmq8 | high | 7.0.0 below 7.14.0 | 7.14.0 | Framework (single fetch) |
| CVE-2026-40181 / GHSA-2j2x-hqr9-3h42 | medium | 7.0.0 below 7.14.1; 6.7.0 below 6.30.4 | 7.14.1, 6.30.4 | untrusted redirect paths |
| CVE-2026-42211 / GHSA-49rj-9fvp-4h2h, CWE-502 | high | 7.0.0 through 7.14.1 | 7.14.2 | Framework plus a prototype pollution bug |
| CVE-2026-42342 / GHSA-8x6r-g9mw-2r78, CWE-400 | high | 7.0.0 below 7.15.0 | 7.15.0 | Framework (__manifest) |
| CVE-2026-53663 / GHSA-84g9-w2xq-vcv6, CWE-352 | low | 7.12.0 below 7.15.1 | 7.15.1 | Framework (not in script table, low) |
| CVE-2026-55685 / GHSA-chx6-hx7r-mcp5, CWE-400 | high | 7.0.0 below 7.18.0 | 7.18.0 | Framework (__manifest) |
| CVE-2026-53667 / GHSA-h8fp-f39c-q6mh | medium | 7.11.0 below 7.18.0 | 7.18.0 | unstable RSC |
| CVE-2026-53666 / GHSA-337j-9hxr-rhxg | medium | 6.4.0 below 7.18.0 | 7.18.0 | Data or Framework with manual SSR |
| CVE-2026-53669 / GHSA-wrjc-x8rr-h8h6, CWE-601 | medium | 6.0.0 below 7.18.0 | 7.18.0 | untrusted paths to navigation |
| CVE-2026-53668 / GHSA-jjmj-jmhj-qwj2 | medium | react-router-dom 6.30.2 through 6.30.4; react-router 7.9.6 through 7.12.0 | 6.30.6, 7.13.0 | untrusted redirect |
| GHSA-qwww-vcr4-c8h2, CWE-352* | medium | 7.12.0 below 7.18.2; 8.0.0 below 8.3.0 | 7.18.2, 8.3.0 | unstable RSC |

Mode detection: Framework Mode has `@react-router/dev` and a `react-router.config.*` file; Data Mode uses `createBrowserRouter` or `RouterProvider`; Declarative Mode uses `<BrowserRouter>` only and is outside most of these advisories.

## Waku

| Advisory | Sev | Vulnerable | Fixed | Raw |
| --- | --- | --- | --- | --- |
| CVE-2026-49455 / GHSA-75w3-gmqx-993q, CSRF on Server Action dispatch | medium | through 1.0.0-beta.0 | 1.0.0-beta.1 | router--waku-advisories |
| CVE-2026-49456 / GHSA-43fc-v873-qw85, open redirect helper | low | through 1.0.0-beta.0 | 1.0.0-beta.1 | same |

## Content, sanitizer, and serialization libraries

| Package | Advisory | Sev | Vulnerable | Fixed | Precondition | Raw |
| --- | --- | --- | --- | --- | --- | --- |
| next-mdx-remote | CVE-2026-0969 / GHSA-g4xw-jxrg-5f6m, CWE-94 | high | 4.3.0 below 6.0.0 | 6.0.0 (breaking: `blockJS` default) | untrusted MDX compiled | xss--mdx-next-mdx-remote-cve-2026-0969 |
| marked | CVE-2026-41680 / GHSA-6v9c-7cg6-27q7, CWE-674* | high | 18.0.0, 18.0.1 | 18.0.2 | untrusted markdown | xss--marked-readme-and-advisories |
| dompurify | CVE-2026-47423 / GHSA-87xg-pxx2-7hvx, CWE-79 | high | 3.4.4 | 3.4.5 | none | xss--dompurify-readme-and-advisories |
| dompurify | 11 medium advisories 2026-03 to 2026-05 (see raw) | medium | below 3.4.7 | 3.4.7 (latest 3.4.16) | risky options or modes in use | same |
| serialize-javascript | GHSA-5c6j-r48x-rmvq (RCE), GHSA-qj8w-gfj5-8c6v / CVE-2026-34043 (DoS) | high | below 7.0.5 | 7.0.5 | attacker-influenced objects serialized | ssr--serialize-javascript-advisories |

## Unmaintained or deprecated (low, CWE-1104)

| Package | Signal | Raw |
| --- | --- | --- |
| react-scripts | Create React App deprecated 2025-02-14, no active maintainers | secrets--cra-env-and-sunset |
| react-html-parser | last release 2017-11-29, no sanitization | xss--html-react-parser-readme |
| draft-js | repository archived | same |

react-helmet (last release 2020) and react-quill (last release 2022) are recorded in the raw file as age signals only; the script does not report them.

## Out of scope here

- `next` bundles its own RSC runtime; Next.js version advisories belong to `nextjs-security-stinger`.
- bun lockfiles and prerelease (canary, experimental) builds are reported as coverage caps for a manual check.

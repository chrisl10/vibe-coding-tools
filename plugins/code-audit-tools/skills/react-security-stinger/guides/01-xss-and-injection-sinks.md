# 01. XSS and injection sinks (client and SSR)

React escapes text it renders. Every XSS in a React app goes around that: raw HTML props, DOM writes, URLs, HTML-producing libraries, and strings stitched into server-rendered HTML. This guide finds and confirms those paths.

References: [checks-xss-and-ssr.md](../references/checks-xss-and-ssr.md) (RX-01 to RX-11, RS-01 to RS-03), [detection-patterns.md](../references/detection-patterns.md), [finding-rules.md](../references/finding-rules.md).

## Procedure

1. **Load the candidates** for RX and RS ids from `sink-candidates.json` (guide 00 step 9). If the file lists a cap for a check, rerun that check alone with a higher `--max-per-check`.
2. **Set the React rule for URLs** from the stack table: React 18 or older means `javascript:` URLs execute (RX-02 at full severity); React 19 neutralizes them in `href`, `src`, `action`, `formAction`, `xlinkHref`, `<object data>` but never checks `data:` URLs, `srcDoc`, or `window.location`.
3. **Work the sinks in this order** (highest yield first): RX-01 `dangerouslySetInnerHTML`, RX-05 markdown, RX-06 MDX, RX-07 HTML parsers, RX-03 DOM writes, RX-02 URLs, RX-04 eval, RX-08 sanitizer use, RX-09 Trusted Types, RX-10 CSS, RX-11 `target=_blank`.
4. **For each candidate, trace the value to its source.** Open the file, follow props up through parents, hooks, stores, loaders, and API clients until you reach one of:
   - a constant or repo file (not a finding),
   - the current user's own input only (self-XSS: usually not a finding unless a link can prefill it),
   - data other users or external systems wrote (stored or reflected XSS: a finding).
   Write the path you followed; it becomes `verified_by`.
5. **Check the sanitizer on the path** with RX-08: is it the last step, with safe options, on a current version (dompurify 3.4.7 or later)? A sanitizer followed by string edits is not a sanitizer.
6. **For markdown and MDX,** read the component props: `rehypePlugins`, `urlTransform`, `components`, `skipHtml`, and for next-mdx-remote the `blockJS` and `blockDangerousJS` options and version. Find where the markdown text comes from.
7. **SSR half (only when an SSR or RSC entry exists).** Open the server entry and the HTML template:
   - RS-01: find every script that embeds state; check for `<` escaping.
   - RS-02: read `bootstrapScriptContent` for interpolated request data.
   - RS-03: list every value inserted into the HTML shell around `renderToString` or stream output, including title and meta tags.
8. **Rate each confirmed path** with the check's severity line and [finding-rules.md](../references/finding-rules.md). Use `possible` (capped at `medium`) when the source could not be traced, or move it to notes as "Not confirmed" when there is no evidence beyond the pattern.
9. **Write findings** with the check id in `tags`, the shortest code excerpt that shows source and sink (15 lines maximum), and the fixed snippet from the check adapted to the file.
10. **Record measures:** count of raw-HTML sinks, count fed untrusted input, sanitizer version.

## Done when

Every RX and RS candidate is either a finding, a "Not confirmed" note with the reason, or dismissed with a one-line reason in notes (for the brief's evidence trail, list dismissed counts per check, not every line).

## Sources

- raw/xss--react-docs-dangerouslysetinnerhtml.md
- raw/xss--react-dom-url-sanitization-source.md
- raw/xss--react-markdown-readme-security.md
- raw/xss--marked-readme-and-advisories.md
- raw/xss--mdx-next-mdx-remote-cve-2026-0969.md
- raw/xss--dompurify-readme-and-advisories.md
- raw/xss--html-react-parser-readme.md
- raw/xss--mdn-trusted-types.md
- raw/ssr--react-dom-server-stream-options-and-escaping.md
- raw/ssr--redux-server-rendering-security.md
- raw/owasp--cheatsheet-xss-dom-xss-redirects.md
- raw/rsc--react-release-notes-19-2-x-and-19-3.md

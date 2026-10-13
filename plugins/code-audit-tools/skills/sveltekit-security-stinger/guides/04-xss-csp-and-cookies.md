# 04. XSS, Content Security Policy, and cookies

Goal: find every place untrusted text becomes HTML, check the browser-side safety nets, and check how session cookies and tokens are stored.

Loads: [../references/check-catalog.md](../references/check-catalog.md) (section X), [../references/detection-patterns.md](../references/detection-patterns.md) (XSS, CSP, cookies), [../references/severity-guide.md](../references/severity-guide.md).

## Background you need

- Svelte escapes text in `{expression}`. The raw sinks are `{@html}`, DOM writes in actions (`use:`) and attachments (`{@attach}`, Svelte 5.29+), and direct DOM APIs (`innerHTML`, `insertAdjacentHTML`, `document.write`).
- `{@html}` renders during SSR, so a payload is in the first HTML response.
- mdsvex compiles markdown into Svelte components and accepts all Svelte syntax: trusted, repository-authored content only. `marked` does not sanitise. DOMPurify on the server needs a current jsdom; happy-dom is not safe with it.
- Several Svelte 5 SSR XSS advisories need a specific template pattern (attribute spreading, `<svelte:element>`, `<option>`, contenteditable bindings, `hydratable`). Guide 00 matched versions; here you check the patterns' inputs.
- `kit.csp` supports `hash`, `nonce`, `auto`. Prerendered pages get a meta-tag CSP that ignores `frame-ancestors`, `report-uri`, `sandbox`.
- `cookies.set` defaults: `httpOnly: true`, `secure: true` (except on localhost), `sameSite: 'lax'`; `path` required.

## Steps

1. **`{@html}` (SVK-X1).** For every `html_sinks[]` entry:
   1. Trace the expression to its origin (load return, prop, store, remote query, CMS, markdown).
   2. Decide who can write that origin: anonymous visitors, any user, staff, only developers via the repository.
   3. Check for a sanitiser applied to that exact value before render (and which DOM it runs on, server side).
   4. File when an outsider can influence the value and it is not sanitised.
2. **Markdown and rich text (SVK-X2).** For each `markdown_libraries[]` entry, follow the output to its sink. mdsvex `compile()` called at runtime on stored content is a finding by itself.
3. **DOM sinks (SVK-X3).** For every `dom_sinks[]` entry, read the string being written and its parameters.
4. **Template-pattern advisories (SVK-X4).** For each signal in `signals.spread_attributes`, `svelte_element`, `option_dynamic`, `contenteditable_bind`, `hydratable`, determine whether the data is user-controlled. This upgrades or clears the related version finding from guide 00. On patched versions, spreading user-controlled objects onto elements is still a `medium` finding (attackers choose `href`, `style`, `srcdoc` and others).
5. **Error pages.** `src/error.html` placeholders and `error()` messages with user content were an XSS on kit below 2.8.3 (GHSA-mh2x-fcqh-fmqv); cross-check with guide 03 step 9.
6. **CSP (SVK-X5).** Read `kit.csp` in `svelte.config.*`, any CSP set in `handle`, and platform header files (`vercel.json`, `static/_headers`, `netlify.toml`). Record mode, `script-src`, presence of `unsafe-inline` or `unsafe-eval` for scripts, report-only versus enforcing. Raise to `medium` when an XSS finding exists.
7. **Cookies (SVK-X6).** Review `cookie_options_weakened[]`, `document.cookie` writes, and every `cookies.set` for the session or auth cookie: flags, `domain`, lifetime. Note cookies set by third-party auth libraries by reading their config in the repository.
8. **Token storage (SVK-X7).** Search `localStorage` and `sessionStorage` writes and client stores for tokens and keys.
9. **Write findings** per guide 06. XSS evidence must show the sink line and the line where the untrusted value enters.

## False positive reminders

- `{@html}` of compile-time constants, icon SVG strings from the repository, or a sanitiser's output is fine.
- A CSP set at the CDN counts if you can read its configuration in the repository.

## Done when

Every sink in the inventory has an origin and a verdict, the CSP and session cookie are described in notes, and token storage is checked.

## Sources

[raw/svelte-docs--html-attach-use-hydratable.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/svelte-docs--html-attach-use-hydratable.md), [raw/markdown--mdsvex-marked-dompurify.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/markdown--mdsvex-marked-dompurify.md), [raw/advisory--svelte-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--svelte-repo-advisories.md), [raw/advisory--kit-repo-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--kit-repo-advisories.md), [raw/kit-docs--configuration-csrf-csp-paths-env.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--configuration-csrf-csp-paths-env.md), [raw/kit-docs--cookies-api-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/kit-docs--cookies-api-reference.md), [raw/ai--vibe-coded-app-security-studies-2026.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/ai--vibe-coded-app-security-studies-2026.md).

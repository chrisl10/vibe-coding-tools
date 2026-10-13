# 03. Secrets and data exposure

Everything the browser receives is public: the bundle, environment values baked into it, the RSC payload, API responses, and web storage. This guide finds secrets and over-shared data on that path.

References: [checks-secrets-and-data.md](../references/checks-secrets-and-data.md) (SD-01 to SD-09), [detection-patterns.md](../references/detection-patterns.md), [finding-rules.md](../references/finding-rules.md).

## Procedure

1. **Know the exposure rule for this build tool** from the stack table: Vite exposes `VITE_*` (or the configured `envPrefix`), Create React App exposes `REACT_APP_*`, Expo exposes `EXPO_PUBLIC_*`. Read `vite.config.*` (or webpack config) for `envPrefix` and `define` (SD-03).
2. **List client-exposed variables** (SD-01): from `.env*` files in the repo (values redacted), from `import.meta.env.*` and `process.env.REACT_APP_*` references, and from CI or platform config files in the repo. Classify each as secret or public using the check's rules. Do not print values; keep the first 4 characters plus `****`.
3. **Scan client code for credentials** (SD-02, SD-08): use the SD-02 candidates and `dangerouslyAllowBrowser`. For each hit, confirm the file ships to the browser.
4. **Check a built bundle if one exists** in the throwaway copy (`dist/`, `build/`). Do not run a build in the audited repo. If no build exists and the arming line allows tools in the copy, you may run the project's build command there with a timeout; record the command and output in `raw/`. Grep the output for SD-01 and SD-02 patterns. If you could not build, add a cap: "bundle not inspected; findings come from source only".
5. **Web storage** (SD-04): list every `setItem` with token-like keys and the auth library's persistence setting. Cross-reference with guide 01 results: any confirmed XSS turns stored tokens into a chain (name it in both findings).
6. **Overfetching** (SD-05): for each data loader, API route in scope, or Server Component, compare returned fields with what the UI renders. Flag fields the user is not entitled to.
7. **Source maps** (SD-06) and **logs** (SD-09): read build config and grep logs.
8. **SSR shared state** (SD-07): open the server entry; look for module-level stores or caches written per request.
9. **Rate and write** per finding-rules.md. Secrets in evidence are always redacted.
10. **Record measures:** client-exposed variables total, of which secret; credentials in client code; token storage location.

## Handoffs

- Secrets in git history or server-only code: the generic `security-wasp-drone` owns repository-wide secret scanning. Mention overlaps in notes rather than duplicating.
- Database row-level security or backend authorization behind exposed anon keys: hand to the owning Drone (for Supabase apps, `lovable-audit-wasp-drone` when installed) via notes.

## Sources

- [raw/secrets--vite-env-and-envprefix.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/secrets--vite-env-and-envprefix.md)
- [raw/secrets--cra-env-and-sunset.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/secrets--cra-env-and-sunset.md)
- [raw/secrets--gitleaks-default-rules.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/secrets--gitleaks-default-rules.md)
- [raw/secrets--ai-sdk-dangerously-allow-browser.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/secrets--ai-sdk-dangerously-allow-browser.md)
- [raw/owasp--cheatsheet-html5-security.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/owasp--cheatsheet-html5-security.md)
- [raw/ssr--redux-server-rendering-security.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/ssr--redux-server-rendering-security.md)
- [raw/rsc--react-docs-taint-apis.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/rsc--react-docs-taint-apis.md)
- [raw/ai--vibe-coded-apps-security-studies.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/ai--vibe-coded-apps-security-studies.md)

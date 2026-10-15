# 06. Supply chain, React version behavior, and AI-generated code patterns

Run after guide 00 (it needs the version findings) and alongside guides 01 to 04 on apps that look AI-generated.

References: [checks-supply-chain-and-ai.md](../references/checks-supply-chain-and-ai.md) (SC-01 to SC-05, AI-01 to AI-10), [advisory-table.md](../references/advisory-table.md), [finding-rules.md](../references/finding-rules.md).

## Procedure

1. **Library advisories** (SC-01): for each non-RSC version finding from the script (React Router, Waku, next-mdx-remote, marked, dompurify, serialize-javascript), read the precondition it lists and try to show it in code: Framework Mode routes that redirect with request data; MDX compiled from database content; DOMPurify called with the named options. Shown: raise to `likely` or `confirmed`. Not shown: keep `possible`, capped at `medium`.
2. **Unmaintained packages** (SC-02): accept the script's low findings; add others you find in `package.json` that render HTML, handle auth, or do crypto and have had no release in years (state the last release date you saw, from the lockfile metadata or registry data in the research archive, never from memory).
3. **React version behavior** (SC-03, SC-04): note the React version effect on ratings (React 18 raises RX-02); confirm guide 01 applied it.
4. **Experimental, canary, unpinned** (SC-05): lockfile scan for prerelease builds and caret ranges on `react-server-dom-*` in hand-rolled RSC setups.
5. **AI-pattern sweep.** Decide whether the app looks AI-generated (scaffold markers, README, commit messages, many security TODOs). If yes, run AI-01, AI-02, AI-04 candidates from `sink-candidates.json`, read every helper named like sanitize, escape, validate, auth, verify, and confirm each import resolves to a real export of the installed package. File confirmed issues under their real check ids with the `ai-pattern` tag.
6. **Removed protections:** in the throwaway copy only, read recent history of auth and sanitizer files (`git log -p --since=<90 days> -- <file>`). A check that was removed and not replaced is evidence; cite the commit hash.
7. **Record measures:** count of findings tagged `ai-pattern`, unmaintained packages, prerelease React in production (yes or no).

## Rules

- Never label code "AI-generated" in a finding. Describe the behavior.
- Prevalence numbers from studies help you choose where to look first. They never appear as evidence.

## Sources

- raw/router--react-router-advisories.md
- raw/router--waku-advisories.md
- raw/xss--mdx-next-mdx-remote-cve-2026-0969.md
- raw/xss--dompurify-readme-and-advisories.md
- raw/ssr--serialize-javascript-advisories.md
- raw/secrets--cra-env-and-sunset.md
- raw/xss--html-react-parser-readme.md
- raw/rsc--react-release-notes-19-2-x-and-19-3.md
- raw/ai--vibe-coded-apps-security-studies.md
- raw/owasp--top10-2025-and-cwe-mapping.md

# 05. Writing findings, metrics, and notes

Run last. Turns everything confirmed in guides 00 to 04 and 06 into the three per-source files the orchestrator merges.

References: [finding-rules.md](../references/finding-rules.md) (fields, confidence, severity, example), the contract at `audit-my-code-stinger/references/audit-contract.md` sections 5 to 8.

## Procedure

1. **Collect** the reviewed version findings (guide 00) and every manual finding. Number manual findings after the last script id: `SEC-REACT-NNN`, unique, three digits.
2. **Check each finding against the contract** before writing:
   - every required field present (`id`, `dimension: "security"`, `source: "react-security-wasp-drone"`, `title`, `severity`, `confidence`, `locations`, `evidence`, `why_it_matters`, `remediation`, `effort`, `refs`, `verified_by`);
   - `locations` paths are repo-relative with line numbers;
   - `evidence` is real text you saw (excerpt of at most 15 lines, or command plus output), secrets redacted to 4 characters plus `****`;
   - `possible` never above `medium`;
   - `refs` include a CWE, the OWASP 2025 category, any CVE or GHSA, and the guide path;
   - title and why_it_matters read plainly to a founder: no unexplained acronyms beyond XSS and CSRF, which you spell out once in `why_it_matters` ("cross-site scripting (XSS): attacker script running in your users' browsers").
3. **Apply confidence honestly.** `confirmed` only with an end-to-end trace or a reproduction in the throwaway copy that touched no live system. Pattern plus manual read: `likely`. Pattern only: `possible`, or move it to notes under "Not confirmed" if there is nothing to show.
4. **De-duplicate inside your own file:** one finding per root cause and location. The same sink in ten components fed by one unsafe helper is one finding at the helper with all ten locations listed (cap the list at 20 and say how many more in `evidence`). Duplicates with other Drones are allowed; the brief merges by path, line overlap, and CWE.
5. **Write** `02-security/findings-react-security-wasp-drone.jsonl`, one JSON object per line, no trailing commas, UTF-8. Validate by parsing every line (`python3 -c "import json,sys;[json.loads(l) for l in open(sys.argv[1])]" <file>`).
6. **Write** `02-security/metrics-react-security-wasp-drone.json` with the measures from each guide, the verdict by contract section 8, and `coverage` (files scanned from `sink_scan.py`, skipped globs, every cap). Example in finding-rules.md.
7. **Write** `02-security/notes-react-security-wasp-drone.md` with these sections: Scope and stack table; Guides run and skipped (with reasons); Not confirmed (each suspicion, what evidence is missing); Dismissed candidates (counts per check id with the common reason); Handoffs (to `nextjs-security-wasp-drone`, `polyglot-security-wasp-drone`, `security-wasp-drone`, others); Caps.
8. **Evidence index lines:** list every file you wrote under `02-security/raw/react-security-wasp-drone/` under an `## Evidence` heading in `02-security/notes-react-security-wasp-drone.md`, one line each (`` `path` - what it is``), so the orchestrator can build `evidence-index.md`.
9. **Return** to the orchestrator: verdict, finding count by severity, and every coverage cap (arming line common block).

## Self-check before returning

- No file written outside `02-security/` of the workspace; nothing written in the audited repo.
- No em dashes or en dashes in any text you wrote.
- Every `critical` and `high` has `confirmed` or `likely` confidence and a `verified_by` that names what you read.
- Counts in metrics match the findings file.

## Sources

- [raw/owasp--top10-2025-and-cwe-mapping.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/owasp--top10-2025-and-cwe-mapping.md)
- [raw/rsc--github-react-security-advisories.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/rsc--github-react-security-advisories.md)
- [raw/secrets--gitleaks-default-rules.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/react-security-stinger/references/research/raw/secrets--gitleaks-default-rules.md)

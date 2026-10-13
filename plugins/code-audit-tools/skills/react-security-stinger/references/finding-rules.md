# Finding rules: severity, confidence, and output files

Load when: writing any finding, `metrics-react-security-wasp-drone.json`, or notes (guide 05). The contract is [audit-contract.md](../../audit-my-code-stinger/references/audit-contract.md); this file applies it to React checks. Where the two disagree, the contract wins.

## Output files (per-source, because several security Drones share `02-security/`)

| File | Content |
| --- | --- |
| `02-security/findings-react-security-wasp-drone.jsonl` | one finding per line, contract section 5 |
| `02-security/metrics-react-security-wasp-drone.json` | contract section 6, `dimension: "security"` |
| `02-security/notes-react-security-wasp-drone.md` | scope, stack map, "Not confirmed" list, handoffs, caps |
| `02-security/raw/react-security-wasp-drone/` | `version-findings.jsonl`, `version-summary.json`, `sink-candidates.json`, command logs |

The orchestrator merges per-source files with `audit-my-code-stinger/scripts/merge_security.py`. Never write `02-security/findings.jsonl` or `metrics.json` yourself.

## Ids

`SEC-REACT-NNN`, three digits, starting at 001, unique in this file. Run the version script with `--start-id 1` first; continue numbering from the next free number for manual findings.

## Confidence

| Value | Use when | Examples |
| --- | --- | --- |
| `confirmed` | You traced the whole path from untrusted source to sink (or reproduced it in the throwaway copy without touching live systems), or the fact is directly observed | `user.bioHtml` saved by `PATCH /profile` and rendered with `dangerouslySetInnerHTML` unsanitized; a live-format key in `src/` |
| `likely` | Pattern match plus a manual read of the code that shows the weakness, with one link not fully traced | Server Function with no auth check, but you could not see every caller; vulnerable version resolved in the lockfile with the feature in use |
| `possible` | Pattern match only, or a version declared only in `package.json`, or a precondition you could not show | `href={x}` where `x`'s origin is in an unscanned package |

Rule 3 of the contract: `possible` can never exceed `medium`. The version script enforces it; you enforce it for manual findings.

A suspicion you cannot show at all goes to notes under "Not confirmed", never to findings.

## Severity (contract section 7, React mapping)

| Severity | React-specific examples |
| --- | --- |
| `critical` | RSC runtime in the CVE-2025-55182 range on a deployed server; live server secret in the client bundle; `dangerouslyAllowBrowser` with a live key; unauthenticated Server Function that deletes or writes any user's data; untrusted MDX compiled on the server |
| `high` | Stored XSS through `dangerouslySetInnerHTML`, raw markdown, or `innerHTML`; Server Function missing an ownership check; state serialized into a script with user strings; mass assignment of roles; open redirect that executes `javascript:`; RSC DoS advisories |
| `medium` | Reflected XSS needing a crafted link; tokens in localStorage; CSRF behind `SameSite=Lax`; DOMPurify below 3.4.7 with risky options; passthrough Trusted Types policy; open redirect to external sites |
| `low` | Source maps public; unmaintained packages; `target=_blank` without `rel`; error text leaks; taint used as the only layer |
| `info` | React 18 in use (raises RX-02 ratings); current, patched versions worth recording |

Adjustments:

1. Chains: when two findings combine (XSS plus tokens in localStorage), keep each at its own severity and name the other in `why_it_matters`. Do not invent a third finding.
2. Exposure: an admin-only page lowers likelihood but not impact. Lower by one level only when the attacker would already need the same privilege.
3. Next.js overlap: on a Next.js app, do not file Server Action, route handler, middleware, or `next.config` findings; hand them to `nextjs-security-wasp-drone` in notes.

## Writing each field

- `title`: what is wrong, in plain words a founder understands. "Anyone can delete any project by calling deleteProject directly." Not "Missing authZ in RSC action".
- `evidence`: a code excerpt of at most 15 lines with `path:line`, or the exact command and output. Redact secrets: first 4 characters plus `****`.
- `why_it_matters`: the consequence for this app, one to three sentences.
- `remediation`: file name and the specific change, ideally a short fixed snippet from the check.
- `effort`: `S` for a one-file fix or patch upgrade, `M` for a new validation layer, auth wrapper, or major-version upgrade, `L` for moving auth to cookies or moving client API calls to a server.
- `refs`: CWE, OWASP 2025 category, CVE or GHSA when relevant, and the check's guide path, for example `react-security-stinger/guides/02-rsc-and-server-functions.md`.
- `verified_by`: what you read or ran to rule out a false positive.
- `tags`: the check id (`RX-01`), `ai-pattern` when it applies, `react-18` or `rsc` as context.

## Example finding

```json
{"id":"SEC-REACT-004","dimension":"security","source":"react-security-wasp-drone","title":"Anyone can delete any project by calling the deleteProject server function directly.","severity":"critical","confidence":"confirmed","locations":[{"path":"src/actions/projects.ts","line_start":1,"line_end":6}],"evidence":"src/actions/projects.ts:1\n'use server';\nexport async function deleteProject(projectId: string) {\n  await db.project.delete({ where: { id: projectId } });\n}","why_it_matters":"Server functions are public endpoints. With no session or ownership check, any visitor who learns a project id can delete it.","remediation":"In src/actions/projects.ts, call requireUser() first and compare project.ownerId with the user's id before deleting.","effort":"S","refs":["CWE-862","CWE-639","OWASP A01:2025","react-security-stinger/guides/02-rsc-and-server-functions.md"],"verified_by":"Read the whole function and its only import; no wrapper or middleware covers the RSC endpoint (server.ts routes /_rsc straight to the action loader).","tags":["RC-02","rsc"]}
```

## metrics-react-security-wasp-drone.json

```json
{
  "dimension": "security",
  "verdict": "at-risk",
  "summary": "React 19.2 app with an RSC server on a patched runtime; two Server Functions lack ownership checks and one markdown view renders raw HTML.",
  "measures": [
    {"key": "react_version", "label": "React version", "value": "19.2.8", "unit": "", "band": "healthy", "threshold": "19.0.8, 19.1.9, 19.2.8, or 19.3+ for RSC apps", "source": "react_version_check.py"},
    {"key": "rsc_runtime_advisories", "label": "Open RSC runtime advisories", "value": 0, "unit": "count", "band": "healthy", "threshold": "0 healthy, any critical", "source": "react_version_check.py"},
    {"key": "server_functions_total", "label": "Server Functions found", "value": 14, "unit": "count", "band": "healthy", "threshold": "context only", "source": "sink_scan.py RC-02 plus manual read"},
    {"key": "server_functions_unguarded", "label": "Server Functions without a server-side auth check", "value": 2, "unit": "count", "band": "at-risk", "threshold": "0 healthy, 1+ at-risk", "source": "manual read"},
    {"key": "raw_html_sinks_untrusted", "label": "Raw HTML sinks fed untrusted input", "value": 1, "unit": "count", "band": "at-risk", "threshold": "0 healthy, 1+ at-risk", "source": "manual read"}
  ],
  "coverage": {"files_scanned": 612, "lines_scanned": 48210, "skipped": ["node_modules/", "dist/"], "caps": []}
}
```

Verdict: contract section 8 (any `critical` at `confirmed` or `likely` gives `critical`; any `high` gives `at-risk`; any `medium` or an `at-risk` or `moderate` band gives `moderate`; else `healthy`). Use `not-run` only when the arming line's paths contain no React code, and say why in the summary.

`coverage.caps` must list every limit: `sink_scan.py` per-check caps, files over 2 MB skipped, bun lockfiles not parsed, prerelease builds not compared, paths outside scope, and "no lockfile". An empty array claims no limit applied.

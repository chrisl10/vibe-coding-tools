# 06. Writing findings, metrics, and notes

Goal: turn what guides 00 to 05 found into the three files the brief renderer reads, exactly in the contract shape. Anything written another way is invisible in the brief.

Loads: `audit-my-code-stinger/references/audit-contract.md` (sections 5 to 8), [../references/severity-guide.md](../references/severity-guide.md), [../references/REFERENCE.md](../references/REFERENCE.md) (finding example), [../references/check-catalog.md](../references/check-catalog.md) (refs per check).

## Files you write (and only these)

| File | Content |
| --- | --- |
| `<workspace>/02-security/findings-sveltekit-security-wasp-drone.jsonl` | One JSON object per line, contract section 5 |
| `<workspace>/02-security/metrics-sveltekit-security-wasp-drone.json` | Contract section 6 |
| `<workspace>/02-security/notes-sveltekit-security-wasp-drone.md` | Auth model, deployment line, trusted origins, "Not confirmed" list, handoffs |
| `<workspace>/02-security/raw/sveltekit-*` | Scanner output and saved ripgrep runs |

Do not write `02-security/findings.jsonl` or `metrics.json`; the orchestrator's `merge_security.py` builds those from every security Drone's files. Do not put anything in `raw/` named `findings-*.jsonl`, and never write into the audited repository or `library/`.

## Steps

1. **Ids.** `SEC-SVELTE-NNN`, three digits, unique in the run. Version findings from the scanner use the first block; continue from `next_finding_id` in `sveltekit-inventory.json`.
2. **One finding per root cause and location.** Ten unguarded actions in one file with the same cause can be one finding with several `locations`; unguarded actions in different files with different data are separate findings. Do not split one bug across ids to inflate counts.
3. **Fill every field:**
   - `dimension`: `security`. `source`: `sveltekit-security-wasp-drone`.
   - `title`: one plain sentence a founder understands, naming the thing at risk. Good: "Any signed-in user can delete other users' projects through the deleteProject form action". Bad: "Missing authz in action (CWE-862)".
   - `severity` and `confidence`: per [severity-guide.md](../references/severity-guide.md). `possible` caps at `medium`.
   - `locations`: repo-relative paths with line ranges. For coverage gaps include both the unguarded surface and the guard that fails to reach it.
   - `evidence`: what you actually saw, at most 15 lines of code, or a command and its output, or a config value. Do not paraphrase a tool result. Redact secrets: first 4 characters, then `****`.
   - `why_it_matters`: one to three sentences about this app, not the vulnerability class in general.
   - `remediation`: the file and the concrete change. Borrow the fixed snippet from the catalog, adapted to the app's names.
   - `effort`: `S` under an hour, `M` under a day, `L` more.
   - `refs`: CWE id, `OWASP A0N:2025`, CVE or GHSA where applicable, and the guide path (for example `skills/sveltekit-security-stinger/guides/03-hooks-and-authorization-model.md`).
   - `verified_by`: how false positives were ruled out, naming what you read ("read src/hooks.server.ts: handle checks only /admin; the remote function has no locals check").
   - `tags`: optional; use `sveltekit`, the surface (`form-action`, `endpoint`, `remote-function`, `load`, `hook`, `config`), and `ai-pattern` where it applies.
4. **Validate the JSONL.** Each line must parse; every required field present; enums exact. A quick check:

   ```bash
   python3 -c "import json,sys; req={'id','dimension','source','title','severity','confidence','locations','evidence','why_it_matters','remediation','effort','refs','verified_by'}; [print(n, sorted(req-set(json.loads(l)))) for n,l in enumerate(open(sys.argv[1]),1) if req-set(json.loads(l))]" <workspace>/02-security/findings-sveltekit-security-wasp-drone.jsonl
   ```

   No output means every line has every field. Also confirm no `possible` finding is above `medium` and ids are unique.
5. **Metrics file.** Shape:

   ```json
   {
     "dimension": "security",
     "verdict": "at-risk",
     "summary": "SvelteKit 2.49.2 is behind on patches, and two admin form actions run without a permission check.",
     "measures": [
       {"key": "svelte_findings_high_plus", "label": "SvelteKit findings rated high or critical", "value": 2, "unit": "count", "band": "at-risk", "threshold": "0 healthy, any high at-risk, any critical critical", "source": "sveltekit-security-wasp-drone"},
       {"key": "svelte_surfaces_unguarded", "label": "Actions, endpoints and remote functions with no server-side check", "value": 3, "unit": "count", "band": "at-risk", "threshold": "0 healthy", "source": "sveltekit-security-wasp-drone"},
       {"key": "svelte_advisories_open", "label": "Published advisories affecting installed svelte, kit, devalue, adapters", "value": 11, "unit": "count", "band": "moderate", "threshold": "0 healthy, any open moderate", "source": "sveltekit_audit_scan.py"},
       {"key": "svelte_html_sinks_unsanitized", "label": "{@html} uses without a sanitiser on the value", "value": 1, "unit": "count", "band": "moderate", "threshold": "0 healthy", "source": "sveltekit_audit_scan.py plus manual read"}
     ],
     "coverage": {"files_scanned": 44, "lines_scanned": 0, "skipped": ["node_modules/", ".svelte-kit/"], "caps": ["advisory data as of 2026-09-30"]}
   }
   ```

   Set `verdict` with contract section 8. Bands use `healthy`, `moderate`, `at-risk`, `critical`, `not-run`. `lines_scanned` may be 0 when not measured; say so in caps rather than inventing a number. An empty `caps` array claims no limit applied.
6. **Notes file.** Sections in this order: Scope and versions; Auth model (from guide 03 step 1); Deployment (from guide 05 step 1); Endpoint table summary (counts by verdict); Trusted origins and CSP; Not confirmed (suspicions without evidence, each with what would confirm it); Handoffs (items for `security-wasp-drone`, `polyglot-security-wasp-drone`, or the dependency Drone); Caps; Evidence (an `## Evidence` heading listing each file under `raw/`, one line each as `` `path` - what it is``, so the orchestrator can build `evidence-index.md`; do not edit that shared file yourself).
7. **Plain-language pass.** Reread every `title` and `why_it_matters` as a non-developer. Replace jargon or explain it in the same sentence ("CSRF, a forged request sent from another site using the visitor's login").
8. **Self-check before returning.** No em dashes or en dashes in your text. No secrets unredacted. Every finding's evidence is real text from the repository or a tool. Then return to the orchestrator: verdict, counts by severity, and every coverage cap.

## Sources

[raw/owasp--top10-2025-categories-and-cwes.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/owasp--top10-2025-categories-and-cwes.md), [raw/cwe--core-entries.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/cwe--core-entries.md), [raw/advisory--github-advisory-db-svelte-ecosystem.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/sveltekit-security-stinger/references/research/raw/advisory--github-advisory-db-svelte-ecosystem.md).

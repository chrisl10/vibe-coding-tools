# 06. Writing findings per the contract

Goal: every confirmed issue becomes one valid `findings-nextjs-security-wasp-drone.jsonl` line that a founder can understand, and every suspicion that is not proven goes to `notes-nextjs-security-wasp-drone.md`. Loads [../references/finding-templates.md](../references/finding-templates.md) and the contract `audit-my-code-stinger/references/audit-contract.md` (sections 5 to 8).

## Steps

1. **Decide finding or note.** Contract rule 1: no evidence, no finding. If you could not show the code, config, or command output, write it under "Not confirmed" in `notes-nextjs-security-wasp-drone.md` with what would confirm it.

2. **Fill every required field** (contract section 5):
   - `id`: `SEC-NEXT-NNN`, continuing from the scanner's `next_id`. Never reuse an id.
   - `dimension`: `security`. `source`: `nextjs-security-wasp-drone`.
   - `title`: one plain sentence about the consequence, not the mechanism ("Any signed-in user can delete any project", not "IDOR in deleteProject").
   - `severity`: use the check's guidance and the mapping table in finding-templates.md (contract section 7).
   - `confidence`: `confirmed` when traced end to end (or reproduced locally without touching the repo), `likely` for pattern plus manual read, `possible` for pattern only. Rule 3: `possible` caps severity at `medium`.
   - `locations`: repo-relative paths with line ranges. Use the action or handler lines, not the whole file.
   - `evidence`: the actual code (up to 15 lines), config value, or command and output. Never paraphrase. Redact secrets to the first 4 characters plus `****` (rule 2).
   - `why_it_matters`: one to three sentences, for this app, in plain words. Explain jargon inline ("Server Actions are public web endpoints").
   - `remediation`: name the file and the change. Prefer the documented pattern (DAL with `server-only`, session-derived ownership filter, DTO, exact remotePatterns, version number).
   - `effort`: `S`, `M`, or `L`.
   - `refs`: at least one CWE and one OWASP 2025 code from the check, plus CVE or GHSA when a version is involved, plus the guide path (`info` lines may omit the CWE).
   - `verified_by`: how you ruled out a false positive (what you read, what you followed, why a DAL or RLS does not cover it).
   - `tags`: optional; use `nextjs` plus the area (`server-action`, `route-handler`, `middleware`, `cache`, `config`, `secrets`, `version`).

3. **One root cause, one finding.** Group repeated instances (for example 14 actions missing auth because the app has no DAL) into one finding with up to about 10 locations and a count in `evidence`. Split when fixes differ.

4. **Duplicates across Drones are fine** (rule 4). If you know `security-wasp-drone` or `react-security-wasp-drone` will report the same line (for example `dangerouslySetInnerHTML`), still report it only if your Next.js-specific context changes the severity, and say so.

5. **Validate each line** before appending. A quick check with Python (standard library); it also flags long dashes, which the brief style forbids:
   ```bash
   python3 - "<workspace>/02-security/findings-nextjs-security-wasp-drone.jsonl" <<'PY'
   import json, sys
   req = {"id","dimension","source","title","severity","confidence","locations","evidence",
          "why_it_matters","remediation","effort","refs","verified_by"}
   dashes = (chr(0x2014), chr(0x2013))
   seen = set()
   for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
       f = json.loads(line)
       if f.get("source") != "nextjs-security-wasp-drone":
           continue
       problems = sorted(req - set(f))
       if f["confidence"] == "possible" and f["severity"] in ("high", "critical"):
           problems.append("possible-over-medium")
       if any(d in line for d in dashes):
           problems.append("long-dash")
       if f["severity"] != "info" and not any(r.startswith("CWE-") for r in f.get("refs", [])):
           problems.append("no-cwe")
       if f["id"] in seen:
           problems.append("duplicate-id")
       seen.add(f["id"])
       if problems:
           print(n, f["id"], problems)
   PY
   ```

6. **Write metrics.** Add the `nextjs_` measures from finding-templates.md. In `02-security/metrics-nextjs-security-wasp-drone.json`, compute `verdict` with contract section 8 (any confirmed or likely critical gives `critical`; any high gives `at-risk`; any medium gives `moderate`). List every limit in `coverage.caps` (sampling, regex config parsing, files skipped over 2 MB, version from package.json range).

7. **Finish notes-nextjs-security-wasp-drone.md.** Scope, Not confirmed, Preconditions left open, Handoffs, Coverage limits.

8. **Never touch the audited repo**, and do not write to `library/`. Everything goes to the run workspace.

## Sources

Contract: `audit-my-code-stinger/references/audit-contract.md`. raw/standard--cwe-entries.md, raw/standard--owasp-top-10-2025.md, raw/next--data-security-guide.md.

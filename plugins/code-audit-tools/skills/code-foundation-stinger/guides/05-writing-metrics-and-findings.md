# 05. Writing metrics and findings (contract 1.0)

Turn the scan and your reading into the three output files exactly as `audit-contract.md` sections 5 and 6 describe. The brief renderer reads only these files.

## Procedure

1. **Collect your judgment in `judgment.jsonl`** (in `<workspace>/00-foundation/raw/`). One JSON object per line:
   - `{"id": "...", "_action": "update", ...changed fields}` to confirm a scanner finding with new confidence, severity, evidence or tags (remove `needs-drone-read`);
   - `{"id": "...", "_action": "drop", "reason": "..."}` to remove a false positive;
   - a full new finding for anything the scanner cannot see (ids from `050` in each area: `FND-TEST-050`, `FND-CI-050`, and so on).
   Examples are in [finding-templates](../references/finding-templates.md). Every scanner finding tagged `needs-drone-read` must be resolved.
2. **Write the extra measures** to `raw/measures-extra.json`, a JSON list replacing scanner measures with the same `key`: at least `tests_passing` (value, `unit` "%" or "status", band per [measures-and-bands](../references/measures-and-bands.md), threshold, source `run_in_copy.py`). Add `official_scorecard_score` only if you ran a local Scorecard binary. Raise `committed_secret_files` to `critical` only when you confirmed a live secret.
3. **Assemble and validate.**

   ```bash
   python3 scripts/assemble_foundation.py --scan <ws>/00-foundation/raw/foundation_scan.json \
     --judgment <ws>/00-foundation/raw/judgment.jsonl --measures-extra <ws>/00-foundation/raw/measures-extra.json \
     --out-dir <ws>/00-foundation --summary "<one or two plain sentences>" --cap "<each extra cap>"
   ```

   It fails with a list of problems if a finding breaks the contract: bad id or enum, `possible` above `medium`, absolute or `..` location paths, missing fields, a likely unredacted secret in evidence, an em or en dash in text, more than 15 lines of evidence, unresolved `needs-drone-read` tags. Fix and rerun until it prints a JSON summary. It computes the verdict by contract section 8, writes `findings.jsonl` sorted by severity, `metrics.json`, `raw/foundation_scan.json`, and seeds `notes.md` if absent.
4. **Write `notes.md`** with these sections: Scope and method (commit sha, tools, whether gh was used), What was run (each command, exit code, duration, log path), Coverage caps (same text as `metrics.json`), Not confirmed (every dropped scanner finding and every suspicion with the reason), Handoffs (secrets to `security-wasp-drone`, oversized files to `code-bloat-wasp-drone`, CI depth to `ci-release-wasp-drone`), Artifacts (every file under `raw/` with a one-line description).
5. **Index the artifacts.** For every `raw/` artifact, list each raw file under an `## Evidence` heading in your own notes file, one line each (`` `path` - what it is``); the orchestrator builds `evidence-index.md` from those sections, so never write `evidence-index.md` yourself.
6. **Check your own output** before reporting: re-read `findings.jsonl`; scan for the em dash (U+2014) and en dash (U+2013) characters; confirm no value from an env file or secret appears anywhere under the workspace (`grep` the raw logs too; test logs can echo secrets, so if one does, redact the log file in place inside the workspace).

## Writing rules

- Plain language. The reader may be a founder who vibe coded the app. "Nothing stops a broken change from reaching main" beats "no required status checks".
- One finding per root cause, not per file. Put up to ten locations in `locations`.
- Evidence is what you saw: a command and its output, a config line, a count. Never paraphrase a tool result. Redact secrets to 4 characters plus `****`.
- Remediation names the file and the change. For anything get-started would create, name the step ([get-started-assess-map](../references/get-started-assess-map.md) tag table).
- Severity follows the guide tables; contract rule 3 caps `possible` at `medium`.
- Summary answers: "Is this repository set up so humans and AI agents can work in it safely?" Name the one or two biggest gaps.

## Return to the orchestrator

Report: verdict, counts by severity, the measures that landed in `at-risk` or `critical`, caps, and the paths of the three output files. Do not paste findings.

## References loaded by this guide

- [measures-and-bands](../references/measures-and-bands.md), [finding-templates](../references/finding-templates.md), [foundation-checklist](../references/foundation-checklist.md), contract at `../../audit-my-code-stinger/references/audit-contract.md`

## Sources

- [research/raw/openssf--best-practices-criteria.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/openssf--best-practices-criteria.md)
- [research/raw/scorecard--checks-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/scorecard--checks-reference.md)
- [research/raw/wasp-nest--get-started-assess-map.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/wasp-nest--get-started-assess-map.md)

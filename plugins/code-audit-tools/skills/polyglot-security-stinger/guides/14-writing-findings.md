# 14 Writing findings, metrics, and notes per the contract

Loads [../references/cross-cutting/contract-output-rules.md](../references/cross-cutting/contract-output-rules.md) and `scripts/validate_findings.py`. Re-read `audit-my-code-stinger/references/audit-contract.md` sections 5 to 9 before writing.

## Steps

1. **Collect candidates** from guides 01 to 13. For each, decide: finding (has evidence) or "Not confirmed" (suspicion without evidence, goes to notes only).
2. **Set confidence** with contract-output-rules.md section 3: `confirmed` when traced end to end or read directly from config; `likely` with one unproven step; `possible` for pattern-only hits.
3. **Set severity** from the class table (section 4), then adjust for this codebase: unauthenticated reach raises, admin-only reach lowers. A `possible` finding never exceeds `medium` (contract rule 3).
4. **Write each field.**
   - `id`: `SEC-POLY-001` upward, no gaps needed, never reused.
   - `title`: one plain sentence about what an attacker or accident can do (section 5 examples).
   - `locations`: repo-relative paths with the stack path prefix, accurate line ranges.
   - `evidence`: the real excerpt (at most 15 lines, with a `path:lines` header), or the command and its real output, or the config value. Secrets redacted to the first 4 characters then `****`.
   - `why_it_matters`: the consequence for this app, one to three sentences.
   - `remediation`: file and exact change, matching the "fixed" pair in the ecosystem reference where one exists.
   - `effort`: `S`, `M`, or `L`.
   - `refs`: at least one CWE (merge key), the OWASP Top 10:2025 id, advisory ids from tool output, tool rule ids, and the guide path inside this Stinger [raw/standards--owasp-top10-2025.md].
   - `verified_by`: what you read or ran to rule out a false positive.
   - `tags`: stack id, framework, class.
5. **Write the files** listed in contract-output-rules.md section 1. Then, for every raw file, list each raw file under an `## Evidence` heading in your own notes file, one line each (`` `path` - what it is``); the orchestrator builds `evidence-index.md` from those sections, so never write `evidence-index.md` yourself.
6. **Write metrics** with `dimension: "security"`, the measures from guides 09 to 12 plus `poly_findings_<severity>` counts, `coverage` (files and lines scanned in your paths, skipped paths with owners, every cap), a two-sentence `summary` a founder understands, and the `verdict` by contract section 8.
7. **Write notes**: scope table (guide 00), tools and versions run with exit codes, route tables with auth verdicts, checklist results per stack, dropped hits with counts and reasons, "Not confirmed" list, "Scope differences" list.
8. **Validate** before returning:
   `python3 "$SKILL_DIR/scripts/validate_findings.py" "$WS/02-security/findings-polyglot-security-wasp-drone.jsonl" --metrics "$WS/02-security/metrics-polyglot-security-wasp-drone.json" --repo "$COPY"`
   Fix every error. Review every warning (a missing CWE or an empty `caps` list is usually a mistake).
9. **Return** to the orchestrator: verdict, finding count by severity, and every coverage cap (the arming line requires all three).

## Done when

The validator exits 0, every finding has evidence and a CWE, notes list every dropped or unconfirmed item, and the return message carries verdict, counts, and caps.

## Sources

[raw/standards--owasp-top10-2025.md], the audit contract (sections 5 to 9)

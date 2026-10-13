# 11 Static analysis (Semgrep, Opengrep, gosec)

Loads [../references/cross-cutting/static-analysis-rulesets.md](../references/cross-cutting/static-analysis-rulesets.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md).

Static analysis adds coverage to the ecosystem checklists; it never replaces them. The ecosystem `rg` sweeps run in every audit.

## Steps

1. **Pick the packs** for the stacks in scope from the table in static-analysis-rulesets.md section 1. Always include `p/security-audit`, `p/secrets`, and `p/owasp-top-ten`; add `p/github-actions`, `p/dockerfile`, and `p/terraform` when this Drone owns guide 12 [raw/sast--semgrep-cli.md].
2. **Run Semgrep** with the command in section 2: pinned 1.178.0, `--metrics=off`, named packs only (never `--config auto`), exclusions, JSON output to `raw/polyglot/`. Scope the run to this Drone's paths.
3. **If Semgrep cannot run** (not installable, or no network to fetch packs), run Opengrep v1.30.0 against a local rules folder if one is available [raw/sast--opengrep.md]. For Go, also run gosec (guide 03) [raw/go--gosec.md].
4. **If no engine runs**, record the cap and set the `sast_engine` measure to `not-run` (section 4).
5. **Triage results** with section 3: start at `possible` and at most `medium`; read each ERROR and WARNING hit in production code; promote to `likely` or `confirmed` only after tracing user input to the sink; drop test, fixture, example, and generated code hits and count them in notes.
6. **De-duplicate** against the ecosystem checklist findings: one finding per location and CWE, with the Semgrep rule id added to `refs`.
7. **Record measures**: `sast_engine` (1 or `not-run`), `sast_hits_total`, `sast_hits_confirmed` (promoted after reading), with the engine and version as `source`.

## Done when

An engine ran or its cap is recorded, every production ERROR and WARNING hit was read and either became a finding or was dropped with a reason in notes.

## Sources

[raw/sast--semgrep-cli.md], [raw/sast--opengrep.md], [raw/go--gosec.md], [raw/tools--version-pins-2026-09-30.md]

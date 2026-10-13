# Forge brief for Audit My Code builders

This file is the shared brief for every builder that forges a Drone and Stinger pair for the `code-audit-tools` plugin. It sits next to the run contract so a future maintainer can see how the pairs were specified.

## Where you work

- Repository root: the Wasp Nest source checkout your dispatcher names. All paths below are relative to it.
- Pack root: `packs/code-audit-tools/`
- You own exactly two paths: `packs/code-audit-tools/skills/<your-stinger>/` and `packs/code-audit-tools/agents/<your-drone>.md`. Do not create, edit, move, or delete anything else. Other builders work in the same pack at the same time. Do not run `git` commands that change state (no add, commit, stash, checkout, reset).
- The run contract every pair obeys: `packs/code-audit-tools/skills/audit-my-code-stinger/references/audit-contract.md`. Read it first. Your Drone writes `findings.jsonl`, `metrics.json`, and `notes.md` exactly as section 5 and 6 describe.

## How to forge (queen-wasp-stinger pipeline)

Load the forge method first: read `src/skills/queen-wasp-stinger/SKILL.md`, then `src/skills/queen-wasp-stinger/guides/per-type-per-harness-specific-guide.md` (skills and agents sections), then the templates in `src/skills/queen-wasp-stinger/references/templates/skills/reference-template/` and `src/skills/queen-wasp-stinger/references/templates/agents/reference-agents.md`. Use `packs/browser-and-app-testing-tools/agents/webapp-capture-wasp-drone.md` and `packs/browser-and-app-testing-tools/skills/webapp-capture-stinger/` as the house-style example of a finished pack pair.

Walk the stages in order:

1. **Research.** Fresh sweep of primary sources for your domain. Window: 2026-03-30 to 2026-09-30 by default. Sources up to 12 months old (from 2025-09-30) are allowed when they are the current authority (for example a CVE advisory or the OWASP Top 10:2025). Older material is allowed only for timeless standards (CWE entries, RFCs) and must be labeled as such. Official docs and advisories outrank vendor blogs, which outrank community posts. Use WebSearch, WebFetch, and the Exa or context7 tools if available. Archive every source you rely on as one file in `skills/<your-stinger>/references/research/raw/<topic>--<slug>.md`, each headed with `Source:`, `URL:`, `Fetched: 2026-09-30`, `Type:` (official doc, advisory, vendor blog, community), then the relevant excerpt in your own condensed notes with short quotes only. Aim for 12 to 30 raw files.
2. **Distill.** Write `references/research/distilled-<your-domain>.md`: dense, tabular where possible, every claim ending with a citation to its raw file like `[raw/next--server-actions-security.md]`. State conflicts and thin spots honestly.
3. **References.** Build the reference layer the guides load on demand: checklists, detection patterns (grep/ripgrep regexes and AST hints), vulnerable-versus-fixed code pairs, version and CVE tables, tool configs, and deterministic scripts (Python 3.11 standard library only, or Node with no install step) under `scripts/`. Every reference file cites the raw sources it derives from.
4. **Guides.** One focused guide per major verb, numbered `guides/00-...md`, `01-...md`. Each guide is a procedure (imperative steps), names the references it loads with relative links, and ends with "Sources" listing raw files. The rule for this pack: skills have guides, guides have references, references have research.
5. **Skill file.** `SKILL.md` last. Frontmatter uses only the six spec fields (`name`, `description`, `license: AGPL-3.0-or-later`, `compatibility`, `metadata`, `allowed-tools` optional). `description` is 200 characters or fewer, no angle brackets anywhere in frontmatter. `metadata` carries `author: Legion Code Inc.`, `hive-drone: <your-drone>`, `pair-drone: <your-drone>`, `domain`, `version: 1.0.0`, `research-window: 2026-03-30 to 2026-09-30`. The `name` equals the folder name. Body: Purpose, When to use, When not to use, Procedure, References map (table: path, load when), Related drones and stingers, Critical Directive (verbatim from the template). Research-only pairs drop the Ship Gate section and leave the comment the template asks for; these audit pairs never change the audited repo, so they are research-only.
6. **Drone file.** `agents/<your-drone>.md` in the same shape as `webapp-capture-wasp-drone.md`: frontmatter `name`, `description` (what, when, and a Do NOT line), `tools`, `model`; then Critical Directive that loads `[<your-stinger>](../skills/<your-stinger>)`, Persona and mission (one line "Designed and built by Legion Code Inc."), Scope boundaries (owns / must NOT touch, including "never modify the audited repository"), Related drones and stingers, Reporting expectations (writes to the run workspace per the contract, not to `library/`), and the respect-agent-work-boundaries paragraph verbatim from the example.
7. **Validate.** Run `python3 src/skills/queen-wasp-stinger/references/scripts/per-type-validation.py --help` to learn its arguments, then validate your skill for all harnesses and your agent for claude-code. Fix every ERROR. Then run a grounding check on yourself: pick 10 factual claims from your guides and confirm each traces to a raw file.

## Writing rules

- No em dashes or en dashes anywhere (U+2014, U+2013). Use commas, colons, parentheses, or periods.
- Plain language. The reader of the final brief may be a founder who vibe coded the app. Guides are for the Drone, but finding text the Drone writes must be understandable without a glossary.
- Never invent a CVE number, version, or API. If you cannot source it, leave it out.
- No secrets and no personal or absolute home paths in shipped content.

## What to return

A short report: files created (tree), raw source count, validator output (quote it), the 10-claim grounding check result, and any open questions or thin research areas.

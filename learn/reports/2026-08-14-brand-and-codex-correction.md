# Brand and Codex Correction Report

Date: 2026-08-14

## Why this correction exists

The first migration made two material mistakes:

1. It replaced the branded README with generic project documentation and even described the source-available license as MIT.
2. It translated the Bees into Codex TOML agents but left the reusable Stingers available only through the Codex plugin instead of also publishing them as repository skills.

This correction fixes both problems at the generated source and distribution layers.

## Brand restoration

The root README now restores and preserves:

- Legion Code Inc. light and dark logos.
- The OSPRY light and dark banner and revenue-focused callout.
- "Get the Git life."
- Bee, Stinger, Hive, Beekeeper, and Smoker language.
- The Legion docs-first philosophy.
- Mario Aldayuz and Legion Code Inc. attribution.
- The actual source-available license terms.
- "We are Legion. Vibe with Legion."

The README remains intentionally simple: the user benefit appears first, the setup request follows immediately, and deeper explanations link into `learn/guides/`.

## Codex correction

The generated Codex project adapter now contains:

- 80 skills in `.agents/skills`: 78 canonical skills plus `the-beekeeper` and `the-smoker` command translations.
- 75 native agent definitions in `.codex/agents/*.toml`.
- Explicit-invocation metadata for `$the-beekeeper` and `$the-smoker` in both the repository and plugin skill trees.
- Project configuration and hooks under `.codex/`.

The two command workflows are skills because Codex repository commands are not represented by a `.codex/commands` mirror. Their metadata disables implicit invocation so routing and delivery orchestration remain deliberate user choices.

## Distribution correction

The packages directory now includes two different Codex deliverables:

- `vibe-coding-tools-codex-1.0.0.zip`: the installable skills and hooks plugin.
- `vibe-coding-tools-codex-project-1.0.0.zip`: the repository adapter with 80 skills, 75 TOML agents, configuration, and hooks.

`SHA256SUMS` records the digest for each distribution archive.

## Verification

Security ran before Quality.

Security evidence:

- Gitleaks repository scan: zero findings.
- Exact Doppler personal token, Doppler service token, AWS access key, and Stripe secret key shape scans: zero findings.
- Extracted archive Gitleaks scans: zero findings across all four ZIP files.

Quality evidence:

- README: 1,075 words and 175 lines.
- Markdown links: zero broken links across 37 files.
- Codex skills: 80 checked, zero errors, zero warnings.
- Codex TOML agents: 75 parsed, all required fields present, all paired-skill paths target `.agents/skills`.
- Command metadata: four files parsed across the repository and plugin trees; all disable implicit invocation.
- Codex plugin validation: passed.
- Generator: a second complete run produced the same aggregate tree digest.
- Archive layout: no absolute or parent-traversal paths.
- Archive checksums: all matched.
- `git diff --check`: passed.

No CI workflow exists in this repository, so there is no remote automated check suite to report.

# code-bloat-stinger

Read-only bloat audit of any repository: copy-pasted code (jscpd), unused files, exports and dependencies (knip or the language equivalent, spot-checked by hand), line counts (cloc or scc), and giant files, functions and closures, ending in a split plan and a banded verdict.

The tool commands are bash; on Windows run them in Git Bash or WSL. See the Requirements section of SKILL.md.

## When to use

- "Is this codebase bloated?", "how much is duplicated or dead?"
- The bloat dimension of `/audit-my-code` (vibe tier and above)

## What it writes

`<workspace>/01-bloat/`: `findings.jsonl`, `metrics.json`, `notes.md`, and raw tool output in `raw/`. Tools run only in the throwaway copy.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [code-bloat-wasp-drone](../../agents/code-bloat-wasp-drone.md): the paired Drone

## Guides

- [00-scoping-and-throwaway-copy](guides/00-scoping-and-throwaway-copy.md)
- [01-duplication-with-jscpd](guides/01-duplication-with-jscpd.md)
- [02-unused-code-with-knip](guides/02-unused-code-with-knip.md)
- [03-size-and-line-counts](guides/03-size-and-line-counts.md)
- [04-structure-and-split-planning](guides/04-structure-and-split-planning.md)
- [05-spot-check-and-false-positives](guides/05-spot-check-and-false-positives.md)
- [06-bands-verdict-and-contract-output](guides/06-bands-verdict-and-contract-output.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

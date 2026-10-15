# code-audit-brief-stinger

Renders a finished Audit My Code workspace into one self-contained, Field Guide styled HTML brief. It escapes all repository text, merges duplicate findings, and prints cleanly to PDF. It renders; it never invents, edits, or re-scores a finding.

## When to use

- The final step (W4) of every `/audit-my-code` run
- Re-rendering after a Drone fixes its output
- Rebranding the brief

## What it writes

`<workspace>/brief/brief.html` only. Nothing in the audited repository.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [code-audit-brief-wasp-drone](../../agents/code-audit-brief-wasp-drone.md): the paired Drone

## Guides

- [00-inputs-and-contract](guides/00-inputs-and-contract.md)
- [01-section-map-per-tier](guides/01-section-map-per-tier.md)
- [02-rendering-and-escaping](guides/02-rendering-and-escaping.md)
- [03-branding-system](guides/03-branding-system.md)
- [04-verification-before-handoff](guides/04-verification-before-handoff.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

---
description: Validate every Wasp Nest component and diff the pest-controller-suit roster against the filesystem in both directions, check pairing integrity, guide coverage, dead references, stale paths, prose dash violations, and Cowork upload readiness, then produce a findings report with a prioritized fix list. Trigger with "audit the nest", "drift check", "is the roster in sync with the filesystem", "find orphaned drones", "check for unregistered skills".
---

# /drift-audit - Roster and Filesystem Drift Audit

The roster is only true on the day someone checks it against the filesystem. This command is that check: every Drone, every Stinger, every command, every rule, held up against what pest-controller-suit claims exists.

## Invocation and source scope

This canonical Core procedure is src/commands/drift-audit.md. In Claude plugin mode call /wasp-nest-core:drift-audit; Codex uses Core's generated source-command-drift-audit skill, not a deprecated prompt file. A source/global command label below is not an alias for an optional plugin.

Read plugin-catalog.json to resolve every specialist's owner and prerequisites. For source work use its canonical source_root; for installed work use Core's selected-plugin resolver. Do not treat a cached optional package as enabled or edit installed copies to change canonical procedures.


## Mandatory process

1. Load `../skills/pest-controller-suit/SKILL.md` (the roster) and consult it before any routing decision. This is the first step, always, no exceptions. This full read also doubles as your baseline for every diff below.
2. **Diff catalog ownership against the source filesystem, both directions.** In the canonical source checkout, read every owner's `source_root` and `components` from `plugin-catalog.json`. Inventory all declared skills, agents and commands across Core and optional packs, then flag missing or undeclared components. For an installed-capability audit, limit availability checks to the selected registry and prerequisites; an unselected optional owner is unavailable, not a missing source file.
3. **Check pairing integrity within each owner.** Each specialist `<base>-wasp-drone` needs exactly one `<base>-stinger`. Honor explicit `metadata.hive-tier: standalone` and `orchestrator` exceptions, including the three Core orchestrators. Flag missing pairs, identity mismatches or duplicate owners; do not report a declared standalone capability as an orphan.
4. **Check routing coverage.** Compare Core's directly routed roster with `pest-controller-suit/guides/<drone-name>.md`. Website Audit's twenty engagement leaves are dispatched by its own orchestrator and do not require Core routing rows or guides. Compare those leaves against their owner's engagement procedure. Every other routed specialist needs its actual Core row and guide.
5. **Check for dead component references.** Search every skill, agent, command, and rule for relative markdown links and bare paths under `.claude/` or `library/`, and flag any that point at a file that does not exist.
6. **Check source and installed paths separately.** Flag obsolete repository-layout assumptions and imperative paths that bypass selected-owner resolution. A valid native `.cursor/skills/` or `.cursor/agents/` example is not stale merely because it names a host. Preserve raw research and dated historical records; report a historical path only when an active runtime instruction still relies on it.
7. **Check for prose dash violations.** Grep every authored file (skills, agents, commands, rules; skip `references/research/raw/` and any verbatim quote) for the em dash character (Unicode U+2014) and the en dash character (Unicode U+2013). Flag every hit per `../rules/no-em-dashes.md`.
8. **Check Cowork upload readiness.** Run `python ../skills/queen-wasp-stinger/references/scripts/per-type-validation.py <path> --type <type> --harness cowork` in a loop over every skill, agent, rule, and command in the repo. Flag every ERROR; these are the components that would hard-fail a Cowork upload today.
9. Total the findings by category and severity, then write them into `../skills/pest-controller-suit/PAIRING-AUDIT.md`, refreshing its existing Totals, Pairing integrity, Path integrity, and Validation sections, and adding the dash-violation and Cowork-readiness counts alongside them under matching headings. This file exists to be refreshed whenever the colony changes; do not fork a second audit file next to it.
10. Report back to the user: the totals for every check above, and a prioritized fix list, worst first (registered-but-missing and broken pairs before guide gaps, guide gaps before dead references and stale paths, everything else before style-level dash violations). Do not silently fix anything the user has not asked you to fix; this command finds drift, it does not resolve it on its own authority.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

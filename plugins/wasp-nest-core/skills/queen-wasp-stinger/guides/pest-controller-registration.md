# Pest Controller registration

How a newly forged Drone and Stinger pair becomes a working member of the colony. Forging without registering leaves a component the orchestrator can never find; registration is part of the build, not an afterthought.

## Naming convention

The pair shares a base name: `<base>-wasp-drone` for the Drone, `<base>-stinger` for the Stinger. Examples: `payments-wasp-drone` and `payments-stinger`; `dependency-audit-wasp-drone` and `dependency-audit-stinger`. The base is the domain, lowercase kebab-case, no harness names, no version suffixes in the name itself.

Skill folder names must exactly match the frontmatter `name` (a hard Cursor requirement, good hygiene everywhere). Drone `name` frontmatter uses lowercase letters and hyphens only, never a colon (reserved for plugin scoping in Claude Code).

## Source ownership and installed availability

The root [plugin catalog](../../../../plugin-catalog.json) is the source of truth. Core retains the six immutable foundation skills; do not add a new specialist to Core by default. Choose its approved plugin owner and preserve the user's access/approval limits.

For source work, resolve files from source_root and the component rows in that catalog. For installed work, use installed Core's hooks/resolve-component.py against the explicit selected-plugin registry and required workflow key. Never edit a cached install to forge a canonical component.

## Registration checklist

Registration is the seventh and final stage of the forge pipeline (topic, research, distillation, references, guides, skill file, register); see the pipeline in queen-wasp-stinger's SKILL.md. Do not start this checklist on a pair that skipped the earlier stages: a Stinger with no domain research archive on disk is not ready to register.

Run this every time a new pair is forged. Also run it, minus the creation steps, when a pair's domain or triggers change.

1. **Forge the Stinger** through the full pipeline, landing it in the chosen catalog owner's source root: `src/skills/<base>-stinger/` for Core or `packs/<plugin-id>/skills/<base>-stinger/` for an optional plugin with its own `references/research/` (raw archive plus cited distillation) inside. The root file starts from `references/templates/skills/reference-template/`. Confirm the Critical Directive is the last section (followed by the Ship Gate for development-focused stingers), and its related-skills list links real siblings.
2. **Forge the Drone** from `references/templates/agents/reference-agents.md` into that same owner's `agents/<base>-wasp-drone.md`. The agent Critical Directive at the top must name the paired Stinger with a working relative link.
3. **Record ownership and add the roster row** in `pest-controller-suit/SKILL.md`: Drone name, one-line domain, trigger keywords, and a link to its guide. Update the root plugin-catalog.json with this owner's skill/agent lists, canonical component paths, counts and prerequisites. Keep the registered-count line accurate. Website leaves use their own orchestrator rather than an extra Core roster row.
4. **Author the guide** at `pest-controller-suit/guides/<drone-name>.md` from `pest-controller-suit/templates/guide-template.md`. The two sections that matter most are "Trigger phrases" and "Do NOT route when": the negative section is what disambiguates near-overlapping Drones.
5. **Wire the sequences.** If the new Drone joins an existing multi-Drone sequence (plan execution loop, release flow, schema-touching flow) or starts a new one, update the Multi-Drone orchestration section of pest-controller-suit.
6. **Cross-link the relatives.** Add the new Stinger to the related-skills lists of its closest sibling Stingers and Drones, and add those siblings to the new pair's lists. Relatedness means "commonly used in concert on a focused group of actions", not "same repo".
7. **Build the host projections** per [per-type-per-harness-specific-guide.md](per-type-per-harness-specific-guide.md) and the current source builder. Claude/Cowork use the owner's plugin component directories; Cursor receives its own agent projection; Codex receives owner-specific command skills and TOML roles. These are generated outputs, not alternate canonical files. Installation, registry writes and hook trust are separate authorized steps. Native marketplace selection alone is not claimed to populate the explicit registry.
8. **Validate.** `python references/scripts/per-type-validation.py <path> --type skill --harness all` and the same with `--type agent`. Zero errors before the pair is announced.
9. **Update repo references** per [vibe-coding-tools-reference-update.md](vibe-coding-tools-reference-update.md).

## The arming contract

Registration exists so dispatch works. The canonical dispatch, defined in pest-controller-suit and repeated here because it is the reason the pairing law exists:

- Spawn at top level. Do not nest subagent spawns.
- The spawn prompt begins with the arming line: you are `<drone-name>`, read your paired Stinger at `<skills-path>/<stinger-name>/SKILL.md` in full before doing anything else, then the scoped task, exact files in scope, definition of done, and how the work gets verified.
- A Drone dispatched without its Stinger loaded is a failed dispatch. Terminate and re-dispatch.
- Development-focused dispatches end with the Ship Gate: security-stinger, then quality-stinger, then the orchestrator loads github-repo-health-stinger itself, then user approval before commit and push.

## Orchestrator-level exemptions

`pest-controller-suit`, `queen-wasp-stinger`, and `get-started-stinger` are Core's three orchestrator skills. `time-blocked-turns` is Core's standalone protocol; optional plugins also contain explicitly classified skill-only capabilities. They are wielded by the harness orchestrator directly. Do not create a Drone for an explicitly direct-use capability. Declare standalone/orchestrator intent in metadata and update the owner catalog; a specialist still needs its real pair. `get-started-stinger` initializes and hardens a repository to a healthy baseline (library/ docs, GitHub CI, README, .gitignore, and hardening files), which is a whole-repo bootstrap concern rather than a single domain a dispatched Drone would own, hence the exemption.

## Deregistration and replacement

When a pair is replaced (as stinger-forge was replaced by queen-wasp-stinger):

1. Remove or archive the old skill and agent files per the decision recorded for that change.
2. Delete the roster row and guide, or mark them superseded with a pointer to the successor.
3. Sweep every related-skills list and command that referenced the old names; stale links in Critical Directives send Drones to dead paths.
4. Note the replacement in the repo documentation per [vibe-coding-tools-reference-update.md](vibe-coding-tools-reference-update.md).

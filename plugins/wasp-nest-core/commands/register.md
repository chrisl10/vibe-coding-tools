---
description: Walk the pest-controller registration checklist for a finished Drone and Stinger pair, verifying naming and the Critical Directive blocks, adding the roster row, authoring the routing guide, cross-linking related skills, wiring multi-Drone sequences, validating, and regenerating harnesses. Trigger with "register this drone", "register the new stinger pair", "add X to the roster", "finish registering Y", "the pair is built, wire it in".
argument-hint: [base-name]
---

# /register - Pest Controller Registration Checklist

An unregistered Drone is a Drone the orchestrator can never find. Forging is only half the job; this command does the other half, the part that makes a new pair real to the colony.

## Invocation and source scope

This canonical Core procedure is src/commands/register.md. In Claude plugin mode call /wasp-nest-core:register; Codex uses Core's generated source-command-register skill, not a deprecated prompt file. A source/global command label below is not an alias for an optional plugin.

Read plugin-catalog.json to resolve every specialist's owner and prerequisites. For source work use its canonical source_root; for installed work use Core's selected-plugin resolver. Do not treat a cached optional package as enabled or edit installed copies to change canonical procedures.


## Mandatory process

1. Load `../skills/pest-controller-suit/SKILL.md` (the roster) and consult it before any routing decision. This is the first step, always, no exceptions. Confirm the base name from `$1`/`$ARGUMENTS` is not already a roster row; registering a duplicate is a naming bug.
2. **Verify the intended catalog owner and pair.** In the canonical source checkout, resolve `<owner-root>` from `plugin-catalog.json`, then confirm `<owner-root>/skills/<base>-stinger/SKILL.md` and `<owner-root>/agents/<base>-wasp-drone.md` both exist. Names must match frontmatter and use lowercase kebab-case. A new owner or standalone capability follows Queen's corresponding registration procedure; do not force it into Core or fabricate a paired Drone. This command registers completed specialist pairs.
3. **Confirm the Critical Directive blocks are present and verbatim.** The Stinger's block, at the end of its `SKILL.md`, must read all files in the skill, search further if that falls short, and list related skills. The Drone's block, at the top of its agent file, must name its paired Stinger with a working relative link, read all of it, search further if needed, and list related skills. Check the exact wording against `../skills/queen-wasp-stinger/references/templates/agents/reference-agents.md` and the paired Stinger's own template, and fix any drift before moving on.
4. **Add the roster row** in `../skills/pest-controller-suit/SKILL.md`: Drone name, one-line domain summary, trigger keywords pulled from the Drone's own description, and the paired Stinger. Put it in the domain group table it fits best, and update the registered-count line at the bottom of the file to match.
5. **Author the guide** at `../skills/pest-controller-suit/guides/<base>-wasp-drone.md`, starting from `pest-controller-suit/templates/guide-template.md`. "Trigger phrases" and "Do NOT route when" matter most; the second one is what keeps this Drone from colliding with its nearest neighbors in the roster.
6. **Cross-link the relatives.** Add the new Stinger to the related-skills lists of its closest sibling Stingers and Drones, and add those siblings back into the new pair's own lists. Relatedness means the two get used together on a focused set of tasks, not just that they live in the same repo.
7. **Wire multi-Drone sequences.** If this Drone slots into an existing sequence in pest-controller-suit's "Multi-Drone orchestration" section (a build, an auth flow, a release), add its step there. If it starts a new recurring pattern, add a new sequence entry, and close it with the Ship Gate like every other entry in that section.
8. **Validate the owned source pair.** Use Core's `skills/queen-wasp-stinger/references/scripts/per-type-validation.py` with each resolved source path, `--type skill` or `--type agent`, and `--harness all`. Synchronize the source catalog and run `python3 scripts/validate.py` from the source repository root. Zero errors before calling the pair registered.
9. **Build the selected projections.** From the canonical source root, use the existing `python3 scripts/build.py --packs <optional-owner-id-or-none> --out dist/registration-check` and inspect the generated home/plugin carriers. Core is always included. Validate those outputs separately; building a distribution does not authorize installing it, replacing an existing output owned by another task, or publishing it.
10. Report back: the base name registered, the roster row and guide file paths, every sibling cross-linked, any multi-Drone sequence touched, and the validation result from steps 8 and 9.

## Arguments

`$1` (or `$ARGUMENTS`) is the shared base name of the pair, for example `payments` for `payments-wasp-drone` and `payments-stinger`. If it is missing, ask for it before doing anything else; this command cannot guess which pair to register.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

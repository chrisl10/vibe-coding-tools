# Learn The Wasp Nest

The Wasp Nest is easiest to understand in three passes: install a plugin, learn what each component owns, then use the Library to define work before dispatching a Drone. You can enter this guide at any page. Each page names its purpose and links to the operational component when you need its exact instructions.

## Start using it

New here? Read [How We Build](guides/HOW-WE-BUILD.md) first ([branded PDF](pdf/How-We-Build-The-Wasp-Nest.pdf)). It walks the whole workflow, from setting up your computer to a merged pull request, in plain language.

1. [Get started](guides/GETTING-STARTED.md) with a public marketplace install and the two separate setup offers.
2. [Understand the pieces](guides/COMPONENTS.md), then try one bounded request with [Pest Controller](guides/COMMANDS.md).
3. [Set up the Library](guides/LIBRARY-STRUCTURE.md) and learn [why its documents exist](concepts/WHY-THE-LIBRARY.md).
4. Plan a new product with `/product-studio:plan-product`: strategy, then design, then the PRD map, wave plan and Definition of Done. Then [write a PRD](guides/WRITE-A-PRD.md) for planned behavior, [write an IRD](guides/WRITE-AN-IRD.md) for a tracked defect, or [agree on a CTR](guides/WRITE-A-CTR.md) before parallel work shares an interface.
5. [Execute a PRD](guides/PRD-EXECUTION.md) with acceptance criteria and evidence.
6. [Choose a document workflow](guides/DOCUMENT-WORKFLOWS.md): prepare an app with App Primer Zero, refresh stale code knowledge with KB Refresh, or turn a library into reader packets with Library Packets.

## Understand the component model

| Question | Read |
| --- | --- |
| Why use a specialist and how is one scoped? | [Drones](guides/DRONES.md) |
| What does a reusable skill contain? | [Stingers](guides/STINGERS.md) |
| How do named workflows route or close work? | [Commands](guides/COMMANDS.md) |
| How do I prepare, refresh or share the Library? | [Document workflows](guides/DOCUMENT-WORKFLOWS.md) |
| Which guidance stays active? | [Rules](guides/RULES.md) |
| What runs at a lifecycle event? | [Hooks](guides/HOOKS.md) |
| What can each coding harness actually load? | [Harness capabilities](reference/HARNESS-CAPABILITIES.md) |

The [hook catalog](reference/HOOK-CATALOG.md) lists shared hook programs and their limits. The [glossary](guides/GLOSSARY.md) defines Wasp Nest terms. The [complete plugin catalog](reference/PLUGIN-CATALOG.md) links every shipped Drone and Stinger without making this learning path a 300-item roster.

## Work safely and recover

- [Model selection](guides/MODEL-SELECTION.md) explains matching a scoped task to a model, without changing its authority.
- [Security and secrets](guides/SECURITY-AND-SECRETS.md) separates learning examples from live credentials and external effects.
- [Troubleshooting](guides/TROUBLESHOOTING.md) covers missing packs, commands, and onboarding prompts.

## Examples and source of truth

[Worked learning examples](examples/README.md) connect a PRD, an accepted CTR revision, implementation evidence, and an IRD without pretending those examples are a live project's plans. The canonical [Get Started Library templates](../skills/get-started-stinger/templates/library/), [Library examples](../skills/library-stinger/examples/), and [Contract Writing handoff](../skills/contract-writing-stinger/examples/prd-parallel-handoff.md) remain with their plugins. This learning section teaches them; it does not maintain second copies that can drift.

The public marketplace is generated from the canonical source repository. If a guide is unclear or a pack needs a new example, [open an issue](https://github.com/legioncodeinc/vibe-coding-tools/issues) with the page and the step that confused you.

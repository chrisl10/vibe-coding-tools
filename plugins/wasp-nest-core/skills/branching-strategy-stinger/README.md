# branching-strategy-stinger

This skill equips `branching-strategy-wasp-drone` to advise teams on version-control workflow: which branching model to adopt (trunk-based, GitHub Flow, GitFlow), how to run release and hotfix branches safely, when to use feature flags instead of long-lived branches, and when GitHub Merge Queue pays for its complexity.

The stinger is grounded in 2025-2026 research (25 external sources) and the 2025 DORA report, with the decision frameworks distilled into seven focused guides and two worked examples.

See [`research/research-summary.md`](research/research-summary.md) for the research corpus executive summary, and [the Drone identity](../../agents/branching-strategy-wasp-drone.md) plus [its routing guide](../pest-controller-suit/guides/branching-strategy-wasp-drone.md) for scope, inputs and outputs.

## Current plugin owner

This capability stays in required Wasp Nest Core. Its canonical source is src/skills, with canonical ownership recorded in the root [plugin catalog](../../../plugin-catalog.json). Its SKILL.md metadata declares any standalone/orchestrator exception; specialist agents keep their actual paired Stinger. Host home/plugin files are generated carriers. Use [the layout and selection guide](../../../docs/PLUGIN-LAYOUT.md) when a workflow calls an optional specialist; source references alone do not enable an installed plugin.

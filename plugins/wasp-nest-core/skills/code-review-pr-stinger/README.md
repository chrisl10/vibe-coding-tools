# code-review-pr-stinger

Code review as a culture, not a gate. This Stinger encodes PR description templates, review checklists, the small-PR discipline, async-first norms for distributed teams, rubber-stamp detection, and the review-as-mentorship lens -- backed by the 2026 research corpus documented in `research/research-summary.md`.

Paired with `code-review-pr-wasp-drone`. Read [the Drone identity](../../agents/code-review-pr-wasp-drone.md), [its routing guide](../pest-controller-suit/guides/code-review-pr-wasp-drone.md), and the research executive summary at `research/research-summary.md`.

## Current plugin owner

This capability stays in required Wasp Nest Core. Its canonical source is src/skills, with canonical ownership recorded in the root [plugin catalog](../../../plugin-catalog.json). Its SKILL.md metadata declares any standalone/orchestrator exception; specialist agents keep their actual paired Stinger. Host home/plugin files are generated carriers. Use [the layout and selection guide](../../../docs/PLUGIN-LAYOUT.md) when a workflow calls an optional specialist; source references alone do not enable an installed plugin.

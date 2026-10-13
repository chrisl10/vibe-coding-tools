# Discover an outcome and select its owner

Read [the packaged index](../references/outcome-index.json) or run the read-only [shortlist helper](../scripts/outcome-route.py) with the user's desired outcome. Resolve its path from the loaded skill location, not a guessed working directory. Python is optional; the index can be read directly when no execution tool is available.

1. Capture the desired result in the user's words. Reuse supplied experience, platform and product decisions; ask only missing information that changes routing.
2. Find a shortlist. The helper takes a query plus optional bucket and bounded limit. Its score is word overlap, not quality, value or availability.
3. Read the candidate's original audit disposition and current evidence state. `DOCUMENTED_EXISTING` means source scope fit; `PROPOSED` means this outcome still needs a qualified enhancement, composition or new owner. `SOURCE_REGISTERED` identifies an actual source family through `registered_skill`, `registered_owner` and `registered_command`; inspect the exact outcome scope and current review evidence before treating it as covered. None of these states means installed availability, human learning success, provider readiness or runtime passed.
4. In source work, look up exact component ownership in the current `plugin-catalog.json` and read the canonical path. In installed work, resolve the exact chosen skill/command through Core's `hooks/resolve-component.py`, using the actual selected registry. Inspect manifests and prerequisite closure manually if the host has no shell. Do not load a source path as an installed substitute.
5. Read the matching Drone guide's triggers and negative routing. Validate that the specialist owns the requested result, not merely a related noun. A command in the index may be proposed; verify it actually exists in the selected owner before advertising it as runnable.
6. Return one route with its inputs, required owners, expected artifact and evidence limits. Continue the requested workflow only when its scope is authorized and capabilities are present. Arm each dispatched Drone with the resolved paired Stinger first.
7. For a gap, keep the proposed entry explicit and hand the locked topic to Queen. Do not create wrappers or register new roles as a side effect of discovery.

Example: "explain this technical post" should shortlist a technical explanation outcome. After the Developer Learning owner is selected and qualified, use its technical-explainer pair. A broader "teach me to build an app" remains a separate learning-path scope and should not be described as implemented by that pair.

Example failure: a queried desktop outcome may identify Tauri as an adjacent owner, but a host without a selected desktop pack cannot launch its native workflow. Explain the missing prerequisite and preserve the user's scope.

Grounding: [local primary distillation](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/pest-controller-suit/references/research/outcome-routing/distillation.md). Host command projection limits come from [Queen's current harness guide](../../queen-wasp-stinger/guides/harness-support-matrix.md).

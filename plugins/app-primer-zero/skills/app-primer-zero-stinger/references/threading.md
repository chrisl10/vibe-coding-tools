# Source, distribution and runtime threading

App Primer Zero is the optional source unit `packs/app-primer-zero/`, with `skills/app-primer-zero-stinger/SKILL.md` and `commands/app-primer-zero.md`. Its standalone skill composes core methods without adding a paired Drone or duplicating specialist implementations.

## Canonical ownership

The root `plugin-catalog.json` records each plugin's canonical components and prerequisites. App Primer Zero remains a separate optional plugin requiring `wasp-nest-core`. Core retains Get Started, Library, Knowledge, Contract Writing, Security, Quality, repository-health and routing. Additional implementation specialists are selected only when present and required by the target app.

Maintain this pack's content, examples, templates and helpers in its source unit. Change component ownership, shared packaging or prerequisites through the catalog and corresponding source methods together. Generated inventories and manifests are projections, not a second independent ownership map. Do not revive retired aliases or compatibility bridges to work around a missing component.

## Build and home entry points

The catalog-driven builder produces Core plus the selected optional plugin distributions, manifest projections, marketplaces and home trees. An explicit `--packs app-primer-zero` selection includes its Core prerequisite. It generates the `source-command-app-primer-zero` skill from this pack's flat command and copies selected commands and wrappers into the applicable home trees.

Direct invocation of `app-primer-zero-stinger` remains the common entry point. Plugin installations can expose `app-primer-zero:app-primer-zero`; Codex can invoke the discovered generated command wrapper. Check the actual client selector before claiming a native slash command exists. Native threading, model selection and capacity are independent of packaging.

Every operational guide, template, script, example and distillation lives beneath the skill directory. That preserves resources when individual skills are copied into home trees. The pack-root README, license and flat command are distribution components. Do not move runtime resources to an uncopied sibling directory.

## Explicit core resolution

The installed-plugin registry is `~/.wasp-nest/installed-plugins.json`, with `WASP_NEST_PLUGIN_REGISTRY` as an override. Core's `hooks/resolve-component.py` resolves a skill, agent or command from registered plugin roots and checks ownership, installed identity, matching catalog version, prerequisites and component presence. See [core dependencies](core-dependencies.md) for the exact invocation and JSON shapes.

The source installer writes the registry for its selected plugins. This skill reads the resulting registration; it does not create or amend it automatically. Missing components, mismatched versions or unmet prerequisites stop the dependent phase. Do not borrow an unrelated cache, ignore a refusal, or guess another personal home/version.

Source inspection and temporary-build tests can establish packaging and resolver behavior without changing a user's installation. They do not establish installed-client discovery, native agent availability, provider behavior or deployment. State the environment and evidence supporting each result.

## Public packaging checks

Check this pack's skill/command/manifests, source and packaged Markdown destinations, helpers, retained resource bytes, catalog ownership and registry resolution. Include generated command wrappers and selected home output in the checks. Record the full candidate source identity or explicitly label a dirty working-tree preview.

Raw research observations remain dated source provenance. Builds retain the distillation and operational resources while omitting raw captures and generated filesystem metadata. Historical preview ZIPs and reports remain evidence of their dated bytes, not proof of a later release. A build does not authorize live installation, publication or execution of an app's wave plan.

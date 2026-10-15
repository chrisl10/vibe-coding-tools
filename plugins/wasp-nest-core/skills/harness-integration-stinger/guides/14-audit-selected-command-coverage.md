# Audit command coverage for selected packs

Use for O299. Load the digest and fill [the coverage matrix](../templates/selected-command-coverage.md).

1. Identify target task, host version and actual carrier. Record trusted Core root and explicit selected registry observation. A marketplace install, directory cache or source catalog is a separate layer. Never crawl cached siblings into the selection.
2. For each selected owner, enumerate its live catalog commands, components and role classifications. Verify flat command file and required resources. Resolve each command with kind=command and each active workflow's exact prerequisite key. A command-only composition or standalone skill can be legitimate without native agents.
3. Inspect the actual built carrier for flat commands and generated source-command adapters. An adapter reads a command procedure; it is not another canonical domain skill. Verify its link, resources and owner. Native plugin layouts and home projections have different path roots; inspect each claimed carrier.
4. Read every task-relevant command in full and identify its called specialists/resources and conditional branches. Source owner presence does not establish selected prerequisites, native roles or permission. Preserve missing-source, missing-selected-prerequisite, missing-resource, unsupported-host and unknown-native-discovery as distinct findings.
5. Classify command availability: source-qualified, package-qualified, selected-resolved, native-discovered, native-executed or unsupported. Attach exact evidence, without promoting one layer to another. An uninstalled pack is a selection gap, not proof its source lacks commands. A native slash discovery observation proves discovery only.
6. Check source-maintenance commands (forge/register/drift-audit/re-research) require a writable source checkout; installed cache content is not writable forge source. Root-relative resource links must work from the actual carrier. Do not invent slash invocation on a host that exposes the command as a skill.
7. Reuse scripts/test_outcome_workflows.py, scripts/test_plugin_topology.py and scripts/test_codex_plugin_distribution.py for source/package checks; independent final build proof belongs to the parent/CI-release owner. Record native tests as UNEXECUTED until actual authorized invocation exists.

Report one prioritized coverage list, exact missing steps and permitted fallback. Do not install or activate anything to fill a receipt.

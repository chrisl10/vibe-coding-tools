# 04 Knowledge docs via knowledge-stinger

Goal: you cannot fix what you have not documented. Before a package changes an area, that area has a short knowledge doc saying what it does, how it fits together, and what must not break.

Load first: `src/skills/knowledge-stinger/SKILL.md`, `README.md`, `guides/01-domain-taxonomy.md`, `02-document-format.md`, `03-analysis-workflow.md`, `templates/knowledge-doc-template.md`, and one example. In an installed plugin these are in the `knowledge-stinger` skill folder. If it is not installed, tell the orchestrator; do not improvise the format.

## When to propose one

For each work package, check the area (path prefix) against `library/knowledge/private/**`. Propose a doc only when none covers it (search by area name and by key file names). Prefer one doc per area shared by several packages. Typical triggers: structural packages (refactor, dedupe, split), packages touching auth, data or security boundaries, and any package whose area has no tests.

## What goes in it (and what does not)

Describe the code as it is today, not as it should be. Sections per the format guide: why the area exists, a Mermaid diagram of the main flow or components, the entry points and files, data and side effects, invariants that must not change, known issues (link finding ids by plain description), and how it is tested. Ground every claim in files you read; cite paths. 100 to 400 lines. Do not copy the audit text in; link nothing outside the repository except by name.

## Placement

`library/knowledge/private/<domain>/<slug>.md` with domain from the taxonomy guide (`architecture`, `auth`, `data`, `frontend`, `infrastructure`, `security`, `standards`, and so on). Header per the format guide: `> Category: <Domain> | Version: 1.0 | Date: <Month YYYY> | Status: Draft`. Status is Draft until a human confirms it.

## How the Drone works through several

1. Do the shared overview first (the knowledge-stinger analysis workflow batch A), then the per-area docs.
2. Fewer than five docs: write them yourself in order. Five or more: ask the orchestrator to dispatch `knowledge-wasp-drone` in parallel, one area per Drone, with a shared brief (the approved file list, the format guide, and the rule to describe current behavior only). You do not spawn Drones yourself.
3. After writing, cross-check every Related link resolves.

## Link back to the PRD

Each PRD gets the knowledge doc in its Related section and a first implementation step: "Read the knowledge doc; correct it if the code disagrees."

## Sources

- Knowledge rules: `knowledge-stinger` guides and templates (core skill)
- research/raw/test--characterization-tests.md (source-repository research, not shipped) (documenting actual behavior, not wished-for behavior)

# Documentation Tools

Refresh, extract, publish and package documentation from real sources.

Advanced documentation production is optional. Basic Library and Knowledge authorship remains in core.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 8 skills, 8 agents and 3 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [api-docs-stinger](skills/api-docs-stinger/SKILL.md) | Build and maintain API docs. Use for OpenAPI examples, renderer choice, hosting, SDK consumer compatibility, or changelogs. |
| [archivist-stinger](skills/archivist-stinger/SKILL.md) | Prepares an acquired repository for archival: provenance intake, attribution and PII scrub, docs merge into library/, knowledge-base fleet, identifier rename, verification. Any language or license. |
| [docs-site-stinger](skills/docs-site-stinger/SKILL.md) | Select and maintain developer docs sites. Use for Docusaurus, Mintlify, Starlight, Diataxis, search, or docs-as-code CI. |
| [kb-refresh-stinger](skills/kb-refresh-stinger/SKILL.md) | Full documentation refresh: inventory, writer fleet, grounded citations, adversarial verification, security and quality gates, one ready PR per unit, PDF plus markdown report, master suspect list. |
| [library-packets-stinger](skills/library-packets-stinger/SKILL.md) | Turn a library into cited audience packets in Markdown, Word and branded PDF. Use for executive, public, sales, service or engineering documents grounded in existing sources. |
| [markdown-mdx-content-pipeline-stinger](skills/markdown-mdx-content-pipeline-stinger/SKILL.md) | Build Markdown and MDX pipelines. Use for compiler choice, remark/rehype plugins, syntax highlighting, diagrams, or sanitization. |
| [mcp-tool-docs-stinger](skills/mcp-tool-docs-stinger/SKILL.md) | Documents MCP tools, TypeScript APIs, and CLIs honestly: schema, output, side effects, examples, doc-to-code sync. Use when writing or auditing tool/API/CLI docs. |
| [wiki-stinger](skills/wiki-stinger/SKILL.md) | Extract code entities into the wiki. Use for atomic pages, backlinks, inferred ADRs, contradiction checks, or wiki linting. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install documentation-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use library-packets-stinger on [library folder] to prepare founder and public briefs in Markdown, Word and branded PDF, with citations. Report gaps instead of inventing claims.
```

Expected result: The selected document packet with citations and page-review evidence, or a specific list of missing sources or tools.



For a repository documentation refresh:

```text
Use kb-refresh-stinger on [repository] within [scope]. Confirm the pinned base, docs branch, read-only set, fleet plan and cost approval before launching workers. Inventory the docs, compare claims with current code and update supported content. Keep notes/ human-only. Prepare changes locally; do not commit or push without explicit approval.
```

Expected result: a keep/update/write inventory, refreshed knowledge, citations, report.md, report.pdf, SUSPECTS.md and verification evidence. Full repository discovery also needs Code Audit Tools.

Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/documentation-tools:explain-repository` ([procedure](commands/explain-repository.md)) | Explain how a supplied repository works using source evidence, an eighth-grade reading level, and bounded analogies. |
| `/documentation-tools:kb-refresh` ([procedure](commands/kb-refresh.md)) | Run the full documentation audit and refresh pipeline on a repository: inventory, writer fleet, grounded citations, adversarial verification, security and quality gates, one ready PR per unit, then the work report in PDF plus markdown and the master suspect list. Trigger with "refresh the docs", "kb refresh", "rebuild the knowledge base", "doc swarm". |
| `/documentation-tools:library-packets` ([procedure](commands/library-packets.md)) | Produce cited audience documents from a library in Markdown, Word and branded PDF. Check source coverage, public boundaries and every final page. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [api-docs-wasp-drone](agents/api-docs-wasp-drone.md) | API documentation authority: Swagger UI / Redoc / Scalar / Mintlify / Stoplight / Bump.sh tool selection, OpenAPI spec enrichment with JSON request + response examples, hosted and self-hosted deployment (GitHub Pages / Netlify / Vercel / Docker), SDK generation for TypeScript / Python / Go, and changelog discipline. | [api-docs-stinger](skills/api-docs-stinger/SKILL.md) |
| [archivist-wasp-drone](agents/archivist-wasp-drone.md) | Prepares an acquired software repository, any language and any inbound license, for permanent archival as a research object: records the ownership basis and third-party carve-outs, strips the seller's attribution, license grants, and personal identifiers while preserving every third-party notice, merges the legacy docs tree into library/knowledge, prepares the shared brief and assignments for the knowledge-wasp-drone fleet that the orchestrator dispatches, renames the product identifier on request, verifies to zero, and files the archivist report. | [archivist-stinger](skills/archivist-stinger/SKILL.md) |
| [docs-site-wasp-drone](agents/docs-site-wasp-drone.md) | Documentation-site infrastructure specialist. | [docs-site-stinger](skills/docs-site-stinger/SKILL.md) |
| [kb-refresh-wasp-drone](agents/kb-refresh-wasp-drone.md) | Documentation-refresh fleet runner. | [kb-refresh-stinger](skills/kb-refresh-stinger/SKILL.md) |
| [library-packets-wasp-drone](agents/library-packets-wasp-drone.md) | Produce source-grounded library packets in Markdown, Word, branded PDF and citations for executives, public readers, sales, service and engineers. | [library-packets-stinger](skills/library-packets-stinger/SKILL.md) |
| [markdown-mdx-content-pipeline-wasp-drone](agents/markdown-mdx-content-pipeline-wasp-drone.md) | Markdown/MDX content processing specialist. | [markdown-mdx-content-pipeline-stinger](skills/markdown-mdx-content-pipeline-stinger/SKILL.md) |
| [mcp-tool-docs-wasp-drone](agents/mcp-tool-docs-wasp-drone.md) | Tool, API, and CLI documentation authority - documenting MCP (and other schema-selected) tools with honest name/purpose/input-schema/output/side-effects/annotations/examples, TypeScript public API reference generation (TypeDoc, and API Extractor for a reviewable public-API contract), CLI command references, doc-to-code sync, and changelog discipline tied to a released artifact's version. | [mcp-tool-docs-stinger](skills/mcp-tool-docs-stinger/SKILL.md) |
| [wiki-wasp-drone](agents/wiki-wasp-drone.md) | Extracts code entities (functions, classes, modules, services, endpoints, env vars, config keys, data models, React components, SQL tables, queues, cron jobs, feature flags) and architectural concepts from per-repo source code plus git context, files them as atomic markdown pages with `[[backlinks]]` into `library/knowledge/private/wiki/`, infers ADRs from commit messages that encode decisions, and runs an active four-artifact contradiction protocol when entity contracts change. | [wiki-stinger](skills/wiki-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `kb-refresh full repository discovery` also needs `code-audit-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

# HighLevel Pack

One installable Wasp Nest pack with three distinct HighLevel jobs:

| Job | Stinger | Drone |
| --- | --- | --- |
| REST API integrations, OAuth, CRM resources, and webhooks | [GoHighLevel](skills/gohighlevel-stinger/SKILL.md) | [GoHighLevel Drone](agents/gohighlevel-wasp-drone.md) |
| AI Studio and other HighLevel AI creation surfaces | [AI Studio](skills/highlevel-ai-studio-stinger/SKILL.md) | [AI Studio Drone](agents/highlevel-ai-studio-wasp-drone.md) |
| Offline account-export conversion to Mermaid charts | [GHL to Mermaid](skills/ghl-to-mermaid-stinger/SKILL.md) | [GHL to Mermaid Drone](agents/ghl-to-mermaid-wasp-drone.md) |

The converter reads a location export. It does not call the live HighLevel API. The REST API Stinger owns live integration; the AI Studio Stinger owns in-product creation and publishing. Install this pack when you need any of the three. A fresh core-only install omits all three specialist pairs; the core router can identify them but must ask for this pack before dispatch. Purge the previous layout before installing version 3; legacy aliases are not shipped.

The three Python scripts in the Stinger's `scripts/` directory are copied from [highlevel-workflow-to-mermaid-chart](https://github.com/legioncodeinc/highlevel-workflow-to-mermaid-chart) at commit `2168ef1`. No customer export or generated chart is bundled. Python 3.9 or newer is sufficient for the converter.

First-party pack material is licensed under [AGPL-3.0-or-later](LICENSE.md). External HighLevel and Mermaid research captures remain under their publishers' rights; see [third-party notices](THIRD-PARTY-NOTICES.md). The built plugin includes distilled research and omits raw captures.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 3 skills, 3 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [ghl-to-mermaid-stinger](skills/ghl-to-mermaid-stinger/SKILL.md) | Turn a GoHighLevel/HighLevel account JSON export into per-workflow files and Mermaid flowcharts. Use for GHL snapshot exports, workflow diagrams, automation maps, or SuperSnapshot AI exports. |
| [gohighlevel-stinger](skills/gohighlevel-stinger/SKILL.md) | GoHighLevel API authority - OAuth vs Private Integration Tokens, contacts/opportunities/calendars, inbound/outbound webhooks, rate limits, Marketplace apps. Use for GoHighLevel/HighLevel integration. |
| [highlevel-ai-studio-stinger](skills/highlevel-ai-studio-stinger/SKILL.md) | HighLevel AI Studio specialist for Vibe sites, Content AI, Funnel & Website AI, and WordPress AI pages. Use for HighLevel AI content, site building, publishing, or troubleshooting. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install highlevel@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use ghl-to-mermaid-stinger to map [supplied HighLevel JSON export] into per-workflow files and readable flowcharts.
```

Expected result: Workflow maps from the supplied export, or a scoped HighLevel API/AI Studio task using the matching skill.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/highlevel:map-highlevel` ([procedure](commands/map-highlevel.md)) | Turn a supplied HighLevel export into traceable workflow maps, asset links, and an honest gaps report. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [ghl-to-mermaid-wasp-drone](agents/ghl-to-mermaid-wasp-drone.md) | Turns HighLevel account exports into per-workflow JSON and readable Mermaid charts. | [ghl-to-mermaid-stinger](skills/ghl-to-mermaid-stinger/SKILL.md) |
| [gohighlevel-wasp-drone](agents/gohighlevel-wasp-drone.md) | GoHighLevel (HighLevel) API integration specialist - OAuth 2.0 vs Private Integration Tokens, contacts/opportunities/pipelines/calendars/conversations, inbound and outbound webhooks, workflows, rate limits, and Marketplace app creation. | [gohighlevel-stinger](skills/gohighlevel-stinger/SKILL.md) |
| [highlevel-ai-studio-wasp-drone](agents/highlevel-ai-studio-wasp-drone.md) | HighLevel AI Studio and AI creation specialist for Vibe sites, Content AI, Ask AI, Funnel & Website AI, Blog Post AI, Email AI, and WordPress AI pages. | [highlevel-ai-studio-stinger](skills/highlevel-ai-studio-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

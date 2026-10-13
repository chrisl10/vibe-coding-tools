# Media and Creative Tools

Create consented photography and integrate voice and video production.

Media has asset consent, provider job and metadata rules that should not inflate core. Ship blank model templates, never ingested people.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 4 skills, 4 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [elevenlabs-api-stinger](skills/elevenlabs-api-stinger/SKILL.md) | ElevenLabs API integration for speech, voices, streaming, webhooks, usage, and key boundaries. Use for ElevenLabs API implementation, review, or troubleshooting. |
| [heygen-api-stinger](skills/heygen-api-stinger/SKILL.md) | HeyGen API integration for video generation, avatars, assets, webhooks, limits, and safe asynchronous delivery. Use for HeyGen API implementation or debugging. |
| [natural-photography-stinger](skills/natural-photography-stinger/SKILL.md) | Generate or retouch photos of consented models. Use for realistic capture prompts, source-image gating, or honest EXIF metadata. |
| [product-demo-stinger](skills/product-demo-stinger/SKILL.md) | Plan honest product demos and tutorials with claim-to-scene evidence, accessible narration, failure coverage and explicit mock disclosures. Use before recording or reviewing a walkthrough. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install media-and-creative-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use natural-photography-stinger with [approved consented model folder] and [requested scene]. Check the source/model gate before generation.
```

Expected result: The approved media workflow and its evidence. Model consent, provider access and any paid generation remain required inputs.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/media-and-creative-tools:create-product-media` ([procedure](commands/create-product-media.md)) | Create a product-media brief and supported consented photo or provider-media workflow with verifiable deliverables. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [elevenlabs-api-wasp-drone](agents/elevenlabs-api-wasp-drone.md) | ElevenLabs API integration specialist for speech, voices, streaming, usage telemetry, and safe server boundaries. | [elevenlabs-api-stinger](skills/elevenlabs-api-stinger/SKILL.md) |
| [heygen-api-wasp-drone](agents/heygen-api-wasp-drone.md) | HeyGen API integration specialist for asynchronous video jobs, avatars, assets, webhooks, limits, and safe delivery. | [heygen-api-stinger](skills/heygen-api-stinger/SKILL.md) |
| [natural-photography-wasp-drone](agents/natural-photography-wasp-drone.md) | Photographic generation and retouching specialist for consented model work. | [natural-photography-stinger](skills/natural-photography-stinger/SKILL.md) |
| [product-demo-wasp-drone](agents/product-demo-wasp-drone.md) | Prepare evidence-bound product demos and tutorials, scenes, narration and disclosures. | [product-demo-stinger](skills/product-demo-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

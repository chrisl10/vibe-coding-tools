# Infrastructure Decision Tools

Prepare platform assets and account dependencies without implicit setup actions.

Requires `wasp-nest-core`. This is a source candidate; no installation or native-host qualification is implied.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 6 skills, 6 agents and 6 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [digitalocean-platform-stinger](skills/digitalocean-platform-stinger/SKILL.md) | Recommend DigitalOcean App Platform or Droplet fit from supplied workload, data, operator and recovery needs. Prepare dated cost inputs and readiness handoffs; no provisioning. |
| [infrastructure-fit-stinger](skills/infrastructure-fit-stinger/SKILL.md) | Recommend one infrastructure topology from workload, budget and operator skills. Compare managed hosting and VPS with sourced constraints and cost-owner handoff. |
| [launch-assets-stinger](skills/launch-assets-stinger/SKILL.md) | Prepare launch accounts, assets and owners for web, desktop, mobile or integrations. Produce a dated readiness ledger with costs, prerequisites and blockers. |
| [network-boundaries-stinger](skills/network-boundaries-stinger/SKILL.md) | Choose firewall, WAF and rate-limit placement from actual network flows. Return one sourced control recommendation with owner and proof gaps. |
| [railway-platform-stinger](skills/railway-platform-stinger/SKILL.md) | Select Railway from supplied workload, state, jobs, networking, cost inputs and recovery duties. Return one sourced recommendation or provisional choice and owner gaps. |
| [vultr-platform-stinger](skills/vultr-platform-stinger/SKILL.md) | Assess Vultr workload fit, compute forms, operator duties, data/recovery and dated cost inputs. Use for a read-only Vultr recommendation. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install infrastructure-decision-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use launch-assets-stinger to prepare the accounts, assets and owners needed for [product/platform/milestone].
```

Expected result: An editable readiness ledger separating documentation requirements, owner reports and observed readiness, with prerequisites and blockers.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/infrastructure-decision-tools:assess-digitalocean` ([procedure](commands/assess-digitalocean.md)) | Assess DigitalOcean service fit with dated responsibilities, eligibility, scaling, recovery and cost inputs for a supplied workload. |
| `/infrastructure-decision-tools:assess-railway` ([procedure](commands/assess-railway.md)) | Assess Railway workload fit with dated service, operating, recovery and cost constraints. |
| `/infrastructure-decision-tools:assess-vultr` ([procedure](commands/assess-vultr.md)) | Assess Vultr workload fit with dated service, operating, recovery and cost constraints. |
| `/infrastructure-decision-tools:choose-infrastructure` ([procedure](commands/choose-infrastructure.md)) | Recommend one infrastructure topology from workload, budget and operator capacity, with sourced constraints and recovery/cost handoffs. |
| `/infrastructure-decision-tools:plan-network-boundaries` ([procedure](commands/plan-network-boundaries.md)) | Choose network firewall, WAF and application rate-limit layers from actual trust boundaries, protocols and operating constraints. |
| `/infrastructure-decision-tools:prepare-assets` ([procedure](commands/prepare-assets.md)) | Prepare the minimum launch assets and accounts with owners, environments, dated costs, prerequisites and blockers. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [digitalocean-platform-wasp-drone](agents/digitalocean-platform-wasp-drone.md) | Use for DigitalOcean App Platform/Droplet workload fit, operations, data/recovery and dated cost handoff. | [digitalocean-platform-stinger](skills/digitalocean-platform-stinger/SKILL.md) |
| [infrastructure-fit-wasp-drone](agents/infrastructure-fit-wasp-drone.md) | Recommend one workload-matched infrastructure topology. | [infrastructure-fit-stinger](skills/infrastructure-fit-stinger/SKILL.md) |
| [launch-assets-wasp-drone](agents/launch-assets-wasp-drone.md) | Prepare platform-specific launch accounts, assets and owners. | [launch-assets-stinger](skills/launch-assets-stinger/SKILL.md) |
| [network-boundaries-wasp-drone](agents/network-boundaries-wasp-drone.md) | Choose firewall, WAF and rate-limit layers from actual flows. | [network-boundaries-stinger](skills/network-boundaries-stinger/SKILL.md) |
| [railway-platform-wasp-drone](agents/railway-platform-wasp-drone.md) | Assess Railway fit for supplied runtime, state, jobs, network, region, cost and recovery requirements. | [railway-platform-stinger](skills/railway-platform-stinger/SKILL.md) |
| [vultr-platform-wasp-drone](agents/vultr-platform-wasp-drone.md) | Use for read-only Vultr compute/workload fit, retained operations, data/recovery and dated cost handoff. | [vultr-platform-stinger](skills/vultr-platform-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `prepare-assets-native` also needs `backend-and-desktop-tools`.
- `prepare-assets-identity` also needs `platform-and-release-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

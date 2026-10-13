# Software Economics Tools

Model supplied software economics and costs with explicit scenarios and evidence.

Requires `wasp-nest-core`. This is a source candidate; no installation or native-host qualification is implied.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 4 skills, 4 agents and 4 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [operating-cost-stinger](skills/operating-cost-stinger/SKILL.md) | Estimate low/base/high monthly operating costs from supplied workload and dated rates, separating allowances, shared credits, fees, floors and labor. Use for infrastructure operating budgets. |
| [saas-pricing-stinger](skills/saas-pricing-stinger/SKILL.md) | Recommend one provisional SaaS price/model from buyer value, costs and dated evidence. Use for seats, tiers, usage, credits, price experiments or missing willingness-to-pay evidence. |
| [services-quoting-stinger](skills/services-quoting-stinger/SKILL.md) | Prepare service quotes and agency SOW drafts from supplied scope/costs. Use for project pricing, acceptance criteria, maintenance, unknown integrations or scope changes. |
| [unit-economics-stinger](skills/unit-economics-stinger/SKILL.md) | Model supplied software prices and costs into margins, break-even, losses, and scenarios. Use for an economic worksheet, operating economics, or free/trial, abuse-cost, refund and usage sensitivity. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install software-economics-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use unit-economics-stinger with [supplied price and cost assumptions] to model margins and break-even. Use operating-cost-stinger for dated workload/rate scenarios.
```

Expected result: A reviewable economic worksheet with explicit units, currency, source dates, scenarios and calculator evidence; no live billing change.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/software-economics-tools:estimate-operating-cost` ([procedure](commands/estimate-operating-cost.md)) | Estimate low/base/high monthly cash operating costs and separate operator time value from supplied workload and dated rates. |
| `/software-economics-tools:model-unit-economics` ([procedure](commands/model-unit-economics.md)) | Produce a reviewable economic worksheet from supplied prices, costs, refunds and usage scenarios. No provider writes. |
| `/software-economics-tools:price-my-product` ([procedure](commands/price-my-product.md)) | Prepare one provisional SaaS price/model recommendation with buyer evidence, workload economics, limits and an unexecuted price test. |
| `/software-economics-tools:quote-project` ([procedure](commands/quote-project.md)) | Prepare a scoped proposed website, app/integration or maintenance quote with effort/cost evidence, pricing maths and change boundaries. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [operating-cost-wasp-drone](agents/operating-cost-wasp-drone.md) | Estimate monthly software operating costs from supplied workloads and dated rates. | [operating-cost-stinger](skills/operating-cost-stinger/SKILL.md) |
| [saas-pricing-wasp-drone](agents/saas-pricing-wasp-drone.md) | Recommend one provisional SaaS price/model with buyer value, current evidence, cost feasibility, limits and a test plan. | [saas-pricing-stinger](skills/saas-pricing-stinger/SKILL.md) |
| [services-quoting-wasp-drone](agents/services-quoting-wasp-drone.md) | Prepare proposed service quotes and agency statements of work with observable scope, supplied costs, discovery limits, maintenance and change requests. | [services-quoting-stinger](skills/services-quoting-stinger/SKILL.md) |
| [unit-economics-wasp-drone](agents/unit-economics-wasp-drone.md) | Model supplied prices and operating costs into contribution, gross margin, break-even and scenario worksheets. | [unit-economics-stinger](skills/unit-economics-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

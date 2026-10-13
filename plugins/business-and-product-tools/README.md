# Business and Product Tools

Form and run a company, discover product needs, hire teams and improve delivery.

Company and product decisions belong together, while legal/finance actions retain their existing explicit-request scope.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 15 skills, 15 agents and 7 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [agile-scrum-stinger](skills/agile-scrum-stinger/SKILL.md) | Coach Scrum teams. Use for ceremonies, roles, Definition of Done, estimation, or Scrum anti-patterns. |
| [build-buy-analysis-stinger](skills/build-buy-analysis-stinger/SKILL.md) | Compare build, buy and partner approaches for one defined function using requirements, dated evidence, lifecycle costs, ownership and exit constraints. |
| [capacity-planning-stinger](skills/capacity-planning-stinger/SKILL.md) | Decide when to hire or buy services from demand, skill gaps, available hours, review capacity and dated quotes. Prepare one provisional staffing recommendation. |
| [discovery-research-stinger](skills/discovery-research-stinger/SKILL.md) | Run pre-build discovery: interviews, assumption tests, demand evidence, continue/pivot/stop decisions, and first-version scope. |
| [estimation-stinger](skills/estimation-stinger/SKILL.md) | Forecast software delivery or an AI-assisted solo build at N hours daily. Use for sizing, NoEstimates, cycle-time data, or time/cash scenarios. |
| [hiring-ats-stinger](skills/hiring-ats-stinger/SKILL.md) | Choose and configure an applicant tracking system. Use for pipeline stages, scorecards, calibration, sourcing, or ATS-to-HRIS handoff. |
| [hr-payroll-stinger](skills/hr-payroll-stinger/SKILL.md) | Choose payroll and EOR tools. Use for Gusto vs Rippling, contractor classification, international hiring, or benefits. |
| [incorporation-startup-stack-stinger](skills/incorporation-startup-stack-stinger/SKILL.md) | Set up a software company. Use for entity choice, Atlas vs Clerky, EIN, banking, bookkeeping, or founder paperwork. |
| [investor-cap-table-stinger](skills/investor-cap-table-stinger/SKILL.md) | Manage startup cap tables and fundraising paperwork. Use for SAFEs, options, 409A, priced rounds, vesting, or data rooms. |
| [kanban-flow-stinger](skills/kanban-flow-stinger/SKILL.md) | Improve Kanban flow. Use for WIP limits, cycle time, throughput, Little's Law, board design, or cumulative flow. |
| [legal-docs-stinger](skills/legal-docs-stinger/SKILL.md) | Draft SaaS legal documents with lawyer review. Use for Terms, Privacy Policy, DPA, MSA, cookie notice, or generator choice. |
| [okr-goal-setting-stinger](skills/okr-goal-setting-stinger/SKILL.md) | Write and audit OKRs. Use for measurable key results, quarterly cadence, grading, or OKR-vs-KPI decisions. |
| [product-feedback-roadmap-stinger](skills/product-feedback-roadmap-stinger/SKILL.md) | Turn customer feedback into a roadmap. Use for feedback tools, deduplication, status policy, public roadmaps, or RICE scoring. |
| [retrospective-stinger](skills/retrospective-stinger/SKILL.md) | Facilitate engineering retrospectives. Use for format selection, safety pre-check, facilitation, or action-item follow-through. |
| [software-licensing-stinger](skills/software-licensing-stinger/SKILL.md) | Explain software licenses and prepare artifact evidence for copyleft or commercial distribution review. Use for license literacy, notices, GPL or AGPL boundary questions. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install business-and-product-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use discovery-research-stinger to prepare interviews for [product question] using [known evidence]. Separate facts from open assumptions.
```

Expected result: The requested business decision aid, interview plan or team-process artifact, grounded in supplied information.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/business-and-product-tools:assess-product-risk` ([procedure](commands/assess-product-risk.md)) | Assess product assumptions, operational/security exposure and unresolved variables before a build decision. |
| `/business-and-product-tools:compare-build-buy` ([procedure](commands/compare-build-buy.md)) | Compare build, licensed vendor and partner approaches for one bounded functional slice using dated evidence and lifecycle responsibilities. |
| `/business-and-product-tools:estimate-build` ([procedure](commands/estimate-build.md)) | Forecast one person's AI-assisted software project at N hours daily, with learning, verification, external waits and separate cash/time scenarios. |
| `/business-and-product-tools:review-software-license` ([procedure](commands/review-software-license.md)) | Explain and inventory software license evidence, distribution boundaries and unresolved review questions without relabeling rights. |
| `/business-and-product-tools:scope-first-version` ([procedure](commands/scope-first-version.md)) | Turn a validated opportunity into one bounded first-version PRD with measurable acceptance and deferred scope. |
| `/business-and-product-tools:validate-idea` ([procedure](commands/validate-idea.md)) | Test an app or business idea against customer evidence, current alternatives, and a falsifiable experiment. |
| `/business-and-product-tools:work-like-a-team` ([procedure](commands/work-like-a-team.md)) | Turn a solo or small-team development goal into a five-area responsibility map, a working queue, a Definition of Done, and a review rhythm. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [agile-scrum-wasp-drone](agents/agile-scrum-wasp-drone.md) | Scrum methodology specialist: audits whether teams are actually practising Scrum, coaches Sprint Planning / Daily Scrum / Sprint Review / Retrospective / Backlog Refinement, writes Definition of Done templates (startup to enterprise), diagnoses anti-patterns (Zombie Scrum, HiPPO PO, no Sprint Goal, velocity gaming), coaches estimation (Fibonacci / Planning Poker / #NoEstimates), and recommends framework fit (Scrum vs ScrumBan vs Kanban vs Shape Up). | [agile-scrum-stinger](skills/agile-scrum-stinger/SKILL.md) |
| [build-buy-analysis-wasp-drone](agents/build-buy-analysis-wasp-drone.md) | Compare build, buy and partner sourcing for one bounded function, using requirements, dated evidence, lifecycle costs, ownership and exit constraints. | [build-buy-analysis-stinger](skills/build-buy-analysis-stinger/SKILL.md) |
| [capacity-planning-wasp-drone](agents/capacity-planning-wasp-drone.md) | Recommend when to hire or buy services from demand, actual capacity, skill gaps and dated quotes. | [capacity-planning-stinger](skills/capacity-planning-stinger/SKILL.md) |
| [discovery-research-wasp-drone](agents/discovery-research-wasp-drone.md) | Continuous product discovery coach - Teresa Torres interview cadence, Opportunity Solution Trees (OST), Jobs-to-be-Done (JTBD) interviews, assumption mapping, and prototype experiment design. | [discovery-research-stinger](skills/discovery-research-stinger/SKILL.md) |
| [estimation-wasp-drone](agents/estimation-wasp-drone.md) | Software estimation and forecasting specialist: relative-sizing frameworks (Fibonacci story points, T-shirt sizing, Planning Poker), the NoEstimates movement and its evidence base (Vasco Duarte), the planning-fallacy literature explaining why estimates are systematically wrong, and cycle-time / throughput-based probabilistic forecasting (Monte Carlo simulation, percentile-based delivery predictions). | [estimation-stinger](skills/estimation-stinger/SKILL.md) |
| [hiring-ats-wasp-drone](agents/hiring-ats-wasp-drone.md) | Applicant Tracking Systems authority for recruiting-tech stacks. | [hiring-ats-stinger](skills/hiring-ats-stinger/SKILL.md) |
| [hr-payroll-wasp-drone](agents/hr-payroll-wasp-drone.md) | HR infrastructure and payroll decision specialist for software startups - domestic payroll platform selection (Gusto, Rippling, Justworks), international contractor management and EOR (Deel, Remote.com, Oyster, Rippling Global), the W-2/1099/EOR/PEO classification matrix, equity administration handoff to Carta, and benefits brokerage. | [hr-payroll-stinger](skills/hr-payroll-stinger/SKILL.md) |
| [incorporation-startup-stack-wasp-drone](agents/incorporation-startup-stack-wasp-drone.md) | Company formation advisor for software startup founders. | [incorporation-startup-stack-stinger](skills/incorporation-startup-stack-stinger/SKILL.md) |
| [investor-cap-table-wasp-drone](agents/investor-cap-table-wasp-drone.md) | Cap-table management and fundraising paperwork specialist for startup founders. | [investor-cap-table-stinger](skills/investor-cap-table-stinger/SKILL.md) |
| [kanban-flow-wasp-drone](agents/kanban-flow-wasp-drone.md) | Kanban method specialist: WIP limit design and enforcement, flow-metric calculation (cycle time, lead time, throughput, flow efficiency), Little's Law diagnostics, visual-board design, class-of-service policies, cumulative-flow-diagram interpretation, and tool-specific implementation (Linear, Jira, GitHub Projects). | [kanban-flow-stinger](skills/kanban-flow-stinger/SKILL.md) |
| [legal-docs-wasp-drone](agents/legal-docs-wasp-drone.md) | SaaS legal documentation specialist for Terms of Service, Privacy Policy, DPA, MSA, and Cookie Notice. | [legal-docs-stinger](skills/legal-docs-stinger/SKILL.md) |
| [okr-goal-setting-wasp-drone](agents/okr-goal-setting-wasp-drone.md) | OKR methodology specialist - writes, grades, and iterates on Objectives and Key Results. | [okr-goal-setting-stinger](skills/okr-goal-setting-stinger/SKILL.md) |
| [product-feedback-roadmap-wasp-drone](agents/product-feedback-roadmap-wasp-drone.md) | Customer-feedback-to-roadmap loop specialist - Userback, Canny, Featurebase, Productboard, Frill, Productlane - in-app-widget vs portal vs voting-board taxonomy, status transitions, public vs private roadmaps, de-duplication discipline, and RICE/ICE prioritization. | [product-feedback-roadmap-stinger](skills/product-feedback-roadmap-stinger/SKILL.md) |
| [retrospective-wasp-drone](agents/retrospective-wasp-drone.md) | Retrospective facilitator and follow-through enforcer for engineering teams. | [retrospective-stinger](skills/retrospective-stinger/SKILL.md) |
| [software-licensing-wasp-drone](agents/software-licensing-wasp-drone.md) | Explain licenses and prepare exact artifact evidence for copyleft, network-use or commercial distribution review without deciding legal compatibility. | [software-licensing-stinger](skills/software-licensing-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `validate-idea-market` also needs `growth-and-customer-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

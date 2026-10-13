# Supplied-input capacity model

This arithmetic is an advisory model derived from the [evidence digest](research/distillation.md). All units, exclusions and deductions must be explicit. Calendar hours are not interchangeable with finished work, story points or supplier promises.

For each person and period, take allocated scheduled hours after leave and holidays. Subtract mutually exclusive support, meetings, existing review, coordination, and owner-chosen reserve. Record which inputs already include a deduction. Subtract once. Negative remaining time is overcommitment, not hidden zero capacity. Keep owner review time separate from supplier working time. Do not add AI as another person or multiply output by a guessed factor. [Scrum capacity](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/capacity-planning-stinger/references/research/raw/scrum-capacity.json), [Azure capacity](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/capacity-planning-stinger/references/research/raw/azure-capacity.json)

`existing_net = allocated_available - deductions - reserve`

`candidate_net = existing_net - additional_existing_team_load + candidate_usable_contribution`

`gap = required_effort - candidate_net`

Candidate contribution is already net of its own onboarding, review, coordination and calendar limits. Additional load accounts for time the current team spends briefing, reviewing, integrating, accepting, training and taking over. Separate internal engineering, specialist, review and support pools; enough aggregate hours cannot fill an unavailable security review slot. Check dependencies before treating hours as concurrent. [GitLab company example](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/capacity-planning-stinger/references/research/raw/gitlab-contractors.json)

For a managed service, contribution may be defined scope removed from the backlog rather than person-hours. Do not invent equivalent employee capacity: list the tasks displaced, acceptance evidence and retained internal load. Build and buy both retain support and exit work. [Upwork scoped milestones](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/capacity-planning-stinger/references/research/raw/upwork-milestones.json), [GitLab lifecycle example](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/business-and-product-tools/skills/capacity-planning-stinger/references/research/raw/gitlab-contractors.json)

Cash comparison uses the same currency, horizon and scope. Sum supplied fees, recruitment, applicable owner-provided employment costs, transition and support charges once. List unknown taxes/benefits/payment fees separately and route to their owner; do not call an incomplete cash total fully loaded cost or ROI. Internal economic time cost is a distinct line, never automatically added as payroll cash again. Quotes keep retrieval date, source, expiry, inclusions and commitment status. No cost is a public market benchmark.

Capacity arithmetic does not establish a completion date or probability. Use actual comparable throughput with a consistent done boundary, and route probabilistic forecasting to Estimation; process data to Kanban Flow. Small/non-comparable samples remain limited. [Evidence digest](research/distillation.md)

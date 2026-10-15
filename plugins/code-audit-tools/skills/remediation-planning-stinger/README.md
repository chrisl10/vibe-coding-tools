# remediation-planning-stinger

Turns audit findings into a fix plan: clusters findings into work packages, orders them Now, Next, Later, and, only with approval of the exact file list, writes Library PRDs, IRDs, knowledge docs, and draft contracts. It never implements fixes.

## When to use

- The W3 remediation wave of a Mario-tier `/audit-my-code` run
- "Give me a remediation plan for these findings"

## What it writes

`<workspace>/04-remediation/roadmap.md` and `plan.json` always. Approved `library/` documents in the audited repository only after the user approves that exact list.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [remediation-planning-wasp-drone](../../agents/remediation-planning-wasp-drone.md): the paired Drone

## Guides

- [00-inputs-and-consent-gate](guides/00-inputs-and-consent-gate.md)
- [01-cluster-findings-into-work-packages](guides/01-cluster-findings-into-work-packages.md)
- [02-prioritization-and-waves](guides/02-prioritization-and-waves.md)
- [03-prds-irds-and-contracts](guides/03-prds-irds-and-contracts.md)
- [04-knowledge-docs-via-knowledge-stinger](guides/04-knowledge-docs-via-knowledge-stinger.md)
- [05-handoff](guides/05-handoff.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

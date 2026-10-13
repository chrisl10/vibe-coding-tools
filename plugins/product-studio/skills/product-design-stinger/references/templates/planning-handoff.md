# Planning handoff: design to product-planning-stinger

<!-- Machine-friendly. product-planning-stinger builds the PRD map and wave plan from these IDs. Keep one row per screen and per flow. Do not write PRDs here. -->

Package version: {date or commit}. Gate B approved: {yes or no; date}.

## Screens

| Screen ID | Name | Journeys | Flows | States specified | Prototype | Complexity (S, M, L) | Depends on | Notes for PRD |
|---|---|---|---|---|---|---|---|---|
| S-{area}-01 | | J-01 | F-01 | empty, loading, error, success | yes | M | S-auth-01 | |

## Flows

| Flow ID | Task | Screens in order | Riskiest step | Data or integration needed |
|---|---|---|---|---|
| F-01 | | S-a, S-b | | |

## Suggested grouping

| Candidate PRD | Screens | Flows | Why together |
|---|---|---|---|
| {Billing basics} | | | {shared data and one journey phase} |

## Cross-cutting requirements

- Accessibility baseline: `accessibility-baseline.md` applies to every PRD.
- Voice: `content-voice.md` applies to every PRD.
- Design system: {exists at path / to be bootstrapped by design-system-stinger before UI waves}.

## Open questions that block planning

| ID | Question | Blocks |
|---|---|---|

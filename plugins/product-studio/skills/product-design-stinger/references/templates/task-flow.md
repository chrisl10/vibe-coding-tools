# F-{nn}: {Task in the user's words}

<!-- A flow is one task inside one product: user steps and system responses. Add the failure branches; they become the error and empty states in screen specs. Grounding: research/raw/ux--nngroup-journeys-vs-flows.md, diagram--mermaid-flowchart.md, diagram--mermaid-accessibility.md -->

| Field | Value |
|---|---|
| Actor | {from J-id} |
| Trigger | {What starts the task} |
| Entry points | {Screen IDs or external links where it can start} |
| Success outcome | {What is true when done} |
| Screens touched | {S-ids} |
| Journey | {J-id and phase} |
| Status | draft |

## Flow

```mermaid
flowchart TD
    accTitle: F-{nn} {task}
    accDescr: The ideal path from {trigger} to {outcome}, with the validation failure and network failure branches.
    START([User {trigger}]) --> S1["S-{area}-01 {screen}: user {action}"]
    S1 --> V{Input valid?}
    V -->|No| E1["Inline error next to field, input kept"]
    E1 --> S1
    V -->|Yes| SYS["System {response}"]
    SYS --> N{Request succeeded?}
    N -->|No| E2["Error banner with retry, nothing lost"]
    E2 --> SYS
    N -->|Yes| DONE(["Success: {outcome} and next step shown"])
```

## Steps

| # | User does | System responds | Screen | State shown |
|---|---|---|---|---|
| 1 | {action} | {response, including time to respond} | S-{id} | {success, loading} |

## Edge cases

| Case | Expected behavior | Where specified |
|---|---|---|
| {Session expires mid-task} | {Keep input, re-auth, return to step} | S-{id} error state |
| {Already entered data} | {Do not ask again: WCAG 3.3.7} | S-{id} |
| {Drag to reorder} | {Single-pointer alternative: WCAG 2.5.7} | S-{id} |

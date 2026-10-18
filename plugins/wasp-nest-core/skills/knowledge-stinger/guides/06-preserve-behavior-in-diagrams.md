# Preserve behavior and authority in diagrams

A useful diagram lets a reader predict the same branches and side effects as the inspected source. Read the notation and evidence digest, then use the [worksheet](../references/templates/source-grounded-diagram.md) and [worked fixtures](../references/examples/diagram-authority/worked-cases.md).

## Lock the journey and evidence

Identify the reader's question, one entrypoint and the relevant revision or working-tree hashes. Record environment and observation time for runtime evidence. Read the actual handler, caller, permission checks, downstream contracts and relevant decisions. Preserve intended/Draft/Accepted requirements, inspected implementation and observed execution as separate layers. An Accepted requirement alone cannot establish that code exists or is deployed. If no code or authoritative contract is supplied, produce a labeled intended flow or an explicit evidence gap, not an implemented architecture.

Capture only authorized local inputs. Do not retrieve credentials, send private diagrams to a remote renderer, install packages, change Mermaid configuration or mutate the product to fill a gap. Prefer existing local parsing/rendering tools when available. Record renderer name/version and which files it checked; missing rendering is an honest qualification limit.

## Trace before drawing

Write the ordered journey in prose first. Record the caller and the trusted identity source, each gate and denial path, the actual call names and data fields, returned status/body, state mutations and errors. Distinguish a caller-controlled tenant identifier from a validated identity or scoped lookup. Name the check that enforces a boundary; a box labeled trusted does not implement one.

Build an edge ledger with exact file, symbol, line range and a short quote. Hash the source used. Include omitted branches and why they are outside the bounded question. If a line locator changes, recheck the quote and hash. A current HEAD alongside dirty files is insufficient to identify their exact bytes.

| Mechanism | What the diagram must preserve |
|---|---|
| Permission and early return | The denial branch terminates before protected reads, writes, sends or charges. Authentication alone does not imply authorization. |
| Request and return | A dotted response arrow is a visual convention. Label the actual returned value and where the function returns; do not place later work after a terminal return in the same path. |
| Conditional and error flow | Show mutually exclusive branches and the actual catch/propagation boundary. `alt` and `opt` mean alternatives and optional paths, not parallel execution. |
| Async call or queue | Separate producer acceptance, durable enqueue evidence, worker start, worker result and caller observation. An open arrow cannot prove delivery, exactly-once execution or await behavior. |
| Transaction and external effect | State the actual transaction boundary, commit point and external calls outside it. A `critical` block cannot manufacture a database transaction or make an external notification/payment atomic. |
| Retry and duplicate handling | Show the actual retry owner, condition, bound/backoff and idempotency/deduplication scope when sourced. Unknown retry policy stays unknown. A loop icon does not grant permission to retry a charge. |
| Concurrency and ordering | Use `par` or fork/join only when source supports concurrent operations. Record awaits, join conditions and independent failure paths; diagram position alone cannot prove cross-worker ordering. |
| Money and sensitive data | Name only source-supported charge/provision/export actions and authorized field categories. Preserve human/provider gates. Omit secrets and unnecessary personal data from labels. |

Mermaid supports the notation in the official sequence, flowchart and state captures. The semantics above require target evidence, not notation alone.

## Choose the smallest representation

Use `sequenceDiagram` for observed call/response order, `flowchart TD` for decision paths and `stateDiagram-v2` for persistent state transitions. Name what each arrow means in the legend. Use camelCase IDs, quoted labels where needed, no click handlers and no explicit colors. Avoid version-specific syntax when the target renderer version is unknown. Split intended changes from current behavior into separate clearly labeled diagrams.

Keep explanations beside the diagram: what source supports it, what it deliberately omits, which boundaries are logical groupings, and which enforcement is unknown. Do not invent an endpoint, role, queue, database transaction or deployment tier to make the picture symmetrical.

## Check the picture against the source

Walk at least the successful path, denied/invalid path and material downstream failure. For queues, also walk accepted-but-not-consumed and duplicate/retry cases if the source implements them. For writes followed by external effects, check the actual saved state after failure. Use existing authorized tests or a disposable synthetic fixture when applicable; no live request is required by this procedure.

For every arrow ask: who can trigger it, which condition permits it, what data crosses, whether it waits, what changes, and what happens when it fails? Compare branches against the ledger before simplifying labels. Fix a pretty-but-false picture by restoring gates, returns and separate states. A successful parse or screenshot proves syntax/display only. Semantic checks, application execution and reader understanding need their own evidence.

## Deliver the bounded artifact

Return the narrative diagram, source ledger, material omissions/discrepancies and actual checks. A targeted diagram does not require scaffolding a full Batch A knowledge base or padding a short source-supported explanation. Actual knowledge docs still use guide 02's header and Related links. ADR/PRD/IRD changes and independent Quality reports retain their respective owners. Diagram authoring does not authorize deployments, sends, payments or acceptance of a contract.

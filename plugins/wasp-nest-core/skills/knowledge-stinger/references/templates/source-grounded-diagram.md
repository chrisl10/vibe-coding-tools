# Source-grounded diagram worksheet

Use with [guide 06](../../guides/06-preserve-behavior-in-diagrams.md). This worksheet is evidence accompanying a narrative doc, not an Accepted contract or a product execution receipt.

## Scope and source

Reader/question:
Entrypoint and caller:
Diagram layer: intended / inspected implementation / observed execution
Source revision plus working-tree file hashes:
Runtime environment/observed date, if any:
Authoritative identity and gate source:
Decision/specification status and disagreements:
Renderer/version/check result, or unverified:

## Node and edge ledger

| ID | Node/edge/branch/state | Exact path, symbol, lines and quote | Source SHA-256 | Caller/condition | Data and side effect | Await/return/error/commit boundary | Evidence layer or unknown |
|---|---|---|---|---|---|---|---|

Record permission denial before protected work, input validation, early returns, transaction commit, external effects, queue acceptance/start/completion, retries/deduplication and join conditions where applicable. A visual boundary must name its actual enforcement source or say logical grouping only. No credentials or unnecessary personal data.

## Diagram and legend

Insert Mermaid using only supported local syntax. State whether each arrow means a call, response, event, data movement or dependency. Keep current and intended flows separate. Colors, shape, box and activation bar convey no extra authority.

## Path checks

| Path | Expected source behavior | Check/observation and result | Diagram correction or missing evidence |
|---|---|---|---|
| Permitted caller | | | |
| Denied/invalid caller | | | |
| Downstream failure | | | |
| Queued but not consumed, if applicable | | | |
| Retry/duplicate/concurrent result, if implemented | | | |

## Omissions and qualification

Omitted paths and bounded reason:
Unknown enforcement/runtime/deployment:
Syntax/display checks actually run:
Semantic source checks actually run:
Product runtime and human understanding evidence:
Unresolved questions:

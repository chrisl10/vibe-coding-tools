# 11 - Put native background work behind an owned boundary

Use when an app needs a native parser, indexer, image transform, blocking SDK, local import or sustained computation. Load the dated source digest, then fill the [worksheet](../templates/native-background-worksheet.md). Explain to a beginner: the async executor is a receptionist serving many arrivals; a long computation at that desk prevents the receptionist answering others. Moving work to another room still needs a door limit, an owner and a closing procedure.

## 1. Classify actual operations

| Operation observed in the proposed path | Candidate boundary | Evidence required |
|---|---|---|
| I/O with a genuinely async API | Await on the existing runtime | Cancellation contract of every await; timeouts, resource cleanup and bytes admitted |
| Finite blocking file/SDK call | Existing `spawn_blocking` bridge or approved worker | Duration/size bounds; thread and queue capacity; library timeout behavior |
| CPU transform | Explicitly limited compute work or already approved CPU pool | Representative cost, cancellation checkpoint spacing, queue bytes and UI responsiveness |
| Persistent blocking consumer | Owned dedicated thread where architecture permits | Admission closure, disconnect policy, cancellation, joined termination |

Calling a function `async` does not move its synchronous computation onto a separate worker. Tokio documents both executor starvation from blocking/compute and limits of blocking-pool cancellation. Never prescribe Rust as universally faster than another language from this table. Measure the application's workload. Source

## 2. Establish one owner and bounded admission

Name the component holding the job queue, cancellation signal, thread/task handles and terminal result. Keep job identifiers separate from raw payloads. Bound message count AND payload bytes before expensive allocation; reject malformed or over-limit inputs at the edge. Define `Full`, `Stopping`, `Disconnected` and accepted acknowledgement distinctly. Return ownership of a rejected job so the caller can dispose of or explicitly retry it. Do not silently retry an import/payment/tool operation.

Review result queues as carefully as input queues. A worker blocked sending its result cannot observe cancellation. Require a bounded, cancellation-aware result path, a latest-state contract, or a fixed terminal result owned by join; decide which fits the actual public contract. A bounded channel alone does not bound total process memory or completion time. Channel, admission errors.

## 3. Make stopping a lifecycle, not a flag

1. Stop new admission at the authoritative owner.
2. Choose drain or discard for accepted queued jobs in the approved product contract. Cancelled work is not reported as completed.
3. Notify running work cooperatively. Check cancellation before costly chunks and before approved side effects. Record the longest indivisible call and whether it can be interrupted.
4. Wait for every owned task/thread. Report domain error, cancellation, panic, and join failure distinctly.
5. If a deadline expires, retain an explicit unresolved-running-work state and invoke the approved escalation. Do not claim that a timeout, dropped handle or UI dismissal stopped a native operation.

Started Tokio blocking work cannot be forcibly aborted. A runtime shutdown timeout merely stops waiting. If a third-party call can hang and has no cancellation/timeout API, cooperative checks around it cannot give a hard deadline; seek the architecture owner's isolation/escalation decision. Rust JoinHandle drop detaches rather than joins. Blocking, join, shutdown.

## 4. Preserve storage, IPC and secret boundaries

Rust owns bounded computation and approved persistence mechanics. The database owner decides schema/durability; cancellation after commit must reconcile with durable truth rather than relabel a commit as undone. Use the existing [persistence procedure](05-prove-persistence-and-state.md) for transactions and crash evidence. A cancelled future does not roll back arbitrary external side effects.

The Tauri owner decides command exposure, permissions, webview identity, scopes and plugin policy. Do not give UI callers arbitrary filesystem paths or secret-bearing SDK handles. Validate the already approved DTO, authorize at its established boundary, and send minimum typed progress/status to the UI. Correlation is an identifier, not a copy of prompt/input text. Default logs exclude content, tokens and raw errors; see [adapter boundaries](06-implement-adapters.md). A backend worker does not acquire harness tools, user interaction or repository authority.

## 5. Prove the boundary before integration

Use the [worked native example](../examples/06-native-background-worker.md) and [standard-only source fixture](../examples/native-background-worker.rs) to learn result/error/cancellation/backpressure/join behavior. Compile it only into a task-owned temporary directory; do not install a runtime. Then build application-specific tests for saturation, concurrent submissions, disconnect, cancellation at each await/commit, stale UI progress, flush failure and shutdown during indivisible I/O. Review operation cancellation safety against the selected version's API. Select.

Return exact compiler/target, source hash, tests, queue/byte assumptions, outstanding-operation state and missing decisions. Fixture proof is not Tauri responsiveness, mobile suspension behavior, crash durability, production concurrency correctness or a product release. Security reviews the final changed source; Quality follows Security and any affected reruns.

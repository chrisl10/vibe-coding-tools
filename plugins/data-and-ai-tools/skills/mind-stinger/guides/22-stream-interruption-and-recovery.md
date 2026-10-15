# 22: Separate streaming, cancellation and business completion

Use for O186 together with [Svelte endpoint mechanics](svelte-streaming-endpoints.md). AI SDK stop, AI SDK resume and SSE framing ground the protocol distinctions. These are design and evidence procedures, not a deployed endpoint.

## Define the three states before wiring abort

| Concern | States to record | Evidence |
|---|---|---|
| Model generation | pending, running, cancellation requested, stopped, completed, failed, unknown | Provider/SDK attempt and terminal callback record |
| Delivery | connected, disconnected, replaying, delivery complete | Connection ID, event sequence/cursor, decoder output |
| Business effects | not attempted, authorized, executing, committed, failed, unknown | Durable operation record and read-back of actual result |

A delivered token is provisional text. EOF may be a disconnect. A finish event does not certify a profile write, message send or charge. Cancellation cannot undo an already committed effect. Reject partial tool arguments; aggregate a complete proposal and recheck authority before executing it.

## Inspect the actual implementation

1. Record endpoint/adapter, pinned SDK/provider, runtime and platform settings from source and deployed evidence. No guessed duration numbers. Check whether request cancellation is enabled and forwarded to upstream work. The SDK docs describe runtime/config requirements; proposing those settings does not authorize changing them.
2. Choose and document intended disconnect behavior. A foreground cancellable request can abort upstream work. A resumable job intentionally continues after disconnect; explicit authenticated stop must identify the current generation. Do not mix these contracts accidentally.
3. Carry run, attempt, generation and operation IDs separately. Link traces without raw prompts, credentials, presigned URLs or media. Enforce both caller authorization and current-generation matching for resume/stop; a leaked cursor or chat ID is not permission.
4. Stream framing is incremental. Test split UTF-8, split SSE lines, multi-line data, comments, malformed event payloads and truncation. Define maximum event/input size, backpressure and cleanup. Raw byte forwarding is valid when no semantic parsing is attempted; consumers still parse incrementally.
5. Record cancellation requests separately from acknowledgments and provider termination. Handle abort, timeout, client close, upstream error and callback failure with one guarded terminal transition; release owned resources. Retain partial text only under explicit product policy and label it incomplete.
6. Resume delivery from a retained event cursor only when retention and authorization permit. Deduplicate events in the client and gate durable writes with [guide 24](24-tool-authority-and-effect-review.md). Replaying events must never resend a business action.
7. Unknown post-timeout effect status requires reconciliation, not blind retry. A client stop from old generation A must not cancel newer generation B. Record pending provider cost as unknown until observed.

## Required task exercises

Fill [the interruption worksheet](../templates/stream-interruption-review.md). Use actual endpoint + client/adapter traces for: close before first token; stop during text; stop while effect pending; committed effect followed by lost acknowledgment; stop during tool argument accumulation; duplicate/reordered delivery; server restart; stale stop; resume by another user; expired cursor; simultaneous stop/finish.

Compare persisted history and actual side effects to expectations. Report cancellation propagation latency, final generation status, partial-output policy, replay correctness and duplicate effect count separately. Test tooling and environment must already be authorized. A mocked callback or SSE parser test is narrower evidence than provider termination or durability. Hand client rendering to the frontend owner and tenant/cursor authorization to Security. Use the existing trace and job owners rather than creating another streaming engine.

# Rendered design case: streamed draft with a separate send

**Evidence class:** hypothetical state review, no endpoint/provider/effect execution. Outcome O186. [Guide 22](../guides/22-stream-interruption-and-recovery.md).

Owner asks to draft a support reply. Send is separately approved only after review of recipient and exact body. Generation G1 streams a draft; delivery C1 disconnects at event 8. The product chose resumable generation, so G1 remains running. Calling browser stop must not be reported as confirmed server cancellation.

| Step | Generation | Delivery | Business effect | Expected disposition |
|---|---|---|---|---|
| G1 emits draft events 1-8 | running | connected C1 | not attempted | Text provisional |
| C1 closes | running | disconnected | not attempted | No send; generation cost pending |
| Authorized reconnect cursor 8 | running | replaying C2 | not attempted | Deliver later events once, no business replay |
| User requests stop of G1 | cancellation requested | connected | not attempted | Verify principal and current generation |
| Provider acknowledgment missing | unknown | closed | not attempted | Report cancellation requested, status unknown |
| G2 starts; late stop cites G1 | G2 running | connected C3 | not attempted | Do not cancel G2 |

Separate allowed-send branch: after exact recipient/body approval, operation S1 commits at provider but acknowledgment is lost. S1 state is unknown until read-back establishes committed. Replaying G1 events does not issue S1 again. A second payload under S1 conflicts. A cancellation request cannot undo that committed send. Compensation is separately scoped.

Actual endpoint tests must cover split UTF-8/SSE framing, partial arguments, stop/finish race, restart and cross-user replay. EventSource IDs and an authored state table do not prove durable send idempotency, cancellation propagation or provider cost termination.

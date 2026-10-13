# Component and browser test contract
Use existing Vue tooling and real components. No fabricated framework adapter.

1. Mount RecordForm with distinct formId per instance; label resolves to its input.
2. Keyboard-submit empty/whitespace draft: accessible error, no save event.
3. Enter valid title and submit: exactly one declared event with trimmed title.
4. Set pending and trigger submit repeatedly: no additional events; visible pending text.
5. Provide serverError containing HTML syntax: display escaped literal text.
6. Change a record parameter while the first request is pending: old response cannot replace new data.
7. Unmount pending view: request cleanup runs; no state changes after invalidation.
8. Resolve empty/malformed/HTTP failure: appropriate empty or error/retry UI; no private error/body logging.
9. Refresh direct history URL and unknown route in the real host: expected entry/fallback/not-found.
10. Exercise actual accepted authentication/API boundary with its owner; route guards cannot replace it.

All framework/component/browser cases are NOT_RUN in the staging forge. Pure model tests do not satisfy these cases.

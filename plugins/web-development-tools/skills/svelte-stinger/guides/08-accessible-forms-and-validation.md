# Build and review accessible forms with server validation

Use this procedure for O075 in an existing Svelte application. It owns form semantics, runtime integration and verification. Route visual styling to its design owner and tenant/persistence policy to Security and the backend owner. Start with the [worksheet](../references/templates/form-contract-worksheet.md), then compare the [same-page reference files](../references/examples/accessible-forms) and [qualification cases](../references/examples/accessible-forms/cases.md).

## 1. Establish the actual contract

Inspect package.json and the lockfile for resolved Svelte and Kit versions, then classify the component's mode. Record the current route and whether it is a page action, standalone endpoint or remote function. Do not add libraries or migrate the project merely to fit this example. Our example requires Svelte 5 runes and conventional page actions; it deliberately avoids generated `PageProps` types because older Kit versions differ. Add the installed project's generated types where available. See props capture.

The October fetch of form-action docs includes cross-page navigation and `refreshAll` semantics, explicitly contrasting with Kit 2 behavior. Read version-matched docs/types before using `navigate`, `refreshAll` or `invalidateAll`. The reference keeps the action on the same page and invokes `update({ reset:false })`. It is not a universal configuration recipe. Remote forms and experimental flags are outside this update.

Ask for missing field, permission, persistence and retry contracts before writing application behavior. Intake needs the actor, resource, mutation, fields, safe response values and test environment. A hidden tenant ID or disabled submit button cannot establish authority.

## 2. Keep native form semantics

Use a real `<form method="POST">`, named controls and a submit button. Conventional `use:enhance` applies to page actions, not GET forms or standalone +server endpoints. The unenhanced request must remain useful. Do not add a click-only handler that prevents keyboard/native submission. When submission must be programmatic, use `requestSubmit` rather than bypassing validation and the submit event with `submit`. Sources: Kit actions, MDN requestSubmit.

Use visible labels linked to stable IDs. Group related choices with fieldset/legend, and attach help text to the control. Placeholder text does not replace the label. Required instructions and correction messages must make sense without color. Give repeated form instances distinct ID prefixes. Source: WAI labels.

## 3. Validate and authorize on the server

Client constraints improve feedback; validate every submitted type, repetition rule, range and resource reference again on the server. FormData entries can be strings or files; do not coerce a File into a valid text value. The reference accepts exactly one trimmed displayName up to 80 characters and rejects duplicates. Unicode, file size and locale rules require the application's contract. Enforce body-size and upload limits before parsing through the deployment/request boundary; the example does not supply a streaming body limiter. Malformed form encoding gets a controlled 400 result. Source: WAI validation.

Server `locals` can carry session-derived identity; it does not automatically grant tenant/resource permission. The reference's `formWriter` is an application adapter contract: `mayEdit()` checks the trusted actor, and `writeAuthorized()` must recheck authority and version/conflict policy at the write boundary. Its absence returns unavailable, not a simulated save. Implement that adapter with the backend owner before using the route. Source for integration point: Kit auth. The policy and atomic-write requirement are engineering recommendations.

Return `fail(422, ...)` for correctable validation, 403 for denied access and a defined conflict result for changed records. Keep returned values on an allowlist. Passwords, tokens and payment details must not be echoed into action data, HTML, analytics or logs. Unexpected failures must not become success. Do not blanket-catch Kit redirect/error control flow. Inspect the installed version's failure serialization and error boundary behavior. Source for structured action failure: Kit actions.

## 4. Apply feedback and move focus deliberately

Render an error summary naming the problem and linking to invalid controls. Use inline correction messages connected through `aria-describedby`, and set `aria-invalid` only for invalid fields. Apply the enhanced action result before moving focus so the summary exists. The reference awaits `update`, then `tick`, then focuses the summary only for a failure result. The user can follow its field link. Source: WAI notifications.

Keep a status region mounted before changing pending/success text. Use short messages and test whether focus plus announcements repeat unnecessarily. Do not put the entire form in a live region. A no-JS failure gets a rendered summary; it does not run our enhanced focus callback. Kit has its own post-submission focus behavior, so verify custom behavior rather than assuming it wins. Source: Kit accessibility.

## 5. Treat pending and concurrency as separate problems

The reference sets pending in the submit callback, cancels a second enhanced submission and makes the input readonly while that snapshot is in flight. It disables the submit button, not all controls. A returned callback overrides default enhancement handling, so it calls `update` and clears pending in `finally`. Source for callback/update mechanics: Kit actions.

These are interaction controls. Native requests, retries, multiple tabs and network ambiguity still reach the server. Consequential writes need an operation identity and a server transaction/uniqueness policy. Do not claim aborting a browser request undoes a committed mutation. Define whether an ambiguous result is queried by operation ID or safely retried before exposing Retry. These are application design requirements, not framework guarantees.

For optional asynchronous availability checks, record a monotonically increasing request generation and the input snapshot. Abort the previous request where practical, but also compare generation and current value before applying a result. Discard stale responses, clear outdated suggestions on edits, and repeat authoritative validation during the POST. Avoid sending sensitive values to suggestion endpoints. Do not derive validation state with an effect that mirrors another state variable. The stale-response policy is an engineering recommendation requiring a real application test.

## 6. Verify the actual surface

Run [qualification cases](../references/examples/accessible-forms/cases.md) against the application's installed version. Minimum evidence:

- Direct malformed POST and permission-denied tests prove the server never calls a write on rejection.
- No-JavaScript and keyboard submission reach the same authoritative action.
- Invalid response preserves only allowed values and provides linked correction messages.
- Delayed, duplicate and out-of-order responses demonstrate pending and stale-result policy.
- Network errors and ambiguous mutation outcomes never announce an unproven success.
- A browser plus assistive technology confirms label/help/error/focus/status behavior.

Use existing compiler/test tools; do not install dependencies without authorization. Compiler output establishes compilation only. Browser automation establishes observed interaction only. Human assistive-technology review has separate evidence. None establishes legal accessibility conformance.

## Delivery

Return the completed worksheet, paths changed, observed versions, test outputs and open adapter/permission/retry gaps. Keep source guidance, actual server execution and manual review explicitly distinguished. This archive qualifies the guide and reference contract; it does not deliver a deployed application.

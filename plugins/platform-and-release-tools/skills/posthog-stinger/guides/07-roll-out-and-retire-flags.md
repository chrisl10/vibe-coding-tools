# Roll out and retire a PostHog flag

Use for O175: a flag with an owner, controlled rollout, evidence of failure behavior and a removal decision. First read the current digest, then [the worksheet](../references/templates/flag-lifecycle.md). Existing integration examples are sketches; bind every API choice to the target lockfile, installed types and configuration before implementation.

## 1. Intake and purpose

Record flag key, accountable owner, backup owner, feature purpose, rollout versus experiment versus intentionally retained operational switch, creation date, review/expiry date, environments, project/region labels, dependent feature/PRD, permitted consumers and intended retained path. Ask only for missing decisions that block work. An expiry is a review trigger, never permission to delete. Keep unknowns unknown.

Inventory the key and aliases in client/server code, wrappers, SSR/bootstrap, mobile/desktop clients, background jobs, config, tests, event definitions, dashboards, experiment/survey links and other flag dependencies. Literal search alone can miss dynamic keys and external consumers; state search scope and review generated/configured keys. Inspect each caller's actual effects before deciding the branch to keep. Vendor stale status is a candidate list, not a removal authorization. Cleanup source.

## 2. Bind evaluation to observed inputs

Record client/server SDK names and exact locked/installed versions, source revision, config revision, evaluation API, remote/local/bootstrap mode, project region, evaluation contexts and where these are configured. Confirm support in installed types and version documentation. Observe requests or local evaluation proof in a permitted test environment. Context filtering differs by SDK and version; context-free flags still evaluate. Contexts source.

Record the stable bucketing unit: person, company/group or supported device; its source; anonymous-to-signed-in policy; group membership change; logout/reset and tenant switch policy. Compare the same definition/version, identity, targeting properties, group and contexts across server and client. Use application-authoritative identifiers and minimal approved properties, with synthetic values in worksheets. A client-supplied header/group/flag cannot prove tenant membership, permissions or entitlement. Every protected server action independently authenticates, checks membership and verifies entitlement before effects. The flag selects an experience only after those checks. Input mechanics.

## 3. Define failure, cache and kill behavior before rollout

For each call site specify pending/missing, false, each valid variant, invalid payload, timeout/error, partial response, stale cache, cold start and missing-property behavior. Distinguish a documented SDK response from the application's chosen fallback. Choose the lowest-risk valid feature path with the product owner; false, empty string and undefined must not be conflated. Validate payload shape before use. Do not assume a thrown exception or success shape across SDKs.

Record cache scope, refresh/poll settings, initial-load wait, observed definition timestamp/version, maximum accepted age, timeout/retry settings and application result lifetime. A bootstrap value can survive a partial/errored refresh. Persisted assignments and evaluate-once designs require explicit invalidation on a kill, identity change or significant rule change. Record the authorized incident operator and who can operate the switch, what action is authorized, independent incident fallback when the provider is unreachable, and a measured maximum convergence time per consumer. A polling interval alone does not prove that maximum. Bootstrap, local evaluation, Node API.

## 4. Prepare rollout and exposure proof

Specify internal synthetic cohort, approved initial audience and percentage, subsequent stages, observation windows, named metrics, baseline, stop thresholds and decision owner. Never invent universal safe percentages or announce improvement from assignment counts. For experiments, record hypothesis, participant unit, variant split, exposure point and metric definition before traffic. Read the single flag value where the experience is actually selected. Verify that the expected exposure and conversions use consistent identity and evaluation snapshot in approved synthetic proof; account for deduplication, transport failure and analytics opt-out. A snapshot read is not proof a person saw UI. Avoid duplicate client/server exposure paths. Exposure source.

Record approved event/property names and an allowlist. Do not add email, names, free text, tokens, URL query strings or raw exception/context dumps for debugging. Keep evaluation properties separate from persisted analytics properties; verify SDK-generated exposure data as well. Identify/reset timing and replay masking are separate reviewed concerns in guides 02 and 04. Region selection and masking do not certify legal compliance. Collection source.

## 5. Exercise and report evidence

Use the worksheet matrix with synthetic users/tenants in authorized environments. For every result record source/config/SDK versions, input class, evaluation origin, value, selected behavior, server authority result, exposure evidence or explicit absence, definition age and proof artifact. Observe initial render, refresh, slow/error responses, missing targeting properties, stale/local cache, identity and tenant changes, invalid variant/payload, denied entitlement and disabled flag. Where unavailable, mark unproven and stop promotion of the dependent rollout. Do not send telemetry or manipulate a live flag to manufacture a passing worksheet. [Worked cases](../references/examples/flag-lifecycle-cases.md).

## 6. Rollback and retirement

Rollback record names the previous code/config, retained safe branch, owner action, effects already committed, data compatibility and convergence proof. Turning off a flag does not undo a migration, payment, external send or durable write. Keep an intentional kill switch on its own review schedule rather than retiring it because it is old.

For a concluded rollout or experiment, obtain a per-flag retained-path decision and exact authorized file scope. Remove code references and unused branches only within that scope, preserving auth and entitlement checks. Run branch, consumer-contract, type/test/build and privacy checks appropriate to the target. Deploy only when explicitly authorized, observe all supported deployed consumers, then prepare a separately approved provider-disable action. Old mobile versions, background jobs, dependent flags and rollback releases can require a compatibility interval. Do not disable/archive/delete while they still depend on the key. Record the completed environment/revision proof and final state; missing deployment/provider proof leaves retirement prepared, not complete. Correct cleanup order.

## Acceptance

The packet passes source review when all required fields and decisions exist, SDK-dependent statements have version-bound sources, evidence classes are explicit, failure/exposure/authority/retirement matrices are complete and unknowns block the relevant live claim. Actual rollout readiness requires observed target evidence and authorized state changes. End implementation work with Security, Quality, then orchestrator Repository Health before user-approved commit or push.

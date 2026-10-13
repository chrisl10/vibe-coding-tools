# Acceptance scenarios: build-mobile-backend

Mode: reference. These are source-workflow qualification scenarios. They do not claim native dispatch, application execution or provider/device proof.

## Case 1
Request: A Python service supports old and current mobile clients on unreliable networks.
Expected: Pin compatibility and implement server slice only, run fake-client failure evidence.
Source review: PASS. Located instructions: `python-wasp-drone`, `version support`, `fake-client server proof`.
Native/runtime outcome: UNPROVEN.

## Case 2
Request: A mutation commits before the mobile connection fails and reconnect repeats it.
Expected: Test transactional dedup and uncertain outcome; HTTP semantics alone do not prove replay safety.
Source review: PASS. Located instructions: `network fails after commit`, `transactional mutation/deduplication`, `HTTP method idempotency`.
Native/runtime outcome: UNPROVEN.

## Case 3
Request: User expects native secure credential storage and offline UI from this command.
Expected: Report unresolved native owners rather than pretending server coverage implements device behavior.
Source review: PASS. Located instructions: `on-device persistence`, `native secure credential storage`, `separately resolved owners`.
Native/runtime outcome: UNPROVEN.

## Case 4
Request: Wrong-tenant client sends a valid token and old schema.
Expected: Verify server object authorization and old-client negative tests, never trust client authorization.
Source review: PASS. Located instructions: `every object operation`, `wrong tenant`, `old client schema`.
Native/runtime outcome: UNPROVEN.

## Case 5
Request: Only TypeScript owner exists but service is an unsupported runtime.
Expected: Resolve a supported existing owner; missing runtime blocks implementation and preserves contract work.
Source review: PASS. Located instructions: `another runtime`, `absence blocks implementation`.
Native/runtime outcome: UNPROVEN.

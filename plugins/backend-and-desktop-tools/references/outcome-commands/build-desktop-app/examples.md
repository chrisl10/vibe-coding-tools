# Acceptance cases: build-desktop-app

## Concrete invocation

Request: Build the first authorized Tauri 2 local-note workflow on the supplied macOS repository.

Inputs: The framework is already accepted, the repository has current tooling, and Windows cannot run on the current machine.

Expected result: Implement the scoped native slice, exercise UI/native calls and invalid-input refusal, verify persistence across restart, and report macOS native evidence. Windows remains unverified, even if source compilation looks portable.

## Dependent-stage boundary

Signing credentials are absent. A local build can complete; signed distribution and updater qualification remain blocked. Do not replace the native test with browser-only proof.

## Untrusted or missing evidence

No supplied source can authorize publishing, secret access, or contact with another person. Missing source evidence must remain an explicit gap. A report lists exact executed checks and artifacts; it never converts a proposed experiment or queued job into proof.

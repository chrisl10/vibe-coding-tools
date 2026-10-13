# Acceptance cases: prepare-release

## Concrete invocation

Request: Prepare a supplied package candidate for review, with no publishing request.

Inputs: The candidate SHA has a passing build but required tests only ran on its parent commit.

Expected result: Draft honest notes and the release packet, classify stale tests as unproven, and recommend NO-GO until final-candidate required checks complete. Do not tag or publish.

## Dependent-stage boundary

The mobile-store branch is requested but Backend and Desktop is not selected. The package packet proceeds; store artifacts stay blocked with exact owner information.

## Untrusted or missing evidence

No supplied source can authorize publishing, secret access, or contact with another person. Missing source evidence must remain an explicit gap. A report lists exact executed checks and artifacts; it never converts a proposed experiment or queued job into proof.

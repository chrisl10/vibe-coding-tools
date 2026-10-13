# 06: Done Checklist

Run this checklist before declaring API documentation complete. All 10 items must pass or be explicitly acknowledged.

| # | Check | Pass criteria |
|---|---|---|
| 1 | **Spec validates** | `redocly lint openapi.yaml` or `openapi-generator validate` exits with 0 errors |
| 2 | **All endpoints have summaries** | No `summary:` field is empty or placeholder text |
| 3 | **All endpoints have descriptions** | No `description:` field is empty or placeholder text |
| 4 | **Request examples present** | Every endpoint with a request body has at least one inline `example:` or named `examples:` entry |
| 5 | **Response examples present** | Every endpoint has at least one `200`/`201` response example |
| 6 | **Error response examples present** | Every endpoint has at least one `400`/`422`/`404` response example where relevant |
| 7 | **Renderer loads locally** | Docs render without console errors in a local browser (run `make docs` or `npm run docs:preview`) |
| 8 | **SDK generation succeeds** | If SDKs are configured, `make sdk` runs to completion without errors |
| 9 | **One-command rebuild documented** | `README.md` or `Makefile` documents how to regenerate docs in one command |
| 10 | **Changelog entry present** | If this is a version bump or has breaking changes, a `CHANGELOG.md` entry exists with correct `[BREAKING]` or `[DEPRECATED]` tags |

## Fast-path for "good enough"

For a quick internal API with no external consumers, items 4, 5, 6, 8 may be deferred if:
- The audience is the same team that owns the spec.
- There is a ticket to add examples in the next sprint.
- The deferred items are explicitly listed in the session output.

Never defer items 1, 2, 7, 9 for any project type.

## How to emit the checklist

At the end of every `api-docs-wasp-drone` session, emit the checklist as a markdown table with `✅ pass` / `⚠️ warn` / `❌ fail` in a "Result" column, plus a brief note for any non-passing item.

## Additional reusable SDK evidence

When SDK generation is requested, complete [guide 07](07-qualify-reusable-sdk.md) and the [packet](../templates/sdk-contract-qualification.md). Record accepted revision, generator/config hashes, regeneration diff, package imports, baseline/candidate consumer behavior and actual server evidence separately. Missing evidence remains unverified. A successful item 8 is only generation success. Bodyless/204, binary and stream operations need relevant status/media examples rather than fabricated 200 JSON bodies.

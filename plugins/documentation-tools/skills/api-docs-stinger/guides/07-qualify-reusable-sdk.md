# Qualify a reusable SDK against a stable API

Use this guide for O201 before the generation commands in [04](04-sdk-generation.md). Read the grounded digest and fill the [qualification packet](../templates/sdk-contract-qualification.md). Keep existing accepted API contracts unchanged.

## 1. Establish the contract and consumer boundary

Obtain the spec and hash all resolved local references, its dialect, existing acceptance reference and owner, server release and authorized environment. A spec's `info.version` is not evidence of acceptance or a running deployment. If acceptance is absent, prepare a Draft packet and stop dependent generation claims. Route missing wire behavior to the API owner; do not decide it through client defaults.

Ask which languages and exact browser/server/native runtime versions consumers require, public package imports they already use, synchronous/async transport expectations, auth/tenant boundaries, and existing tooling/output ownership. Scope named operations and compatibility behaviors. Do not assume every operation needs a JSON body or JSON response; bodyless, 204, streaming and binary operations need their actual media/status examples. OpenAPI describes those separate surfaces. OAS

## 2. Characterize behavior before changing generation

Build the packet's behavior ledger from an existing baseline client plus sanitized authorized server evidence or explicitly synthetic fixtures. Capture exact path/query/header serialization; auth refresh and tenant placement; omitted/null/empty values; errors and request IDs; cursor terminal conditions; enum changes, dates and integer precision. Do not fetch arbitrary spec references or send a token to an unreviewed server URL. Security owns scheme and tenant enforcement audits.

Pin retry ownership so callers, SDK and proxies do not multiply attempts. Require accepted operation semantics, maximum attempts and total deadline; account for Retry-After and cancellation. A timed-out mutation may have succeeded, so transport failure alone cannot authorize replay. Stream framing, mid-stream errors, cancellation/close, binary sizes and multipart encoding each need their own characterization. Unsupported generator features remain explicit gaps. HTTP, generator feature tables

## 3. Reproduce the existing generator

Choose one compatible installed tool and selected generator using actual feature requirements. Record executable version and artifact hash, input dialect, config, template overrides, type/import mappings and runtime/library choice. Run its installed `config-help`/validation commands; never copy stale option names or versions as current guidance. Refuse silent dialect downgrade. If no approved compatible generator exists, report the gap without installing or creating a replacement.

Generate only into an approved task-owned output folder. Preserve manually maintained adapters outside generated files. Use the exact pinned executable rather than unversioned `npx`, which may download tools. Regenerate with identical inputs to compare normalized outputs and document timestamps or other nondeterminism. Review generated changes and dependency/license notices. Existing Makefile snippets are historical starting points, not safe turnkey installation or publication authorization. Usage, customization, license

## 4. Exercise packed consumer behavior

Use existing build/package commands under the task's authorization. Inspect package contents, export map, declarations, peer/runtime dependencies and browser/server separation. Test each promised consumer against the packed artifact, including public imports and any previously supported deep import. Node conditional exports can change what consumers resolve. Python and Go consumers need their own existing import/runtime checks; a TypeScript compile says nothing about them. Node packages, Python options

Run baseline and candidate against the same independent fixtures or authorized test server. Compare actual requests and success/error semantics, auth/tenant handling, cancellation, pagination bounds, rate/retry behavior and required streams/binary operations. Use generated code only after generation; the included [synthetic characterization exercise](../examples/sdk-consumer-contracts.md) demonstrates assertions, not a generated SDK. Separate generation, compile, synthetic transport, actual server and native consumer results in the report.

## 5. Version and hand off

Classify wire and package changes separately. A renamed method, removed import or stricter response parser can break consumers without a wire change. An added enum can break an exhaustive consumer; an optional field can break a strict decoder. Review actual consumer assumptions before applying [05's changelog rules](05-changelog.md). Use `[BREAKING]`, affected consumers, migration steps and approved timelines. Route unresolved contract changes to the owner. Do not fabricate acceptance or automatic deprecation dates.

Deliver the packet, pinned regeneration invocation, sanitized evidence and compatibility matrix. Run Security then Quality; parent owns repository-health/distribution gates. Publishing, credential/provider access and installation require the user's explicit authorization. No rendered docs, compiler exit or generator exit may stand in for running-server compatibility.

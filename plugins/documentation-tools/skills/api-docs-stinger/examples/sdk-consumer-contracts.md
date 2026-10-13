# Worked SDK consumer decisions

These cases demonstrate the [SDK qualification procedure](../guides/07-qualify-reusable-sdk.md). They do not assert that a real generated SDK or server has passed.

## Stable wire, broken package

A fictional API keeps `GET /projects` unchanged. A regenerated TypeScript package adds an export map but omits the old `client/models` import. The old consumer's import now fails. Record the wire version unchanged and package change `[BREAKING]`; either preserve the promised import or obtain an approved migration decision. A successful generator run cannot close this case. Node's export-map behavior is documented in the [primary archive](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/documentation-tools/skills/api-docs-stinger/references/research/sdk-contracts/raw/node22-packages.md).

## Timed-out mutation

A fictional `POST /jobs` times out after sending the body. Neither the spec nor supplied observation establishes idempotency-key retention or duplicate suppression. Recommendation: surface the uncertain outcome and do not add automatic mutation replay. Ask the API owner for the accepted semantics before promising retry safety. The SDK still needs a total deadline, cancellation policy and caller retry ownership. [HTTP idempotence](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/documentation-tools/skills/api-docs-stinger/references/research/sdk-contracts/raw/http-semantics.html)

## Unsupported stream or dialect

A team supplies an OAS 3.2.1 stream description; its installed generator's relevant stream support has not been characterized. Recommendation: mark stream generation and runtime behavior unverified, retain the accepted description, and produce the compatibility gap. Do not downgrade the spec or substitute buffered JSON to get a green compile. [OAS](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/documentation-tools/skills/api-docs-stinger/references/research/sdk-contracts/raw/openapi-3.2.1.html), [selected generator feature table](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/documentation-tools/skills/api-docs-stinger/references/research/sdk-contracts/raw/typescript-fetch.html)

## Actual local exercise: synthetic request/response characterization

Run with the existing Python interpreter:

```bash
python3 packs/documentation-tools/skills/api-docs-stinger/examples/sdk-contract-exercise.py
```

The file uses only the standard library, fake credentials and an injected in-memory transport. It opens no sockets, creates no accounts, writes no files and imports no generated SDK. Independent literal assertions exercise path/query encoding, per-client tenant/auth headers, null/omitted distinction, JSON and bodyless responses, error shape/status, unknown enum preservation, pagination termination/page bounds and a non-retried mutation failure. A transport callback records outbound requests and supplies fixture responses. This proves the example's stated boundaries only. It does not prove generator compatibility, server authorization, Retry-After timing, cancellation, refresh, streaming, binary behavior, native consumers or publishing.

Qualification result: synthetic exercise can pass while O201 remains unknown for an actual project until the packet's project-specific generation and consumer evidence exists.

## Actual local exercise: package exports break a deep import

```bash
node packs/documentation-tools/skills/api-docs-stinger/examples/sdk-export-exercise.mjs
```

The exercise creates a disposable synthetic ESM package and consumer, runs three fresh Node processes with inherited resolver/preload environment cleared, and removes only its own temporary tree. It observes the old deep import working, the candidate public root import working, and the old deep import failing with `ERR_PACKAGE_PATH_NOT_EXPORTED` after the candidate adds a restrictive export map. It does not install, pack or publish a real SDK. The observed runtime version is printed, so it must not be relabeled as every supported Node version, browser or CJS proof. This is the concrete package-break case above.

# Worked normalized vector choices

All quantities and goals below are hypothetical fixture inputs; no store performance measurement is claimed.

## Small SaaS knowledge base

Inputs: existing Postgres, 20,000 text chunks, one fixed embedding model, strong tenant filters, relational permissions and a small query rate. Recommend evaluating pgvector on the existing system first to keep relational scope together. Missing: exact extension/version, filtered recall and latency under writes. Counterevidence: if measured search contention violates the accepted transactional budget, a dedicated collection/read topology could be justified. Store selection remains provisional until labeled query and deny cases pass; corpus count alone does not prove fit.

## High-concurrency filtered retrieval

Inputs: existing Postgres authority, forecast five million continuously updated chunks, per-account selective filters and independent search scaling requirement. Recommend a bounded Qdrant evaluation for the dedicated collection when isolation is the accepted deciding need, with its sync/operator cost explicit. Missing actual tenant distribution, p95 under writes, deletion/revocation latency and recovery. Counterevidence: tuned Postgres exact filtered plans, iterative scans or isolation may satisfy goals without a new store. No fixed two-million cutoff or secondary 850-QPS result decides the choice.

## Multimodal reference library

Inputs: captions, image vectors and text vectors from distinct models, binary object storage, user permissions and semantic search. Store each model/dimension/distance separately; comparable width does not make different embedding spaces interchangeable. Recommend retaining Postgres provisionally when metadata/permissions dominate and the corpus fits accepted tests; evaluate Qdrant if measured multi-vector/query isolation needs justify it. Missing model compatibility, per-modality relevance labels, payload filter distribution and object/storage recovery. Counterevidence: stronger query capability or isolation can justify Qdrant, but multimodal alone cannot.

## Delayed deletion

A record is deleted in relational truth while a delayed projection update arrives after its tombstone. The accepted version/tombstone contract prevents resurrection; missing sync proof blocks release. Successful vector lookup or a vendor consistency claim cannot qualify cross-store tenant/deletion semantics.

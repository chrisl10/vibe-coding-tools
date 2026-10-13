# Qualification examples

These are hypothetical exercises, not execution claims.

## Happy path

A tenant document search uses lexical Postgres first. The accepted API orders tied ranks by unique document id, binds its cursor to normalized query/filters, denies other-tenant snippets, and records relevance on a labeled corpus.

## Missing owner

data-and-ai-tools is absent: UI shell design can use the accepted contract, but query/index/evaluation work is blocked on retrieval/database owners.

## Failure path

The semantic provider is unavailable: the accepted fallback produces authorized lexical results and an explicit fallback state; semantic relevance and semantic latency remain unproven.

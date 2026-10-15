# lovable-audit-stinger

Empirical security audit of Lovable-built apps on Supabase: row-level-security denial checks, role-differential reads, Edge Function gating, auth posture, and what the shipped client bundle exposes. It reports; it never patches.

## When to use

- "Audit this Supabase app", "check the RLS", "probe the Edge Functions", "where did they leak keys?"

## What it writes

A findings ledger, control-effectiveness attestations, and stated unknowns, shaped into a report per `guides/audit-reporting.md`. Any test write is minimal, labelled, and cleaned up.

## Start here

- [SKILL.md](SKILL.md): procedure, references map, and boundaries
- [lovable-audit-wasp-drone](../../agents/lovable-audit-wasp-drone.md): the paired Drone

## Guides

- [audit-reporting](guides/audit-reporting.md)
- [auth-posture](guides/auth-posture.md)
- [bundle-forensics](guides/bundle-forensics.md)
- [differential-visibility](guides/differential-visibility.md)
- [rpc-function-enumeration](guides/rpc-function-enumeration.md)
- [write-denial-discrimination](guides/write-denial-discrimination.md)

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.

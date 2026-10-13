# Normalized platform fit cases

All numerical workloads here are hypothetical, owner-supplied fixtures; no vendor rate or benchmark result is asserted.

## Small normalized SaaS

Inputs: 50 organizations, 500 active accounts, normalized relational records, server-rendered app, existing chosen external auth and object store, bursty traffic. No current concurrent-connection measurement or restore rehearsal. Recommend Neon provisionally when branch-based development and integration with those already-chosen services are the deciding constraints. Its current managed auth is acknowledged but does not authorize replacing chosen auth. Counterevidence: a team wanting one integrated platform might reduce service ownership with Supabase. First spike verifies actual driver/pool mode, tenant denials and isolated restoration; cost and latency remain unknown until supplied/measured.

## Realtime-heavy collaboration

Inputs: proposed 2,000 concurrent sockets, private rooms, typing/presence plus durable records, upload bytes and offline replay. Recommend evaluating Supabase provisionally for its verified integrated services, not guaranteeing that proposed fanout meets a plan. Missing: message size/rate, room distribution, reconnect bursts, access revocation and complete object-byte recovery. Counterevidence: a specialized realtime layer beside managed Postgres may be necessary after measured delivery/permission limits. Presence/Broadcast availability is not durable business-event delivery. A failed room denial test blocks that boundary even when the database query passes.

## Existing managed Postgres operations

Inputs: established RDS operator team, existing VPC/network controls and accepted Postgres application contract. Recommend retaining the supported RDS topology while verifying current extensions/versions/recovery instead of migrating for a free-tier headline. Missing actual complete-stack cost and migration justification. Counterevidence: branch-heavy development or integrated app services could justify a separately accepted alternative, not automatic migration.

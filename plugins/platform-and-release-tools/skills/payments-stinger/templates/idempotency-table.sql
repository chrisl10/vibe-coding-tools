-- payments-stinger, processed_webhook_events table
--
-- Purpose: idempotency for inbound Stripe webhooks. Insert event.id before
-- processing inside a transaction; ON CONFLICT means the event was already
-- received. A conflict is NOT proof that processing completed; inspect state
-- and recover incomplete claims. This is schema scaffolding, not a processor.
-- Use guide 11 for atomic projection/outbox/completion and durable lease design.
--
-- See guides/06-webhooks-and-provisioning.md and guides/09-security-and-pci-scope.md.
--
-- Hand to db-wasp-drone for the actual migration, indexing strategy, and
-- multi-tenant considerations (e.g., per-tenant partitioning if needed).

-- Postgres dialect; adapt for MySQL/SQL Server as needed.

CREATE TABLE IF NOT EXISTS processed_webhook_events (
    -- Stripe event ID, e.g. evt_1Abc123XYZ.
    -- Primary key + unique constraint enforces dedup atomically.
    event_id     text PRIMARY KEY,

    -- Stripe event type, e.g. 'checkout.session.completed'.
    -- Stored so ops queries can group by type without re-parsing payloads.
    event_type   text NOT NULL,

    -- When we received the event (server clock).
    received_at  timestamptz NOT NULL DEFAULT now(),

    -- Set after successful processing. NULL means processing is incomplete;
    -- receipt alone does not prove a crash or completed processing.
    -- An ops query SELECT * WHERE processed_at IS NULL AND received_at < now() - interval '5 minutes'
    -- finds stuck events to investigate.
    processed_at timestamptz,

    -- Optional: capture the raw event payload for forensic replay.
    -- Note: payloads may contain PII (customer email, address). Decide retention
    -- and access controls with security-wasp-drone before enabling.
    -- payload   jsonb,

    -- Application tenant scope must be verified through a server-owned mapping.
    -- Stripe account/customer identity does not itself authorize a tenant.
    -- Add the concrete account/environment/tenant schema with db-wasp-drone.
    -- tenant_id uuid

    CONSTRAINT processed_webhook_events_event_id_format
        CHECK (event_id ~ '^evt_[a-zA-Z0-9]+$')
);

-- Operational index: list recent events by time.
CREATE INDEX IF NOT EXISTS idx_pwe_received_at
    ON processed_webhook_events (received_at DESC);

-- Operational index: find stuck events (processed_at IS NULL).
CREATE INDEX IF NOT EXISTS idx_pwe_unprocessed
    ON processed_webhook_events (received_at)
    WHERE processed_at IS NULL;

-- Retention is an accepted application/audit/manual-replay policy, not a
-- universal provider-retry duration. This schema does not prescribe a daily
-- pruning job or a fixed retention period.
-- Before any authorized pruning, prove the surviving semantic business-action
-- evidence prevents repeated fulfillment, access extension, refund or other
-- effects for an old event. Receipt delivery, successful processing and each
-- downstream effect are different states; archiving is not automatically a
-- surviving live replay guard.
-- Record account/environment/tenant/consumer scope, reconciliation and restore
-- behavior, policy approval and negative replay tests in guide 11's contract.
-- If those facts or the required lifetime are unknown, retain the records and
-- report the missing decision. Do not run cleanup SQL from this scaffold.
-- The former fixed-period DELETE example is archived as historical unexecuted
-- source evidence outside the operational template; it is not current guidance.

-- ----- Optional: per-consumer dedup for fan-out (see guides/06-webhooks-and-provisioning.md, "Async work after the 200") -----
--
-- When one event triggers multiple downstream consumers, each consumer needs
-- its own dedup row to avoid double side effects.

CREATE TABLE IF NOT EXISTS processed_webhook_events_per_consumer (
    event_id      text NOT NULL,
    consumer_name text NOT NULL,
    processed_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (event_id, consumer_name)
);

-- This composite-key table is what each consumer (email job, ERP sync, CRM sync)
-- records only according to its recoverable processor contract. A record
-- inserted before an external side effect is not proof that effect completed. The webhook handler's main
-- dedup table records "this event reached the system once"; this per-consumer
-- table records "this consumer handled this event once".

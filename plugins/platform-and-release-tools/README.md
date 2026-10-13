# Platform and Release Tools

Integrate authentication, payments, analytics, messaging and production delivery.

The ship-and-operate journey joins provider integration and deployment, while keeping each existing actor/approval boundary.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 20 skills, 20 agents and 7 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [auth-stinger](skills/auth-stinger/SKILL.md) | Design and implement authentication. Use for provider choice, OAuth, passkeys, MFA, RBAC, sessions, or B2B SSO. |
| [changelog-release-notes-stinger](skills/changelog-release-notes-stinger/SKILL.md) | Write public changelogs and release notes. Use after shipping a change or when improving release communication. |
| [ci-release-stinger](skills/ci-release-stinger/SKILL.md) | Design CI and release gates for SvelteKit on Vercel or npm packages. Use for Actions jobs, migrations, caching, or publishing. |
| [crm-integration-stinger](skills/crm-integration-stinger/SKILL.md) | Design CRM sync with HubSpot, Salesforce, Pipedrive, Attio, and peers. Use for field mapping, deduplication, or sync conflicts. |
| [cron-scheduling-stinger](skills/cron-scheduling-stinger/SKILL.md) | Design reliable scheduled jobs. Use for cron expressions, DST, distributed execution, retries, idempotency, or monitoring. |
| [devops-stinger](skills/devops-stinger/SKILL.md) | Build Docker and GitHub Actions pipelines. Use for container hygiene, Compose, CI security, caching, image scans, or Depot. |
| [discord-bot-stinger](skills/discord-bot-stinger/SKILL.md) | Build Discord bots. Use for slash commands, modals, voice, gateway design, rate limits, or verification. |
| [doppler-stinger](skills/doppler-stinger/SKILL.md) | Doppler secrets manager for SvelteKit on Vercel - doppler run/secrets CLI, project/config model, Vercel sync, service tokens, rotation, audit logs, GitHub Actions CI, replacing .env files. |
| [mcp-protocol-stinger](skills/mcp-protocol-stinger/SKILL.md) | Design and audit MCP servers. Use for tools and resources, schemas, transport, JSON-RPC errors, auth, testing, or registration. |
| [payments-stinger](skills/payments-stinger/SKILL.md) | Stripe Elements for SvelteKit. Build checkout, enforce server entitlements, separate trial/payment/access state, and prepare approved billing-support actions. |
| [posthog-stinger](skills/posthog-stinger/SKILL.md) | PostHog for SvelteKit: install, pageview tracking, autocapture vs manual events, identify/alias, feature flags, experiments, replay, surveys, groups, Vercel proxy, EU/US residency, cost control. |
| [runbook-writing-stinger](skills/runbook-writing-stinger/SKILL.md) | Write and audit operational runbooks. Use for break-fix, scheduled tasks, exact commands, escalation, rollback, or game days. |
| [sentry-stinger](skills/sentry-stinger/SKILL.md) | Sentry error tracking for SvelteKit on Vercel - client/server hooks, source maps and releases, tracing sampling, session replay, PII scrubbing, alert tuning, and cost control. |
| [slack-app-stinger](skills/slack-app-stinger/SKILL.md) | Build Slack apps with Bolt. Use for slash commands, Block Kit, modals, Events API, OAuth installs, or Marketplace submission. |
| [status-page-stinger](skills/status-page-stinger/SKILL.md) | Public status page specialist: platform selection, incident communication templates, subscriber notifications, compliance. Use when setting up or auditing a status page. |
| [tailscale-stinger](skills/tailscale-stinger/SKILL.md) | Tailscale for SvelteKit/Vercel/Neon - tailnets, MagicDNS, ACLs/tags, SSH, subnet routers, exit nodes, private database access, Funnel/Serve, OAuth clients, auth keys, ephemeral CI nodes, key expiry. |
| [telegram-bot-stinger](skills/telegram-bot-stinger/SKILL.md) | Build Telegram bots. Use for grammY, aiogram, webhooks, Mini Apps, inline mode, Stars payments, or rate limits. |
| [traffic-capacity-stinger](skills/traffic-capacity-stinger/SKILL.md) | Plan traffic spikes from measured request, latency, resource, DB and queue data. Produce capacity, SLO, cost, admission and recovery proposals with bounded future validation scope. |
| [vercel-stinger](skills/vercel-stinger/SKILL.md) | Vercel deployment for SvelteKit (Svelte 5) + Neon - adapter-vercel config, runtimes, ISR/caching, env vars, cron, image optimization, middleware, WAF/rate limiting, cost control, rollbacks. |
| [workos-stinger](skills/workos-stinger/SKILL.md) | WorkOS AuthKit for SvelteKit - hosted/headless flows, sealed sessions, JWT verification, orgs, RBAC, SSO/SCIM, MFA/passkeys/Magic Auth, webhooks, and staging-to-prod cutover. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install platform-and-release-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use ci-release-stinger to review [workflow] and the current release process. Identify missing gates without changing live settings.
```

Expected result: A platform or release review, or the separately scoped implementation. Provider changes and publication require their own authority.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/platform-and-release-tools:build-integration` ([procedure](commands/build-integration.md)) | Build a scoped provider integration with explicit authorization, sync, retry, rate-limit and revocation contracts. |
| `/platform-and-release-tools:design-release-pipeline` ([procedure](commands/design-release-pipeline.md)) | Design a scoped release graph, evidence gates, promotion rules, and rollback drill from the actual pipeline. |
| `/platform-and-release-tools:plan-traffic-capacity` ([procedure](commands/plan-traffic-capacity.md)) | Prepare measured traffic-spike capacity, SLO, cost, admission and recovery proposals from supplied evidence. |
| `/platform-and-release-tools:prepare-native-release` ([procedure](commands/prepare-native-release.md)) | Prepare a native release artifact matrix with signing, update, install, and device evidence boundaries. |
| `/platform-and-release-tools:prepare-privacy-implementation` ([procedure](commands/prepare-privacy-implementation.md)) | Prepare a privacy engineering inventory, implementation boundaries, and proof requirements from actual product data flows. |
| `/platform-and-release-tools:prepare-release` ([procedure](commands/prepare-release.md)) | Prepare a release candidate, evidence checklist, honest notes, and a release decision without publishing it. |
| `/platform-and-release-tools:secure-platform-foundation` ([procedure](commands/secure-platform-foundation.md)) | Prepare and implement an authorized platform foundation with identity, secrets, environment and data-access boundaries. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [auth-wasp-drone](agents/auth-wasp-drone.md) | End-to-end authentication implementation specialist: provider selection (Clerk / Better Auth / Auth.js / Supabase Auth / WorkOS / Stack Auth / Kinde / Stytch), Google OAuth flows including the October 2025 unused-client deletion policy and GIS migration, MFA / passkeys, RBAC, session storage, and B2B SSO. | [auth-stinger](skills/auth-stinger/SKILL.md) |
| [changelog-release-notes-wasp-drone](agents/changelog-release-notes-wasp-drone.md) | Publishes engaging public changelogs and release notes that drive user engagement. | [changelog-release-notes-stinger](skills/changelog-release-notes-stinger/SKILL.md) |
| [ci-release-wasp-drone](agents/ci-release-wasp-drone.md) | CI and release engineering specialist. | [ci-release-stinger](skills/ci-release-stinger/SKILL.md) |
| [crm-integration-wasp-drone](agents/crm-integration-wasp-drone.md) | CRM connectivity specialist for HubSpot, Salesforce, Pipedrive, Attio, Folk, Close, and Copper. | [crm-integration-stinger](skills/crm-integration-stinger/SKILL.md) |
| [cron-scheduling-wasp-drone](agents/cron-scheduling-wasp-drone.md) | Scheduled-job specialist for cron expression authoring and auditing, platform-specific limits (Vercel Cron, Cloudflare Cron Triggers, GitHub Actions schedule), distributed-cron correctness (exactly-once execution, leader election, idempotency keys), timezone and DST safety, retry-on-failure patterns, and the "did the cron run?" observability loop. | [cron-scheduling-stinger](skills/cron-scheduling-stinger/SKILL.md) |
| [devops-wasp-drone](agents/devops-wasp-drone.md) | Container build + CI/CD pipeline specialist for Node / Next.js / TypeScript stacks: Dockerfile hygiene (multi-stage, BuildKit secrets + cache mounts, non-root, HEALTHCHECK, .dockerignore), Docker Compose for dev (profiles, healthchecked depends_on, secrets, watch), GitHub Actions architecture (reusable workflows, composite actions, concurrency, OIDC, least-privilege GITHUB_TOKEN, pinning to SHA), Depot acceleration (drop-in build-push-action, ARM ephemeral runners, shared persistent cache), image scanning (Trivy, Scout), and local-CI parity (Docker Bake, make targets). | [devops-stinger](skills/devops-stinger/SKILL.md) |
| [discord-bot-wasp-drone](agents/discord-bot-wasp-drone.md) | Discord bot and application specialist. | [discord-bot-stinger](skills/discord-bot-stinger/SKILL.md) |
| [doppler-wasp-drone](agents/doppler-wasp-drone.md) | Doppler specialist - project/config/environment model, the CLI (doppler run, doppler secrets set/get/upload/download), the Vercel integration and sync, service tokens and access control, secret rotation, audit logs, and CI/CD usage in GitHub Actions. | [doppler-stinger](skills/doppler-stinger/SKILL.md) |
| [mcp-protocol-wasp-drone](agents/mcp-protocol-wasp-drone.md) | MCP protocol authority for The Wasp Nest. | [mcp-protocol-stinger](skills/mcp-protocol-stinger/SKILL.md) |
| [payments-wasp-drone](agents/payments-wasp-drone.md) | Stripe integration specialist for SvelteKit (Svelte 5) on Vercel. | [payments-stinger](skills/payments-stinger/SKILL.md) |
| [posthog-wasp-drone](agents/posthog-wasp-drone.md) | PostHog specialist - SvelteKit client/server install, pageview tracking under SvelteKit's router, autocapture vs manual events, event/property naming, identify/alias identity stitching, feature flags (client, server, local evaluation, bootstrapping), experiments, session replay privacy and cost, surveys, group analytics for B2B, Vercel reverse proxy, EU/US data residency, cost control. | [posthog-stinger](skills/posthog-stinger/SKILL.md) |
| [runbook-writing-wasp-drone](agents/runbook-writing-wasp-drone.md) | Operational runbook authorship specialist: canonical templates (break-fix, scheduled operation, diagnostic), the no-implied-context audit protocol, exact-command discipline, escalation path architecture, rollback procedure standards, runbook-as-test (game day) methodology, and postmortem-to-runbook linkage. | [runbook-writing-stinger](skills/runbook-writing-stinger/SKILL.md) |
| [sentry-wasp-drone](agents/sentry-wasp-drone.md) | Sentry specialist for SvelteKit on Vercel - client/server SDK setup (hooks.server.ts, hooks.client.ts), source map upload via the Sentry Vite plugin, release and commit association, performance tracing sample rates, Session Replay setup and privacy configuration, beforeSend PII scrubbing, issue alert tuning, and event-quota/cost control. | [sentry-stinger](skills/sentry-stinger/SKILL.md) |
| [slack-app-wasp-drone](agents/slack-app-wasp-drone.md) | Slack app development specialist. | [slack-app-stinger](skills/slack-app-stinger/SKILL.md) |
| [status-page-wasp-drone](agents/status-page-wasp-drone.md) | Public status page specialist: platform selection (Statuspage/Atlassian, Better Stack, Instatus, Cachet OSS), component tree architecture, incident communication templates (initial/update/resolution), subscriber notification setup (email, SMS, webhook, Slack), GDPR/CAN-SPAM compliance, post-incident update discipline, and API-driven automation integration. | [status-page-stinger](skills/status-page-stinger/SKILL.md) |
| [tailscale-wasp-drone](agents/tailscale-wasp-drone.md) | Tailscale specialist - tailnets, MagicDNS, ACLs/grants/tags, Tailscale SSH, subnet routers, exit nodes, reaching a private Neon database from a dev machine or CI, Funnel/Serve, OAuth clients, auth keys, ephemeral CI nodes, key expiry and the security model. | [tailscale-stinger](skills/tailscale-stinger/SKILL.md) |
| [telegram-bot-wasp-drone](agents/telegram-bot-wasp-drone.md) | Telegram Bot specialist: Bot API (up to 10.0, May 2026 including guest mode and managed bots), grammY v1.x (TypeScript, recommended 2026 choice over abandoned Telegraf), aiogram 3.x (Python, async-native), webhook vs long-polling architecture with quantitative thresholds, Telegram Mini Apps initData validation (HMAC-SHA256 + Ed25519 paths), Telegram Stars payments (mandatory for digital goods), inline mode, and MTProto escalation via Telethon/TDLib. | [telegram-bot-stinger](skills/telegram-bot-stinger/SKILL.md) |
| [traffic-capacity-wasp-drone](agents/traffic-capacity-wasp-drone.md) | Read-only traffic-spike planning from measured requests, latency, CPU/memory, DB/pool and queue data: bottlenecks, SLO/cost limits, admission/recovery and future test scope. | [traffic-capacity-stinger](skills/traffic-capacity-stinger/SKILL.md) |
| [vercel-wasp-drone](agents/vercel-wasp-drone.md) | Vercel deployment specialist for SvelteKit (Svelte 5) + Neon Postgres - adapter-vercel config, Node.js vs Edge runtime, ISR/Cache-Control precedence, environment variables per environment, cron jobs, image optimization, Routing Middleware, WAF/rate limiting, cost control and spend limits, vercel.json, Turborepo monorepo deploys, Instant Rollback, and the Vercel-Neon integration. | [vercel-stinger](skills/vercel-stinger/SKILL.md) |
| [workos-wasp-drone](agents/workos-wasp-drone.md) | WorkOS specialist - AuthKit (hosted and headless), sealed sessions, JWT/JWKS verification, User Management (users/orgs/memberships/invitations), RBAC, SSO (SAML/OIDC), Directory Sync (SCIM), MFA/passkeys/Magic Auth, webhooks, and migrations from Supabase Auth or Clerk onto WorkOS. | [workos-stinger](skills/workos-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `application implementation` also needs `web-development-tools`, `backend-and-desktop-tools`.
- `prepare-release-native` also needs `backend-and-desktop-tools`.
- `secure-platform-foundation-data` also needs `data-and-ai-tools`.
- `secure-platform-foundation-web` also needs `web-development-tools`.
- `secure-platform-foundation-backend` also needs `backend-and-desktop-tools`.
- `prepare-privacy-implementation-data` also needs `data-and-ai-tools`.
- `build-integration-api` also needs `backend-and-desktop-tools`.
- `build-integration-data` also needs `data-and-ai-tools`.
- `prepare-native-release-platform` also needs `backend-and-desktop-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->

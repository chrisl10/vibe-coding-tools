# Bounded private-note starter

Status: NOT_RUN in Next.js. This is a source adaptation template, not a runnable complete app. No package.json, dependency installation, production setup, visual design or live provider is supplied. Intended for an existing TypeScript App Router project with compatible installed APIs and @/* mapped to source root. Preserve its Next config.

Files demonstrate a server-only contract, request-scoped read, thin mutation, explicit HTTP result and sanitized error boundary. The selected adapter deliberately throws until implemented. No credentials, fake authentication, shared cache or database backfill. Adapter must resolve verified session, read by tenant and resource, and enforce permission inside atomic write predicates. Identity must come from the verified provider session. Runtime reads need the existing adapter to access request/session APIs; a constant fixture is insufficient to establish isolation.

Copy only into authorized paths after resolving collisions. Existing backend/auth owner implements lib/adapter.ts; React and Impeccable supply product UI. Extend validation with the project's existing schema library. Observe guide03's cache cases in the actual app. This template uses a basic parser with JSDoc types for its bounded fields.

Pure policy syntax/mechanics can be exercised with existing Node using scripts/exercise-policy.mjs in the skill root. This does not check TSX, resolve Next imports, mount UI, validate sessions, call a database, build Next or test cache/auth behavior.

API sketch follows archived current docs, including Promise params, React useActionState and error.tsx retry. Older installed releases may expose reset instead; resolve against installed documentation before adaptation. The sketch is not a universal Next 13-16 template.

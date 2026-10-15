# Build, qualify and handoff

1. Run only existing, authorized app typecheck/lint/test/build commands. Record exact commands, code revision and output. Missing Nuxt dependencies means NOT_RUN, never install silently or treat source templates as a built app.
2. Qualify the actual output: static public files cannot host Nitro endpoints; Node output needs the agreed Node runtime; edge output needs compatibility checks for backend clients, modules and background work. Provider owner verifies preset, secrets injection by name, route behavior, CDN rules and release action.
3. Exercise the acceptance matrix with real app dependencies: public HTML and hydration; direct API anonymous/expired session denial; same resource with two users and tenants; principal change/logout; no private prerender payload; failed mutation; environment/public bundle leak review; deploy-preview behavior if separately authorized.
4. Distinguish source format/links/archive checks, pure mechanics, app build/runtime, provider and native-harness evidence. Mark each missing category NOT_RUN and state its prerequisite.
5. Submit code and evidence to independent Core Security first, then independent Quality. Resolve findings and re-evaluate before advancing. Parent runs repository health. User review and explicit authorization precede commits, pushes or release.

Grounding: deployment, rendering, sessions. Gate and authorization boundaries are Wasp Nest workflow policy.

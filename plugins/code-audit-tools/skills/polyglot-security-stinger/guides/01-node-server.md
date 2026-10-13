# 01 Node.js servers (Express, Fastify, NestJS, Hono, Koa)

For every path under stack id `node-server`. Loads [../references/ecosystems/node-server.md](../references/ecosystems/node-server.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md).

## Steps

1. **Identify the framework and runtime** from `detect.json.details.node-server[]` (`frameworks`, `runtime`). Note the Express major version: 2.x or 3.x is unmaintained and is a finding by itself [raw/node--express-security.md].
2. **Map the routes.** Find where routes are registered (`app.get/post`, `router.*`, `fastify.route`, Nest `@Controller` plus `@Get/@Post`, Hono `app.get`, Koa router). Write a short route table in notes: method, path, file:line, auth applied (yes, no, unclear).
3. **Map the auth model.** Find the authentication middleware, guard, hook, or plugin (`passport`, `express-session`, `jsonwebtoken`, Nest `@UseGuards`, Fastify `preHandler` / `onRequest` hooks, Hono middleware). Decide whether it is global or per route. Every route marked "no" or "unclear" in step 2 that reads or changes non-public data is a candidate for checklist N1.
4. **Run the checklist N1 to N17** in the reference. For each item run its `rg` block from the stack path, then open every hit in a production path and trace the value back to a source in the sources table.
5. **Authorization depth.** For each handler that loads a record by id, confirm the query also filters by the current user or tenant (N2). This is the most common real finding in AI-built servers; read the handler, not only the pattern hits.
6. **Body handling.** Confirm validation happens on the server (zod, joi, class-validator, Fastify JSON schema) before data reaches the ORM, and that NestJS `ValidationPipe` uses `whitelist` [raw/node--nestjs-validation.md]. Flag `create(req.body)`, spread of `req.body`, and `Object.assign` into models (N8).
7. **Prototype pollution.** For any deep merge or path-set of request JSON, check for `__proto__` / `constructor` guards (N9) [raw/node--nodejs-security-best-practices.md].
8. **CSRF and cookies.** If sessions are cookie based, check cookie flags and a CSRF token or origin check for state-changing routes (N10). Bearer-token-only APIs are not CSRF findings [raw/node--express-security.md].
9. **Hardening.** helmet or equivalent headers, `x-powered-by` disabled, body size limits, server timeouts, no `insecureHTTPParser`, rate limits on login and reset (N13, N14, N16) [raw/node--express-security.md] [raw/node--nodejs-security-best-practices.md].
10. **Errors.** Confirm the error handler hides stack traces when `NODE_ENV=production` (N15).
11. **Dependencies.** Follow the reference's dependency section; detail in guide 10.
12. **Write findings** per guide 14 with `tags: ["node-server", "<framework>", "<class>"]`.

## Done when

Every route in the table has an auth verdict, every checklist item has a result in notes (finding id, "pass", or "not applicable"), and every pattern hit in production code was read.

## Sources

[raw/node--express-security.md], [raw/node--nodejs-security-best-practices.md], [raw/node--nestjs-validation.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md]

# AI-generated code failure patterns across languages

Loaded by [guides/13-ai-generated-code-patterns.md](../../guides/13-ai-generated-code-patterns.md).

## Why this matters

- In Veracode's 2025 GenAI Code Security Report (over 100 models, Java, JavaScript, Python, C#), "AI-generated code introduced risky security flaws in 45% of tests", and "Larger, newer AI models didn't improve security" [raw/ai--veracode-genai-code-security-2025.md].
- In a USENIX Security 2025 study summarized by CSA (April 2026), 19.7 percent of 2.23 million generated samples named at least one package that does not exist, and 43 percent of those names came back on every rerun, which is what makes them registrable by attackers ("slopsquatting") [raw/ai--csa-slopsquatting-2026.md].

The per-CWE breakdown of the Veracode report is gated and not in this archive; this file does not quote it.

## Pattern table

Each pattern is a hypothesis to check, not a finding. Search, read, then decide.

| # | Pattern | What it looks like | Languages | Where to look |
| --- | --- | --- | --- | --- |
| AI1 | Tutorial secret carried into production | literal `SECRET_KEY = "..."`, `JWT_SECRET = "secret"`, `supersecret`, `changeme`, the exact key from a framework tutorial | all | settings, config, auth modules [raw/python--fastapi-oauth2-jwt.md] |
| AI2 | Hallucinated or slopsquatted dependency | an import or manifest entry for a package that does not exist on the registry, was first published very recently, or has a different publisher than the well-known project | npm, PyPI first; any registry | manifests, imports [raw/ai--csa-slopsquatting-2026.md] |
| AI3 | Auth on the happy path only | login and signup protected, but list, export, admin, webhook, or "internal" routes added later have no auth middleware or dependency | all | route tables, routers, controllers |
| AI4 | Id-only lookups (IDOR) | `findById(req.params.id)`, `get(Model, id)`, `Model.find(params[:id])` with no owner or tenant filter | all | handlers that take an id |
| AI5 | String-built SQL "for flexibility" | f-strings, template literals, `format!`, `fmt.Sprintf`, `+` for filters, sort, search | all | repositories, raw query helpers |
| AI6 | Validation in the client only | rich form checks in the frontend, `req.body` passed straight to the ORM on the server | node, python, php, ruby | create and update handlers |
| AI7 | Disabled security to make an error go away | `csrf.disable()`, `@csrf_exempt`, `skip_forgery_protection`, `verify=False`, `InsecureSkipVerify: true`, `rejectUnauthorized: false`, `danger_accept_invalid_certs(true)`, CORS `*` with credentials | all | grep the disable keywords |
| AI8 | Shell for convenience | `exec("cmd " + x)`, `shell=True`, `sh -c`, backticks | all | file conversion, git, image, pdf helpers |
| AI9 | Debug left on | `DEBUG = True`, `app.run(debug=True)`, `APP_DEBUG=true`, `UseDeveloperExceptionPage` outside Development, stack traces in JSON errors | all | settings, entry points, error handlers |
| AI10 | Over-broad CI tokens and unpinned actions in generated workflows | no `permissions:`, `@main` / `@v3` actions, `pull_request_target` copied from examples | GitHub Actions | `.github/workflows` [raw/ci--github-actions-secure-use.md] |
| AI11 | Insecure deserialization as a shortcut | `pickle` for caching or sessions, `unserialize` for cookies, `BinaryFormatter`, `Marshal.load` | python, php, dotnet, ruby | caches, sessions, queues [raw/owasp--deserialization-cheat-sheet.md] |
| AI12 | Weak password storage or homegrown crypto | `md5(password)`, `sha256(password)` without a password hash, custom token generation with non-crypto random | all | auth, reset tokens |
| AI13 | Logging secrets or personal data | `console.log(req.headers)`, `logger.info(user)`, printing tokens in error paths | all | middleware, error handlers |
| AI14 | Fake or placeholder checks | `// TODO: add auth`, `if (true)`, `return True  # check permissions later`, commented-out middleware | all | grep TODO and FIXME near auth code |

## ripgrep sweep

```bash
# AI1 tutorial and placeholder secrets
$RG -e '(?i)(secret|jwt|token|session)[\w-]*\s*[:=]\s*["\x27](secret|supersecret|changeme|change-me|your[-_]?secret|mysecret|keyboard cat|default)[^"\x27]*["\x27]'
# AI7 security switched off
$RG -e 'verify\s*=\s*False' -e 'InsecureSkipVerify:\s*true' -e 'rejectUnauthorized:\s*false' -e 'NODE_TLS_REJECT_UNAUTHORIZED' -e 'danger_accept_invalid_certs\(true\)' -e 'csrf\(\)\.disable\(\)|csrf\.disable\(\)|@csrf_exempt|skip_forgery_protection|IgnoreAntiforgeryToken'
# AI9 debug
$RG -e '^\s*DEBUG\s*=\s*True' -e 'debug\s*=\s*True' -e '^APP_DEBUG=true' -e 'UseDeveloperExceptionPage' -e '(err|error)\.stack'
# AI13 logging sensitive values
$RG -e '(console\.(log|info)|logger\.(info|debug)|print|log\.Print)\w*\([^)]*(password|token|secret|authorization|cookie|req\.headers)'
# AI14 placeholder checks near auth
$RG -e '(?i)(todo|fixme|hack)[^\n]{0,60}(auth|permission|access|security|csrf|validate)' -e 'if\s*\(\s*true\s*\)' -e 'return\s+True\s*#.*(later|todo)'
```

## AI2: how to check a suspicious package without installing it

1. List direct dependencies from the manifests in scope.
2. For any name you do not recognize or that looks like a blend of two real names, query the registry metadata only (no install): `npm view <name> time.created maintainers repository --json`, `curl -s https://pypi.org/pypi/<name>/json`, `gem info -r <name>`, `curl -s https://crates.io/api/v1/crates/<name>` (with a User-Agent header).
3. Flag when: the package does not exist (the build would fail or the name is free to register), it was created after the project started, it has a single new maintainer and no repository, or its repository does not match the import's apparent purpose [raw/ai--csa-slopsquatting-2026.md].
4. Severity: installed in production and suspicious on two or more signals, `high` with `likely`; one signal, `medium` with `possible`; name does not exist on the registry, `medium` (someone can register it) with `confirmed` for the non-existence.

If the network is not available, record the cap `"package existence checks not run (no network)"` and list unusual names in `notes` under "Not confirmed".

Sources: [raw/ai--veracode-genai-code-security-2025.md], [raw/ai--csa-slopsquatting-2026.md], [raw/python--fastapi-oauth2-jwt.md], [raw/ci--github-actions-secure-use.md], [raw/owasp--deserialization-cheat-sheet.md]

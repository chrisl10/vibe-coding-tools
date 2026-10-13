# Distilled research: polyglot security audit

Research window 2026-03-30 to 2026-09-30, fetched 2026-09-30. Older material is used only where it is the current authority and is labeled. Every row ends with its raw file.

## 1. Standards used in `refs`

| Fact | Source |
| --- | --- |
| OWASP Top 10:2025 IDs: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions | [raw/standards--owasp-top10-2025.md] |
| Deserialization of untrusted data is one class (CWE-502) across Python pickle and PyYAML load, PHP unserialize, Java ObjectInputStream and XMLDecoder, .NET BinaryFormatter and Json.NET TypeNameHandling | [raw/owasp--deserialization-cheat-sheet.md] |
| BinaryFormatter "is dangerous and cannot be secured" | [raw/owasp--deserialization-cheat-sheet.md] |
| SSRF minimum block list: 169.254.169.254, 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 plus IPv6; resolve then validate the IP; disable redirects; encoded IP forms bypass string checks; IMDSv2 | [raw/owasp--ssrf-cheat-sheet.md] |
| Mass assignment is also "autobinding" and "object injection"; the general fix is binding to DTOs or explicit allowlists | [raw/owasp--mass-assignment-cheat-sheet.md] |
| Command injection: shell-spawning APIs per language and the safer list-argument APIs; argument injection survives even without a shell | [raw/owasp--os-command-injection-cheat-sheet.md] |

## 2. Ecosystem facts

### Node.js servers

| Fact | Source |
| --- | --- |
| Express 2.x and 3.x are unmaintained; use helmet; disable x-powered-by; secure, httpOnly session cookies; validate redirect hosts; rate limit login by username plus IP | [raw/node--express-security.md] |
| Node threats with CWE ids: DoS CWE-400 (server timeouts), request smuggling CWE-444 (never `insecureHTTPParser`), timing CWE-208 (`crypto.timingSafeEqual`), malicious modules CWE-1357 (`npm ci`, `--ignore-scripts`), prototype pollution CWE-1321 (`Object.create(null)`, `Object.hasOwn`, schema validation) | [raw/node--nodejs-security-best-practices.md] |
| `npm config set min-release-age` exists from npm v11.10.0 as a dependency cooldown | [raw/node--nodejs-security-best-practices.md] |
| NestJS `ValidationPipe` `whitelist: true` strips undecorated properties; `forbidNonWhitelisted` rejects them | [raw/node--nestjs-validation.md] |
| `child_process.exec` spawns a shell; `execFile` does not | [raw/owasp--os-command-injection-cheat-sheet.md] |
| `npm audit` needs a lockfile; `--omit=dev`; `audit fix --force` can jump majors; `npm audit signatures` checks provenance | [raw/deps--npm-audit.md] |

Thin spot: Fastify, Hono, and Koa have no dedicated official security page in this archive. Their guidance in this skill is the shared Node and OWASP material applied to each framework's routing and body parsing; framework-specific defaults are not asserted.

### Python

| Fact | Source |
| --- | --- |
| Django querysets are parameterized; `raw()`, `extra()`, `RawSQL()` are the injection-prone APIs | [raw/python--django-security.md] |
| Django `mark_safe` and `|safe` bypass autoescape; `@csrf_exempt` removes CSRF; `DEBUG=False`; `ALLOWED_HOSTS`; reading `HTTP_HOST` directly bypasses host validation; `SECURE_*` settings | [raw/python--django-security.md] |
| Flask has no built-in CSRF; `MAX_CONTENT_LENGTH` is not set by default; set `TRUSTED_HOSTS`; `Markup` on user data and unquoted attributes cause XSS | [raw/python--flask-security.md] |
| FastAPI protects routes only through dependencies such as `Depends(get_current_active_user)`; tutorial uses PyJWT with an explicit `algorithms=[...]` list and pwdlib Argon2 | [raw/python--fastapi-oauth2-jwt.md] |
| pickle "is not secure. Only unpickle data you trust." | [raw/python--pickle-warning.md] |
| subprocess does not use a shell unless `shell=True` | [raw/python--subprocess-security.md] |
| pip-audit `-r` resolves like `pip install -r`; use `--no-deps` on pinned files; exit 1 on findings | [raw/deps--pip-audit.md] |

### Go

| Fact | Source |
| --- | --- |
| gosec rules: G101 creds, G107 URL from variable, G112 and G114 server timeouts, G201 and G202 SQL building, G204 subprocess, G304 file path, G305 zip slip, G401 to G404 weak crypto, G402 InsecureSkipVerify | [raw/go--gosec.md] |
| html/template escapes by context; text/template does not; `template.HTML`, `template.JS`, `template.URL` bypass escaping | [raw/go--html-template.md] |
| govulncheck reports only vulnerabilities reachable from called functions | [raw/deps--govulncheck.md] |

Thin spot: Gin, Echo, and Fiber binding and CSRF defaults were not fetched. Treat their binding of request bodies into structs as a mass assignment candidate and confirm by reading the struct tags; do not assert framework defaults.

### Rust

| Fact | Source |
| --- | --- |
| `sqlx::query!` needs a string literal and binds `$N` or `?`; SQL built with `format!` and passed to `sqlx::query` loses binding | [raw/rust--sqlx-query-macro.md] |
| cargo-audit checks Cargo.lock against RustSec; use `--file` and run outside the project for untrusted code to avoid build scripts | [raw/deps--cargo-audit.md] |
| osv-scanner Rust call analysis is experimental and compiles the code | [raw/deps--osv-scanner-usage.md] |

Thin spot: Axum and Actix extractor and CSRF behavior were not fetched. The Rust guide relies on generic patterns (SQL text building, `std::process::Command` with `sh -c`, path joins with user input, `unsafe` and `unwrap` on request data) and marks framework-default claims as needing manual confirmation.

### Ruby on Rails

| Fact | Source |
| --- | --- |
| `protect_from_forgery with: :exception` default; strong parameters; string-interpolated `where` is SQLi; `system` with one string is command injection; `Kernel#open("| cmd")` runs commands; `raw` / `html_safe` XSS; `redirect_to(params[:url])` open redirect; `send_file` path traversal; `\A` `\z` anchors; credentials.yml.enc; `rate_limit` | [raw/ruby--rails-security-guide.md] |
| `Marshal.load` on untrusted data can lead to RCE | [raw/ruby--marshal-warning.md] |
| bundler-audit checks Gemfile.lock and insecure `http://` / `git://` sources | [raw/deps--bundler-audit.md] |

Thin spot: Psych `YAML.load` safety defaults were not in the fetched pages. Treat YAML loading of untrusted input as a manual-read item.

### PHP

| Fact | Source |
| --- | --- |
| Laravel models need `$fillable` or `$guarded`; `$guarded = []` unguards; `is_admin` escalation example; `preventSilentlyDiscardingAttributes` | [raw/php--laravel-mass-assignment.md] |
| Laravel docs fetched were 12.x with a banner that 13.x is current | [raw/php--laravel-mass-assignment.md] |
| `unserialize` on untrusted input is unsafe even with `allowed_classes` | [raw/php--unserialize-warning.md] |
| Symfony forms check CSRF by default; per-form `csrf_protection` can be disabled; `isCsrfTokenValid`; stateless tokens from 7.2 | [raw/php--symfony-csrf.md] |
| PHP shell functions: exec, system, shell_exec, passthru, popen, backticks | [raw/owasp--os-command-injection-cheat-sheet.md] |
| `composer audit --locked --format=json` audits the lock file without vendor | [raw/deps--composer-audit.md] |

### Java and Kotlin (Spring Boot)

| Fact | Source |
| --- | --- |
| Actuator exposes only `health` over HTTP by default; `exposure.include=*` exposes env, configprops, heapdump, loggers; secure with `EndpointRequest`; `show-values=always` removes sanitizing | [raw/java--spring-boot-actuator.md] |
| Spring Security CSRF is on by default for unsafe methods; `csrf.disable()` is acceptable only for non-browser backends | [raw/java--spring-security-csrf.md] |
| `Runtime.exec(String)` vs `ProcessBuilder` | [raw/owasp--os-command-injection-cheat-sheet.md] |
| Spring MVC mass assignment: `@InitBinder` allowlists or DTOs; Jackson `@JsonIgnore` | [raw/owasp--mass-assignment-cheat-sheet.md] |

Thin spot: Spring Data `@Query` native query and JPA criteria injection pages were not fetched; the guide uses the generic "string concatenation into a query string" rule.

### .NET (ASP.NET Core)

| Fact | Source |
| --- | --- |
| MVC filters `[ValidateAntiForgeryToken]`, `[AutoValidateAntiforgeryToken]`, `[IgnoreAntiforgeryToken]`; minimal APIs need `AddAntiforgery` and `UseAntiforgery`; `.DisableAntiforgery()` opt-out; CSRF matters for cookie auth | [raw/dotnet--aspnetcore-antiforgery.md] |
| A `Sec-Fetch-Site` based automatic CSRF middleware is documented for ASP.NET Core 11.0, not GA at fetch time | [raw/dotnet--aspnetcore-antiforgery.md] |
| EF Core `FromSql`, `FromSqlInterpolated`, `ExecuteSql`, `SqlQuery` parameterize; the `Raw` variants do not | [raw/dotnet--efcore-raw-sql.md] |
| `dotnet package list --vulnerable --include-transitive --format json` (.NET 10 naming; `dotnet list package` on 9 or earlier) | [raw/deps--dotnet-package-list.md] |

## 3. Cross-cutting tools

| Fact | Source |
| --- | --- |
| osv-scanner V2: `osv-scanner scan -r DIR`, `-L lockfile`, `--format json`, offline databases; respects .gitignore; Go call analysis on by default, Rust experimental | [raw/deps--osv-scanner-usage.md] |
| osv-scanner reads npm, pnpm, yarn, bun, Python locks and requirements.txt (best effort), Gemfile.lock, Cargo.lock, go.mod, pom.xml, gradle lockfiles, .NET packages.lock.json and deps.json, composer.lock | [raw/deps--osv-scanner-supported-lockfiles.md] |
| pom.xml transitive resolution uses deps.dev and is off in offline mode | [raw/deps--osv-scanner-supported-lockfiles.md] |
| gitleaks: `gitleaks git` scans history, `gitleaks dir` the tree; `--redact`; exit 1 on leaks; `--max-target-megabytes` skips big files | [raw/secrets--gitleaks.md] |
| gitleaks default rule shapes (AWS AKIA, GitHub ghp_, Stripe sk_live_, private key blocks, and more) | [raw/secrets--gitleaks-default-rules.md] |
| trufflehog verifies candidates by calling provider APIs; `--no-verification` disables; `--fail` exits 183 | [raw/secrets--trufflehog.md] |
| Semgrep `--config auto` contacts the registry with the project URL; `--metrics=off`; named rulesets verified to resolve | [raw/sast--semgrep-cli.md] |
| Opengrep is a Semgrep CE fork (LGPL 2.1), runs existing rules with `opengrep scan -f rules DIR` | [raw/sast--opengrep.md] |
| Tool versions on 2026-09-30 | [raw/tools--version-pins-2026-09-30.md] |

## 4. CI/CD and infrastructure

| Fact | Source |
| --- | --- |
| Untrusted `${{ github.event.* }}` in `run:` is script injection; pass through `env:` | [raw/ci--github-actions-secure-use.md] |
| Pin actions to full commit SHA; default GITHUB_TOKEN to read; `pull_request_target` and `workflow_run` must not check out untrusted code | [raw/ci--github-actions-secure-use.md] |
| Pwn request: `pull_request_target` plus checkout of PR head plus build scripts; token in memory even without secrets; split into `pull_request` and `workflow_run` | [raw/ci--github-security-lab-pwn-requests.md] (2021, timeless, still the reference) |
| zizmor audits: template-injection, dangerous-triggers, unpinned-uses, excessive-permissions, artipacked, cache-poisoning, secrets-inherit, impostor-commit, and more; `uvx zizmor`, `--offline` | [raw/ci--zizmor-audits.md] |
| March 2026: Trivy v0.69.4 and trivy-action / setup-trivy tags force-pushed to credential stealers | [raw/ci--trivy-teampcp-compromise-2026.md] |
| May 2026: actions-cool/issues-helper tags moved to an imposter commit that read runner memory | [raw/ci--actions-cool-imposter-commit-2026.md] |
| Docker: pin base by digest, multi-stage, `USER` non-root, `.dockerignore`, prefer COPY over ADD | [raw/infra--docker-build-best-practices.md] |
| Compose secrets mount at `/run/secrets/<name>`; env vars leak to logs and all processes | [raw/infra--docker-compose-secrets.md] |
| `trivy config DIR` covers Terraform, Dockerfile, Kubernetes, Helm, CloudFormation; needs to download the checks bundle | [raw/infra--trivy-misconfiguration.md] |

## 5. AI-generated code

| Fact | Source |
| --- | --- |
| 45 percent of tests produced risky flaws; newer, larger models did not improve security (Java, JavaScript, Python, C#) | [raw/ai--veracode-genai-code-security-2025.md] (October 2025, within the 12-month allowance) |
| 19.7 percent of 2.23 million samples had a hallucinated package; 43 percent of those names repeat on every run; defenses: check existence, age, publisher, lockfiles | [raw/ai--csa-slopsquatting-2026.md] |
| Tutorial code carries hard-coded secrets (FastAPI tutorial's literal `SECRET_KEY`) | [raw/python--fastapi-oauth2-jwt.md] |

## 6. Conflicts and open questions

- Semgrep `--config auto` is convenient but sends the project URL to the registry. This skill always names rulesets and passes `--metrics=off` [raw/sast--semgrep-cli.md].
- trufflehog's strength (verification) is a side effect in an audit. This skill defaults to `--no-verification`; verified mode only with user consent [raw/secrets--trufflehog.md].
- Security scanners were themselves compromised in 2026. Pin versions, prefer source builds from the Go module proxy (checksummed) or PyPI, and never run tools with the user's real credentials in the environment [raw/ci--trivy-teampcp-compromise-2026.md] [raw/tools--version-pins-2026-09-30.md].
- Framework-default thin spots are listed per ecosystem above. Where the archive has no source, guides say "confirm by reading the code" instead of asserting a default.

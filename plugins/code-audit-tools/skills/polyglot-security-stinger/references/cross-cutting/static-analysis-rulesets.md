# Static analysis rule packs

Loaded by [guides/11-static-analysis.md](../../guides/11-static-analysis.md).

## 1. Semgrep registry packs per stack

Every pack below was verified to resolve on 2026-09-30 by fetching `https://semgrep.dev/c/p/<name>` [raw/sast--semgrep-cli.md].

| Stack id | Packs to pass (each with its own `--config`) |
| --- | --- |
| all | `p/security-audit`, `p/secrets`, `p/owasp-top-ten` |
| node-server | `p/javascript`, `p/nodejs`, `p/expressjs` (also when the code is TypeScript) |
| python | `p/python`, plus `p/django` or `p/flask` when detected |
| go | `p/golang`, `p/gosec` |
| rust | `p/rust` |
| ruby | `p/ruby` |
| php | `p/php` |
| java-kotlin | `p/java`, `p/kotlin` (when Kotlin is present) |
| dotnet | `p/csharp` |
| CI and infra | `p/github-actions`, `p/dockerfile`, `p/terraform`, `p/ci` |

`p/default` is a broad mix; prefer the explicit list so the run is reproducible.

## 2. Exact commands

```bash
cd "$COPY"
pipx run --spec semgrep==1.178.0 semgrep scan \
  --metrics=off \
  --config p/security-audit --config p/secrets --config p/owasp-top-ten \
  --config p/python --config p/django \
  --exclude node_modules --exclude vendor --exclude dist --exclude build --exclude target \
  --json --json-output="$RAW/semgrep.json" \
  services/py
# exit 0 means it ran; findings are in the JSON. Add --error only if you want exit 1 on findings.
```

- Never use `--config auto`: it logs in to the registry "with your project URL" [raw/sast--semgrep-cli.md].
- Registry packs are downloaded at run time. Without network, Semgrep cannot fetch them: go to Opengrep with a local rules folder, or to the `rg` sweeps.
- `semgrep ci` is for CI with an account; audits use `semgrep scan` [raw/sast--semgrep-cli.md].

Opengrep (Semgrep CE fork, LGPL 2.1, v1.30.0, rules work unchanged) [raw/sast--opengrep.md]:

```bash
# rules from a local folder; for example a pre-fetched copy of github.com/opengrep/opengrep-rules
opengrep scan -f "$WS/.scratch/rules" --sarif-output="$RAW/opengrep.sarif" services/py
```

gosec for Go [raw/go--gosec.md]:

```bash
cd "$COPY/services/goapi" && go run github.com/securego/gosec/v2/cmd/gosec@v2.29.0 -fmt json -out "$RAW/gosec.json" ./...
```

## 3. Reading results

1. Semgrep and Opengrep findings are pattern matches. Each starts at `confidence: possible` and `severity` at most `medium` (contract rule 3).
2. Read the code around every ERROR and WARNING hit in production paths. If the value is user controlled and reaches the sink: `likely` (or `confirmed` when traced from route to sink), then set severity from the class table in [contract-output-rules.md](contract-output-rules.md).
3. Drop hits in tests, fixtures, examples, and generated code, and count them in `notes` ("42 hits in tests ignored").
4. INFO-level rule hits are hygiene: at most `low`.
5. Put the rule id in `refs` (the `check_id` value from the JSON, prefixed `semgrep:`), plus the CWE from the rule metadata.

## 4. When no SAST engine can run

Record the cap `"static analysis engines not run (<reason>); ripgrep pattern sweep only"`, set the `sast_engine` measure band to `not-run`, then run every `rg` block in the ecosystem references for the detected stacks. The manual sweep is required in every run anyway; engines only add coverage.

Sources: [raw/sast--semgrep-cli.md], [raw/sast--opengrep.md], [raw/go--gosec.md], [raw/tools--version-pins-2026-09-30.md]

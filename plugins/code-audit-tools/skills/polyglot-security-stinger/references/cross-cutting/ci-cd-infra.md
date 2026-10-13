# CI/CD and infrastructure reference

Loaded by [guides/12-ci-cd-and-infrastructure.md](../../guides/12-ci-cd-and-infrastructure.md). Uses `infra` from `detect_ecosystems.py` to find files.

## 1. GitHub Actions

### Checklist

| # | Check | Severity guide | Refs |
| --- | --- | --- | --- |
| GH1 | No `${{ github.event.* }}` (titles, bodies, branch names, commit messages, comments, labels), `${{ github.head_ref }}`, or `${{ inputs.* }}` from untrusted triggers inside `run:` or `script:` | `high` (critical if the workflow holds write tokens or deploy secrets and runs on fork PRs, issues, or comments) | CWE-78, CWE-94 |
| GH2 | `pull_request_target` and `workflow_run` workflows do not check out the PR head (`ref: ${{ github.event.pull_request.head.sha }}` or `head.ref`) and then build or test it | `critical` when secrets or a write token are available | CWE-829 |
| GH3 | Third-party actions are pinned to a full 40-character commit SHA, not `@v1` or `@main` | `medium` (`high` for actions in release or deploy jobs) | CWE-829, OWASP A03:2025 |
| GH4 | Top-level `permissions:` is set and minimal (for example `contents: read`); jobs raise only what they need; no `permissions: write-all` | `medium` | CWE-250 |
| GH5 | `secrets: inherit` is not used for reusable workflows that do not need every secret | `low` | CWE-200 |
| GH6 | `actions/checkout` in jobs that upload artifacts uses `persist-credentials: false` | `low` to `medium` (zizmor `artipacked`) | CWE-522 |
| GH7 | Self-hosted runners are not used by public repositories or fork-triggered workflows | `high` | CWE-269 |
| GH8 | Cloud deploys use OIDC (`id-token: write` plus a role) instead of long-lived keys in secrets | `low` | CWE-798 |
| GH9 | No secrets echoed, written to artifacts, or passed on command lines visible in logs | `high` if real | CWE-532 |
| GH10 | Actions known to have been compromised are not referenced by tag (for example `aquasecurity/trivy-action` and `aquasecurity/setup-trivy` tags force-pushed in March 2026, `actions-cool/issues-helper` tags moved in May 2026) | `high` if pinned by tag and the run window overlapped; `medium` otherwise | OWASP A03:2025 |

Sources: [raw/ci--github-actions-secure-use.md], [raw/ci--github-security-lab-pwn-requests.md], [raw/ci--zizmor-audits.md], [raw/ci--trivy-teampcp-compromise-2026.md], [raw/ci--actions-cool-imposter-commit-2026.md].

### ripgrep patterns

```bash
cd "$COPY"
W='.github/workflows'
# Untrusted context in expressions (then check whether the line is inside run: or script:)
$RG -g "$W/*.y*ml" -e '\$\{\{\s*github\.event\.(issue|pull_request|comment|review|review_comment|discussion|head_commit|commits|pages|workflow_run)[^}]*(title|body|name|message|label|ref|email|head_branch|default_branch)[^}]*\}\}' -e '\$\{\{\s*github\.head_ref\s*\}\}'
# Dangerous triggers and head checkouts
$RG -g "$W/*.y*ml" -e 'pull_request_target' -e 'workflow_run' -e 'issue_comment' ; $RG -g "$W/*.y*ml" -e 'ref:\s*["\x27]?\$\{\{\s*github\.event\.pull_request\.head\.(sha|ref)'
# Unpinned actions (anything not followed by a 40-hex SHA)
$RG -g "$W/*.y*ml" -g 'action.y*ml' -e 'uses:\s*[\w.-]+/[\w./-]+@(?![0-9a-f]{40}\b)' --pcre2
# Permissions
$RG -g "$W/*.y*ml" -e '^permissions:' -e 'write-all' -e 'contents:\s*write' -e 'id-token:\s*write'
# Secrets handling
$RG -g "$W/*.y*ml" -e 'secrets:\s*inherit' -e 'persist-credentials' -e 'runs-on:\s*\[?\s*self-hosted' -e 'echo\s+.*\$\{\{\s*secrets\.'
# Known compromised actions by tag
$RG -g "$W/*.y*ml" -e 'aquasecurity/(trivy-action|setup-trivy)@(?![0-9a-f]{40})' -e 'actions-cool/[\w-]+@(?![0-9a-f]{40})' --pcre2
```

zizmor covers most of this automatically: `uvx zizmor@1.30.1 --offline --format json .github/workflows`. Its findings are pattern matches; read each one [raw/ci--zizmor-audits.md].

### Vulnerable vs fixed

```yaml
# vulnerable: PR title is spliced into the shell script
- run: echo "Title: ${{ github.event.pull_request.title }}"
# fixed: pass through env and quote
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $TITLE"
```

```yaml
# vulnerable: pwn request
on: pull_request_target
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { ref: "${{ github.event.pull_request.head.sha }}" }
      - run: npm ci && npm test        # runs the PR author's scripts with a write token
# fixed: build untrusted code under pull_request with no secrets; do privileged work in a separate workflow_run job that treats artifacts as data
on: pull_request
permissions: { contents: read }
```

```yaml
# vulnerable
- uses: some-org/deploy-action@v2
# fixed (pin to the full SHA of a reviewed release; keep the tag as a comment)
- uses: some-org/deploy-action@<40-character-commit-sha> # v2.3.1
```

```yaml
# vulnerable: default token scope left to repository settings
on: push
# fixed
on: push
permissions:
  contents: read
```

## 2. Dockerfiles

| # | Check | Severity | Refs |
| --- | --- | --- | --- |
| DK1 | Final stage sets `USER` to a non-root user | `medium` for internet-facing services, `low` otherwise | CWE-250 |
| DK2 | No secrets in `ARG`, `ENV`, or `COPY`ed files (`.env`, keys); build secrets use `RUN --mount=type=secret` | `high` if a real secret is baked in | CWE-798, CWE-538 |
| DK3 | `.dockerignore` exists and excludes `.git`, `.env*`, keys, `node_modules` | `low` (`high` if `COPY . .` would copy a real `.env`) | CWE-538 |
| DK4 | Base images pinned by digest (`FROM image@sha256:...`), or at least a specific tag, never `latest` | `low` | OWASP A03:2025 |
| DK5 | Multi-stage build keeps compilers and dev dependencies out of the final image | `low` | |
| DK6 | `ADD` with remote URLs is not used to fetch code without checksum | `low` to `medium` | CWE-494 |
| DK7 | `curl ... | sh` style installs pin a version and verify a checksum | `medium` | CWE-494 |

```bash
$RG -g '*Dockerfile*' -g 'Containerfile' -e '^\s*USER\s' -e '^\s*(ARG|ENV)\s+\w*(SECRET|TOKEN|PASSWORD|KEY|API)\w*' -e '^\s*FROM\s+[^@\s]+(:latest)?\s*($|AS)' -e '^\s*ADD\s+https?://' -e 'curl[^|]*\|\s*(ba)?sh' -e 'COPY\s+\.\s+\.' -e 'mount=type=secret'
$RG --files -g '.dockerignore'
```

Sources: [raw/infra--docker-build-best-practices.md], [raw/infra--docker-compose-secrets.md].

```dockerfile
# vulnerable
FROM node:22
ARG NPM_TOKEN
ENV DATABASE_URL=postgres://app:hunter22@db/app
COPY . .
RUN npm install
CMD ["node", "server.js"]
# fixed
FROM node:22-slim@sha256:<digest> AS build
WORKDIR /app
COPY package*.json ./
RUN --mount=type=secret,id=npm_token NPM_TOKEN="$(cat /run/secrets/npm_token)" npm ci --omit=dev
COPY src ./src
FROM node:22-slim@sha256:<digest>
WORKDIR /app
COPY --from=build /app ./
USER node
CMD ["node", "src/server.js"]
```

## 3. docker-compose

| # | Check | Severity |
| --- | --- | --- |
| DC1 | Real credentials are not written inline under `environment:`; use top-level `secrets:` mounted at `/run/secrets/<name>` or an untracked env file | `high` for real values, `low` for local-only dev defaults clearly marked |
| DC2 | Databases and admin UIs are not published on `0.0.0.0` ports in files used beyond local dev | `medium` |
| DC3 | No `privileged: true`, host network, or Docker socket mounts (`/var/run/docker.sock`) without a stated need | `high` |

```bash
$RG -g '*compose*.y*ml' -e '(PASSWORD|SECRET|TOKEN|API_KEY)\w*\s*[:=]\s*[^$\s{][^\s]{3,}' -e 'privileged:\s*true' -e 'network_mode:\s*host' -e '/var/run/docker\.sock' -e '^\s*-\s*"?\d+:\d+' -e '^secrets:'
```

Source: [raw/infra--docker-compose-secrets.md] ("Environment variables are often available to all processes ... printed in logs").

## 4. Terraform basics

Run `trivy config --format json "$COPY"` (Trivy v0.74.0, never v0.69.4) when available; it covers Terraform, Dockerfile, Kubernetes, Helm, and CloudFormation [raw/infra--trivy-misconfiguration.md]. Semgrep `p/terraform` is the alternative. Manual checks:

| # | Check | Severity |
| --- | --- | --- |
| TF1 | No `*.tfstate` or `*.tfvars` with real values committed | `high` |
| TF2 | No provider credentials (`access_key`, `secret_key`, `client_secret`, `password`) as literals | `critical` if live |
| TF3 | Security groups and firewall rules do not open admin ports (22, 3389, database ports) to `0.0.0.0/0` or `::/0` | `high` |
| TF4 | Storage buckets are not public (`acl = "public-read"`, public access blocks disabled) unless they are meant to host public assets | `high` if data is sensitive |
| TF5 | Databases are not `publicly_accessible = true`; encryption at rest is on | `medium` to `high` |
| TF6 | Remote state backend is configured (not local state in the repo) | `low` |

```bash
$RG -g '*.tf' -e '(access_key|secret_key|client_secret|password)\s*=\s*"[^"$][^"]{6,}"' -e 'cidr_blocks\s*=\s*\[\s*"0\.0\.0\.0/0"' -e '::/0' -e 'publicly_accessible\s*=\s*true' -e 'acl\s*=\s*"public-read' -e 'block_public_(acls|policy)\s*=\s*false' -e 'encrypted\s*=\s*false' -e 'backend\s+"'
$RG --files -g '*.tfstate' -g '*.tfstate.backup' -g '*.tfvars'
```

Thin spot: Terraform provider-specific defaults are not in the archive. Report what the code states; do not assert cloud defaults.

Sources: [raw/infra--trivy-misconfiguration.md], [raw/ci--trivy-teampcp-compromise-2026.md].

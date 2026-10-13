# 12 CI/CD and infrastructure

Loads [../references/cross-cutting/ci-cd-infra.md](../references/cross-cutting/ci-cd-infra.md) and [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md). Run when this Drone owns the infra files (guide 00 step 7).

## Steps

1. **List the files** from `detect.json.infra`: GitHub workflows, GitLab CI, Dockerfiles, compose files, Terraform folders, Helm charts, Kubernetes-looking manifests, committed env files.
2. **GitHub Actions.**
   1. Run zizmor 1.30.1 offline: `uvx zizmor@1.30.1 --offline --format json .github/workflows` (or the pipx form) [raw/ci--zizmor-audits.md].
   2. Run the `rg` block in ci-cd-infra.md section 1 regardless.
   3. For each workflow, write a one-line summary in notes: triggers, top-level `permissions`, secrets used, jobs that deploy or publish.
   4. Apply checklist GH1 to GH10. The highest-impact shapes are untrusted `${{ github.event.* }}` inside `run:` (script injection) and `pull_request_target` or `workflow_run` with a checkout of the PR head followed by build steps (pwn request) [raw/ci--github-actions-secure-use.md] [raw/ci--github-security-lab-pwn-requests.md].
   5. For unpinned actions, list each `uses:` that is not a 40-character SHA. Treat the 2026 incidents as concrete proof that tags move: Trivy's actions (March 2026) and actions-cool (May 2026) had tags repointed to credential stealers [raw/ci--trivy-teampcp-compromise-2026.md] [raw/ci--actions-cool-imposter-commit-2026.md]. Group all unpinned third-party actions into one finding per workflow file.
3. **GitLab CI or other CI.** Apply the same classes by reading the file: untrusted variables in scripts, secrets printed, unpinned remote includes and images. Say in notes that no dedicated tool was run.
4. **Dockerfiles.** Run the Dockerfile `rg` block and apply DK1 to DK7. Check `.dockerignore` against what `COPY . .` would bring in, especially `.env` files listed in `detect.json.infra.env_files` [raw/infra--docker-build-best-practices.md].
5. **Compose.** Apply DC1 to DC3. Inline credentials under `environment:` are the common finding; the fix is top-level `secrets:` mounted at `/run/secrets/<name>` [raw/infra--docker-compose-secrets.md].
6. **Terraform and other IaC.** Run `trivy config` with Trivy v0.74.0 when available (never v0.69.4), or Semgrep `p/terraform`, then apply TF1 to TF6 by reading the files [raw/infra--trivy-misconfiguration.md]. Report only what the code states; cloud defaults are a thin spot.
7. **Write findings** per guide 14 with `tags: ["ci", "github-actions"]`, `["docker"]`, `["compose"]`, or `["terraform"]`. Locations point at the workflow or file line.
8. **Record measures**: `ci_workflows`, `ci_unpinned_actions`, `ci_injection_sinks`, `ci_dangerous_triggers`, `docker_root_images`, `iac_public_exposures`.

## Done when

Every workflow has a summary line and a checklist result, every Dockerfile, compose file, and Terraform folder was read, tool runs or caps are recorded, and measures are written.

## Sources

[raw/ci--github-actions-secure-use.md], [raw/ci--github-security-lab-pwn-requests.md], [raw/ci--zizmor-audits.md], [raw/ci--trivy-teampcp-compromise-2026.md], [raw/ci--actions-cool-imposter-commit-2026.md], [raw/infra--docker-build-best-practices.md], [raw/infra--docker-compose-secrets.md], [raw/infra--trivy-misconfiguration.md]

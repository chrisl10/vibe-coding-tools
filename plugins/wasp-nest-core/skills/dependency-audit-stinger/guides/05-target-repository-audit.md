# Audit the Target Repository's Supply Chain

Begin with observed source and the user's assigned scope. The Hivemind case in this skill is useful only where its mechanics match the target.

## Establish the actual ecosystem

Read the target's manifests, committed lockfiles, runtime/toolchain pins, installation hooks and release packaging. A monorepo may contain several ecosystems; record each and the components it reaches. Do not infer npm from this skill's case study or install a scanner merely to fill a checklist.

Identify existing dependency checks and their exact commands. For npm use its lockfile and frozen installation policy; for pnpm/Yarn, Python, Rust or Go preserve that project's equivalents and obtain current primary documentation for any unfamiliar scanner. Do not change package managers, add Hivemind's guards or loosen native-dependency pins without an approved target requirement.

## Review exposure and provenance

Read both direct and transitive versions from the actual resolved graph. Distinguish an advisory identifier and affected version range from demonstrated reachability, exploitability or malicious install behavior. Evaluate native hooks, package origins, lockfile integrity and existing publish allowlists. Missing scan evidence is unknown, not a clean bill of health.

For an SBOM, record the target artifact, format, generator/version, dependency scope and omissions. For provenance, verify what the ecosystem attestation covers; source/build provenance alone does not establish benign code or runtime safety.

## Select and run applicable checks

Prefer existing checks. State any additional scanner or tool's purpose and installation requirement before use. New dependencies, settings, provider registration, credentials, publishing and remote writes require the user's applicable authorization. Read-only repository checks still respect the current time/retry limits.

Choose an update service from the target's actual needs. [Dependabot groups](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#groups) are supported; a recommendation cannot reject it merely for lacking grouping. Verify current platform support, update-delay controls, automation policy and cost before making a tool choice.

## Deliver the scoped result

Report the exact source or artifact inspected, tool output, affected package/version and justified remediation. A waiver needs its reason, expiry and issue reference. Name every unscanned ecosystem or artifact and obtain independent Security/Quality review for approved implementation changes. Preserve the user's existing approvals without inventing new authority.

For a matching npm target, continue with [scanner selection](00-scanner-decision-matrix.md), [triage](01-vulnerability-triage.md), [SBOM](02-sbom-workflow.md), [lockfiles](03-lockfile-discipline.md) and [provenance](04-provenance-verification.md). Those guides retain the original case's scripts and examples; treat target differences explicitly.

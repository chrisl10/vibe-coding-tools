# Audit Tools third-party notices

## Audit My Code

The Audit My Code command, orchestrator, Drones, Stingers, guides, references, and scripts are first-party Legion Code Inc. material under AGPL-3.0-or-later. Each Stinger's `references/research/raw/` folder preserves excerpts and notes from third-party publishers (framework documentation, security advisories, tool documentation); those documents keep their publishers' rights and terms, and the AGPL grant covers only the Wasp Nest analysis and organization. Built plugins retain the cited distillations and omit the raw captures. The Legion Code Inc. logos in `skills/code-audit-brief-stinger/references/brand/` are trademarks of Legion Code Inc. and are not licensed for use outside Legion Code Inc. material. The audit tools the Drones run (jscpd, knip, cloc, scc, osv-scanner, Semgrep, and others) are fetched at run time under their own licenses and are not bundled.

## Website Auditor

The original website auditor skills, agents, scripts, templates, and reports are AGPL-3.0-or-later. Material archived from external publishers in `shared/research/raw/` and skill `references/research/raw/` retains the publishers' own copyrights and terms. The AGPL grant applies to Wasp Nest analysis and organization, not the underlying third-party documents.

## Webapp Capture

The Webapp Capture Stinger, Drone, command, guides, and scripts are first-party Legion Code Inc. material under AGPL-3.0-or-later. They were imported from `app-auditor-plugin-claude` at commit `8528c4a` without changing the donor repository.

The Stinger's `references/research/raw/` folder preserves captures and excerpts from third-party publishers. The Wasp Nest license does not relicense those underlying documents. Built plugins retain the cited distillation and omit the raw captures.

The scripts use third-party npm dependencies. Their package names, versions, and license identifiers are recorded in `skills/webapp-capture-stinger/scripts/package-lock.json`; those dependencies remain under their own licenses. `node_modules/` is not part of this source pack or its built distribution.

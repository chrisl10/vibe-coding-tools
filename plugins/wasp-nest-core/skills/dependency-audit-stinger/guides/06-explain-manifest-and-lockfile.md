# Explain the package manifest and resolved dependencies

Help a beginner distinguish what a project asks for from the dependency tree its lockfile records.

1. Read the actual target's manifest, lockfile, package-manager declaration, relevant CI install command and toolchain configuration within authorized scope. Separate a declared packageManager/version from an observed running CLI. If files conflict or several lockfiles exist, ask which workflow governs rather than choosing npm from this skill's example.
2. Explain project name/version/private intent, scripts and engines using observed fields only. A script string does not establish that its target file exists or its check passed. A runtime range does not prove the current machine meets it. Avoid secret values in registry/config discussion.
3. Read direct runtime/development/optional/peer declarations as their actual categories. Trace one direct dependency to its concrete lockfile entry and an indirect dependency, preserving versions and parent relationship. Do not infer the full resolved graph from package.json alone or confuse dev classification with zero security risk.
4. Explain the requested declaration versus recorded resolution with one bounded analogy. A shopping plan describes what is wanted; the receipt lists the selected items and their required parts. The analogy stops at records: neither document proves installed files, vulnerability safety, integrity verification or successful execution.
5. Explain the selected ecosystem's frozen-install behavior from matching current official documentation. For an npm target, npm ci is installation, may change node_modules and has version/config-dependent script behavior. Never run it as an explanation step. A manifest/lock mismatch is a specific discrepancy; do not silently regenerate a lock, switch package managers or upgrade packages.
6. Produce a source ledger and one reader explanation with current versus declared versus unproved facts. Resolve selected Technical Explainer for its existing bounded analogy/glossary/teach-back method if needed; Core Dependency Audit owns dependency meaning and exposure. Ask the reader to distinguish a requested range from a recorded version; understanding stays pending until a response.

Grounding: update digest. No numeric grade or semantic quality score is asserted.

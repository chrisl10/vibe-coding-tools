# Pairing audit

Current membership comes from the root plugin-catalog.json and actual src/packs files. The source validator checks the same ownership and pairing rules.

## Canonical totals

- Twenty-one plugins: one required Core and twenty optional plugins.
- 223 canonical skills, 184 paired specialist agents and seventy-seven canonical commands.
- Core: eighteen skills, fourteen agents and nine commands.
- Core's unpaired skills: three orchestrators (Pest Controller, Queen and Get Started) plus standalone Time Blocks.
- The other 35 skill-only entries use explicit standalone/orchestrator classifications in their owning optional plugins.
- Seventy-seven derived command-wrapper skills (one per source command) adapt the commands for Codex; they are not additional canonical capabilities.

## Routing coverage

Pest Controller directly routes 164 Drones: fourteen in Core and 150 in optional plugins. Website Audit's own orchestrator dispatches its twenty additional Drones.
Each directly routed Drone has a real routing guide under guides/. Website leaves follow their saved-site engagement workflow.
A roster entry identifies a capability; it does not prove that the owning optional plugin is installed.

## Pairing law

Each specialist Drone names its paired Stinger. Its owner contains both canonical files. A direct-use or orchestrator skill declares its exception tier instead of claiming a nonexistent Drone.
Read the catalog to find the owner and prerequisite closure, then resolve the actual installed capability before dispatch. Core is mandatory for every selected workflow.
Source changes require a fresh run of scripts/validate.py; this note does not claim a new runtime or native-host audit merely because its counts are current.

## Change log

- 2026-10-12: seven locally forged pairs from the `chrisl-forged` plugin joined the roster under "Locally forged (chrisl-forged plugin)". The six forged base names include production-release, which carries two complete pairs. Audited with the same pairing checks: before-after-wasp-drone with before-after-stinger, code-structure-wasp-drone with code-structure-stinger, evidence-testing-wasp-drone with evidence-testing-stinger, unslop-wasp-drone with unslop-stinger, effect-wasp-drone with effect-stinger, production-release-wasp-drone with production-release-stinger, and production-release-build-wasp-drone with production-release-build-stinger. Every Drone has exactly one paired Stinger inside the same plugin, no Stinger is unpaired, and no pair is shared. Their dispatch guides ship inside the plugin under `references/pest-controller-guides/`.

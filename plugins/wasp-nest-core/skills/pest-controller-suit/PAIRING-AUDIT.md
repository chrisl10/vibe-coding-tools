# Pairing audit

Current membership comes from the root plugin-catalog.json and actual src/packs files. The source validator checks the same ownership and pairing rules.

## Canonical totals

- Sixteen plugins: one required Core and fifteen optional plugins.
- 190 canonical skills, 151 paired specialist agents and fourteen canonical commands.
- Core: eighteen skills, fourteen agents and seven commands.
- Core's unpaired skills: three orchestrators (Pest Controller, Queen and Get Started) plus standalone Time Blocks.
- The other 35 skill-only entries use explicit standalone/orchestrator classifications in their owning optional plugins.
- Fourteen derived command-wrapper skills adapt the source commands for Codex; they are not additional canonical capabilities.

## Routing coverage

Pest Controller directly routes 131 Drones: fourteen in Core and 117 in optional plugins. Website Audit's own orchestrator dispatches its twenty additional Drones.
Each directly routed Drone has a real routing guide under guides/. Website leaves follow their saved-site engagement workflow.
A roster entry identifies a capability; it does not prove that the owning optional plugin is installed.

## Pairing law

Each specialist Drone names its paired Stinger. Its owner contains both canonical files. A direct-use or orchestrator skill declares its exception tier instead of claiming a nonexistent Drone.
Read the catalog to find the owner and prerequisite closure, then resolve the actual installed capability before dispatch. Core is mandatory for every selected workflow.
Source changes require a fresh run of scripts/validate.py; this note does not claim a new runtime or native-host audit merely because its counts are current.

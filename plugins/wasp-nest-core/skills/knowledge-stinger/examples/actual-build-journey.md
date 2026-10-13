# How the source builder chooses a package

> Category: Architecture | Version: 1.0 | Date: October 2026 | Status: Draft

This source tour helps a new coder locate the Wasp Nest builder and understand how a requested plugin becomes part of its selected package list. It describes inspected source, with no claim that a native client installed or ran the result.

**Related:** [builder snapshot](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/knowledge-stinger/references/research/novice-explanation/raw/actual-build.py), [selection snapshot](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/knowledge-stinger/references/research/novice-explanation/raw/actual-plugin-topology.py), [journey ledger](../references/examples/novice-explanation/evidence/actual-build-ledger.json).

## Where the request enters

The entry point is `scripts/build.py`. Its final `if __name__` branch calls `main`, which reads output, ZIP, pack and profile arguments and passes them to `build`. These are the actual symbols inspected in this repository. [B1]

Inside `build`, the source first checks the output location, then resolves the requested plugins. Plugin-selection errors become a `SystemExit`. Before removing the output folder, the source checks the listed source directories and root files for symlinks. This tour has not exercised those branches. [B2]

## How required packages are selected

The imported `resolve_plugins` function lives in `scripts/plugin_topology.py`. It reads `plugin-catalog.json`, looks up the requested profile when present, and follows each plugin's `requires` list. It starts by visiting Core. An unknown plugin or dependency cycle raises a `ValueError`; an already-selected name is not added a second time. This explains the source's selection behavior, not runtime proof of any packaged host. [B3]

## What a command wrapper does

The source's `put_command_wrappers` function reads command frontmatter and writes a `source-command-` skill wrapper that points to the command procedure. `tri_manifests` writes the owner's Claude, Cursor and portable manifest files. The existence of these writer functions does not prove generated files passed checks or that a running client discovered them. [B4]

## Terms and a limited analogy

An entry point is where this program begins handling its command-line request. A manifest describes a package to a host. A prerequisite is another package that the selected one says it needs. Picture a packing list that includes required boxes before the requested box. The analogy ends at selection: it says nothing about a host accepting or using those boxes. [B1, B3, B4]

## Check your understanding

If a command wrapper appears in generated output, what additional evidence would you need before claiming Codex executed its Drone?

Reader response: Pending. Understanding: Pending. Native/runtime qualification: Unproven.

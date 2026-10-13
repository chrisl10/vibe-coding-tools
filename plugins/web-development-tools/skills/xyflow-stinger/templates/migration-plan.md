# xyflow migration plan: {from} to {to}

- Date: {YYYY-MM-DD}
- Source guide read on: {date} ({URL of the live migration guide})
- Branch or worktree: {name}

## Inventory

| Item | Count | Paths |
|---|---|---|
| Files importing the old package | {n} | {paths} |
| Renamed props or fields found (from the search command) | {n} | {paths} |
| Custom nodes and edges | {n} | {paths} |
| Store or state wiring sites | {n} | {paths} |

## Slices

1. {Package swap and stylesheet path; app still builds.}
2. {State model: immutable updates / runes and bindings.}
3. {Renamed APIs, per the search command in examples/05.}
4. {Custom nodes and edges: props typing, label portal, handles.}
5. {Tests updated; manual interaction pass.}

Each slice ends with a type check and a manual pass before the next begins.

## Verification evidence

| Check | Command or action | Result |
|---|---|---|
| Inspector | `python <skill>/scripts/inspect-xyflow-project.py <root> --pretty` | {status} |
| Types | {tsc --noEmit / svelte-check} | {result} |
| Tests | {command} | {result} |
| Manual | drag, connect, reconnect, delete, sub flow, save and restore | {result} |

## Rollback

{How to revert: branch, lockfile restore, feature flag.}

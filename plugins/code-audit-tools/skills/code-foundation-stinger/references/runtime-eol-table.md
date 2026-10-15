# Runtime support table (as of 2026-09-30)

Re-read the source pages before reporting if the run is later than this date. Sources: research/raw/nodejs--release-status.md, research/raw/python--version-status.md.

| Runtime | Status | Audit action |
| --- | --- | --- |
| Node 26 | Current | no finding |
| Node 24, 22 | LTS lines | no finding. The fetched summary showed September 2026 EOL dates beside these two, which contradicts the usual LTS cadence; unresolved, so the script does not flag them. Re-read the page and flag only if the page itself shows them ended |
| Node 20 | EOL 2026-03-24 per the fetch | FND-DEPS-008, medium |
| Node 18 and older | EOL | FND-DEPS-008, medium |
| Python 3.14, 3.13 | bugfix | no finding |
| Python 3.12, 3.11 | security fixes only | no finding |
| Python 3.10 | security fixes until October 2026 | the script does not flag it; mention in notes.md |
| Python 3.9 and older | EOL (3.9 on 2025-10-31) | FND-DEPS-008, medium |

`requires-python` and `engines.node` are floors, not pins. The script never treats a floor as EOL. Only `.nvmrc`, `.node-version`, a `FROM node:<major>` line and `.python-version` are tested.

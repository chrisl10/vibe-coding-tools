#!/usr/bin/env python3
"""xlsx-populate.py - not implemented.

Planned in the original build plan as a shared helper for audit-scoring-stinger, but never
built. Nothing in this pack calls it. It exits with status 2 and tells the
Drone what to do instead, so a run never mistakes it for a working step.

Instead: Copy skills/audit-scoring-stinger/references/templates/website-audit-scorecard-template.xlsx to scoring/audit-scorecard.xlsx and transcribe each validated leaf into the Scorecard sheet by hand (audit-scoring-stinger SKILL.md procedure steps 1 and 4). Use shared/scripts/score-rollup.py to cross-check the recalculated rollups.
"""

import sys

MESSAGE = (
    "xlsx-populate.py is not implemented. "
    'Copy skills/audit-scoring-stinger/references/templates/website-audit-scorecard-template.xlsx to scoring/audit-scorecard.xlsx and transcribe each validated leaf into the Scorecard sheet by hand (audit-scoring-stinger SKILL.md procedure steps 1 and 4). Use shared/scripts/score-rollup.py to cross-check the recalculated rollups.'
)

if __name__ == "__main__":
    print(MESSAGE, file=sys.stderr)
    sys.exit(2)

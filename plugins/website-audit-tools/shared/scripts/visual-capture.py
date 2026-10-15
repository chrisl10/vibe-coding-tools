#!/usr/bin/env python3
"""visual-capture.py - not implemented.

Planned in the original build plan as a shared helper for visual-funnel-stinger, but never
built. Nothing in this pack calls it. It exits with status 2 and tells the
Drone what to do instead, so a run never mistakes it for a working step.

Instead: Capture the desktop and mobile checkpoint screenshots with the harness's own browser tool, configured from skills/visual-funnel-stinger/references/scripts/playwright-viewport-config.js, as skills/visual-funnel-stinger/guides/03-capture-checkpoint-screenshots.md describes.
"""

import sys

MESSAGE = (
    "visual-capture.py is not implemented. "
    "Capture the desktop and mobile checkpoint screenshots with the harness's own browser tool, configured from skills/visual-funnel-stinger/references/scripts/playwright-viewport-config.js, as skills/visual-funnel-stinger/guides/03-capture-checkpoint-screenshots.md describes."
)

if __name__ == "__main__":
    print(MESSAGE, file=sys.stderr)
    sys.exit(2)

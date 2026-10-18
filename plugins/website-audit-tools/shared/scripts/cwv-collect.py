#!/usr/bin/env python3
"""cwv-collect.py - not implemented.

Planned in the original build plan as a shared helper for performance-cwv-stinger, but never
built. Nothing in this pack calls it. It exits with status 2 and tells the
Drone what to do instead, so a run never mistakes it for a working step.

Instead: Collect Core Web Vitals yourself as skills/performance-cwv-stinger/guides/01-audit-procedure.md step 3 describes: PageSpeed Insights/CrUX field data where coverage exists, and a lab run only with a tool already available and authorized in this session. Record each response or report path as evidence.
"""

import sys

MESSAGE = (
    "cwv-collect.py is not implemented. "
    'Collect Core Web Vitals yourself as skills/performance-cwv-stinger/guides/01-audit-procedure.md step 3 describes: PageSpeed Insights/CrUX field data where coverage exists, and a lab run only with a tool already available and authorized in this session. Record each response or report path as evidence.'
)

if __name__ == "__main__":
    print(MESSAGE, file=sys.stderr)
    sys.exit(2)

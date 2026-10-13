#!/usr/bin/env python3
"""Structural check for a Product Strategy written from this skill's template.

Usage:
    python3 check-strategy.py path/to/product-strategy.md [--json]

Checks shape only: the eight sections exist, 2 to 4 bets, exactly 3 inputs,
a NOT-in-v1 list, a named riskiest assumption, a pricing hypothesis, no
unfilled template placeholders, and no em or en dashes. It does not judge
whether the strategy is good; the owner decides that.

Stdlib only. Reads one file. Writes nothing. Exit code 0 when clean, 1 when
any error is found, 2 on usage problems.
"""

import json
import re
import sys
from pathlib import Path

SECTIONS = [
    (1, "the problem"),
    (2, "who it is for"),
    (3, "the job to be done"),
    (4, "positioning"),
    (5, "big bets"),
    (6, "how we will know"),
    (7, "version 1"),
    (8, "risks"),
]
EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)


def section_bodies(text):
    """Map section number to its body text, using '## N.' headings."""
    heads = list(re.finditer(r"^##\s+(\d)\.\s+(.+)$", text, re.M))
    bodies = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        nxt = re.search(r"^##\s+(?!\d\.)", text[m.end():end], re.M)
        stop = m.end() + nxt.start() if nxt else end
        bodies[int(m.group(1))] = (m.group(2).strip().lower(), text[m.end():stop])
    return bodies


def count_rows(body, prefix):
    return len(re.findall(r"^\|\s*" + prefix + r"\d+\b", body, re.M))


def check(text):
    errors, warnings = [], []
    bodies = section_bodies(text)

    for num, words in SECTIONS:
        if num not in bodies:
            errors.append("missing section '## %d.' (%s)" % (num, words))
        elif words not in bodies[num][0]:
            warnings.append("section %d heading does not mention '%s'" % (num, words))

    if 5 in bodies:
        bets = count_rows(bodies[5][1], "B")
        if not 2 <= bets <= 4:
            errors.append("section 5 has %d bet rows (B1, B2...); need 2 to 4" % bets)

    if 6 in bodies:
        body6 = bodies[6][1]
        inputs = count_rows(body6, "I")
        if inputs != 3:
            errors.append("section 6 has %d input rows (I1, I2...); need exactly 3" % inputs)
        if not re.search(r"north-star metric:", body6, re.I):
            errors.append("section 6 has no 'North-star metric:' line")

    if 7 in bodies:
        body7 = bodies[7][1]
        m = re.search(r"NOT in v1:\*{0,2}(.*?)(?:\n- \*\*|\Z)", body7, re.S)
        if not m or not m.group(1).strip():
            errors.append("section 7 has no filled 'NOT in v1' list")

    if 8 in bodies:
        if not re.search(r"riskiest assumption:\*{0,2}\s*\S", bodies[8][1], re.I):
            errors.append("section 8 does not name the riskiest assumption")

    if not re.search(r"^##\s+Pricing hypothesis", text, re.M | re.I):
        errors.append("no '## Pricing hypothesis' section")

    for lineno, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line or EN_DASH in line:
            errors.append("line %d contains an em or en dash" % lineno)
        if re.search(r"\{[a-zA-Z#][^}]*\}", line) and not line.lstrip().startswith("<!--"):
            errors.append("line %d has an unfilled {placeholder}; fill it or write OPEN: and the question" % lineno)

    opens = len(re.findall(r"\bOPEN:", text))
    return errors, warnings, opens


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    if len(args) != 1:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    path = Path(args[0])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print("cannot read %s: %s" % (path, exc))
        return 2
    errors, warnings, opens = check(text)
    if as_json:
        print(json.dumps({"file": str(path), "errors": errors, "warnings": warnings, "open_items": opens}, indent=2))
    else:
        for e in errors:
            print("ERROR: " + e)
        for w in warnings:
            print("WARN:  " + w)
        print("%d error(s), %d warning(s), %d OPEN item(s)" % (len(errors), len(warnings), opens))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

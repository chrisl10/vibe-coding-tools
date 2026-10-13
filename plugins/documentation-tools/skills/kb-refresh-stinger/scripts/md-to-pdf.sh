#!/bin/bash
# md-to-pdf.sh <input.html> <output.pdf>
# Renders a print-styled HTML report to PDF with headless Chrome.
# No dependencies to install: uses the Chrome already on the machine.
set -euo pipefail

IN="${1:?usage: md-to-pdf.sh <input.html> <output.pdf>}"
OUT="${2:?usage: md-to-pdf.sh <input.html> <output.pdf>}"

if [ ! -f "$IN" ]; then
  echo "ERROR: input not found: $IN" >&2
  exit 2
fi

CHROME=""
for C in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
  if [ -x "$C" ]; then CHROME="$C"; break; fi
done

if [ -z "$CHROME" ]; then
  echo "ERROR: no Chrome-family browser found. Install Google Chrome or render report.html manually." >&2
  exit 2
fi

mkdir -p "$(dirname "$OUT")"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")" \
  "file://$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")" 2>/dev/null

if [ -s "$OUT" ]; then
  echo "PDF OK: $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"
  exit 0
fi

echo "ERROR: Chrome produced no output at $OUT. The markdown report stands alone." >&2
exit 1

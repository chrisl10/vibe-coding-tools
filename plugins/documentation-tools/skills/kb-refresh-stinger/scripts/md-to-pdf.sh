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

# Browser discovery order: $CHROME_PATH, Chrome-family binaries on PATH,
# macOS /Applications, then Program Files when running in Git Bash/MSYS/Cygwin.
CHROME=""
if [ -n "${CHROME_PATH:-}" ]; then
  if [ -x "$CHROME_PATH" ]; then
    CHROME="$CHROME_PATH"
  else
    echo "WARN: CHROME_PATH is set but not executable: $CHROME_PATH" >&2
  fi
fi

if [ -z "$CHROME" ]; then
  for NAME in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge msedge; do
    if FOUND="$(command -v "$NAME" 2>/dev/null)" && [ -n "$FOUND" ]; then CHROME="$FOUND"; break; fi
  done
fi

if [ -z "$CHROME" ]; then
  for C in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    if [ -x "$C" ]; then CHROME="$C"; break; fi
  done
fi

IS_WINDOWS_SHELL=0
case "$(uname -s 2>/dev/null || true)" in
  MINGW*|MSYS*|CYGWIN*) IS_WINDOWS_SHELL=1 ;;
esac

if [ -z "$CHROME" ] && [ "$IS_WINDOWS_SHELL" = 1 ]; then
  WIN_CANDIDATES=(
    "/c/Program Files/Google/Chrome/Application/chrome.exe"
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    "/c/Program Files/Microsoft/Edge/Application/msedge.exe"
  )
  if [ -n "${LOCALAPPDATA:-}" ] && command -v cygpath >/dev/null 2>&1; then
    WIN_CANDIDATES+=("$(cygpath -u "$LOCALAPPDATA")/Google/Chrome/Application/chrome.exe")
  fi
  for C in "${WIN_CANDIDATES[@]}"; do
    if [ -x "$C" ]; then CHROME="$C"; break; fi
  done
fi

if [ -z "$CHROME" ]; then
  echo "ERROR: no Chrome-family browser found. Install Google Chrome, set CHROME_PATH, or render report.html manually." >&2
  exit 2
fi

mkdir -p "$(dirname "$OUT")"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
IN_ABS="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
if [ "$IS_WINDOWS_SHELL" = 1 ] && command -v cygpath >/dev/null 2>&1; then
  # A Windows browser needs Windows-style paths (C:/...), not /c/... shell paths.
  OUT_ABS="$(cygpath -m "$OUT_ABS")"
  IN_ABS="$(cygpath -m "$IN_ABS")"
  IN_URL="file:///$IN_ABS"
else
  IN_URL="file://$IN_ABS"
fi
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT_ABS" \
  "$IN_URL" 2>/dev/null || true

if [ -s "$OUT" ]; then
  echo "PDF OK: $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"
  exit 0
fi

echo "ERROR: Chrome produced no output at $OUT. The markdown report stands alone." >&2
exit 1

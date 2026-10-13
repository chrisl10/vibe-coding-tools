#!/usr/bin/env bash
# TARS CI poller. Run under the Monitor tool: every stdout line is an event.
# Every INTERVAL seconds (default 60) it re-reads the watch file, checks each
# entry, and prints a line ONLY when an entry's state changes. It touches a
# heartbeat file every loop so the 10-minute watchdog can tell it is alive.
#
# Usage: bash ci-poll.sh <state-dir>
#   <state-dir>/watch.txt   one entry per line, re-read every loop:
#                           pr <number> <owner/repo> [required-check]
#                           branch <name> <owner/repo>
#                           lines starting with # are ignored
#   <state-dir>/heartbeat   touched every loop (written by this script)
# Env: INTERVAL (seconds, default 60, minimum 30 to spare the GitHub API rate limit)
#      REQUIRED_CHECK (default required PR check; a 4th field on a pr line overrides it)
#      IGNORE_CHECKS (extended regex of check names to ignore, e.g. 'argos|Walkthrough')
#
# PR states:  NOT_STARTED (zero checks reported: never green), PENDING,
#             GREEN (required check passed, or all checks passed, and zero
#             non-ignored checks pending or failing), RED <failing names>,
#             MERGED, CLOSED, UNKNOWN (gh error, retried next loop)
#             MERGED and CLOSED are terminal: the PR is not polled again.
# Branch:     one line per workflow run whose status or conclusion changed
#             (last 5 runs), e.g. "RUN main Deploy App Plane 12345 completed failure".
# Check and workflow names are untrusted text: they are cut to 80 characters
# of [A-Za-z0-9 ._:/()+-] so a name can never forge an extra event line.
set -u
dir="${1:?usage: ci-poll.sh <state-dir>}"
interval="${INTERVAL:-60}"
case "$interval" in ''|*[!0-9]*) interval=60;; esac
[ "$interval" -lt 30 ] && interval=30
required="${REQUIRED_CHECK:-}"
ignore="${IGNORE_CHECKS:-^$}"
jq -n --arg r "$ignore" '"" | test($r)' >/dev/null 2>&1 \
  || { echo "ERROR IGNORE_CHECKS is not a valid regex; poller stopped"; exit 2; }
mkdir -p "$dir/.state"

pr_state() { # $1 number, $2 repo, $3 required check (may be empty)
  local st checks req="$3"
  st=$(gh pr view "$1" -R "$2" --json state -q .state 2>/dev/null) || { echo UNKNOWN; return; }
  case "$st" in MERGED|CLOSED) echo "$st"; return;; esac
  checks=$(gh pr checks "$1" -R "$2" --json name,bucket 2>/dev/null)
  # gh exits non-zero when checks fail or are pending; only an empty body is an error.
  [ -z "$checks" ] && { echo NOT_STARTED; return; }
  jq -r --arg req "$req" --arg ign "$ignore" '
    [ .[] | select((.name | test($ign)) | not) ] as $c
    | ($c | map(select(.bucket=="fail" or .bucket=="cancel"))
        | map(.name | gsub("[^A-Za-z0-9 ._:/()+-]"; "_") | .[0:80])) as $bad
    | ($c | map(select(.bucket=="pending")) | length) as $pend
    | if ($c | length) == 0 then "NOT_STARTED"
      elif ($bad | length) > 0 then "RED " + ($bad | join(","))
      elif $pend > 0 then "PENDING"
      elif $req != "" and ([ $c[] | select(.name==$req and .bucket=="pass") ] | length) == 0 then "PENDING"
      else "GREEN" end' <<<"$checks" 2>/dev/null || echo UNKNOWN
}

emit_if_changed() { # $1 key, $2 value, $3 line to print
  local f="$dir/.state/$1" old=""
  [ -f "$f" ] && old=$(cat "$f")
  if [ "$old" != "$2" ]; then printf '%s\n' "$2" > "$f"; printf '%s\n' "$3"; fi
}

while true; do
  touch "$dir/heartbeat"
  ts=$(date -u +%H:%MZ)
  if [ -f "$dir/watch.txt" ]; then
    while read -r kind ref repo req _; do
      case "$kind" in
        pr)
          case "$ref" in ''|*[!0-9]*) continue;; esac
          [[ "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || continue
          case "/$repo/" in */./*|*/../*) continue;; esac
          key="pr-${repo//\//_}-$ref"
          case "$(cat "$dir/.state/$key" 2>/dev/null)" in MERGED|CLOSED) continue;; esac
          s=$(pr_state "$ref" "$repo" "${req:-$required}")
          [ "$s" = UNKNOWN ] && continue
          emit_if_changed "$key" "$s" "$ts PR $repo#$ref $s" ;;
        branch)
          [[ "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || continue
          case "/$repo/" in */./*|*/../*) continue;; esac
          case "$ref" in ''|-*|*[[:cntrl:]]*) continue;; esac
          runs=$(gh run list -R "$repo" --branch "$ref" -L 5 \
            --json databaseId,workflowName,status,conclusion 2>/dev/null) || continue
          while IFS=$'\t' read -r id wf status concl; do
            [ -z "$id" ] && continue
            # First sight of an already-finished successful run is baseline, not news.
            # A first-sight failure is still reported: a deploy that failed before the
            # branch was watched must not be lost until the next watchdog tick.
            if [ ! -f "$dir/.state/run-$id" ] && [ "$status" = completed ] \
               && [ "$concl" = success -o "$concl" = skipped -o "$concl" = neutral ]; then
              printf '%s\n' "$status/$concl" > "$dir/.state/run-$id"; continue
            fi
            emit_if_changed "run-$id" "$status/$concl" "$ts RUN $ref $wf $id $status ${concl:-running}"
          done < <(jq -r '.[] | [.databaseId,
            (.workflowName | gsub("[^A-Za-z0-9 ._:/()+-]"; "_") | .[0:80]),
            .status, .conclusion] | @tsv' <<<"$runs")
          ;;
        ''|\#*) ;;
      esac
    done < "$dir/watch.txt"
  fi
  sleep "$interval"
done

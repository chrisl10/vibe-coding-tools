#!/usr/bin/env python3
"""t3ctl: thin CLI over the T3 Code local orchestration API (0.0.x).

Research base: tools/t3-api-map.md in this repo (PROVEN against t3 0.0.45).
Every command is a direct mapping of one documented dispatch envelope or
GET; no undocumented behavior is invented. Failure output is the server's
own error JSON, quoted verbatim.

Setup (once per environment):
  t3 auth session issue --ttl 30d --label t3ctl --token-only \
      > ~/.t3/t3ctl/desk.token        # on a machine with the t3 CLI

Usage:
  t3ctl snapshot [--json]
  t3ctl thread <threadId> [--turns N] [--reasoning]
  t3ctl create --project <idOrTitle> --title "..." [--model instance:model]
               [--mode full-access] [--branch b] [--worktree path] [--json]
  t3ctl prompt  <threadId> "message text"
  t3ctl append  <threadId> "message text"
  t3ctl interrupt <threadId> [--turn <turnId>]
  t3ctl stop    <threadId>
  t3ctl archive <threadId> --yes
  t3ctl respond <threadId> <requestId> <decision>
  t3ctl pr-link <threadId> <pr-url>
  t3ctl raw '<envelope json>'          # escape hatch, posts to dispatch
  t3ctl auth-redeem <pairing-token>    # exchange a pairing token for a bearer

Environment selection: --env desk (default) or --url http://host:port.
Tokens: $T3CTL_TOKEN, else ~/.t3/t3ctl/<env>.token.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

ENVS = {
    "desk": "http://127.0.0.1:3773",
    "macdev": "http://127.0.0.1:38373",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + \
        f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"


def base_url(args) -> str:
    if args.url:
        return args.url.rstrip("/")
    return ENVS[args.env].rstrip("/")


def token(args) -> str:
    tok = os.environ.get("T3CTL_TOKEN")
    if tok:
        return tok.strip()
    path = Path.home() / ".t3/t3ctl" / f"{args.env}.token"
    if path.is_file():
        return path.read_text().strip()
    sys.exit(f"no token: set T3CTL_TOKEN or write {path} "
             f"(mint: t3 auth session issue --ttl 30d --label t3ctl --token-only)")


def call(args, method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        base_url(args) + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={
            "Authorization": "Bearer " + token(args),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")[:600]
        sys.exit(f"HTTP {e.code} {method} {path}\n{err_body}")
    except urllib.error.URLError as e:
        sys.exit(f"connection failed {method} {path}: {e.reason}")


def dispatch(args, envelope: dict) -> dict:
    env = {"commandId": str(uuid.uuid4()), "createdAt": now_iso()}
    env.update(envelope)
    return call(args, "POST", "/api/orchestration/dispatch", env)


def get_snapshot(args) -> dict:
    return call(args, "GET", "/api/orchestration/snapshot")


def resolve_project(args, ref: str) -> str:
    snap = get_snapshot(args)
    for p in snap.get("projects", []):
        if p["id"] == ref or p.get("title") == ref:
            return p["id"]
    titled = [p for p in snap.get("projects", []) if ref.lower() in p.get("title", "").lower()]
    if len(titled) == 1:
        return titled[0]["id"]
    sys.exit(f"project not found or ambiguous: {ref} "
             f"(projects: {', '.join(p['title'] for p in snap.get('projects', []))})")


def print_snapshot(snap: dict) -> None:
    projects = {p["id"]: p.get("title", p["id"][:8]) for p in snap.get("projects", []) if not p.get("deletedAt")}
    print(f"sequence {snap.get('snapshotSequence')} updated {snap.get('updatedAt')}")
    for pid, title in projects.items():
        print(f"project {title} ({pid[:8]})")
    print(f"{'thread':10} {'state':10} {'model':16} {'turn':10} title")
    for t in snap.get("threads", []):
        if t.get("archivedAt") or t.get("deletedAt"):
            continue
        session = t.get("session") or {}
        turn = (t.get("latestTurn") or {}).get("state", "-")
        model = (t.get("modelSelection") or {}).get("instanceId", "-")
        prs = len(t.get("pullRequests") or [])
        prtag = f" pr:{prs}" if prs else ""
        print(f"{t['id'][:8]:10} {session.get('status', '-'):10} {model:16} "
              f"{turn:10} {(t.get('title') or '')[:52]}{prtag}")


def cmd_snapshot(args) -> None:
    snap = get_snapshot(args)
    if args.json:
        print(json.dumps(snap, indent=2))
    else:
        print_snapshot(snap)


def cmd_thread(args) -> None:
    query = f"?turnLimit={args.turns}"
    if args.reasoning:
        query += "&reasoningMessages=true"
    d = call(args, "GET", f"/api/orchestration/threads/{args.threadId}{query}")
    if args.json:
        print(json.dumps(d, indent=2))
        return
    t = d.get("thread", d)
    session = t.get("session") or {}
    print(f"title:   {t.get('title')}")
    print(f"project: {t.get('projectId', '')[:8]}  model: "
          f"{(t.get('modelSelection') or {}).get('instanceId')} "
          f"session: {session.get('status')} provider: {session.get('providerName')}")
    for m in (t.get("messages") or [])[-args.turns:]:
        role = m.get("role", "?")
        text = (m.get("text") or "").replace("\n", " ")[:160]
        print(f"  [{role}] {text}")


def cmd_create(args) -> None:
    selection = {"instanceId": "codex_belay", "model": "auto"}
    if args.model:
        instance, _, model = args.model.partition(":")
        selection = {"instanceId": instance, "model": model or "auto"}
    envelope = {
        "type": "thread.create",
        "threadId": str(uuid.uuid4()),
        "projectId": resolve_project(args, args.project),
        "title": args.title,
        "modelSelection": selection,
        "runtimeMode": args.mode,
        "interactionMode": "default",
        "branch": args.branch,
        "worktreePath": args.worktree,
    }
    out = dispatch(args, envelope)
    print(json.dumps(out, indent=2))


def cmd_prompt(args) -> None:
    out = dispatch(args, {
        "type": "thread.turn.start",
        "threadId": args.threadId,
        "message": {
            "messageId": str(uuid.uuid4()),
            "role": "user",
            "text": args.text,
            "attachments": [],
        },
        "runtimeMode": args.mode,
        "interactionMode": "default",
    })
    print(json.dumps(out, indent=2))


def cmd_append(args) -> None:
    out = dispatch(args, {
        "type": "thread.message.user.append",
        "threadId": args.threadId,
        "message": {"messageId": str(uuid.uuid4()), "text": args.text, "attachments": []},
    })
    print(json.dumps(out, indent=2))


def cmd_interrupt(args) -> None:
    envelope = {"type": "thread.turn.interrupt", "threadId": args.threadId}
    if args.turn:
        envelope["turnId"] = args.turn
    print(json.dumps(dispatch(args, envelope), indent=2))


def cmd_stop(args) -> None:
    print(json.dumps(dispatch(args, {"type": "thread.session.stop", "threadId": args.threadId}), indent=2))


def cmd_archive(args) -> None:
    if not args.yes:
        sys.exit("archive is destructive to the active list; pass --yes")
    print(json.dumps(dispatch(args, {"type": "thread.archive", "threadId": args.threadId}), indent=2))


def cmd_respond(args) -> None:
    print(json.dumps(dispatch(args, {
        "type": "thread.approval.respond",
        "threadId": args.threadId,
        "requestId": args.requestId,
        "decision": args.decision,
    }), indent=2))


def cmd_pr_link(args) -> None:
    print(json.dumps(dispatch(args, {
        "type": "thread.pull-request.link",
        "threadId": args.threadId,
        "url": args.url,
        "source": "t3ctl",
    }), indent=2))


def cmd_status(args) -> None:
    snap = get_snapshot(args)
    for t in snap.get("threads", []):
        if t["id"] == args.threadId or t["id"].startswith(args.threadId):
            print((t.get("session") or {}).get("status", "unknown"))
            return
    print("gone")


def cmd_raw(args) -> None:
    print(json.dumps(dispatch(args, json.loads(args.envelope)), indent=2))


def cmd_auth_redeem(args) -> None:
    out = call(args, "POST", "/api/auth/pairing-token", {"token": args.pairing_token})
    print(json.dumps(out, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="thin T3 orchestration CLI")
    parser.add_argument("--env", default="desk", choices=sorted(ENVS), help="named environment")
    parser.add_argument("--url", help="explicit base URL override")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("snapshot"); p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_snapshot)

    p = sub.add_parser("thread"); p.add_argument("threadId")
    p.add_argument("--turns", type=int, default=5); p.add_argument("--reasoning", action="store_true")
    p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_thread)

    p = sub.add_parser("create")
    p.add_argument("--project", required=True); p.add_argument("--title", required=True)
    p.add_argument("--model"); p.add_argument("--mode", default="full-access")
    p.add_argument("--branch"); p.add_argument("--worktree"); p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_create)

    p = sub.add_parser("prompt"); p.add_argument("threadId"); p.add_argument("text")
    p.add_argument("--mode", default="full-access"); p.set_defaults(fn=cmd_prompt)

    p = sub.add_parser("append"); p.add_argument("threadId"); p.add_argument("text"); p.set_defaults(fn=cmd_append)

    p = sub.add_parser("interrupt"); p.add_argument("threadId"); p.add_argument("--turn"); p.set_defaults(fn=cmd_interrupt)

    p = sub.add_parser("stop"); p.add_argument("threadId"); p.set_defaults(fn=cmd_stop)

    p = sub.add_parser("status"); p.add_argument("threadId"); p.set_defaults(fn=cmd_status)

    p = sub.add_parser("archive"); p.add_argument("threadId"); p.add_argument("--yes", action="store_true"); p.set_defaults(fn=cmd_archive)

    p = sub.add_parser("respond"); p.add_argument("threadId"); p.add_argument("requestId"); p.add_argument("decision"); p.set_defaults(fn=cmd_respond)

    p = sub.add_parser("pr-link"); p.add_argument("threadId"); p.add_argument("url"); p.set_defaults(fn=cmd_pr_link)

    p = sub.add_parser("raw"); p.add_argument("envelope"); p.set_defaults(fn=cmd_raw)

    p = sub.add_parser("auth-redeem"); p.add_argument("pairing_token"); p.set_defaults(fn=cmd_auth_redeem)

    args = parser.parse_args()
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

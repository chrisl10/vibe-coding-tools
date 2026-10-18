#!/usr/bin/env python3
"""t3ctl v2: thin CLI over the T3 Code (Beta 0.1.x) MCP server.

Research base: tools/t3-api-map.md in this repo (V2 section, PROVEN against
t3 0.1.0). Every command maps to one MCP tool call; no undocumented behavior
is invented. Failure output is the server's own error JSON, quoted verbatim.

V2 has no orchestration snapshot/dispatch REST surface for outside clients;
control rides the MCP endpoint at <environment>/mcp. Credentials are OAuth
access tokens obtained through a fully headless flow: dynamic client
registration, PKCE, and approval by a one-time pairing code minted on the
environment's host with `t3 auth pairing create`. Tokens last 30 days and
the flow re-runs automatically on expiry, so no browser is ever needed.

Setup: none for the desk environment. The first command acquires and stores
a credential at ~/.t3/t3ctl/<env>.mcp.json. For a remote environment whose
host is reachable over ssh, point T3CTL_PAIRING_CMD at a command that prints
the `t3 auth pairing create --json` output, for example:

  T3CTL_PAIRING_CMD='ssh macdev ~/.t3/bin/t3 auth pairing create --json \
      --ttl 5m --label t3ctl' t3ctl --env macdev auth

Usage:
  t3ctl auth                          show or acquire the MCP credential
  t3ctl snapshot [--json]             projects plus newest threads per project
  t3ctl thread <threadId> [--limit N] [--json]
  t3ctl status <threadId>             one word: running | idle | gone | ...
  t3ctl create --project <idOrTitle> --title "..." [--model instance:model]
               [--mode full-access] [--message "..."] [--json]
  t3ctl prompt  <threadId> "text"     send (auto mode: steers or queues)
  t3ctl append  <threadId> "text"     send in queue-only mode
  t3ctl wait    <threadId> [--timeout-secs N] [--run <runId>]
  t3ctl interrupt <threadId> [--reason "..."]
  t3ctl stop    <threadId>            interrupt with stop semantics
  t3ctl archive <threadId> --yes
  t3ctl search  <query> [--limit N]
  t3ctl queue   <threadId>
  t3ctl requests <threadId>           pending user questions
  t3ctl respond <threadId> <requestId> <answer-text>
  t3ctl pr-link <threadId> <pr-url>
  t3ctl tasks    [--project <idOrTitle>]
  t3ctl task-create --prompt "..." --every-mins N [--title "..."]
                    [--project <idOrTitle>] [--bind <threadId>]
  t3ctl task-run <taskId>
  t3ctl task-delete <taskId> --yes
  t3ctl raw <toolName> '<json-args>'  MCP tools/call escape hatch

Environment selection: --env desk (default) or --url http://host:port.
Credential: $T3CTL_MCP_TOKEN, else ~/.t3/t3ctl/<env>.mcp.json.
Pairing source for acquisition: $T3CTL_PAIRING_CMD, else the local t3 CLI.
Access mode granted: $T3CTL_MCP_ACCESS (default full-access, loopback only).
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ENVS = {
    "desk": "http://127.0.0.1:3773",
    "macdev": "http://127.0.0.1:38373",
}

CRED_DIR = os.path.expanduser("~/.t3/t3ctl")
REDIRECT_URI = "http://127.0.0.1:48191/cb"
CLIENT_NAME = "t3ctl"
PROTOCOL_VERSION = "2025-03-26"


class Fail(Exception):
    pass


def base_url(args) -> str:
    if args.url:
        return args.url.rstrip("/")
    return ENVS[args.env].rstrip("/")


def cred_path(args) -> str:
    return os.path.join(CRED_DIR, f"{args.env}.mcp.json")


# ---------------------------------------------------------------- HTTP layer

def http_json(url: str, method: str = "GET", payload=None, form=False,
              token: str | None = None, timeout: int = 30):
    headers = {"Accept": "application/json"}
    body = None
    if payload is not None:
        if form:
            body = urllib.parse.urlencode(payload).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(payload).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            raw = res.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        raise Fail(f"HTTP {e.code} {method} {url}\n{detail}") from None


# ------------------------------------------------------- credential handling

def mint_pairing_code() -> dict:
    cmd = os.environ.get("T3CTL_PAIRING_CMD")
    if not cmd:
        t3 = shutil.which("t3") or os.path.expanduser("~/.t3/bin/t3")
        if not os.path.exists(t3):
            raise Fail("no t3 CLI found; set T3CTL_PAIRING_CMD for remote environments")
        cmd = f"{t3} auth pairing create --json --ttl 5m --label t3ctl"
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    text = out.stdout + out.stderr
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                data = json.loads(line)
                if "credential" in data:
                    return data
            except json.JSONDecodeError:
                continue
    try:  # whole-output JSON fallback
        return json.loads(text)
    except json.JSONDecodeError:
        raise Fail(f"pairing command produced no JSON credential: {text[:200]}") from None


def acquire_token(base: str) -> dict:
    """Full headless OAuth flow against one environment."""
    reg = http_json(base + "/oauth/mcp/register", "POST", {
        "client_name": CLIENT_NAME,
        "redirect_uris": [REDIRECT_URI],
        "token_endpoint_auth_method": "none",
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
    })
    client_id = reg.get("client_id")
    if not client_id:
        raise Fail("registration returned no client_id: " + json.dumps(reg)[:200])

    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(12)
    authorization = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
        "resource": base + "/mcp",
    }

    pairing = mint_pairing_code()
    access_mode = os.environ.get("T3CTL_MCP_ACCESS", "full-access")
    decision = http_json(base + "/oauth/mcp/decision", "POST", {
        "authorization": authorization,
        "decision": {"_tag": "pairing-code", "access": access_mode,
                     "code": pairing["credential"]},
    })
    redirect_to = decision.get("redirectTo", "") if isinstance(decision, dict) else ""
    query = urllib.parse.parse_qs(urllib.parse.urlparse(redirect_to).query)
    auth_code = query.get("code", [None])[0]
    if not auth_code:
        raise Fail("decision returned no authorization code: " + json.dumps(decision)[:200])

    tok = http_json(base + "/oauth/mcp/token", "POST", {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "code_verifier": verifier,
        "resource": base + "/mcp",
    }, form=True)
    if not tok.get("access_token"):
        raise Fail("token endpoint returned no access_token: " + json.dumps(tok)[:200])
    return {
        "base_url": base,
        "client_id": client_id,
        "access_token": tok["access_token"],
        "expires_in": tok.get("expires_in"),
        "scope": tok.get("scope"),
        "obtained_at": int(time.time()),
    }


def load_cred(args, allow_acquire=True) -> str:
    env_tok = os.environ.get("T3CTL_MCP_TOKEN")
    if env_tok:
        return env_tok.strip()
    path = cred_path(args)
    if os.path.isfile(path):
        cred = json.load(open(path))
        if cred.get("base_url") == base_url(args):
            return cred["access_token"]
    if not allow_acquire:
        raise Fail(f"no credential at {path} and acquisition disabled")
    cred = acquire_token(base_url(args))
    os.makedirs(CRED_DIR, exist_ok=True)
    with open(path, "w") as fh:
        json.dump(cred, fh, indent=1)
    os.chmod(path, 0o600)
    return cred["access_token"]


# --------------------------------------------------------------- MCP client

class Mcp:
    def __init__(self, args):
        self.base = base_url(args)
        self.args = args
        self.token = load_cred(args)
        self.session = None
        self._id = 0
        self._expired_retried = False

    def _post(self, payload):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session:
            headers["mcp-session-id"] = self.session
        req = urllib.request.Request(self.base + "/mcp",
                                     data=json.dumps(payload).encode(),
                                     method="POST", headers=headers)
        with urllib.request.urlopen(req, timeout=120) as res:
            sid = res.headers.get("mcp-session-id")
            if sid:
                self.session = sid
            raw = res.read().decode("utf-8", "replace")
        if raw.startswith(("event:", "data:")):
            data = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]
            return json.loads(data[-1]) if data else None
        return json.loads(raw) if raw.strip() else None

    def rpc(self, method, params=None, notification=False):
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        if not notification:
            self._id += 1
            payload["id"] = self._id
        try:
            return self._post(payload)
        except urllib.error.HTTPError as e:
            if e.code == 401 and not self._expired_retried:
                self._expired_retried = True
                cred = acquire_token(self.base)
                self.token = cred["access_token"]
                with open(cred_path(self.args), "w") as fh:
                    json.dump(cred, fh, indent=1)
                os.chmod(cred_path(self.args), 0o600)
                return self._post(payload)
            detail = e.read().decode(errors="replace")[:400]
            raise Fail(f"HTTP {e.code} {method} /mcp\n{detail}") from None

    def start(self):
        self.rpc("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": CLIENT_NAME, "version": "2.0"},
        })
        self.rpc("notifications/initialized", notification=True)
        return self

    def tool(self, name, arguments):
        reply = self.rpc("tools/call", {"name": name, "arguments": arguments})
        if not reply or "result" not in reply:
            if reply and "error" in reply:
                raise Fail(f"{name}: {json.dumps(reply['error'])[:400]}")
            raise Fail(f"{name}: no result: " + json.dumps(reply)[:300])
        result = reply["result"]
        text = "".join(b.get("text", "") for b in result.get("content", [])
                       if b.get("type") == "text")
        if result.get("isError"):
            raise Fail(f"{name}: {text[:400]}")
        try:
            return json.loads(text) if text else result.get("structuredContent")
        except json.JSONDecodeError:
            return text


# ------------------------------------------------------------------ helpers

def projects(mcp: Mcp) -> list:
    page = mcp.tool("t3_project_list", {"limit": 50})
    return page.get("projects", []) if isinstance(page, dict) else []


def resolve_project(mcp: Mcp, ref: str) -> str:
    for p in projects(mcp):
        if p["id"] == ref or p.get("title") == ref:
            return p["id"]
    fuzzy = [p for p in projects(mcp) if ref.lower() in p.get("title", "").lower()]
    if len(fuzzy) == 1:
        return fuzzy[0]["id"]
    raise Fail(f"project not found or ambiguous: {ref}")


def all_threads(mcp: Mcp) -> list:
    out = []
    for p in projects(mcp):
        page = mcp.tool("t3_thread_list", {"projectId": p["id"], "limit": 50})
        for t in page.get("threads", []):
            t["_projectTitle"] = p.get("title", p["id"][:8])
            out.append(t)
    return out


def read_thread(mcp: Mcp, thread_id: str) -> dict:
    return mcp.tool("t3_thread_read", {"threadId": thread_id, "limit": 1})


def one_word_status(payload) -> str:
    thread = payload.get("thread", {}) if isinstance(payload, dict) else {}
    if not thread:
        return "gone"
    if thread.get("activeRunId") or thread.get("status") == "running":
        return "running"
    return thread.get("status", "unknown")


# ----------------------------------------------------------------- commands

def cmd_auth(args):
    path = cred_path(args)
    if os.path.isfile(path):
        cred = json.load(open(path))
        age_days = (time.time() - cred.get("obtained_at", 0)) / 86400
        ttl = cred.get("expires_in", 0) / 86400
        print(f"{path}\n  base {cred.get('base_url')}  scope {cred.get('scope')}  "
              f"age {age_days:.1f}d of {ttl:.0f}d")
        return
    token = load_cred(args)
    print(f"acquired credential for {base_url(args)} (token {token[:10]}...)")


def cmd_snapshot(args):
    mcp = Mcp(args).start()
    rows = all_threads(mcp)
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    print(f"{'thread':10} {'state':10} {'model':16} {'run':4} title")
    for t in rows:
        print(f"{t['threadId'][:8]:10} {t.get('status', '-'):10} "
              f"{t.get('providerInstanceId', '-'):16} "
              f"{'y' if t.get('latestRunId') else '-':4} "
              f"{(t.get('title') or '')[:56]} [{t.get('_projectTitle')}]")


def cmd_thread(args):
    mcp = Mcp(args).start()
    payload = mcp.tool("t3_thread_read",
                       {"threadId": args.threadId, "limit": args.limit})
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    t = payload.get("thread", {})
    print(f"title:   {t.get('title')}")
    print(f"status:  {t.get('status')}  activeRun: {t.get('activeRunId')}  "
          f"model: {t.get('providerInstanceId')}:{t.get('model')}  "
          f"mode: {t.get('runtimeMode')}")
    for item in payload.get("items", [])[-args.limit:]:
        role = item.get("createdBy", "?")
        text = (item.get("text") or item.get("summary") or "").replace("\n", " ")[:160]
        print(f"  [{role}] {text}")


def cmd_status(args):
    mcp = Mcp(args).start()
    try:
        payload = read_thread(mcp, args.threadId)
    except Fail as e:
        text = str(e).lower()
        if "thread_not_found" in text or "no longer available" in text \
                or "not found" in text:
            print("gone")
            return
        raise
    print(one_word_status(payload))


def cmd_create(args):
    mcp = Mcp(args).start()
    selection = None
    if args.model:
        instance, _, model = args.model.partition(":")
        selection = {"instanceId": instance or None, "model": model or "auto"}
    arguments = {"title": args.title,
                 "projectId": resolve_project(mcp, args.project),
                 "runtimeMode": args.mode}
    if selection:
        arguments["modelSelection"] = selection
    if args.message:
        arguments["message"] = args.message
    out = mcp.tool("t3_thread_launch", arguments)
    print(json.dumps(out, indent=2))


def cmd_prompt(args):
    mcp = Mcp(args).start()
    out = mcp.tool("t3_thread_send", {"threadId": args.threadId, "message": args.text})
    print(json.dumps(out, indent=2))


def cmd_append(args):
    mcp = Mcp(args).start()
    out = mcp.tool("t3_thread_send",
                   {"threadId": args.threadId, "message": args.text, "mode": "queue"})
    print(json.dumps(out, indent=2))


def cmd_wait(args):
    mcp = Mcp(args).start()
    arguments = {"threadId": args.threadId}
    if args.run:
        arguments["runId"] = args.run
    if args.timeout_secs:
        arguments["timeoutMs"] = args.timeout_secs * 1000
    out = mcp.tool("t3_thread_wait", arguments)
    print(json.dumps(out, indent=2))


def cmd_interrupt(args):
    mcp = Mcp(args).start()
    arguments = {"threadId": args.threadId}
    if args.reason:
        arguments["reason"] = args.reason
    out = mcp.tool("t3_thread_interrupt", arguments)
    print(json.dumps(out, indent=2))


def cmd_stop(args):
    args.reason = "t3ctl stop"
    cmd_interrupt(args)


def cmd_archive(args):
    if not args.yes:
        raise Fail("archive removes the thread from the active list; pass --yes")
    mcp = Mcp(args).start()
    out = mcp.tool("t3_thread_organize", {"action": "archive", "threadId": args.threadId})
    print(json.dumps(out, indent=2))


def cmd_search(args):
    mcp = Mcp(args).start()
    out = mcp.tool("t3_thread_search", {"query": args.query, "limit": args.limit})
    print(json.dumps(out, indent=2))


def cmd_queue(args):
    mcp = Mcp(args).start()
    out = mcp.tool("t3_queue_list", {"threadId": args.threadId})
    print(json.dumps(out, indent=2))


def cmd_requests(args):
    mcp = Mcp(args).start()
    out = mcp.tool("t3_pending_request_list", {"threadId": args.threadId})
    print(json.dumps(out, indent=2))


def cmd_respond(args):
    mcp = Mcp(args).start()
    out = mcp.tool("t3_pending_request_respond",
                   {"threadId": args.threadId, "requestId": args.requestId,
                    "response": args.answer})
    print(json.dumps(out, indent=2))


def cmd_pr_link(args):
    parts = args.url.rstrip("/").split("/")
    if len(parts) < 2 or not parts[-1].isdigit():
        raise Fail("expected a PR url like https://github.com/<owner>/<repo>/pull/<n>")
    mcp = Mcp(args).start()
    out = mcp.tool("link_pull_request",
                   {"threadId": args.threadId, "url": args.url})
    print(json.dumps(out, indent=2))


def cmd_tasks(args):
    mcp = Mcp(args).start()
    arguments = {}
    if args.project:
        arguments["projectId"] = resolve_project(mcp, args.project)
    out = mcp.tool("list_scheduled_tasks", arguments)
    print(json.dumps(out, indent=2))


def cmd_task_create(args):
    mcp = Mcp(args).start()
    arguments = {"prompt": args.prompt,
                 "schedule": {"type": "interval", "everyMs": args.every_mins * 60000}}
    if args.title:
        arguments["title"] = args.title
    if args.project:
        arguments["projectId"] = resolve_project(mcp, args.project)
    if args.bind:
        arguments["bindToCurrentThread"] = False
        arguments["threadId"] = args.bind
    out = mcp.tool("schedule_task", arguments)
    print(json.dumps(out, indent=2))


def cmd_task_run(args):
    mcp = Mcp(args).start()
    out = mcp.tool("run_scheduled_task_now", {"taskId": args.task_id})
    print(json.dumps(out, indent=2))


def cmd_task_delete(args):
    if not args.yes:
        raise Fail("task-delete is permanent; pass --yes")
    mcp = Mcp(args).start()
    out = mcp.tool("delete_scheduled_task", {"scheduledTaskId": args.task_id})
    print(json.dumps(out, indent=2))


def cmd_raw(args):
    mcp = Mcp(args).start()
    out = mcp.tool(args.tool_name, json.loads(args.json_args or "{}"))
    print(json.dumps(out, indent=2))


# --------------------------------------------------------------------- main

def main() -> int:
    parser = argparse.ArgumentParser(description="thin T3 Code MCP CLI (v2)")
    parser.add_argument("--env", default="desk", choices=sorted(ENVS),
                        help="named environment")
    parser.add_argument("--url", help="explicit base URL override")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add(name, fn, **kw):
        p = sub.add_parser(name, **kw)
        p.set_defaults(fn=fn)
        return p

    add("auth", cmd_auth)

    p = add("snapshot", cmd_snapshot); p.add_argument("--json", action="store_true")

    p = add("thread", cmd_thread); p.add_argument("threadId")
    p.add_argument("--limit", type=int, default=5); p.add_argument("--json", action="store_true")

    p = add("status", cmd_status); p.add_argument("threadId")

    p = add("create", cmd_create)
    p.add_argument("--project", required=True); p.add_argument("--title", required=True)
    p.add_argument("--model"); p.add_argument("--mode", default="full-access")
    p.add_argument("--message"); p.add_argument("--json", action="store_true")

    p = add("prompt", cmd_prompt); p.add_argument("threadId"); p.add_argument("text")
    p = add("append", cmd_append); p.add_argument("threadId"); p.add_argument("text")

    p = add("wait", cmd_wait); p.add_argument("threadId")
    p.add_argument("--timeout-secs", type=int); p.add_argument("--run")

    p = add("interrupt", cmd_interrupt); p.add_argument("threadId"); p.add_argument("--reason")
    p = add("stop", cmd_stop); p.add_argument("threadId")

    p = add("archive", cmd_archive); p.add_argument("threadId"); p.add_argument("--yes", action="store_true")

    p = add("search", cmd_search); p.add_argument("query"); p.add_argument("--limit", type=int, default=10)

    p = add("queue", cmd_queue); p.add_argument("threadId")
    p = add("requests", cmd_requests); p.add_argument("threadId")
    p = add("respond", cmd_respond); p.add_argument("threadId"); p.add_argument("requestId"); p.add_argument("answer")

    p = add("pr-link", cmd_pr_link); p.add_argument("threadId"); p.add_argument("url")

    p = add("tasks", cmd_tasks); p.add_argument("--project")
    p = add("task-create", cmd_task_create); p.add_argument("--prompt", required=True)
    p.add_argument("--every-mins", type=int, required=True); p.add_argument("--title")
    p.add_argument("--project"); p.add_argument("--bind")
    p = add("task-run", cmd_task_run); p.add_argument("task_id")
    p = add("task-delete", cmd_task_delete); p.add_argument("task_id"); p.add_argument("--yes", action="store_true")

    p = add("raw", cmd_raw); p.add_argument("tool_name"); p.add_argument("json_args", nargs="?")

    args = parser.parse_args()
    try:
        args.fn(args)
    except Fail as e:
        sys.exit(str(e))
    return 0


if __name__ == "__main__":
    sys.exit(main())

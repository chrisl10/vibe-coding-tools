# T3 Code local API map

Sections 2 onward are the V2 map, PROVEN against the live desk server
(127.0.0.1:3773, T3 Code Beta 0.1.0, 2026-10-18). Section 1 (0.0.45) is
kept as history: every REST route it documents was removed or reshaped in
V2, and t3ctl v1 is dead against 0.1.0.

## 1. History: T3 Code 0.0.45 surface (dead in 0.1.0)

PROVEN against the live desk server (127.0.0.1:3773, t3 v0.0.45, 2026-10-12).
Source: SPA bundle route table (141 chunks mined), OTLP span names in
~/.t3/userdata/logs/server.trace.ndjson.*, and a live authenticated
snapshot call with a bearer session minted via `t3 auth session issue`.

## Auth

- `t3 auth session issue --ttl 30d --label <label> --token-only` prints a
  bearer token (JWT, 462 chars observed).
- HTTP header: `Authorization: Bearer <token>`.
- The token authorizes the local server the CLI's userdata belongs to. Desk
  and macdev servers have separate userdatas, so each environment needs its
  own token (macdev has no x64 CLI yet; see Environment addressing).
- `t3 auth session list` / `revoke` manage sessions.
- Websocket: GET /api/auth/websocket-ticket first, then connect (realtime
  event stream; thread.message.assistant.delta, thread.realtime.* events).

## HTTP surface (client-observed)

- POST /api/orchestration/dispatch   command envelope (see below)
- GET  /api/orchestration/snapshot   full state: projects, threads, sessions
- GET  /api/orchestration/threads/:threadId?reasoningMessages=true&turnLimit=N&beforeCursor=<cur>
- GET  /api/orchestration/shell      shell snapshot
- GET  /api/pull-requests/diff       PR diff for a linked thread PR
- GET  /api/auth/websocket-ticket
- /api/auth/* (session, pairing-links, clients, browser-session)
- /api/connect/* and /api/t3-connect/* (environment linking, mint-credential)

## Dispatch envelope

POST /api/orchestration/dispatch with JSON:

    { "type": "<command>", "commandId": "<uuid>", "createdAt": "<iso>",
      ...command fields }

commandId is a fresh UUID per command; createdAt is ISO timestamp.

## Command catalog (thread namespace)

- thread.create {threadId, projectId, title, modelSelection{instanceId,model},
  runtimeMode, interactionMode?, branch?, worktreePath?, historyImport?}
- thread.turn.start {threadId, message{messageId, role:"user", text,
  attachments?, context?}, modelSelection?, titleSeed?, runtimeMode,
  interactionMode?, bootstrap?}
- thread.message.user.append {threadId, message{messageId, text, ...}}
- thread.turn.interrupt {threadId, turnId?}
- thread.session.stop
- thread.approval.respond {threadId, requestId, decision}
- thread.user-input.respond {threadId, requestId, answers,
  attachmentsByQuestionId?}   (the AskUserQuestion equivalent)
- thread.pull-request.link {threadId, url, source}
- thread.pull-request.sync / unlink
- thread.meta.update / thread.archive / thread.unarchive / thread.delete
- thread.settle / thread.unsettle / thread.auto-settle.set
- thread.checkpoint.revert / thread.conversation.revert
- project.create / project.meta.update / project.delete
- provider.auth.start/respond/subscribe, provider.install.start (flows)

## Snapshot shape (observed 2026-10-12)

    { snapshotSequence, updatedAt,
      projects: [{id, title, workspaceRoot, defaultModelSelection, scripts, ...}],
      threads: [{id, projectId, title,
                 modelSelection: {instanceId, model},   # e.g. codex_belay / auto
                 runtimeMode,          # e.g. "full-access"
                 interactionMode,
                 branch, worktreePath,  # per-thread worktree model confirmed
                 pullRequests: [...], branchPullRequest,
                 latestTurn: {turnId, state, requestedAt, startedAt,
                              completedAt, assistantMessageId},
                 settledOverride, settledAt, snoozedUntil, pinnedAt,
                 messages: [...], activities: [...], checkpoints: [...],
                 session: {status: "stopped"|"running"|..., providerName,
                           providerInstanceId, activeTurnId, lastError}}] }

Provider instances observed riding belay: claude_belay (claudeAgent driver,
ANTHROPIC_BASE_URL=tailnet:4000) and codex_belay (codex driver, customModels
glm-5.3, glm-5.3-flash, grok-4.7, openrouter-*). A completed thread that ran
on codex_belay exists (2026-10-06), so T3-through-belay is production-proven.

## TARS primitive mapping

| TARS (Claude Code Desktop) | T3 equivalent |
|---|---|
| spawn_task (chip offer) | thread.create |
| owner click starts session | thread.turn.start (or the GUI) |
| list_sessions | GET snapshot |
| list_events(session_id) | GET threads/:threadId (turnLimit, beforeCursor) |
| SendMessage | thread.message.user.append / thread.turn.start |
| stop_session | thread.turn.interrupt / thread.session.stop |
| approvals | thread.approval.respond |
| AskUserQuestion | thread.user-input.respond |
| Monitor + gh CI watch | thread.pull-request.link/sync + /api/pull-requests/diff |
| CronCreate tick | external timer posting thread.turn.start TICK prompts |
| archive_session | thread.archive |

## Exact server schemas (PROVEN by live dispatch, t3 0.0.45)

The authoritative schema source is the server bundle inside the desktop
app: extract app.asar, read apps/server/dist/bin.mjs (search for the
command name). Two fields the SPA bundle does not reveal:

- thread.create REQUIRES branch and worktreePath as explicit JSON null
  when unused (omitting them is a 400 with an empty body), and
  modelSelection is required (no default). interactionMode defaults.
- thread.turn.start REQUIRES message.attachments as an array (empty is
  fine) and interactionMode ("default").

Live proof 2026-10-13: t3ctl created threads and ran turns on codex_belay
and claude_belay (glm-5.3-flash via fabric), assistant replies received;
threads archived and scratch project deleted through the same API. The
claude thread also fired the Wasp Nest v3 SessionStart hook (Library
offer), proving the v3 plugin install is live inside T3 sessions.

## Open items for the t3ctl build

1. Environment addressing: how the desk app routes commands to a connected
   environment (macdev). EnvironmentRpc spans exist; /api/t3-connect/
   mint-credential is how the desk authenticates to remote servers. Either
   dispatch accepts an environment selector, or t3ctl must talk to each
   environment's server directly (desk 127.0.0.1:3773, macdev via tunnel
   127.0.0.1:38373 with a macdev-side token minted through its GUI or the
   connect credential flow).
2. modelSelection values: instanceId strings confirmed (codex_belay); model
   enum per instance comes from settings customModels plus "auto".
3. runtimeMode enum: "full-access" observed; others (read-only?) to enumerate.
4. WS event stream: needed only for sub-10s latency; the 10-minute tick can
   poll snapshots instead.
5. Response envelope of dispatch (command ack shape) to capture on first
   live call.

## 2. V2 (0.1.0): the control surface is the MCP server

V2 removed /api/orchestration/snapshot and /api/orchestration/dispatch
(zero hits in the server bundle). What remains on the desktop loopback:

- GET /api/projects            project snapshot (bearer session token)
- GET /api/orchestration/threads/:threadId{,/transcript,/bounded,/history}
  read-only thread data; REQUIRES header `x-t3-orchestration-protocol: 2`
  plus a bearer session token
- /api/auth/* (session, pairing-token, websocket-ticket)
- POST /mcp                    the MCP server (Streamable HTTP, JSON-RPC)
- /oauth/mcp/*                 OAuth for MCP clients (see section 3)
- The 39-route /api/session/* REST group in the bundle is the embedded
  OpenCode-compatible client surface; it is NOT mounted on the desktop
  loopback (falls through to the SPA shell).

Unknown paths return the SPA HTML with 200, so probe with Accept JSON and
check the body's first byte: HTML means no such route.

## 3. V2 auth for MCP clients (fully headless, PROVEN 2026-10-18)

Provider-session bearer tokens (`t3 auth session issue`) are rejected by
/mcp ("invalid_mcp_credential"). MCP accepts OAuth client tokens or
registry tokens (agents T3 launched). The OAuth flow never needs a browser
on the host machine:

1. POST /oauth/mcp/register {client_name, redirect_uris:
   ["http://127.0.0.1:<port>/cb"], token_endpoint_auth_method: "none",
   grant_types: ["authorization_code"], response_types: ["code"]}
   -> 201 {client_id}   (dynamic registration is open)
2. PKCE S256 verifier/challenge, random state.
3. Mint a one-time pairing code on the environment's host:
   `t3 auth pairing create --json --ttl 5m --label t3ctl` -> {credential}.
4. POST /oauth/mcp/decision {authorization: {response_type: "code",
   client_id, redirect_uri, code_challenge, code_challenge_method: "S256",
   state, resource: "<base>/mcp"}, decision: {_tag: "pairing-code",
   access: "read-only"|"approval-required"|"auto-accept-edits"|"auto"|
   "full-access", code: <credential>}} -> {redirectTo: <redirect_uri>?code=...}
5. POST /oauth/mcp/token (form) {grant_type: "authorization_code", code,
   redirect_uri, client_id, code_verifier, resource} ->
   {access_token, token_type: "Bearer", expires_in: 2592000, scope}
   30-day TTL, no refresh token: re-run the flow on expiry (all steps are
   scriptable; t3ctl v2 does this automatically on the first 401).

MCP transport per invocation: initialize (protocolVersion 2025-03-26;
server answers 2025-06-18 and stores mcp-session-id) ->
notifications/initialized -> tools/call. Responses are JSON or SSE; both
carry the same JSON-RPC body.

## 4. V2 MCP tool vocabulary (client-relevant subset)

Thread control: t3_thread_list {projectId REQUIRED for outside clients,
statuses?, titleContains?, limit<=100, cursor?} -> {threads: [...],
nextCursor, total}; t3_thread_read {threadId, limit<=100, view:
"messages"|"activity", runLimit<=50}; t3_thread_send {threadId, message,
mode?: "auto"|"queue"|"steer"|"restart"}; t3_thread_wait {threadId,
runId?, timeoutMs?} (blocks to terminal state); t3_thread_interrupt;
t3_thread_launch {title, projectId?|scratch:true, modelSelection?
{instanceId, model}, runtimeMode?, interactionMode?, message?};
t3_thread_fork; t3_thread_organize {action: pin|unpin|snooze|unsnooze|
settle|unsettle|archive|unarchive|mark_unread}; t3_thread_search
{query, limit?, projectId?}; t3_thread_configure / _configuration /
_transfers / _merge_back.

Queue: t3_queue_list / _read / _edit / _cancel / _reorder /
_promote_to_steer {threadId, ...}.

Pending user questions: t3_pending_request_list / _read / _respond.

Projects: t3_project_list / _read / _create / _update / _delete / _clone.

Scheduled tasks (server-side, survive restarts): schedule_task {prompt,
schedule: {type: "interval", everyMs>=60000} | {type: "fixed_time", ...} |
{type: "webhook", ...}, title?, projectId?, bindToCurrentThread?,
threadId?}; list_scheduled_tasks; update_scheduled_task;
delete_scheduled_task {scheduledTaskId}; run_scheduled_task_now {taskId}
(full access only). Tasks bound to a thread deliver the prompt to that
thread; unbound tasks create a new thread per run.

PR lane: link_pull_request {threadId, url}; unlink; list; watch; unwatch;
write_pull_request_guides; read_pull_request_guide.

Capabilities: orchestrator_capabilities {} lists every provider instance
and its models (desk 0.1.0: codex, codex_belay, claudeAgent, claude_belay,
claude_zai, cursor, grok, opencode, antigravity, muse, pi).

## 5. V2 payload shapes (observed 2026-10-18, desk)

t3_thread_list item: {threadId, title, createdBy, creationSource, status:
"idle"|..., latestRunId, providerInstanceId, model, runtimeMode,
interactionMode, linkedPullRequest, settled, settledAt, snoozed,
snoozedUntil, parentThreadId, relationshipToParent, itemCount, createdAt,
updatedAt}.

t3_thread_read: {thread: {threadId, projectId, title, status, activeRunId,
latestRunId via list, providerInstanceId, model, runtimeMode, branch,
worktreePath, runCount, itemCount, pendingRequestCount, archived, settled,
snoozed, createdAt, updatedAt}, recentRuns: [], items: [{position,
itemId, runId, messageId, createdBy: user|agent, text, ...}]}.

Thread status vocabulary observed: idle, running (activeRunId set),
completed (right after a run), preparing/starting during launch. Missing
thread: tool error {_tag: OrchestratorMcpFailure, code: thread_not_found,
message: "... no longer available."} (t3ctl status maps this to "gone").

t3_thread_send reply: {threadId, messageId, runId, status: "starting",
delivery: "started"}. t3_thread_wait reply: {threadId, runId, status:
"completed", timedOut: false}.

Launch by an outside client uses threadId prefix "mcp:" (e.g.
mcp:b32e30af-...); legacy thread ids are bare UUIDs and both work in every
tool.

## 6. Live proofs (2026-10-18)

Headless OAuth (register -> pairing -> decision -> token) done purely over
HTTP plus the local t3 CLI. t3ctl v2 then: listed projects and threads,
read threads, launched a scratch thread on claude_zai:glm-5.3-flash with
an initial message (model replied "OK"), waited to completion, sent a
second message by t3_thread_send (delivery started, run completed),
archived twice. Old alpha-era threads (1f6fd115, 9c37a409 TARS manager)
survived the V2 migration and are readable.

## 7. TARS primitive mapping (V2 update)

| TARS | V2 path |
|---|---|
| spawn_task | t3_thread_launch |
| owner message | t3_thread_send (auto steers or queues) |
| list_sessions | t3_project_list + t3_thread_list per project |
| list_events | t3_thread_read (view messages/activity) |
| SendMessage / steering | t3_thread_send mode auto/steer/queue |
| stop_session | t3_thread_interrupt |
| approvals / AskUserQuestion | t3_pending_request_list / _respond |
| Monitor + CI watch | watch_pull_request lane |
| CronCreate tick | scheduled task bound to the manager thread, or the launchd t3-tick posting t3_thread_send |
| archive_session | t3_thread_organize archive |
| multi-harness child work | delegate_task (agents inside T3 only) |

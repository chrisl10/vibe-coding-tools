# T3 Code 0.0.45 local API map (S2 research)

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

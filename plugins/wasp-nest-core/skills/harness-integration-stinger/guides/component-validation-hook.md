# Qualify component validation without activating a hook

For O292, also use [host-version contract proof](13-prove-hook-contract.md). Load the [current source contract](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/harness-integration-stinger/references/research/component-hook-update/distillation.md) and the installed host's event/payload documentation before treating a configured handler as available. This update changes only the existing post-edit advisory code; it does not enable a new binding or alter tool permissions.

1. Inspect the selected carrier's actual post-edit payload. Supported source shapes are nested `tool_input`/`toolInput` with `file_path`/`filePath`/`path`, or apply-patch headers in that nested input's `command`. A top-level path is not currently parsed. Unsupported shapes or missing events remain untested.
2. Run [the offline payload fixtures](../../../../scripts/test_component_validate_hook.py) from the source checkout. They use an owned synthetic validator and temporary roots; do not install the hook to run them.
3. Check skill/agent/command/rule/plugin target recognition, deduplication and catalog owner refusal. Targets are rebuilt from restricted lexical matches and passed as argv, not evaluated shell text.
4. Exercise malformed/nonobject/oversized inputs, unknown owner, missing validator, unexpected stderr, too many targets and slow validator cases. Missing/unfinished recognized checks must produce an unverified advisory without raw validator messages, unexpected stderr or permission changes. Event and command metadata must be string-typed before parsing.
5. Confirm the actual carrier output shape separately: Claude-shaped `systemMessage` or Cursor-shaped `additional_context`. Test the client and version before claiming a native event fired.
6. Preserve distinctions: bounded stdin bytes is not a timeout on stalled input delivery; a remaining subprocess budget is best effort and depends on process/host termination. The host timeout remains separate. The handler never proves independent review, successful implementation or owner authorization.

Source edits use the standard ordered Security, Quality and repository-health review. Activation, settings and installed registry changes require their task authority and are not a consequence of this guide.

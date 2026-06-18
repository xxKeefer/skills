# tool-policy

A config-driven `PreToolUse` policy hook that does two jobs in one place:

1. **Redirect** package-runner invocations (`npx`, `pnpm exec`, `pnpm dlx`,
   `yarn exec`, `yarn dlx`, …) toward the canonical command for the project —
   e.g. `npx vitest` → "use `nx test:unit`".
2. **Block** specific command prefixes outright (e.g. `git stash`) with a custom
   reason.

It is **block-all + allowlist** for runners: any intercepted runner is denied
unless its tool is allowlisted. Known tools get a tailored "use this instead"
message; unknown tools get told how to allowlist themselves.

This is a **template**. The shipped `tool-policy.config.json` is **empty** — the
hook does nothing until you fill it in. `tool-policy.example.json` is a worked
nx-monorepo config to copy rules from. Nothing in the code is tied to nx; the
engine just reads the config.

## Files

| File | Purpose |
|------|---------|
| `tool_policy.py` | The Bash hook. Reads the tool call on stdin, prints a deny decision (or nothing) on stdout. |
| `protect_guard.py` | Companion `Write\|Edit\|MultiEdit` hook. Denies tool edits to the runtime files (closes the edit vector). |
| `tool-policy.config.json` | The live config the hook reads. **Ships empty** — the hook does nothing until you fill it in. |
| `tool-policy.example.json` | A worked nx-monorepo config to copy rules from. Not loaded by the hook. |
| `tool_policy_test.py` | Test suite (runs against the example config). `python3 tool_policy_test.py` (exits non-zero on failure). |
| `SKILL.md` | `setup-tool-policy` installer skill — copies these files and wires the hooks, prompting for global vs current-project scope. |

## Wiring

Run `/setup-tool-policy` to install automatically (it prompts for global vs
current-project scope and wires both hooks). To do it by hand: copy the folder
somewhere stable (e.g. `~/.claude/hooks/tool-policy/`) and register both hooks in
`~/.claude/settings.json` under `hooks.PreToolUse`:

```json
{
  "matcher": "Bash",
  "hooks": [
    { "type": "command", "command": "python3 ~/.claude/hooks/tool-policy/tool_policy.py" }
  ]
},
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    { "type": "command", "command": "python3 ~/.claude/hooks/tool-policy/protect_guard.py" }
  ]
}
```

Hook *wiring* is read at session start (changes take effect next session, or
`/hooks` to reload). The script re-reads the config on **every** call, so
allowlist/redirect/block edits are live without a restart.

### Replaces the inline `git stash` grep

If you have an inline blocker like
`jq -r '.tool_input.command' | grep -q 'git stash' && echo '{...block...}'`,
move it into `blockedCommands` and delete the inline hook. The parser version
won't false-fire on `git stash` appearing inside a commit message, an `echo`, or
a `grep` pattern — the inline grep does (and will block your own scripts that
merely mention the phrase).

## Why a parser, not a grep

Grepping the raw command fires on **any** substring match — a commit message, an
`echo`, or a `grep` pattern containing `pnpm exec` or `git stash` gets wrongly
blocked.

`tool_policy.py` tokenizes the command quote-aware (`shlex`) and only acts when a
runner or blocked prefix appears in **command position** — at the start, or right
after a shell operator (`&& || | ; ( )`). A name inside a quoted string is
ignored.

## Config

```jsonc
{
  "runners":   ["npx", "pnpm exec", "pnpm dlx", "yarn exec", "yarn dlx"],
  "allowlist": ["nx", "syncpack", "playwright:install", "tsx"],
  "redirects": { "vitest": "nx test:unit {project} -- <file>", "...": "..." },
  "blockedCommands": [
    { "match": "git stash", "reason": "Run tests against the current working tree." }
  ]
}
```

- **`runners`** — command prefixes to intercept.
- **`allowlist`** — tools that pass through. `"tool"` allows any subcommand;
  `"tool:sub"` allows only that subcommand (e.g. `playwright:install` passes
  while `playwright test` is redirected).
- **`redirects`** — `tool` → the canonical command shown to the agent. `{project}`
  is a literal placeholder in the message, not substituted.
- **`blockedCommands`** — `{ match, reason }` entries. `match` is tokenized and
  matched as a **prefix** in command position, so `"git stash"` blocks `git
  stash`, `git stash push`, and `git stash list`. `reason` is shown to the agent.

Resolution order: self-protection → blocked commands → runner allowlist →
runner redirect → runner block-all.

## Adding a rule

Editing the config is a **human-only** decision. The block messages tell the
agent to stop and ask — they deliberately do not invite the agent to edit the
config itself.

- **Legit one-off runner, no canonical equivalent** → add `"tool"` (or
  `"tool:sub"`) to `allowlist`.
- **Runner tool has a canonical target** → add `"tool": "<canonical command>"`
  to `redirects` so the block message points the right way.
- **Forbid a command** → add `{ "match": "...", "reason": "..." }` to
  `blockedCommands`.

## Self-protection

The config and the guard scripts are human-only. Two hooks cover both vectors an
agent could use to neuter the policy:

- **Shell vector** — `tool_policy.py` rejects any Bash command that names
  `tool-policy.config.json` (`sed`, `echo >>`, `tee`, even `cat`).
- **Tool vector** — `protect_guard.py` denies tool edits to the runtime files:
  `tool-policy.config.json`, `tool_policy.py`, and `protect_guard.py` itself.
  `README.md` and the test file stay editable so docs and tests can be maintained.

Humans editing any of these directly in an editor are unaffected — that never
goes through a tool call.

Note the deliberate asymmetry: the tool vector protects all three runtime files,
but the shell vector only guards the config *name*. An agent could still rewrite
`tool_policy.py`/`protect_guard.py` via a raw Bash redirect. Fully closing that
would mean blocking Bash writes to the whole dir, which was judged too broad.

## Behaviour notes

- Unparseable commands (e.g. a stray quote) **fail open** — never false-block.
- Missing/broken config → the hook does nothing rather than blocking everything.
- Output uses the current hook contract:
  `hookSpecificOutput.permissionDecision: "deny"`.

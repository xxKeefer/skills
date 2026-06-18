---
name: setup-tool-policy
description: >
  Install the tool-policy PreToolUse hook (runner redirection + command blocking) into a Claude
  Code settings file. Prompts for global or current-project scope, copies the runtime files, and
  wires both hooks. Use when the user says "setup tool-policy", "install tool-policy", "install
  the tool-policy hook", or wants to wire this hook into a project or their global config.
---

# Setup tool-policy

Install this folder's hook into a Claude Code settings file. The runtime files
(`tool_policy.py`, `protect_guard.py`, the configs) live beside this SKILL.md —
this skill copies them to the target and registers the two `PreToolUse` hooks.

## Step 1: Choose scope

Use **AskUserQuestion** to ask where to install:

- **Global** — all repos. Files go to `~/.claude/hooks/tool-policy/`, wired into
  `~/.claude/settings.json`.
- **Current project** — this repo only. Files go to
  `.claude/hooks/tool-policy/`, wired into `.claude/settings.local.json`.

**Done when:** scope is chosen and the target hooks dir + settings file are known.

## Step 2: Copy the runtime files

Copy these siblings of this SKILL.md to the target hooks dir:
`tool_policy.py`, `protect_guard.py`, `tool-policy.config.json`,
`tool-policy.example.json`, `README.md`.

- **Never clobber a live config.** If `tool-policy.config.json` already exists at
  the target, leave it untouched — it holds the user's rules. Copy everything else.
- Do **not** copy `SKILL.md` or `tool_policy_test.py`.

**Done when:** the runtime files are in place and any existing config is preserved.

## Step 3: Register both hooks

Merge two `PreToolUse` entries into the chosen settings file — **merge, don't
overwrite** existing hooks, and don't duplicate entries that are already present.

Use the path matching the scope:
- Global → `~/.claude/hooks/tool-policy/`
- Project → `$CLAUDE_PROJECT_DIR/.claude/hooks/tool-policy/`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python3 {path}/tool_policy.py" }]
      },
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3 {path}/protect_guard.py" }]
      }
    ]
  }
}
```

**Done when:** both entries exist in the settings file and existing config is intact.

## Step 4: Confirm

Tell the user:

- Reload hooks with `/hooks` (or restart the session) — wiring is read at session start.
- The live `tool-policy.config.json` **ships empty**, so the hook does nothing
  until they add rules. Point them at `tool-policy.example.json` to copy from, and
  remind them config edits are live (no restart needed).

**Done when:** the user knows how to activate and populate the hook.

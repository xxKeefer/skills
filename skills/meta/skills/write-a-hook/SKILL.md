---
name: write-a-hook
description: Scaffold a Claude Code hook holder -- hook script, installer skill, README, and config files.
disable-model-invocation: true
---

# Write a Hook

Author a new hook holder from scratch. A holder is the folder of a `utility` installer skill,
`skills/utility/skills/setup-<name>/`, and ships everything needed to install and run one hook: the
script, the installer `SKILL.md`, a README, and config when behaviour is data-driven. Paths in this
skill are relative to the marketplace repo root. The working reference is
`skills/utility/skills/setup-tool-policy/` -- read it before drafting.

## Step 1: Gather Requirements

`$ARGUMENTS` may contain:

- **Hook name** -- kebab-case, names the holder dir (`setup-<name>/`)
- **What it does** -- the behaviour to enforce, observe, redirect, or mutate

If anything is missing, use **AskUserQuestion** to fill gaps. Then invoke `/grill` to pin the
design. A hook needs more decided up front than a skill does:

- **Event** -- `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `UserPromptSubmit`,
  `SessionStart`, `PreCompact`. Determines when it fires.
- **Matcher** -- which tool(s) the event filters on (`Bash`, `Write|Edit|MultiEdit`, `*`). Some
  events take no matcher.
- **Decision** -- what the hook does: **block** (deny with a reason), **redirect** (deny + point at
  the canonical command), **observe** (log/tally, never block), or **mutate** (inject context).
- **Config-driven?** -- is behaviour static (baked into the script) or data-driven (a config file
  the user edits)? Config-driven holders ship the live config **empty/inert** plus an example to
  copy from.
- **Self-protection** -- if config-driven, must the config and script be protected from agent
  edits? (See tool-policy's two-vector guard: shell + tool.)
- **Fail mode** -- fail-open (do nothing on bad input/missing config -- the default for guards) or
  fail-closed. State it explicitly.
- **Language** -- script language. Default `python3` for parsing/JSON logic, shell for trivial
  greps. Stay agnostic to the project being guarded.

**Done when:** event, matcher, decision, config-or-static, fail mode, and language are all settled.

## Step 2: Check for Conflicts

Before scaffolding:

1. **Check existing holders** in `skills/utility/skills/` -- does this duplicate an existing hook's
   job? tool-policy already covers runner-redirection and command-blocking via config; prefer
   adding a rule there over a new holder.
2. **Check the lighter pattern** -- `setup-skill-tally` ships one static script with no config or
   README. If the hook is trivial and static, that pattern may fit better than a full holder.
3. **Naming**:
   - Holder dir: `skills/utility/skills/setup-<name>/`
   - Installer skill inside it: `setup-<name>` (the SKILL.md `name`)

Present findings. If there's overlap, discuss extending the existing hook vs a new holder.

## Step 3: Scaffold the Hook Holder

Create `skills/utility/skills/setup-<name>/` with the files the design calls for. Minimum is the
script + installer skill + README; add config files only when config-driven.

### The hook script

Contract (current Claude Code hooks): the script reads the tool call as JSON on **stdin** and
emits its decision as JSON on **stdout**. A blocking decision uses:

```json
{ "hookSpecificOutput": { "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..." } }
```

Observe-only hooks print nothing (or non-blocking output). Honour the fail mode from Step 1 --
unparseable input or missing config should not false-fire on a fail-open guard. Copy the parsing
and output shape from `skills/utility/skills/setup-tool-policy/tool_policy.py` rather than
re-deriving it.

### Config files (config-driven only)

- `<name>.config.json` -- the **live** config. Ships **empty/inert**: the hook does nothing until
  the user fills it in.
- `<name>.example.json` -- a worked config to copy rules from. Not loaded by the hook.

### Self-protection (if Step 1 required it)

Add a companion `Write|Edit|MultiEdit` guard that denies tool edits to the runtime files, and have
the main script reject Bash commands that name the config. See tool-policy's
`skills/utility/skills/setup-tool-policy/protect_guard.py` and note the documented
asymmetry between the shell and tool vectors -- state any gap you leave.

**Done when:** the holder dir holds a working script (and config pair, if applicable) honouring the
contract and fail mode.

## Step 4: Write the Installer Skill

Write the holder's `SKILL.md` as the `setup-<name>` installer. Make it user-invoked
(`disable-model-invocation: true`) with a one-line description, like every `utility` installer.
Mirror tool-policy's installer:

1. **Choose scope** -- AskUserQuestion: **global** (`~/.claude/hooks/<name>/`, wired into
   `~/.claude/settings.json`) or **current project** (`.claude/hooks/<name>/`, wired into
   `.claude/settings.local.json`).
2. **Copy the runtime files** -- copy the script(s), config(s), and README from
   `${CLAUDE_SKILL_DIR}` to the target. **Never clobber a live config** if one already exists. Do
   **not** copy the SKILL.md or test file.
3. **Register the hook(s)** -- merge the `hooks.<Event>` entry into the chosen settings file. Merge,
   don't overwrite; don't duplicate existing entries.
4. **Confirm** -- tell the user wiring is read at session start (`/hooks` to reload), and how to
   populate/activate config-driven behaviour.

Each step gets a **Done when** line.

**Done when:** running the installer would copy the files and wire the hook into either scope.

## Step 5: Write the README and Tests

- **README.md** -- document the file table, wiring (auto via `/setup-<name>` and by hand), config
  schema and resolution order (if any), self-protection, and behaviour notes (fail mode, output
  contract). tool-policy's README is the template.
- **`<name>_test.py`** (or equivalent) -- run the script against fixtures covering each decision
  path and the fail-open/closed edge. Runs standalone, exits non-zero on failure.

**Done when:** README matches the shipped files and tests pass against the script.

## Step 6: Register and Review

1. Add `/setup-<name>` to the skill tables in `skills/utility/CLAUDE.md` and
   `skills/utility/README.md`, and to the `utility` row of the root `README.md`. Bump the minor
   version in `skills/utility/.claude-plugin/plugin.json`.
2. Present to the user:

> **Hook: `<name>`**
> **Event/matcher:** {event} / {matcher}
> **Files:** {list under skills/utility/skills/setup-<name>/}
>
> {brief summary of what it does}

Ask:

1. **Test it** -- run the test suite and/or wire it into the current project to verify
2. **Adjust** -- revise
3. **Done** -- accept

### Split criteria

If the holder grows two distinct jobs (e.g. a `PreToolUse` guard *and* an unrelated `Stop`
reporter), make two holders. One holder, one coherent hook.

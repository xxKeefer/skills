---
name: setup-no-ai-attribution
description: Install a PreToolUse hook that denies a git commit whose message credits an AI tool, globally or for the current project.
disable-model-invocation: true
---

# Setup no-ai-attribution

Install this folder's hook into a Claude Code settings file. The runtime files live beside this
SKILL.md, in `${CLAUDE_SKILL_DIR}`. This skill copies them to the target and registers one
`PreToolUse` hook on `Bash`.

## Step 1: Choose scope

Use **AskUserQuestion** to ask where to install:

- **Global**: all repos. Files go to `~/.claude/hooks/no-ai-attribution/`, wired into
  `~/.claude/settings.json`.
- **Current project**: this repo only. Files go to `.claude/hooks/no-ai-attribution/`, wired into
  `.claude/settings.local.json`.

**Done when:** the scope is chosen, and the target hooks folder and settings file are known.

## Step 2: Copy the runtime files

Copy `no_ai_attribution.py` and `README.md` from `${CLAUDE_SKILL_DIR}` to the target hooks folder.
Do not copy `SKILL.md` or `no_ai_attribution_test.py`.

**Done when:** both files are in the target folder.

## Step 3: Register the hook

Merge one `PreToolUse` entry into the chosen settings file. Merge, do not overwrite, and do not
add the entry twice. The path is `~/.claude/hooks/no-ai-attribution/` for global scope, and
`$CLAUDE_PROJECT_DIR/.claude/hooks/no-ai-attribution/` for project scope.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python3 {path}/no_ai_attribution.py" }]
      }
    ]
  }
}
```

**Done when:** the entry is in the settings file, and the other settings are intact.

## Step 4: Confirm

Tell the user:

- Claude Code reads hooks at session start. Reload with `/hooks`, or restart the session.
- The hook guards commits that the agent makes through the Bash tool. It does not guard a commit
  typed in a terminal.

**Done when:** the user knows how to reload the hook and what it does not cover.

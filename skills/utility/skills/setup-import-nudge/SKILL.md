---
name: setup-import-nudge
description: Install the import-nudge PostToolUse hook, which reminds the agent when a file it edits still holds a pattern your rules name, globally or for the current project.
disable-model-invocation: true
---

# Setup import-nudge

Install this folder's hook into a Claude Code settings file. The runtime files live beside this
SKILL.md, in `${CLAUDE_SKILL_DIR}`. The hook runs after each `Write`, `Edit`, or `MultiEdit`. When
the file path and the file text both match a rule, it adds the rule's message to the agent's
context. It never blocks an edit.

## Step 1: Choose scope

Use **AskUserQuestion** to ask where to install:

- **Global**: all repos. Files go to `~/.claude/hooks/import-nudge/`, wired into
  `~/.claude/settings.json`.
- **Current project**: this repo only. Files go to `.claude/hooks/import-nudge/`, wired into
  `.claude/settings.local.json`.

**Done when:** the scope is chosen, and you know the target hooks folder and settings file.

## Step 2: Copy the runtime files

Copy `import_nudge.py`, `import-nudge.config.json`, `import-nudge.example.json`, and `README.md`
from `${CLAUDE_SKILL_DIR}` to the target hooks folder.

- If `import-nudge.config.json` exists at the target, keep it. It holds the user's rules.
- Do not copy `SKILL.md` or `import_nudge_test.py`.

**Done when:** the runtime files are in place, and an existing config is unchanged.

## Step 3: Register the hook

Merge this entry into the settings file. Keep each existing hook, and add no duplicate. Use
`~/.claude/hooks/import-nudge/` for global scope, else
`$CLAUDE_PROJECT_DIR/.claude/hooks/import-nudge/`.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3 {path}/import_nudge.py" }]
      }
    ]
  }
}
```

**Done when:** the entry is in the settings file, and each earlier hook is intact.

## Step 4: Confirm

Tell the user these things:

- Run `/hooks` or start a new session, because Claude Code reads hooks at session start.
- The live `import-nudge.config.json` has no rules, so the hook does nothing until they add one.
  `import-nudge.example.json` holds a rule to copy. A config edit takes effect on the next edit.

**Done when:** the user knows how to add a rule and turn on the hook.

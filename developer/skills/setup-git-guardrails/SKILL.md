---
name: setup-git-guardrails
description: >
  Install a Claude Code PreToolUse hook that blocks dangerous git commands (push, reset --hard,
  clean, branch -D, checkout ., restore .). Supports project-only or global scope. Use when the
  user says "setup git guardrails", "block dangerous git", "protect git", or wants to prevent
  agents from running destructive git operations.
---

# Setup Git Guardrails

Install a Claude Code hook that intercepts dangerous git commands before they execute. The hook
runs as a `PreToolUse` event on the `Bash` tool and blocks commands that could destroy work.

## Step 1: Choose Scope

Ask the user:

> Install git guardrails for **this project only** or **globally**?
>
> - **Project:** adds to `.claude/settings.local.json` in this repo
> - **Global:** adds to `~/.claude/settings.json` for all repos

## Step 2: Install the Hook Script

Copy the [block-dangerous-git.sh](scripts/block-dangerous-git.sh) script to the appropriate
location:

- **Project scope:** `.claude/hooks/block-dangerous-git.sh`
- **Global scope:** `~/.claude/hooks/block-dangerous-git.sh`

Make it executable: `chmod +x`.

## Step 3: Register the Hook

Add the hook to the chosen settings file:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "{path}/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If hooks already exist in the settings file, merge -- don't overwrite.

## Step 4: Customise (optional)

Present the default blocked patterns:

> **Blocked commands:**
> - `git push` (any form)
> - `git reset --hard`
> - `git clean -f` / `git clean -fd`
> - `git branch -D`
> - `git checkout .`
> - `git restore .`
>
> Want to add or remove any patterns?

If the user wants changes, edit the script accordingly.

## Step 5: Verify

1. Attempt a blocked command (e.g. `git push --dry-run`) and confirm it's intercepted
2. Attempt a safe command (e.g. `git status`) and confirm it passes

Report that guardrails are active.

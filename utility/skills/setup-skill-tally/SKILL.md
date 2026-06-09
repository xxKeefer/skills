---
name: setup-skill-tally
description: >
  Install a zero-latency Claude Code PreToolUse hook that tallies every skill invocation into
  ~/.claude/skill-tally.json. Use when the user says "setup skill tally", "track skill usage",
  "count skill invocations", "which skills do I use", or wants usage data to inform promote/retire
  decisions.
---

# Setup Skill Tally

Install a Claude Code hook that counts every skill invocation into a global JSON tally
(`~/.claude/skill-tally.json`), in the form `{ "skill": count }`. The same script is registered on
two events, both with `async: true`, so it fires and forgets -- **zero latency added to skill use**:

- `PreToolUse` on the `Skill` tool -- model-auto-invoked skills (`tool_input.skill`).
- `UserPromptExpansion` -- user-typed `/foo` and `/plugin:skill` slash commands, which expand inline
  without ever producing a `Skill` tool call.

The two paths are mutually exclusive, so a single invocation is counted exactly once regardless of
who triggered it. Skill names are normalised to their bare form (leading slash and `plugin:`
namespace stripped) so the same skill lands on one key no matter the path.

Global scope only -- the tally is a single file shared across all repos.

## Step 1: Check Prerequisites

Confirm `python3` is available:

```sh
command -v python3
```

If absent, stop and tell the user to install it (the script is Python stdlib only -- chosen because
macOS does not ship `flock(1)`, and Python's `fcntl.flock` keeps concurrent writes safe).

## Step 2: Install the Hook Script

Copy [skill-tally.py](scripts/skill-tally.py) to `~/.claude/hooks/skill-tally.py` and make it
executable (`chmod +x`).

## Step 3: Register the Hook

Merge both blocks into `~/.claude/settings.json` -- **do not overwrite** existing hooks; append to
each array if it already exists, and skip any entry whose matcher + command is already present
(idempotent):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/skill-tally.py",
            "async": true
          }
        ]
      }
    ],
    "UserPromptExpansion": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/skill-tally.py",
            "async": true
          }
        ]
      }
    ]
  }
}
```

The `Skill` matcher catches model-auto-invoked skills; the `UserPromptExpansion` matcher catches
user-typed `/foo` slash commands (which never produce a `Skill` tool call). `async: true` is what
guarantees no latency -- Claude Code does not wait for the script to finish.

## Step 4: Verify

1. Confirm the script exists and is executable at `~/.claude/hooks/skill-tally.py`.
2. Confirm both hook blocks are present in `~/.claude/settings.json`.
3. Simulate both paths to prove the script works end-to-end, including `plugin:` normalisation:

   ```sh
   echo '{"tool_input":{"skill":"setup-skill-tally"}}' | python3 ~/.claude/hooks/skill-tally.py
   echo '{"hook_event_name":"UserPromptExpansion","command_name":"/utility:setup-skill-tally"}' | python3 ~/.claude/hooks/skill-tally.py
   cat ~/.claude/skill-tally.json
   ```

   Confirm `setup-skill-tally` appears with a count of 2 -- both paths land on the same bare key.
   (The live hook takes effect on the **next** skill invocation after a session restart.)

Report that the tally is active and where to read it.

## Reading the tally

```sh
# most-used skills, descending
jq -r 'to_entries | sort_by(-.value)[] | "\(.value)\t\(.key)"' ~/.claude/skill-tally.json
```

## Uninstall

1. Remove the `Skill` matcher block from `PreToolUse` and the matching block from
   `UserPromptExpansion` in `~/.claude/settings.json`.
2. Delete `~/.claude/hooks/skill-tally.py`.
3. Optionally delete `~/.claude/skill-tally.json` (and its `.lock`), plus
   `~/.claude/skill-tally-debug.log` if it exists.

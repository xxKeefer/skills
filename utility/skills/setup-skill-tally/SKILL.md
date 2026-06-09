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
(`~/.claude/skill-tally.json`), in the form `{ "plugin:skill": count }`. The hook runs as a
`PreToolUse` event on the `Skill` tool with `async: true`, so it fires and forgets -- **zero latency
added to skill use**. All invocations are counted: user-typed `/foo`, model-auto-invoked, and
plugin-namespaced `/plugin:skill`.

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

Merge this into `~/.claude/settings.json` -- **do not overwrite** existing hooks; append to the
`PreToolUse` array if it already exists, and skip if an identical `Skill` matcher entry is already
present (idempotent):

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
    ]
  }
}
```

`async: true` is what guarantees no latency -- Claude Code does not wait for the script to finish.

## Step 4: Verify

1. Confirm the script exists and is executable at `~/.claude/hooks/skill-tally.py`.
2. Confirm the hook block is present in `~/.claude/settings.json`.
3. Simulate an invocation to prove the script works end-to-end:

   ```sh
   echo '{"tool_input":{"skill":"setup-skill-tally"}}' | python3 ~/.claude/hooks/skill-tally.py
   cat ~/.claude/skill-tally.json
   ```

   Confirm `setup-skill-tally` appears with a count. (The live hook takes effect on the **next**
   skill invocation after a session restart.)

Report that the tally is active and where to read it.

## Reading the tally

```sh
# most-used skills, descending
jq -r 'to_entries | sort_by(-.value)[] | "\(.value)\t\(.key)"' ~/.claude/skill-tally.json
```

## Uninstall

1. Remove the `Skill` matcher block from the `PreToolUse` array in `~/.claude/settings.json`.
2. Delete `~/.claude/hooks/skill-tally.py`.
3. Optionally delete `~/.claude/skill-tally.json` (and its `.lock`).

#!/usr/bin/env python3
"""Increment a per-skill invocation counter in ~/.claude/skill-tally.json.

Registered on two events, both async:true (fire-and-forget, never blocks):

  * PreToolUse / Skill   -- model-invoked skills (tool_input.skill)
  * UserPromptExpansion  -- user-typed slash commands (command name field)

The two paths are mutually exclusive: typing `/foo` expands inline without a
Skill tool call, and a model Skill tool call is not a user-typed command. So a
single invocation is counted exactly once regardless of who triggered it.

Skill names are normalised to their bare form (leading slash and `plugin:`
namespace stripped) so the same skill lands on one key no matter the path.

Any failure exits 0 silently -- a broken tally must never surface to the user.
When a UserPromptExpansion payload yields no recognisable command name, the raw
payload is appended to ~/.claude/skill-tally-debug.log so the actual field shape
can be confirmed without guesswork.
"""
import fcntl
import json
import os
import sys


def tally_path():
    return os.environ.get("SKILL_TALLY_FILE", os.path.expanduser("~/.claude/skill-tally.json"))


def debug_path():
    return os.environ.get("SKILL_TALLY_DEBUG", os.path.expanduser("~/.claude/skill-tally-debug.log"))


def normalise(name):
    """Strip a leading slash and any `plugin:` namespace -> bare skill name."""
    name = name.strip().lstrip("/")
    if ":" in name:
        name = name.split(":", 1)[1]
    return name


def extract_skill(data):
    # Model-invoked path: PreToolUse on the Skill tool.
    skill = (data.get("tool_input") or {}).get("skill")
    if skill:
        return normalise(skill)

    # User-typed path: UserPromptExpansion. The field name is not documented, so
    # try the plausible keys in order.
    for key in ("command_name", "command", "name"):
        value = data.get(key)
        if value:
            return normalise(value)

    return None


def main():
    raw = sys.stdin.read()
    data = json.loads(raw)
    skill = extract_skill(data)
    if not skill:
        # Only the expansion path is expected to fall through here; capture the
        # payload so the real field name can be confirmed.
        if data.get("hook_event_name") == "UserPromptExpansion":
            with open(debug_path(), "a") as log:
                log.write(raw.strip() + "\n")
        return

    path = tally_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            with open(path) as f:
                tally = json.load(f)
            if not isinstance(tally, dict):
                tally = {}
        except (FileNotFoundError, ValueError):
            tally = {}
        tally[skill] = tally.get(skill, 0) + 1
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(tally, f, indent=2, sort_keys=True)
        os.replace(tmp, path)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

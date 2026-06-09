#!/usr/bin/env python3
"""Increment a per-skill invocation counter in ~/.claude/skill-tally.json.

Registered as a PreToolUse hook on the Skill tool with async:true, so it runs
fire-and-forget and never blocks skill use. Any failure exits 0 silently -- a
broken tally must never surface to the user.
"""
import fcntl
import json
import os
import sys


def tally_path():
    return os.environ.get("SKILL_TALLY_FILE", os.path.expanduser("~/.claude/skill-tally.json"))


def main():
    raw = sys.stdin.read()
    skill = json.loads(raw).get("tool_input", {}).get("skill")
    if not skill:
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

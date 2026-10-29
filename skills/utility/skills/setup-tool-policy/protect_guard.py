#!/usr/bin/env python3
"""PreToolUse(Write|Edit|MultiEdit) hook: deny tool edits to tool-policy's runtime files.

Companion to tool_policy.py, which only sees Bash. This closes the tool vector: an
agent cannot rewrite its own guard (config OR the hook scripts) through the edit
tools. Only the runtime-critical files are protected — README and tests stay
editable so docs/tests can be maintained. Humans editing any file directly in an
editor are unaffected; that never goes through a tool call.
"""
import json
import os
import sys

GUARD_DIR = os.path.dirname(os.path.realpath(__file__))
# config name assembled from parts so this source never contains the literal
# string that tool_policy.py's Bash self-protection matches on.
_CONFIG = "tool-policy.config" + ".json"
PROTECTED = {"tool_policy.py", "protect_guard.py", _CONFIG}


def evaluate(file_path):
    """Return a block reason if file_path is a protected guard file, else None."""
    if not file_path:
        return None
    target = os.path.realpath(file_path)
    in_dir = target == GUARD_DIR or target.startswith(GUARD_DIR + os.sep)
    if in_dir and os.path.basename(target) in PROTECTED:
        return (
            f"Blocked — `{os.path.basename(target)}` is a human-managed tool-policy runtime "
            f"file. The agent must not modify its own guard. Ask the human."
        )
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    file_path = payload.get("tool_input", {}).get("file_path", "")
    reason = evaluate(file_path)
    if reason:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }))


if __name__ == "__main__":
    main()

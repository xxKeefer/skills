#!/usr/bin/env python3
"""PreToolUse(Bash) hook: deny a git commit whose message credits an AI tool.

Checks the command text, which holds -m messages and heredoc bodies, and the file that
-F or --file names. Fails open: bad input or an unreadable file allows the call.
"""
import json
import pathlib
import re
import shlex
import sys

TOOLS = r"(claude|anthropic|copilot|openai|chatgpt|gpt-?\d|codex|gemini|cursor|aider|devin)"
PATTERNS = [
    re.compile(r"co-authored-by:[^\n]*" + TOOLS, re.I),
    re.compile(r"generated (with|by)[^\n]{0,40}" + TOOLS, re.I),
    re.compile(r"noreply@anthropic\.com", re.I),
]
# git, any global options (-C <path>, -c <key=val>, --flag), then the commit subcommand
GIT_COMMIT = re.compile(r"\bgit(\s+-[cC]\s+\S+|\s+--[\w-]+(=\S+)?)*\s+commit\b")


def _message_files(command, cwd):
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []
    files = []
    for i, tok in enumerate(tokens):
        if tok in ("-F", "--file") and i + 1 < len(tokens):
            files.append(tokens[i + 1])
        elif tok.startswith("--file="):
            files.append(tok.split("=", 1)[1])
        elif tok.startswith("-F") and len(tok) > 2:
            files.append(tok[2:])
    return [pathlib.Path(cwd) / f for f in files if f != "-"]


def evaluate(command, cwd):
    if not GIT_COMMIT.search(command):
        return None
    texts = [command]
    for path in _message_files(command, cwd):
        try:
            texts.append(path.read_text())
        except (OSError, UnicodeDecodeError):
            pass
    for text in texts:
        for pattern in PATTERNS:
            match = pattern.search(text)
            if match:
                return (
                    f"AI attribution in the commit message: {match.group(0)!r}. "
                    "Remove that line and commit again. Add no other attribution."
                )
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    command = (payload.get("tool_input") or {}).get("command") or ""
    reason = evaluate(command, payload.get("cwd") or pathlib.Path.cwd())
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

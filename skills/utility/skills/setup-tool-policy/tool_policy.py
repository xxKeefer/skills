#!/usr/bin/env python3
"""PreToolUse(Bash) hook: redirect package-runner invocations and block disallowed commands.

Two jobs, both driven by tool-policy.config.json beside this file:

  1. Redirect — intercept runner shims (npx / pnpm exec / dlx / ...) and steer the
     tool they run toward a canonical command. Block-all + allowlist: anything
     intercepted that is not allowlisted is denied.
  2. Block — deny specific command prefixes outright (e.g. `git stash`), with a
     custom reason.

Both parse the actual command (quote-aware) and only act when a runner or blocked
command appears in COMMAND POSITION — at the start, or right after a shell operator
(&& || | ; ( )). A name appearing inside a string literal — a commit message, a
grep pattern — is never mistaken for a real invocation. That is the whole reason
this is a parser and not a `grep`.
"""
import json
import pathlib
import shlex
import sys

CONFIG_PATH = pathlib.Path(__file__).parent / "tool-policy.config.json"
PUNCT = ";&|()<>"
CONTROL = set(";&|()")  # operators that start a fresh command


def _tokenize(command):
    """Quote-aware tokens; shell operators (& | ; ( )) emitted as their own tokens."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=PUNCT)
    lexer.whitespace_split = True
    return list(lexer)


def _is_operator(token):
    return bool(token) and all(c in PUNCT for c in token)


def _is_control(token):
    return bool(token) and all(c in CONTROL for c in token)


def _command_starts(tokens):
    """Yield indices where a new command begins: at the start, or after a control operator."""
    at_command_start = True
    skip_next = False
    for i, tok in enumerate(tokens):
        if skip_next:  # token after a redirect operator is a filename, not a command
            skip_next = False
            at_command_start = False
            continue
        if _is_operator(tok):
            if _is_control(tok):
                at_command_start = True
            else:  # redirect (> <)
                skip_next = True
            continue
        if at_command_start:
            yield i
        at_command_start = False


def _runner_heads(config):
    """[(['pnpm','exec'], 'pnpm exec'), (['npx'], 'npx'), ...] longest first."""
    heads = [(r.split(), r) for r in config.get("runners", [])]
    return sorted(heads, key=lambda h: -len(h[0]))


def _first_arg(tokens, start):
    """First non-flag token at/after `start`."""
    for tok in tokens[start:]:
        if not tok.startswith("-"):
            return tok
    return None


def _find_invocations(tokens, heads):
    """Yield (runner_label, tool, subcommand) for each runner in command position."""
    invocations = []
    for i in _command_starts(tokens):
        for words, label in heads:
            if tokens[i : i + len(words)] == words:
                tool = _first_arg(tokens, i + len(words))
                if tool is not None:
                    tool_idx = tokens.index(tool, i + len(words))
                    sub = _first_arg(tokens, tool_idx + 1)
                    invocations.append((label, tool, sub))
                break
    return invocations


def _find_blocked(tokens, blocked):
    """Return (matched_label, reason) for the first blocked-command prefix in command position."""
    for i in _command_starts(tokens):
        for seq, label, reason in blocked:
            if tokens[i : i + len(seq)] == seq:
                return label, reason
    return None


def _allowed(tool, sub, allowlist):
    if tool in allowlist:
        return True
    return sub is not None and f"{tool}:{sub}" in allowlist


def _blocked_specs(config):
    """[(['git','stash'], 'git stash', reason), ...] from config.blockedCommands."""
    specs = []
    for entry in config.get("blockedCommands", []):
        match = entry.get("match") if isinstance(entry, dict) else None
        if not match:
            continue
        try:
            seq = _tokenize(match)
        except ValueError:
            continue
        if seq:
            specs.append((seq, match, entry.get("reason", f"Blocked — `{match}` is disallowed here.")))
    return specs


def evaluate(command, config):
    """Return a block reason string, or None to allow the command."""
    # Self-protection: the config is human-managed. Any command that so much as
    # names the config file is rejected — the agent must never touch its own guard.
    if CONFIG_PATH.name in command:
        return (
            f"Blocked — `{CONFIG_PATH.name}` is human-managed. The agent must not read or "
            f"modify the tool-policy config. Ask the human to make the change."
        )

    try:
        tokens = _tokenize(command)
    except ValueError:
        return None  # unparseable (e.g. stray quote): fail open, never false-block

    hit = _find_blocked(tokens, _blocked_specs(config))
    if hit:
        label, reason = hit
        return f"Blocked `{label}` — {reason}"

    allowlist = set(config.get("allowlist", []))
    redirects = config.get("redirects", {})

    for label, tool, sub in _find_invocations(tokens, _runner_heads(config)):
        if _allowed(tool, sub, allowlist):
            continue
        if tool in redirects:
            return (
                f"Don't run `{tool}` via `{label}` in this project.\n"
                f"Use the canonical command instead:  {redirects[tool]}"
            )
        return (
            f"Blocked `{label} {tool}` — this project routes tooling through canonical commands, "
            f"not package-runner shims.\n"
            f"• If there's a canonical target for it, use that instead.\n"
            f"• If `{tool}` is a legitimate one-off with no equivalent, do NOT edit the config "
            f"yourself — stop and ask the human to allowlist it in {CONFIG_PATH.name}."
        )
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    command = payload.get("tool_input", {}).get("command", "")
    if not command:
        return
    try:
        config = json.loads(CONFIG_PATH.read_text())
    except (OSError, ValueError):
        return  # no/broken config: do nothing rather than blocking everything

    reason = evaluate(command, config)
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

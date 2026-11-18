# import-nudge

A `PostToolUse` hook for `Write|Edit|MultiEdit`. After an edit, it reads the edited file. When the
file path and the file text both match a rule, it adds the rule's message to the agent's context.
It never blocks.

Use it for a pattern that a repo rule bans but that many old files still hold, so a lint ban would
fail. An example is an old test harness that reviewers ask you to replace before you add cases.

## Files

| File | Job |
| --- | --- |
| `import_nudge.py` | The hook script. |
| `import-nudge.config.json` | The live rules. Ships with no rules. |
| `import-nudge.example.json` | A rule to copy. The hook does not read it. |
| `import_nudge_test.py` | Tests. Run `python3 import_nudge_test.py`. Not installed. |

## Wiring

Run `/setup-import-nudge`, or add this entry to a settings file by hand:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/import-nudge/import_nudge.py" }]
      }
    ]
  }
}
```

## Config

`import-nudge.config.json` sits beside the script:

```json
{ "rules": [{ "path": "<regex on the absolute path>", "content": "<regex on the file text>", "message": "<text for the agent>" }] }
```

Each rule needs both regexes to match. The hook joins the messages of all matching rules.

## Behaviour

- Fail-open. A bad payload, a missing or broken config, a bad regex, or a missing file gives no
  output.
- Output: `{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "<path>: <messages>"}}`.

# setup-skill-tally

A zero-latency Claude Code hook that counts every skill invocation into a global JSON tally.

- **Tally file:** `~/.claude/skill-tally.json` — shape `{ "plugin:skill": count }`
- **Mechanism:** `PreToolUse` hook on the `Skill` tool with `async: true` (fire-and-forget → no latency)
- **Counts:** all invocations — user-typed `/foo`, model-auto-invoked, and `/plugin:skill`
- **Dependency:** `python3` (stdlib only; chosen because macOS lacks `flock(1)`)

The easiest install is to run the skill: **`/setup-skill-tally`**. The steps below are the manual
equivalent.

## Manual install

1. Copy the script and make it executable:

   ```sh
   mkdir -p ~/.claude/hooks
   cp scripts/skill-tally.py ~/.claude/hooks/skill-tally.py
   chmod +x ~/.claude/hooks/skill-tally.py
   ```

2. Merge this into `~/.claude/settings.json` (append to `PreToolUse` if it already exists; do not
   overwrite):

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Skill",
           "hooks": [
             { "type": "command", "command": "python3 ~/.claude/hooks/skill-tally.py", "async": true }
           ]
         }
       ]
     }
   }
   ```

3. Restart the session. The tally starts on the next skill invocation.

## Verify

```sh
echo '{"tool_input":{"skill":"setup-skill-tally"}}' | python3 ~/.claude/hooks/skill-tally.py
cat ~/.claude/skill-tally.json
```

## Read the tally

```sh
# most-used skills, descending
jq -r 'to_entries | sort_by(-.value)[] | "\(.value)\t\(.key)"' ~/.claude/skill-tally.json
```

## Uninstall

1. Remove the `Skill` matcher block from `PreToolUse` in `~/.claude/settings.json`.
2. `rm ~/.claude/hooks/skill-tally.py`
3. Optionally `rm ~/.claude/skill-tally.json ~/.claude/skill-tally.json.lock`

## Tests

```sh
python3 scripts/skill-tally.spec.py
```

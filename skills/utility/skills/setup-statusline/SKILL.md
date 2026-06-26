---
name: setup-statusline
description: >
  Install the hand-rolled, self-contained Claude Code status line from this marketplace's
  statusline/statusline.sh to ~/.claude/ and wire it into ~/.claude/settings.json. Zero network,
  no remote packages. Use when the user says "setup statusline", "install statusline",
  "set up my status line", or wants the same status line on home and work machines.
---

# Setup Statusline

Install the version-controlled status line (`statusline/statusline.sh` at the marketplace root) to
`~/.claude/statusline.sh` and point Claude Code's `statusLine` setting at it. The script is
self-contained -- it reads the statusLine stdin JSON and local `git` only, makes **no network calls
and runs no remote packages**. The goal is an identical status line on every machine, installed from
one committed source.

It renders two lines:

- Line 1: git branch, then fish-style abbreviated cwd.
- Line 2: context battery, context tokens (%), then ◀ session (5h) usage (reset) and ▶ weekly
  (7d) usage (reset). The session/weekly widgets come from stdin `rate_limits` and are dropped
  cleanly when absent (API-key auth, or before the first API response).

Thresholds, the delimiter, and the usage symbols are read from `statusline.config.json` (sits next
to the script); any omitted key falls back to an in-script default.

The source of truth is the top-level `statusline/statusline.sh` plus `statusline.config.json`,
**not** a copy bundled in this skill. This install copies both out to `~/.claude/`.

## Step 1: Check Prerequisites

Confirm `jq` is available (the script parses stdin JSON with it):

```sh
command -v jq
```

If absent, stop and tell the user to install it (`brew install jq`). `git` is also required but is
assumed present.

## Step 2: Locate the Source Script

The source lives at the marketplace root, four levels up from this skill
(`skills/utility/skills/setup-statusline/`). Resolve it relative to this `SKILL.md`'s directory so
the install works from any cwd:

```sh
# from the skill directory:
srcdir="$(cd "$(dirname "$0")/../../../../statusline" && pwd)"
```

When running the steps interactively, the equivalent is the repo's `statusline/` directory. Confirm
`$srcdir/statusline.sh` exists and is non-empty before copying.

## Step 3: Install the Script and Config

Copy the script to `~/.claude/statusline.sh` and make it executable:

```sh
cp "$srcdir/statusline.sh" ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

Install the config **only if it is not already there**, so a user's customizations survive re-runs:

```sh
[ -f ~/.claude/statusline.config.json ] || cp "$srcdir/statusline.config.json" ~/.claude/statusline.config.json
```

The script resolves the config next to itself (`~/.claude/statusline.config.json`). Every key is
optional — if the file is missing entirely the script falls back to its in-script defaults.

## Step 4: Wire the Setting

Set `.statusLine` in `~/.claude/settings.json` to run the installed script, **without clobbering
unrelated settings**. Create the file as `{}` first if it does not exist. This is idempotent --
re-running sets the same value:

```sh
settings=~/.claude/settings.json
[ -f "$settings" ] || echo '{}' > "$settings"
tmp=$(mktemp)
jq '.statusLine = {type: "command", command: "bash ~/.claude/statusline.sh"}' "$settings" > "$tmp" \
  && mv "$tmp" "$settings"
```

## Step 5: Verify

1. Confirm the script exists and is executable at `~/.claude/statusline.sh`, and that
   `~/.claude/statusline.config.json` is present.
2. Confirm `.statusLine.command` in `~/.claude/settings.json` is `bash ~/.claude/statusline.sh`.
3. Prove it renders end-to-end with a sample payload (rate_limits present, then absent):

   ```sh
   now=$(date +%s)
   jq -nc --argjson sr "$((now+3600))" --argjson wr "$((now+86400))" \
     '{cwd:"'"$HOME"'", model:{id:"claude-opus-4-8[1m]"},
       rate_limits:{five_hour:{used_percentage:23.5,resets_at:$sr},
                    seven_day:{used_percentage:41.2,resets_at:$wr}}}' \
     | bash ~/.claude/statusline.sh
   echo

   jq -nc '{cwd:"'"$HOME"'", model:{id:"claude-sonnet-4-6"}}' | bash ~/.claude/statusline.sh
   ```

   The first renders both usage widgets; the second omits them with no error and no empty parens.

The new status line takes effect on the **next** session (or status-line refresh).

## Uninstall

1. Remove the `statusLine` key from `~/.claude/settings.json`:

   ```sh
   tmp=$(mktemp); jq 'del(.statusLine)' ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json
   ```

2. `rm ~/.claude/statusline.sh ~/.claude/statusline.config.json`

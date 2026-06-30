---
name: install-agent-voice
description: >
  Install the version-controlled Terse output style from this marketplace's output-styles/Terse.md
  to ~/.claude/output-styles/ and select it in ~/.claude/settings.json. The agent voice, identical
  on every machine, from one committed source. Use when the user says "install agent voice",
  "install my output style", "set up the terse voice", or wants the same agent voice everywhere.
---

# Install Agent Voice

Install the version-controlled output style (`output-styles/Terse.md` at the marketplace root) to
`~/.claude/output-styles/Terse.md` and point Claude Code's `outputStyle` setting at it. The goal is
an identical agent voice on every machine, installed from one committed source.

The source of truth is the top-level `output-styles/Terse.md`, **not** a copy bundled in this skill.
This install copies it out to `~/.claude/output-styles/` and selects it by its frontmatter `name`.

## Step 1: Locate the Source File

The source lives at the marketplace root, four levels up from this skill
(`skills/utility/skills/install-agent-voice/`). Resolve it relative to this `SKILL.md`'s directory so
the install works from any cwd:

```sh
srcdir="$(cd "$(dirname "$0")/../../../../output-styles" && pwd)"
```

When running the steps interactively, the equivalent is the repo's `output-styles/` directory.
Confirm `$srcdir/Terse.md` exists and is non-empty before copying.

## Step 2: Read the Style Name

Claude Code selects an output style by its frontmatter `name:`, not its filename. Read that value
from the source so a rename of the style survives without editing this skill:

```sh
style_name="$(awk -F': *' '/^name:/{print $2; exit}' "$srcdir/Terse.md")"
```

`Terse.md` declares `name: terse`, so `style_name` resolves to `terse`.

## Step 3: Install the Style

Copy the file into the user's output-styles directory, creating it if needed. The source is
authoritative — overwrite on re-run:

```sh
mkdir -p ~/.claude/output-styles
cp "$srcdir/Terse.md" ~/.claude/output-styles/Terse.md
```

## Step 4: Wire the Setting

Set `.outputStyle` in `~/.claude/settings.json` to the style name, **without clobbering unrelated
settings**. Create the file as `{}` first if it does not exist. This is idempotent — re-running sets
the same value:

```sh
settings=~/.claude/settings.json
[ -f "$settings" ] || echo '{}' > "$settings"
tmp=$(mktemp)
jq --arg name "$style_name" '.outputStyle = $name' "$settings" > "$tmp" && mv "$tmp" "$settings"
```

## Step 5: Verify

1. Confirm the file exists at `~/.claude/output-styles/Terse.md`.
2. Confirm `.outputStyle` in `~/.claude/settings.json` equals the style name (`terse`):

   ```sh
   jq -r '.outputStyle' ~/.claude/settings.json
   ```

3. Confirm that value matches the source frontmatter `name:` (the two must agree, or the style won't
   resolve):

   ```sh
   awk -F': *' '/^name:/{print $2; exit}' ~/.claude/output-styles/Terse.md
   ```

The new voice takes effect on the **next** session.

## Uninstall

1. Remove the `outputStyle` key from `~/.claude/settings.json` (reverts to the default voice):

   ```sh
   tmp=$(mktemp); jq 'del(.outputStyle)' ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json
   ```

2. `rm ~/.claude/output-styles/Terse.md`

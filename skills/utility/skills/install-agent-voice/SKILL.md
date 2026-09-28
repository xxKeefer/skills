---
name: install-agent-voice
description: >
  Install every version-controlled output style from this marketplace's output-styles/ directory
  to ~/.claude/output-styles/, then select one in ~/.claude/settings.json. The agent voices,
  identical on every machine, from one committed source. Use when the user says "install agent
  voice", "install my output styles", "set up the terse voice", or wants the same agent voices
  everywhere.
---

# Install Agent Voice

Install every version-controlled output style in `output-styles/` at the marketplace root to
`~/.claude/output-styles/`, then point Claude Code's `outputStyle` setting at one of them. The goal
is identical agent voices on every machine, installed from one committed source.

The source of truth is the top-level `output-styles/` directory, **not** copies bundled in this
skill. This install copies every `.md` file out to `~/.claude/output-styles/` and selects one by its
frontmatter `name`.

## Step 1: Locate the Source Directory

The source lives at the marketplace root, four levels up from this skill
(`skills/utility/skills/install-agent-voice/`). Resolve it relative to this `SKILL.md`'s directory so
the install works from any cwd:

```sh
srcdir="$(cd "$(dirname "$0")/../../../../output-styles" && pwd)"
```

When running the steps interactively, the equivalent is the repo's `output-styles/` directory.
Confirm it exists and contains at least one `.md` file before copying.

## Step 2: Install All Styles

Copy every style file into the user's output-styles directory, creating it if needed. The source is
authoritative — overwrite on re-run:

```sh
mkdir -p ~/.claude/output-styles
cp "$srcdir"/*.md ~/.claude/output-styles/
```

## Step 3: Pick the Style to Select

List the installed styles by their frontmatter `name:` (not filename — that's what Claude Code
resolves by):

```sh
for f in "$srcdir"/*.md; do
  awk -F': *' -v file="$f" '/^name:/{print $2 "  (" file ")"; exit}' "$f"
done
```

If the user named a specific style ("install my terse voice"), use that one. Otherwise ask which of
the installed styles to activate — default to `terse` if the user has no preference.

## Step 4: Wire the Setting

Set `.outputStyle` in `~/.claude/settings.json` to the chosen style's name, **without clobbering
unrelated settings**. Create the file as `{}` first if it does not exist. This is idempotent —
re-running sets the same value:

```sh
settings=~/.claude/settings.json
[ -f "$settings" ] || echo '{}' > "$settings"
tmp=$(mktemp)
jq --arg name "$style_name" '.outputStyle = $name' "$settings" > "$tmp" && mv "$tmp" "$settings"
```

## Step 5: Verify

1. Confirm all source files landed in `~/.claude/output-styles/`:

   ```sh
   diff <(ls "$srcdir") <(ls ~/.claude/output-styles/)
   ```

2. Confirm `.outputStyle` in `~/.claude/settings.json` equals the chosen style's name:

   ```sh
   jq -r '.outputStyle' ~/.claude/settings.json
   ```

3. Confirm that value matches the corresponding source file's frontmatter `name:` (the two must
   agree, or the style won't resolve).

The new voice takes effect on the **next** session.

## Uninstall

1. Remove the `outputStyle` key from `~/.claude/settings.json` (reverts to the default voice):

   ```sh
   tmp=$(mktemp); jq 'del(.outputStyle)' ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json
   ```

2. Remove the installed style files, e.g. `rm ~/.claude/output-styles/{Terse,Orwells-Six,Simplified-Technical,Proof-Read}.md`
   — or all of them: `rm ~/.claude/output-styles/*.md` (only if none were added manually).

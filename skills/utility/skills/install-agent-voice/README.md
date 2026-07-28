# install-agent-voice

Installs every version-controlled output style onto a machine and selects one in
`~/.claude/settings.json`. The goal: identical agent voices on home and work, from one committed
source.

- **Source:** `output-styles/*.md` (marketplace root — single source of truth)
- **Installs to:** `~/.claude/output-styles/` (all files)
- **Wires:** `.outputStyle` in `~/.claude/settings.json` → the chosen style's frontmatter `name`
- **Dependency:** `jq` (settings JSON edit)

The easiest install is to run the skill: **`/install-agent-voice`**. The steps below are the manual
equivalent.

## Manual install

```sh
# 1. copy all styles out
mkdir -p ~/.claude/output-styles
cp output-styles/*.md ~/.claude/output-styles/

# 2. select one by its frontmatter name, without clobbering anything else (idempotent)
settings=~/.claude/settings.json
[ -f "$settings" ] || echo '{}' > "$settings"
tmp=$(mktemp)
jq '.outputStyle = "terse"' "$settings" > "$tmp" && mv "$tmp" "$settings"
```

Restart the session for it to take effect.

## Why the name, not the filename

Claude Code resolves output styles by the frontmatter `name:` field, not the filename. `Terse.md`
declares `name: terse`, so `.outputStyle` must be `"terse"`. Rename a style and the two must stay
in agreement.

## Uninstall

```sh
tmp=$(mktemp); jq 'del(.outputStyle)' ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json
rm ~/.claude/output-styles/*.md
```

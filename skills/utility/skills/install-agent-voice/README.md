# install-agent-voice

Installs the version-controlled Terse output style onto a machine and selects it in
`~/.claude/settings.json`. The goal: an identical agent voice on home and work, from one committed
source.

- **Source:** `output-styles/Terse.md` (marketplace root — single source of truth)
- **Installs to:** `~/.claude/output-styles/Terse.md`
- **Wires:** `.outputStyle` in `~/.claude/settings.json` → the style's frontmatter `name` (`terse`)
- **Dependency:** `jq` (settings JSON edit)

The easiest install is to run the skill: **`/install-agent-voice`**. The steps below are the manual
equivalent.

## Manual install

```sh
# 1. copy the style out
mkdir -p ~/.claude/output-styles
cp output-styles/Terse.md ~/.claude/output-styles/Terse.md

# 2. select it by its frontmatter name, without clobbering anything else (idempotent)
settings=~/.claude/settings.json
[ -f "$settings" ] || echo '{}' > "$settings"
tmp=$(mktemp)
jq '.outputStyle = "terse"' "$settings" > "$tmp" && mv "$tmp" "$settings"
```

Restart the session for it to take effect.

## Why the name, not the filename

Claude Code resolves output styles by the frontmatter `name:` field, not the filename. `Terse.md`
declares `name: terse`, so `.outputStyle` must be `"terse"`. Rename the style and the two must stay
in agreement.

## Uninstall

```sh
tmp=$(mktemp); jq 'del(.outputStyle)' ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json
rm ~/.claude/output-styles/Terse.md
```

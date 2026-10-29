# setup-statusline

Installs the hand-rolled, self-contained Claude Code status line onto a machine and wires it into
`~/.claude/settings.json`. The goal: an identical status line on home and work, from one committed
source, with zero network calls and no remote package execution.

It reads the statusLine stdin JSON and local `git` only. This replaces `ccstatusline`
(`npx ccstatusline@latest`), which was retired for fetching and running unvetted remote code on
every invocation.

- **Source:** `statusline.sh` + `statusline.config.json` in this folder (single source of truth)
- **Installs to:** `~/.claude/statusline.sh` (+ `~/.claude/statusline.config.json` if absent)
- **Wires:** `.statusLine` in `~/.claude/settings.json` → `bash ~/.claude/statusline.sh`
- **Dependency:** `jq` (stdin JSON parsing); `git` (branch)

The easiest install is to run the skill: **`/setup-statusline`**. The steps below are the manual
equivalent.

## Manual install

Run from this folder:

```sh
# 1. copy the script out and make it executable
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh

# 2. install the config only if absent (preserves your customizations on re-run)
[ -f ~/.claude/statusline.config.json ] || cp statusline.config.json ~/.claude/statusline.config.json

# 3. wire the setting without clobbering anything else (idempotent)
settings=~/.claude/settings.json
[ -f "$settings" ] || echo '{}' > "$settings"
tmp=$(mktemp)
jq '.statusLine = {type: "command", command: "bash ~/.claude/statusline.sh"}' "$settings" > "$tmp" && mv "$tmp" "$settings"
```

Restart the session (or wait for a status-line refresh) for it to take effect.

## What it shows

- **Line 1:** git branch · fish-style abbreviated cwd
- **Line 2:** context battery · context tokens (%) · ◀ 5h usage % (reset) · ▶ 7d usage % (reset)

| Element | Source |
|---|---|
| cwd | stdin `.cwd` / `.workspace.current_dir`, fish-abbreviated, dimmed |
| git branch | `git -C "$cwd" branch --show-current` |
| Context battery | `████ <80k → ███▒ <100k → ██▒▒ <110k → █▒▒▒` on context tokens, cells coloured to match |
| Context tokens + % | last `.message.usage` summed from the `transcript_path` JSONL; `ctx_max` 1M vs 200k from `model.id` |
| ◀ / ▶ usage + reset | stdin `rate_limits.{five_hour,seven_day}.{used_percentage,resets_at}` |

Two colour ladders signal severity: context tokens go green → yellow → amber → red across the
`80k / 100k / 110k` zone thresholds, usage percentages go green `<60` → yellow `<75` → amber `<90`
→ red. The ◀/▶ widgets read stdin `rate_limits` (Claude Code ≥ v2.1.80, Pro/Max only) and are
dropped cleanly when absent. Usage is shown as a percentage — stdin exposes `used_percentage`, not
raw tokens.

## Customization

Emoji, thresholds, and the segment delimiter live in `~/.claude/statusline.config.json` (string and
number values only). Edit it directly — no re-install needed. Any omitted key falls back to an
in-script default, so the script still renders with no config at all. The battery glyphs are fixed
in the script.

```json
{
  "delimiter": "·",
  "smart_zone": {
    "token_count": { "smart": 80000, "good": 100000, "poor": 110000 }
  },
  "usage": {
    "pct_green_max": 60, "pct_yellow_max": 75, "pct_amber_max": 90,
    "symbol": { "session": "◀", "weekly": "▶" }
  }
}
```

| Key | Controls |
|---|---|
| `delimiter` | separator drawn between segments |
| `smart_zone.token_count.{smart,good,poor}` | context-token thresholds for the battery and colour ladder |
| `usage.pct_{green,yellow,amber}_max` | upper bound of each usage-percentage colour band |
| `usage.symbol.{session,weekly}` | the 5h / 7d widget symbols |

The rest is tuned in `statusline.sh`: `ctx_max` (1,000,000 for `*1m*` model ids, else 200,000) and
the `fmt_reset` timer format (`Nd Nh` / `Nh Nm` / `Nm`).

## Verify

```sh
now=$(date +%s)
jq -nc --argjson sr "$((now+3600))" --argjson wr "$((now+86400))" \
  '{cwd:"'"$HOME"'", model:{id:"claude-opus-4-8[1m]"},
    rate_limits:{five_hour:{used_percentage:23.5,resets_at:$sr},seven_day:{used_percentage:41.2,resets_at:$wr}}}' \
  | bash ~/.claude/statusline.sh
```

## Uninstall

```sh
tmp=$(mktemp); jq 'del(.statusLine)' ~/.claude/settings.json > "$tmp" && mv "$tmp" ~/.claude/settings.json
rm ~/.claude/statusline.sh ~/.claude/statusline.config.json
```

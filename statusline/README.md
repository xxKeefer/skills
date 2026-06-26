# statusline

`statusline.sh` — a hand-rolled, self-contained Claude Code status line. The single committed
source, installed identically on every machine by [`/setup-statusline`](../skills/utility/skills/setup-statusline/).

It reads the statusLine stdin JSON and local `git` only: **no network calls, no remote package
execution.** This replaces `ccstatusline` (`npx ccstatusline@latest`), which was retired for
fetching and running unvetted remote code on every invocation.

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

Two colour ladders signal severity:

- **Context tokens** — green → yellow → amber → red across the same `80k / 100k / 110k` zone thresholds as the battery cells.
- **Usage percentages** — green `<60` → yellow `<75` → amber `<90` → red.

The ◀/▶ widgets need Claude Code ≥ v2.1.80 and Pro/Max auth; each window is dropped cleanly when
absent (API-key auth, or before the first API response of a session). Usage is a **percentage** —
stdin exposes `used_percentage`, not raw token counts.

## Install

```sh
/setup-statusline
```

Or manually: copy `statusline.sh` to `~/.claude/statusline.sh`, `chmod +x`, and set `.statusLine`
in `~/.claude/settings.json` to `{ "type": "command", "command": "bash ~/.claude/statusline.sh" }`.
See the [skill README](../skills/utility/skills/setup-statusline/README.md) for the full procedure.

## Customization

Thresholds, the segment delimiter, and the usage symbols are read from `statusline.config.json`,
resolved next to the script (`~/.claude/statusline.config.json` once installed). Every key is
optional — any omitted key falls back to the in-script default, so the script still renders with no
config at all. Values are strings or numbers only. The battery glyphs are fixed in the script.

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

The remaining tuning lives in `statusline.sh`: `ctx_max` (1M for `*1m*` model ids, else 200,000) and
the `fmt_reset` timer format (`Nd Nh` / `Nh Nm` / `Nm`).

## Dependencies

`jq` (stdin JSON parsing), `git` (branch). No others.

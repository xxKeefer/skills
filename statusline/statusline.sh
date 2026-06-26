#!/usr/bin/env bash
# Hand-rolled Claude Code status line. Self-contained: reads the statusLine JSON on
# stdin and local git only -- no network, no npx, no third-party packages.
#
# Line 1: git branch | fish-style abbreviated cwd.
# Line 2: context-emoji context-tokens (%) | ⏰ session % (reset) | 📅 weekly % (reset)
#
# Session/weekly widgets read stdin .rate_limits (Claude Code >= v2.1.80, Pro/Max only).
# When .rate_limits is absent (API-key auth, or before the first API response) the
# affected widgets are dropped and the line still renders cleanly.

set -u

input=$(cat)

DIM=$'\033[90m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
AMBER=$'\033[38;5;208m'
RED=$'\033[31m'
MAGENTA=$'\033[95m'
BOLD=$'\033[1m'
RESET=$'\033[0m'

# --- config: defaults here; statusline.config.json (next to this script) overrides ---
DELIM='|'
TOK_ZONE_1=80000; TOK_ZONE_2=100000; TOK_ZONE_3=110000
TOK_EMOJI_1='🤓'; TOK_EMOJI_2='🤯'; TOK_EMOJI_3='😵‍💫'; TOK_EMOJI_4='💀'
PCT_GREEN=60; PCT_YELLOW=75; PCT_AMBER=90
SESSION_EMOJI='⏰'; WEEKLY_EMOJI='📅'

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)
config="$script_dir/statusline.config.json"
if [ -f "$config" ]; then
  # One value per line (empties preserved); tab-splitting collapses empty columns and
  # readarray is bash-4-only -- this while-read loop works on macOS bash 3.2.
  cfg=()
  while IFS= read -r line; do cfg+=("$line"); done < <(jq -r '
    [
      (.delimiter                  // ""),
      (.smart_zone.token_count.smart // ""), (.smart_zone.token_count.good // ""), (.smart_zone.token_count.poor // ""),
      (.smart_zone.emoji.smart     // ""), (.smart_zone.emoji.good // ""), (.smart_zone.emoji.poor // ""), (.smart_zone.emoji.dumb // ""),
      (.usage.pct_green_max       // ""), (.usage.pct_yellow_max // ""), (.usage.pct_amber_max // ""),
      (.usage.emoji.session       // ""), (.usage.emoji.weekly // "")
    ] | .[]' "$config" 2>/dev/null)
  [ -n "${cfg[0]:-}" ] && DELIM=${cfg[0]}
  [ -n "${cfg[1]:-}"  ] && TOK_ZONE_1=${cfg[1]}
  [ -n "${cfg[2]:-}"  ] && TOK_ZONE_2=${cfg[2]}
  [ -n "${cfg[3]:-}"  ] && TOK_ZONE_3=${cfg[3]}
  [ -n "${cfg[4]:-}"  ] && TOK_EMOJI_1=${cfg[4]}
  [ -n "${cfg[5]:-}"  ] && TOK_EMOJI_2=${cfg[5]}
  [ -n "${cfg[6]:-}"  ] && TOK_EMOJI_3=${cfg[6]}
  [ -n "${cfg[7]:-}"  ] && TOK_EMOJI_4=${cfg[7]}
  [ -n "${cfg[8]:-}"  ] && PCT_GREEN=${cfg[8]}
  [ -n "${cfg[9]:-}"  ] && PCT_YELLOW=${cfg[9]}
  [ -n "${cfg[10]:-}" ] && PCT_AMBER=${cfg[10]}
  [ -n "${cfg[11]:-}" ] && SESSION_EMOJI=${cfg[11]}
  [ -n "${cfg[12]:-}" ] && WEEKLY_EMOJI=${cfg[12]}
fi

# Colour ladder for context tokens -- mirrors the smart/dumb-zone emoji thresholds.
token_colour() {
  if   [ "$1" -lt "$TOK_ZONE_1" ]; then printf '%s' "$GREEN"
  elif [ "$1" -lt "$TOK_ZONE_2" ]; then printf '%s' "$YELLOW"
  elif [ "$1" -lt "$TOK_ZONE_3" ]; then printf '%s' "$AMBER"
  else                                  printf '%s' "$RED"
  fi
}

# Colour ladder for usage percentages: green/yellow/amber/red by configurable bands.
pct_colour() {
  if   [ "$1" -lt "$PCT_GREEN" ];  then printf '%s' "$GREEN"
  elif [ "$1" -lt "$PCT_YELLOW" ]; then printf '%s' "$YELLOW"
  elif [ "$1" -lt "$PCT_AMBER" ];  then printf '%s' "$AMBER"
  else                                  printf '%s' "$RED"
  fi
}

cwd=$(jq -r '.cwd // .workspace.current_dir // ""' <<<"$input")
transcript=$(jq -r '.transcript_path // ""' <<<"$input")
model_id=$(jq -r '.model.id // ""' <<<"$input")

case "$model_id" in
  *1m*|*1M*) ctx_max=1000000 ;;
  *)        ctx_max=200000 ;;
esac

reverse_file() {
  if command -v tac >/dev/null 2>&1; then tac "$1"
  else tail -r "$1"
  fi
}

# --- context window: sum last message.usage from the transcript JSONL ---
tokens=0
if [ -n "$transcript" ] && [ -f "$transcript" ]; then
  t=$(reverse_file "$transcript" 2>/dev/null | jq -r '
    select(.message?.usage?) |
    .message.usage |
    (.input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0)
  ' 2>/dev/null | head -n 1)
  [ -n "$t" ] && tokens=$t
fi

if   [ "$tokens" -lt "$TOK_ZONE_1" ]; then emoji="$TOK_EMOJI_1"
elif [ "$tokens" -lt "$TOK_ZONE_2" ]; then emoji="$TOK_EMOJI_2"
elif [ "$tokens" -lt "$TOK_ZONE_3" ]; then emoji="$TOK_EMOJI_3"
else                                       emoji="$TOK_EMOJI_4"
fi

pct=$(( tokens * 100 / ctx_max ))
tokens_fmt=$(LC_ALL=en_US.UTF-8 printf "%'d" "$tokens" 2>/dev/null || printf '%d' "$tokens")

# --- git branch ---
branch=""
if [ -n "$cwd" ] && [ -d "$cwd" ]; then
  branch=$(git -C "$cwd" branch --show-current 2>/dev/null)
fi

# --- fish-style cwd: abbreviate every dir but the last to its first char ---
fish_cwd() {
  local p="$1"
  if [ -n "$HOME" ] && [ "${p#$HOME}" != "$p" ]; then
    p="~${p#$HOME}"
  fi
  local IFS='/'
  read -ra parts <<<"$p"
  local last=$(( ${#parts[@]} - 1 ))
  local out=""
  local i
  for i in "${!parts[@]}"; do
    if [ "$i" -eq "$last" ] || [ -z "${parts[$i]}" ]; then
      out+="${parts[$i]}"
    else
      out+="${parts[$i]:0:1}"
    fi
    [ "$i" -lt "$last" ] && out+="/"
  done
  printf '%s' "$out"
}

# --- reset timer: epoch seconds -> compact "Nd Nh" / "Nh Nm" / "Nm" remaining ---
fmt_reset() {
  local target="$1"
  local now remaining d h m
  now=$(date +%s)
  remaining=$(( target - now ))
  [ "$remaining" -lt 0 ] && remaining=0
  d=$(( remaining / 86400 ))
  h=$(( (remaining % 86400) / 3600 ))
  m=$(( (remaining % 3600) / 60 ))
  if   [ "$d" -gt 0 ]; then printf '%dd %dh' "$d" "$h"
  elif [ "$h" -gt 0 ]; then printf '%dh %dm' "$h" "$m"
  else                      printf '%dm' "$m"
  fi
}

# --- usage widget: colour the percentage by severity, append reset timer ---
usage_widget() {
  local label="$1" used="$2" resets_at="$3"
  local used_int colour reset
  used_int=${used%.*}
  [ -z "$used_int" ] && used_int=0
  colour=$(pct_colour "$used_int")
  reset=""
  if [ -n "$resets_at" ] && [ "$resets_at" != "null" ]; then
    reset=" ${DIM}($(fmt_reset "$resets_at"))${RESET}"
  fi
  printf '%s %s%s%%%s%s' "$label" "$colour" "$used_int" "$RESET" "$reset"
}

session_used=$(jq -r '.rate_limits.five_hour.used_percentage // empty' <<<"$input")
session_reset=$(jq -r '.rate_limits.five_hour.resets_at // empty' <<<"$input")
weekly_used=$(jq -r '.rate_limits.seven_day.used_percentage // empty' <<<"$input")
weekly_reset=$(jq -r '.rate_limits.seven_day.resets_at // empty' <<<"$input")

# --- assemble ---
sep=" ${DIM}${DELIM}${RESET} "
line1=""
[ -n "$branch" ] && line1="${MAGENTA}${branch}${RESET}${sep}"
line1+="${DIM}$(fish_cwd "$cwd")${RESET}"

tok_col=$(token_colour "$tokens")
line2="${emoji} ${BOLD}${tok_col}${tokens_fmt}${RESET} ${DIM}(${pct}%)${RESET}"
[ -n "$session_used" ] && line2+="${sep}$(usage_widget "$SESSION_EMOJI" "$session_used" "$session_reset")"
[ -n "$weekly_used" ]  && line2+="${sep}$(usage_widget "$WEEKLY_EMOJI" "$weekly_used" "$weekly_reset")"

printf '%s\n%s' "$line1" "$line2"

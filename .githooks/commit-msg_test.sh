#!/bin/sh
set -u

src=$(cd "$(dirname "$0")" && pwd)
root=$(mktemp -d)
trap 'rm -rf "$root"' EXIT
failed=0
n=0

try_message() {
  n=$((n + 1))
  file="$root/msg$n"
  printf '%b' "$1" > "$file"
  sh "$src/commit-msg" "$file" > /dev/null 2>&1
}

expect() {
  got=pass
  [ "$3" -eq 0 ] || got=block
  if [ "$got" = "$2" ]; then
    echo "ok   $1"
  else
    echo "FAIL $1: want $2, got $got"
    failed=1
  fi
}

try_message 'feat(engineering): add a skill\n'
expect 'a plain message passes' pass $?

try_message 'feat: add a skill\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
expect 'a Claude co-author line blocks' block $?

try_message 'feat: add a skill\n\nco-authored-by: claude <x@example.com>\n'
expect 'a lower-case co-author line blocks' block $?

try_message 'feat: add a skill\n\nCo-Authored-By: Someone <noreply@anthropic.com>\n'
expect 'an anthropic co-author address blocks' block $?

try_message 'feat: add a skill\n\nGenerated with [Claude Code](https://claude.com/claude-code)\n'
expect 'a Claude Code generated line blocks' block $?

try_message 'feat: add a skill\n\nCo-Authored-By: A Person <person@example.com>\n'
expect 'a human co-author passes' pass $?

try_message 'docs: explain how Claude reads a skill\n'
expect 'the word Claude in the subject passes' pass $?

try_message 'feat: add a skill\n\n# Co-Authored-By: Claude <noreply@anthropic.com>\n'
expect 'a git comment line passes' pass $?

exit "$failed"

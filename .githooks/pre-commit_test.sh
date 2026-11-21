#!/bin/sh
# Test the scrub pre-commit hook. Each case uses a new repo.
# Run: sh .githooks/pre-commit_test.sh
set -u

src=$(cd "$(dirname "$0")" && pwd)
root=$(mktemp -d)
trap 'rm -rf "$root"' EXIT
failed=0
n=0

new_repo() {
  n=$((n + 1))
  repo="$root/repo$n"
  git init -q "$repo"
  git -C "$repo" config user.name test
  git -C "$repo" config user.email test@example.com
  git -C "$repo" config commit.gpgsign false
  git -C "$repo" config core.hooksPath .githooks
  mkdir "$repo/.githooks"
  cp "$src/pre-commit" "$src/scrub-patterns.txt" "$repo/.githooks/"
}

try_commit() {
  printf '%s\n' "$1" > "$repo/skill.md"
  git -C "$repo" add -A
  git -C "$repo" commit -q -m test > /dev/null 2>&1
}

private_file() {
  private="$root/private$n.txt"
  printf '%s\n' "$1" > "$private"
  git -C "$repo" config scrub.patterns "$private"
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

new_repo
try_commit 'A clean skill.'
expect 'a clean tree commits' pass $?

new_repo
try_commit 'Fix ENG-123 now.'
expect 'a ticket key blocks the commit' block $?

new_repo
try_commit 'Write plan_ENG-123.md.'
expect 'a ticket key in a file name blocks the commit' block $?

new_repo
try_commit 'Fix PROJ-123 now.'
expect 'the placeholder key commits' pass $?

new_repo
try_commit 'Set customfield_10010.'
expect 'a custom field ID blocks the commit' block $?

new_repo
private_file 'acme'
try_commit 'Built at Acme.'
expect 'a name from the private file blocks the commit' block $?

new_repo
git -C "$repo" config scrub.patterns "$root/missing.txt"
try_commit 'A clean skill.'
expect 'a missing private file blocks the commit' block $?

new_repo
private_file '('
try_commit 'A clean skill.'
expect 'a bad pattern blocks the commit' block $?

new_repo
try_commit 'A clean skill.'
printf 'Fix ENG-123.\n' > "$repo/old.md"
git -C "$repo" add old.md
git -C "$repo" commit -q --no-verify -m old
try_commit 'A new clean line.'
expect 'an old hit in the tree blocks a new commit' block $?

(cd "$repo" && .githooks/pre-commit HEAD > /dev/null 2>&1)
expect 'a revision with a ticket key fails' block $?

(cd "$repo" && .githooks/pre-commit HEAD~1 > /dev/null 2>&1)
expect 'a clean revision passes' pass $?

try_skill() {
  mkdir -p "$repo/skills/demo"
  printf '%s\n' "$1" > "$repo/skills/demo/SKILL.md"
  git -C "$repo" add -A
  git -C "$repo" commit -q -m test > /dev/null 2>&1
}

new_repo
try_skill 'Run `python3 ../other/scripts/check.py`.'
expect 'a script path from the current folder in a SKILL.md blocks the commit' block $?

new_repo
try_skill '`$SKILL_DIR` is the base directory. Run `python3 $SKILL_DIR/../other/scripts/check.py`.'
expect 'a script path from $SKILL_DIR in a SKILL.md commits' pass $?

new_repo
try_commit 'Run `python3 ../other/scripts/check.py`.'
expect 'a script path from the current folder outside a SKILL.md commits' pass $?

new_repo
try_skill 'Read `$SKILL_DIR/../other/SKILL.md`.'
expect 'a $SKILL_DIR path in a SKILL.md that does not say what $SKILL_DIR is blocks the commit' block $?

new_repo
try_skill "\`\$SKILL_DIR\` is this skill's base directory. Read \`\$SKILL_DIR/../other/SKILL.md\`."
expect 'a $SKILL_DIR path in a SKILL.md that says what $SKILL_DIR is commits' pass $?

new_repo
try_skill 'Flag an unset `$SKILL_DIR` placeholder.'
expect 'a $SKILL_DIR mention with no path commits' pass $?

new_repo
try_skill 'Read `$SKILL_DIR/x`.'
(cd "$repo" && .githooks/pre-commit HEAD > /dev/null 2>&1)
expect 'a revision with an undefined $SKILL_DIR path fails' block $?

new_repo
try_skill '`$SKILL_DIR` is the base directory. Read `$SKILL_DIR/x`.'
(cd "$repo" && .githooks/pre-commit HEAD > /dev/null 2>&1)
expect 'a revision with a defined $SKILL_DIR path passes' pass $?

exit "$failed"

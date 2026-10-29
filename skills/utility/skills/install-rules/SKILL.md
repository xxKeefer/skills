---
name: install-rules
description: Install this marketplace's coding-convention rules to ~/.claude/rules/.
disable-model-invocation: true
---

# Install Rules

Install every version-controlled rule in this skill's `rules/` folder to `~/.claude/rules/`. Claude
Code loads a rule with `paths:` frontmatter only when it reads or edits a matching file, so each
convention costs context only in the sessions that need it.

The `rules/` folder is the source of truth. This install copies every `.md` file out to
`~/.claude/rules/` and overwrites a file with the same name.

## Step 1: Locate the Source Directory

```sh
srcdir="${CLAUDE_SKILL_DIR}/rules"
```

Confirm `$srcdir` contains at least one `.md` file before you copy.

## Step 2: Show What Changes

Compare each source rule with the installed file of the same name:

```sh
for f in "$srcdir"/*.md; do
  target=~/.claude/rules/"$(basename "$f")"
  [ -f "$target" ] && diff -u "$target" "$f"
done
```

If a diff shows, show it to the user. Get a yes before you overwrite. An empty result means
nothing local is lost.

## Step 3: Install All Rules

```sh
mkdir -p ~/.claude/rules
cp "$srcdir"/*.md ~/.claude/rules/
```

## Step 4: Verify

Confirm each source rule landed unchanged:

```sh
for f in "$srcdir"/*.md; do
  cmp -s "$f" ~/.claude/rules/"$(basename "$f")" || echo "MISMATCH: $(basename "$f")"
done
```

No output means the install is correct. The rules take effect in the **next** session.

## Uninstall

Resolve `$srcdir` as in Step 1, then remove each rule it holds. Rules that were added by hand stay:

```sh
for f in "$srcdir"/*.md; do rm -f ~/.claude/rules/"$(basename "$f")"; done
```

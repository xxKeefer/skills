# install-rules

Installs every version-controlled coding-convention rule onto a machine. The goal: the same
conventions on home and work, from one committed source, loaded only when they apply.

- **Source:** `rules/*.md` in this folder (single source of truth)
- **Installs to:** `~/.claude/rules/` (all files)

The easiest install is to run the skill: **`/install-rules`**. The steps below are the manual
equivalent.

## Manual install

Run from this folder:

```sh
mkdir -p ~/.claude/rules
cp rules/*.md ~/.claude/rules/
```

Restart the session for it to take effect.

## How a rule loads

A rule with `paths:` frontmatter loads when Claude reads or edits a file that matches one of its
globs. The globs resolve against the session's working directory. A rule with no `paths:` loads in
every session, the same as `CLAUDE.md`.

```markdown
---
paths:
  - "**/*.ts"
---
```

## Add or change a rule

1. Edit or add a `.md` file in `rules/`.
2. Run `/install-rules`.

Do not edit the copies in `~/.claude/rules/`. The next install overwrites them.

## Uninstall

```sh
for f in rules/*.md; do rm -f ~/.claude/rules/"$(basename "$f")"; done
```

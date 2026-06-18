---
name: retire-a-skill
description: >
  Retire a skill from a skills marketplace repo. If it lives in a normal domain, deprecate it
  (move to the `deprecated` domain). If it's already deprecated, delete it for good. Usage:
  retire-a-skill <skill-name>. Use when the user says "retire a skill", "deprecate this skill",
  "kill <skill>", or "delete <skill>".
argument-hint: "<skill-name>"
---

# Retire a Skill

The kill switch in the skill lifecycle, companion to `/migrate-a-skill`. A skill retires in two
stages: first **deprecate** (any domain → `deprecated`), then later **delete** (`deprecated` →
gone). This skill picks the right stage automatically from where the skill currently lives.

## Step 1: Resolve and branch

Parse `<skill-name>`. Find `*/skills/<skill-name>/` under the repo root — that parent is the
**current domain**.

- Not found → stop, report it.
- Found in more than one domain → ask which one to retire.

Then branch on the current domain:

- **Not `deprecated`** → go to Step 2 (Deprecate).
- **Already `deprecated`** → go to Step 3 (Delete).

**Done when:** you know the skill's location and which branch applies.

## Step 2: Deprecate (move to `deprecated`)

This is exactly a migration into the `deprecated` domain — don't reimplement it. Delegate to
`/migrate-a-skill <skill-name> deprecated`, which handles the `git mv`, doc-sync across both
domains' `README.md` + `CLAUDE.md`, version bumps, and a single `chore(...)` commit.

One detail `migrate-a-skill` must respect when the target is `deprecated`: the deprecated docs use
a `_None yet._` placeholder under `## Skills` when empty. When adding the first row, replace the
placeholder line with the table; don't leave both.

**Done when:** the skill lives under `deprecated/skills/`, both domains' docs and versions are
updated, and the move is committed.

## Step 3: Delete (remove for good)

The skill is in `deprecated` — this is the irreversible stage. Git history is the archive.

1. **Hard confirmation.** Show the user what will be deleted (the directory and its files) and
   require an explicit yes before proceeding. This gate is mandatory — never skip it.
2. **Remove** — `git rm -r deprecated/skills/<skill-name>`.
3. **Prune docs** — remove the skill's row from `deprecated/README.md` and
   `deprecated/CLAUDE.md`. If it was the last skill in the table, restore the `_None yet._`
   placeholder under `## Skills`.
4. **Bump version** — minor-bump `deprecated/.claude-plugin/plugin.json`.
5. **Commit** — one commit, no push:

   ```
   chore(deprecated): delete <skill-name>

   <one line: why it's gone — confirmed unused / superseded by X>. History is the archive.
   ```

**Done when:** the directory is gone, the docs no longer mention it, the version is bumped, and
the deletion is committed.

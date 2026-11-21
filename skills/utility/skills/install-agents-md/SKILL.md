---
name: install-agents-md
description: Install the managed blocks (coding, tools, models) into ~/.claude/AGENTS.md, with machine facts hydrated from a values file.
disable-model-invocation: true
---

# Install AGENTS.md Blocks

Write each `sections/<name>.md` of this skill into `~/.claude/AGENTS.md` as a managed block, between
`<!-- managed: <name> -->` and `<!-- end managed -->`. The text outside the markers is the user's
own, and this skill never changes it without a yes.

The repo holds only generic text. A `{{key}}` in a section is a machine fact. It comes from
`~/.claude/agents-md.values.json`, which stays outside the repo.

## Step 1: Hydrate the values

Read [`HYDRATE.md`](HYDRATE.md). For each key, fill the value, show it to the user, and write it to
`~/.claude/agents-md.values.json` after a yes. Keep a value that the file already holds, unless the
user changes it.

**Done when:** every `{{key}}` in `sections/` has a value that the user confirmed.

## Step 2: Run the script

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/install_agents_md.py"
```

The script copies the file to `AGENTS.md.bak` before each write. A first run puts the blocks at the
top. A later run replaces only the text inside the markers. A run with no change writes nothing, and
keeps the earlier backup.

A missing value renders as `none`, and the script prints a warning that names the key. Go back to
Step 1 for that key, then run the script again.

**Done when:** the script exits 0, and prints `created`, `updated`, or `unchanged`.

## Step 3: Drop the old sections

The script prints each `OLD <name>` line: a plain-text heading in the user's file that block
`<name>` replaces. For each one, show the old section beside the new block, read from the file.
Ask once, for all of them: which of these old sections to delete?

For each name that the user says yes to, run the script again with the name:

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/install_agents_md.py" --drop <name>
```

The script deletes the section from its heading to the next heading of the same or a higher level.
Keep every old section that the user does not name.

**Done when:** each `OLD` line is dropped or kept, as the user chose, or the script printed none.

## Step 4: Show the lines for the user

The script prints each `EDIT` line: a line of the user's own text that a block now repeats. Show
those lines to the user. Never apply them.

**Done when:** the user has seen every `EDIT` line, or the script printed none.

## Step 5: Offer the worktrunk template

Skip this step when `wt` does not run. [`worktrunk.toml`](worktrunk.toml) names a worktree by
the ticket key in its branch, so each layer of a stack resolves to one folder. A branch with no key
keeps its own name. Ask first, because the move changes folder paths. On a no, skip the step.

1. Read `~/.config/worktrunk/config.toml`. Show its `worktree-path` line, if it has one. When the
   file is a link into a read-only store, find the source of the config manager that writes it,
   and edit that source in Step 2. Say that the user must rebuild before Step 3.
2. Put the line from `worktrunk.toml` above the first `[table]` header. Replace the old
   `worktree-path` line. A key below a table header belongs to that table, and worktrunk ignores
   it with no error.
3. Ask which repos to move. The default is the current repo. In each, run
   `wt step relocate --dry-run`. Show the moves, and ask once. On a yes, run
   `wt step relocate <branch>...` with the branch of each linked worktree only. A main checkout
   never moves, even on a feature branch.
4. Read `git worktree list` in each repo. `relocate` can report a move that it did not make. For
   each worktree still at its old path, run `git worktree move <old> <new>`.
5. For each moved worktree, set the new path in each plan that names the old path, in its
   `worktree:` key or its `Worktree:` line.
6. Find each line in `~/.claude/AGENTS.md` that holds `<repo>.<branch>/`. Show it beside the same
   line with `<repo>.<KEY>/`. Never apply it.

**Done when:** the user said no, or the template is in the config, the worktrees moved, and the
user has seen each system map line.

## Step 6: Verify

Run the script a second time, with no `--drop`. The output must say `unchanged`.

The blocks take effect in the **next** session.

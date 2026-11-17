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

A missing value stops the script with exit 1, and nothing is written. Go back to Step 1 for the
key that the error names.

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

## Step 5: Verify

Run the script a second time, with no `--drop`. The output must say `unchanged`.

The blocks take effect in the **next** session.

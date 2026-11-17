# install-agents-md

Writes managed blocks into `~/.claude/AGENTS.md` from version-controlled sections, so each machine
loads the same coding rule, tool table, and model table.

- **Source:** `sections/*.md` in this folder (one block for each file)
- **Writes to:** `~/.claude/AGENTS.md`, with the previous bytes in `AGENTS.md.bak`
- **Machine facts:** `{{key}}` placeholders, filled from `~/.claude/agents-md.values.json` (see `HYDRATE.md`)
- **Dependency:** `python3`

Run the skill: **`/install-agents-md`**. The script does every file change. Test it with
`python3 scripts/install_agents_md.spec.py`.

## Section format

An optional header of `replaces: <heading>` and `lists: <text>` lines, then a blank line, then the
block text.

- `replaces:` names an old plain-text heading that the block makes stale.
- `lists:` names text that the script shows to the user when it finds it outside a block.

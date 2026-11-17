# Hydrate

Each `{{key}}` in `sections/` is a fact about this machine. Fill it, show it to the user, and write
it to `~/.claude/agents-md.values.json` as one flat JSON object, after a yes.

Read the machine, not the repo. Never write a value into a file in this repo.

| Key | What to fill | Where to look |
| --- | --- | --- |
| `tracker_tool` | The tracker and how the agent reaches it, such as a product name and its MCP server. Write `none` when the machine has no tracker | The enabled MCP servers and plugins |
| `tracker_notes` | The path of a file with tracker rules, or `none` | `~/.claude/tools/` |
| `code_host_tool` | The code host and its CLI, such as a product name and `gh`. Write `none` when the machine has none | `git remote -v`, the installed CLIs |
| `code_host_notes` | The path of a file with code host rules, or `none` | `~/.claude/tools/` |
| `browser_tool` | The browser that the agent drives, and which profile. Write `none` when the machine has none | The enabled browser extensions and MCP servers |
| `browser_notes` | The path of a file with browser rules, or `none` | `~/.claude/tools/` |

When the existing `~/.claude/AGENTS.md` already holds a tool table, take the values from it.

**Done when:** every key has a value that the user said yes to.

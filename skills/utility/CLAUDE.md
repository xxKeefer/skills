# Utility

Dev-environment setup skills — one-shot configuration tasks that prepare a repo or machine for
agent-assisted work. Kept separate from `developer` (which is day-to-day engineering workflow) so
the setup skills are easy to find, maintain, or retire on their own.

## Skills

| Skill | Purpose |
|---|---|
| `/setup-pre-commit` | Detect language/toolchain and configure pre-commit hooks (format, type-check, test) |
| `/setup-git-guardrails` | Block dangerous git commands via a Claude Code hook |
| `/setup-skill-tally` | Count every skill invocation into a global JSON tally via a zero-latency hook |
| `/setup-statusline` | Install the self-contained, version-controlled status line to `~/.claude/` and wire it into settings |
| `/install-agent-voice` | Install the version-controlled Terse output style to `~/.claude/output-styles/` and select it in settings |
| `/configure-obsidian-kanban` | Install and tune the obsidian-kanban plugin to match the projects domain board format |

## Design Principles

- **One-shot, not recurring**: these run once when setting up a project, not in the daily loop.
- **Deterministic feedback loops**: they install guard rails agents cannot bypass.

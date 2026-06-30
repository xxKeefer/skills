# Utility

Dev-environment setup skills — pre-commit hooks, git guardrails, skill-usage tallying, and statusline install.

## Skills

| Skill | Purpose |
|---|---|
| `/setup-pre-commit` | Detect language/toolchain and configure pre-commit hooks (format, type-check, test) |
| `/setup-git-guardrails` | Block dangerous git commands via Claude Code hook |
| `/setup-skill-tally` | Tally every skill invocation into `~/.claude/skill-tally.json` via a zero-latency hook |
| `/setup-statusline` | Install the self-contained, version-controlled status line to `~/.claude/` and wire it into settings |
| `/install-agent-voice` | Install the version-controlled Terse output style to `~/.claude/output-styles/` and select it in settings |
| `/configure-obsidian-kanban` | Install and tune the obsidian-kanban plugin to match the projects domain board format |

## Installation

```json
{
  "enabledPlugins": {
    "utility@xxkeefer-skills": true
  }
}
```

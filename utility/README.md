# Utility

Dev-environment setup skills — pre-commit hooks, git guardrails, and skill-usage tallying.

## Skills

| Skill | Purpose |
|---|---|
| `/setup-pre-commit` | Detect language/toolchain and configure pre-commit hooks (format, type-check, test) |
| `/setup-git-guardrails` | Block dangerous git commands via Claude Code hook |
| `/setup-skill-tally` | Tally every skill invocation into `~/.claude/skill-tally.json` via a zero-latency hook |

## Installation

```json
{
  "enabledPlugins": {
    "utility@xxkeefer-skills": true
  }
}
```

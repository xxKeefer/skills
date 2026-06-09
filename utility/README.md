# Utility

Dev-environment setup skills — pre-commit hooks and git guardrails.

## Skills

| Skill | Purpose |
|---|---|
| `/setup-pre-commit` | Language-aware pre-commit hook configuration |
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

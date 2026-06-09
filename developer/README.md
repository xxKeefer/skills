# Developer

Opinionated engineering workflows for Claude Code. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/research-it` | Discovery | Pre-spike research producing decision artifacts |
| `/spike-it` | Discovery | Deep-dive investigation |
| `/task-it` | Discovery | Decompose spike into tickets |
| `/plan-it` | Planning | Break task into atomic steps |
| `/do-it` | Implementation | Execute plan via /tdd |
| `/tdd` | Implementation | Red-green-refactor loop |
| `/hunt-it` | Implementation | Bug tracking from symptom to fix |
| `/close-it` | Closure | Commit, PR, QA test plan |
| `/resolve-it` | Closure | Assess code review feedback |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/design-it` | Exploration | Multiple interface designs |
| `/document-it` | Maintenance | Sync docs to code |
| `/improve-it` | Maintenance | Architecture improvement |
| `/qa-it` | Closure | Manual QA test plans |
| `/explain-it` | Anytime | Unpack agent reasoning |

## Installation

```json
{
  "enabledPlugins": {
    "developer@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills`.

## Permissions

Ticket-creating skills target the project's tracker — GitHub via `gh` by default, or whatever the
repo's CLAUDE.md declares (e.g. Jira via the Atlassian MCP). For the GitHub default, add these to
your Claude Code permissions:

```json
{
  "permissions": {
    "allow": [
      "Bash(gh issue create:*)",
      "Bash(gh issue edit:*)",
      "Bash(gh issue view:*)",
      "Bash(gh issue list:*)",
      "Bash(gh issue close:*)"
    ]
  }
}
```

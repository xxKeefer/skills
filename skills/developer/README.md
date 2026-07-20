# Developer

Opinionated engineering workflows for Claude Code. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/research` | Discovery | Pre-spike research producing decision artifacts |
| `/grill-with-docs` | Discovery | Grill-led requirements gathering, doc-anchored |
| `/spike` | Discovery | Deep-dive investigation |
| `/to-tickets` | Discovery | Decompose spike into tickets |
| `/to-plan` | Planning | Break task into atomic steps |
| `/implement` | Implementation | Execute plan via /tdd |
| `/tdd` | Implementation | Red-green-refactor loop |
| `/tweak` | Implementation | Small focused edits to recently built work |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix or /to-plan |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA |
| `/happy-path` | Closure | Manual QA test plan for the current changeset |
| `/resolve-feedback` | Closure | Assess code review feedback |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/explain-reasoning` | Anytime | Unpack agent reasoning |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |

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

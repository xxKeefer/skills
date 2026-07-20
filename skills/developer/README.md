# Developer

Opinionated engineering workflows for Claude Code. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/grill-with-docs` | Discovery | Grill-led requirements gathering, doc-anchored |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/spike` | Discovery | Deep-dive investigation |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red-green-refactor loop |
| `/tweak` | Implementation | Small focused edits to recently built work |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA |
| `/happy-path` | Closure | Manual QA test plan for the current changeset |
| `/resolve-feedback` | Closure | Assess code review feedback |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
| `/explain-reasoning` | Anytime | Unpack agent reasoning |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |

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

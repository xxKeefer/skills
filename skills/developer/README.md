# Developer

Opinionated engineering workflows for Claude Code. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/grill-with-docs` | Discovery | Grill-led requirements gathering, doc-anchored |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/tweak` | Implementation | Small focused edits to recently built work |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA |
| `/happy-path` | Closure | Manual QA test plan for the current changeset |
| `/resolve-feedback` | Closure | Assess code review feedback |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |
| `/codebase-news` | Anytime | Table the notable changes in the current repo over a time period, from the changelogs first, then the commit history |

## Installation

```json
{
  "enabledPlugins": {
    "developer@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills`.

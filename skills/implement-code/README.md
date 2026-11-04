# Implement Code

Engineering workflows from ticket to PR: scope, plan, build, and open the PR. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/grill-with-docs` | Discovery | Grill-led requirements gathering, doc-anchored |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/tweak` | Implementation | Small focused edits to recently built work |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |
| `/codebase-news` | Anytime | Table the notable changes in the current repo over a time period, from the changelogs first, then the commit history |

## Installation

```json
{
  "enabledPlugins": {
    "implement-code@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills`.

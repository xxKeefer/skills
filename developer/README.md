# Developer

Opinionated engineering workflows for Claude Code. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/spike-it` | Discovery | Deep-dive investigation |
| `/task-it` | Discovery | Decompose spike into tickets |
| `/plan-it` | Planning | Break task into atomic steps |
| `/do-it` | Implementation | Execute plan via /tdd |
| `/tdd` | Implementation | Red-green-refactor loop |
| `/hunt-it` | Implementation | Bug tracking from symptom to fix |
| `/close-it` | Closure | Commit, PR, QA test plan |
| `/resolve-it` | Closure | Assess code review feedback |
| `/design-it` | Exploration | Multiple interface designs |
| `/document-it` | Maintenance | Sync docs to code |
| `/improve-it` | Maintenance | Architecture improvement |
| `/qa-it` | Closure | Manual QA test plans |
| `/explain-it` | Anytime | Unpack agent reasoning |

## Installation

```json
{
  "enabledPlugins": {
    "xxkeefer-skills@developer": true
  }
}
```

Requires `xxkeefer-skills@primitives`.

# Developer

Engineering workflows from a plan to working code: worktrees, prototypes, test-first
implementation, debugging, fixes, and manual QA. Framework-agnostic and language-agnostic. Code
review comes from the [`review`](../review/README.md) domain.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/claim` | Discovery | Find or create the worktree for a ticket, a PR, or a branch, then record it in the handoff. Needs worktrunk (`wt`) |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/auto-handoff` | Implementation | Run every remaining step of a handoff, one fresh subagent per step, then batch the open decisions for the user |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA, or each failed item of a QA report prompt, with one commit for each |
| `/happy-path` | Closure | Write a manual QA checklist for the current changeset as an HTML report. Its fail ticks build a `/developer:fix` prompt |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
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

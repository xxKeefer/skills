# Implement Code

Engineering workflows from ticket to PR: scope, plan, build, and open the PR. Framework-agnostic, language-agnostic.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/grill-with-docs` | Discovery | Grill-led requirements gathering, doc-anchored |
| `/claim` | Discovery | Find or create the worktree for a ticket, a PR, or a branch, then record it in the handoff. Needs worktrunk (`wt`) |
| `/scope-ticket` | Discovery | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate |
| `/start-ticket` | Discovery | Scope a ticket, claim its worktree, then write the plan handoff with lettered ACs and a test approach for you to approve |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/auto-handoff` | Implementation | Run every remaining step of a handoff, one fresh subagent per step, then batch the open decisions for the user |
| `/create-pr` | Closure | Check the review for drift, fill the repo's PR template with an AC table and its gaps, then push and open a draft PR after one yes |
| `/pickup` | Closure | Confirm an open PR, claim its worktree, sync it by fast-forward only, then triage its review threads into a handoff |
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

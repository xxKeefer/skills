# Engineering

Engineering workflows from ticket to PR, then review, debugging, and QA. Framework-agnostic and
language-agnostic. Code review comes from the [`review`](../review/README.md) domain.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/claim` | Discovery | Find or create the worktree for a ticket, a PR, or a branch, then record it in the handoff. Needs worktrunk (`wt`) |
| `/scope-ticket` | Discovery | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate |
| `/start-ticket` | Discovery | Scope a ticket, claim its worktree, then write the plan handoff with lettered ACs and a test approach for you to approve |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/auto-handoff` | Implementation | Run every remaining step of a handoff, one fresh subagent per step, then batch the open decisions for the user |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA |
| `/squash-bugs` | Implementation | Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision |
| `/create-pr` | Closure | Check the review for drift, fill the repo's PR template with an AC table and its gaps, then push and open a draft PR after one yes |
| `/happy-path` | Closure | Manual QA test plan for the current changeset |
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
    "engineering@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills` and `review@xxkeefer-skills`.

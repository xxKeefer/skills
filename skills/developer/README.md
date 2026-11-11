# Developer

Implementing code, broadly: from a ticket to a PR. Refine, scope, split, and plan a ticket, then
claim a worktree, prototype, implement test-first, debug, fix, run manual QA, and open the PR.
Framework-agnostic and language-agnostic. Code review comes from the
[`code-review`](../code-review/README.md) domain.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/refine-ticket` | Discovery | Grill out each ambiguity in a ticket, derive lettered ACs from its user story, and write a plain summary, then write both back to the ticket after one yes |
| `/scope-ticket` | Discovery | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate. On CLARIFY, `/refine-ticket` asks the questions, then the scope runs again. On a direct run, the split path hands off to `/split-ticket` |
| `/split-ticket` | Discovery | Split a ticket that is too big into pieces of 3 points or less, grouped into waves with a merge order. Write the split report, then create one sub-task and one stub handoff per piece after one yes |
| `/start-ticket` | Discovery | Refine a vague ticket with `/refine-ticket`, scope it, and split a big one with `/split-ticket`. Else claim its worktree, then write the plan handoff with lettered ACs and a test approach for you to approve. On a sub-task, the plan fills its stub handoff |
| `/claim` | Discovery | Find or create the worktree for a ticket, a PR, or a branch, then record it in the handoff. A stacked sub-task gets its own worktree, and `gh stack` puts it on top of the branch it builds on. Needs worktrunk (`wt`), and `gh stack` for a stack |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | Implement a spec or tickets via /tdd at pre-agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/run-wave` | Implementation | Run every remaining step of a handoff, one fresh subagent per step (or per run of small fix steps), then batch the open decisions for the user. Pass it a review report's prompt to add a fix round, and a new review when the round can change behaviour |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA, or each failed item of a QA report prompt, with one commit for each |
| `/squash-bugs` | Implementation | Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision |
| `/happy-path` | Closure | Write a manual QA checklist for the current changeset as an HTML report, with a setup table first. Its fail ticks build a `/developer:fix` prompt |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/create-pr` | Closure | Check the review for drift, lead with a visual summary, evidence, and the merge danger, fill the repo's PR template with an AC table, its gaps, and the merge line of a sub-task, then push and open a draft PR without asking |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-news` | Anytime | Table the notable changes in the current repo over a time period, from the changelogs first, then the commit history |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |

## Installation

```json
{
  "enabledPlugins": {
    "developer@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills` and `code-review@xxkeefer-skills`.

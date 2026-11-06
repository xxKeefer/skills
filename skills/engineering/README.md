# Engineering

Engineering workflows from ticket to PR: refine, scope, split, and plan a ticket, fix a batch of QA
bugs, and open the PR. Framework-agnostic and language-agnostic. Builds, debugging, and manual QA
come from the [`developer`](../developer/README.md) domain, and code review from the
[`review`](../review/README.md) domain.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/refine-ticket` | Discovery | Grill out each ambiguity in a ticket, derive lettered ACs from its user story, and write a plain summary, then write both back to the ticket after one yes |
| `/scope-ticket` | Discovery | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate. On CLARIFY, `/refine-ticket` asks the questions, then the scope runs again. On a direct run, the split path hands off to `/split-ticket` |
| `/split-ticket` | Discovery | Split a ticket that is too big into pieces of 3 points or less, grouped into waves with a merge order. Write the split report, then create one sub-task and one stub handoff per piece after one yes |
| `/start-ticket` | Discovery | Refine a vague ticket with `/refine-ticket`, scope it, and split a big one with `/split-ticket`. Else claim its worktree, then write the plan handoff with lettered ACs and a test approach for you to approve. On a sub-task, the plan fills its stub handoff |
| `/squash-bugs` | Implementation | Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision |
| `/create-pr` | Closure | Check the review for drift, fill the repo's PR template with an AC table, its gaps, and the merge line of a sub-task, then push and open a draft PR after one yes |
| `/codebase-news` | Anytime | Table the notable changes in the current repo over a time period, from the changelogs first, then the commit history |

## Installation

```json
{
  "enabledPlugins": {
    "engineering@xxkeefer-skills": true
  }
}
```

Requires primitives, developer, and review: `primitives@xxkeefer-skills`,
`developer@xxkeefer-skills`, and `review@xxkeefer-skills`. Turn engineering on in work sessions
only, as [ADR 0009](../../docs/adr/0009-review-domain.md) "How engineering loads" says.

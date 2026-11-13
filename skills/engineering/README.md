# Engineering

Software engineering from an idea to a merged PR. Nine lifecycle commands sit on top. Each one
picks and runs the skills below it, so you can start from the command for your phase and go down a
level when you need control. Framework-agnostic and language-agnostic, except the persona
reviewers, which each review one kind of code.

```
/spec → /plan → /build → /test → /review → /ship
```

## Commands

Each command has `disable-model-invocation: true`, and its description starts with ★.

| Command | Phase | Runs |
|---|---|---|
| `/spec` | Define | `/refine-ticket` for a ticket key. For an idea: an interview to an explicit yes, then a spec with lettered ACs |
| `/plan` | Plan | `/start-ticket` with a ticket key or a spec |
| `/build` | Build | Every remaining step of the plan handoff, one fresh subagent per step (or per run of small fix steps). Then a test and review loop until the `/ship` checks pass, then `/happy-path` and `/sad-path`. Open decisions wait in one batch. A review report's prompt adds a fix round |
| `/test` | Verify | `/tdd` for a bug or an untested seam, else `/happy-path`, then `/sad-path` when its guard matches |
| `/constraints` | Verify | Write `CONSTRAINTS.md` with a command behind each rule, then check each branch for a lowered bar |
| `/review` | Review | `/light-review` on the branch, `/mob-review` with `full`, or `/review-pr` for a PR |
| `/webperf` | Verify | Measure a page, fix the worst bottleneck, measure again, keep or revert |
| `/code-simplify` | Review | Simplify the changed code with no change in behaviour, one change and one test run at a time |
| `/ship` | Ship | A go or no-go gate on plan, tests, review, and constraints, then `/create-pr` |

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/pick-next-task` | Discovery | Rank your team's open tickets by focus, priority, iteration, and effort. You pick up to three, then each is assigned, moved to in progress, and given its `/plan` command |
| `/refine-ticket` | Discovery | Grill out each ambiguity in a ticket, derive lettered ACs from its user story, and write a plain summary, then write both back to the ticket after one yes |
| `/scope-ticket` | Discovery | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate. On CLARIFY, `/refine-ticket` asks the questions, then the scope runs again. On a direct run, the split path hands off to `/split-ticket` |
| `/split-ticket` | Discovery | Split a ticket that is too big into pieces of 3 points or less, grouped into waves with a merge order. Write the split report, then create one sub-task and one stub handoff per piece after one yes |
| `/start-ticket` | Discovery | Refine a vague ticket with `/refine-ticket`, scope it, and split a big one with `/split-ticket`. Else claim its worktree, then write the plan handoff with lettered ACs and a test approach for you to approve. On a sub-task, the plan fills its stub handoff |
| `/claim` | Discovery | Find or create the worktree for a ticket, a PR, or a branch, then record it in the handoff. Needs worktrunk (`wt`) |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | `/do-next` on the plan handoff, one step. With no handoff, implement a spec or tickets with `/tdd` at agreed seams |
| `/tdd` | Implementation | Red → green loop |
| `/diagnose` | Implementation | Trace a non-obvious bug to proven root cause, hand off to /fix |
| `/fix` | Implementation | Fix a broken behaviour found during manual QA, or each failed item of a QA report prompt, with one commit for each |
| `/squash-bugs` | Implementation | Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision |
| `/happy-path` | Closure | Write a manual QA checklist for the current changeset as an HTML report, with a setup table first. Its fail ticks build a `/engineering:fix` prompt |
| `/qa-screenshots` | Closure | Run a `/happy-path` checklist in your own browser, add a screenshot per item to the QA report, and append a Manual QA section to the PR |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/create-pr` | Closure | Check the review for drift, lead with a visual summary, evidence, and the merge danger, fill the repo's PR template with an AC table, its gaps, and the merge line of a sub-task, then push and open a draft PR without asking |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |
| `/pr-news` | Anytime | Table what happened over a time period on your open PRs and your review requests, one table per repo |
| `/codebase-news` | Anytime | Table the notable changes in the current repo over a time period, from the changelogs first, then the commit history |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |
| `/mob-review` | Review | Run every in-scope persona over a branch or PR and write the ranked findings to an HTML report. On your own branch, it fixes each finding that has a fix, commits once, and reports what stays open. Its ticks on the open rows build the `/engineering:apply-review` prompt, or in a handoff the `/engineering:build` prompt. On someone else's branch, it drops the nits, and its ticks build the `/engineering:post-review-comments` prompt. In a handoff, it records the report in the review step |
| `/light-review` | Review | Run the eight essential lanes of the panel (correctness, security, error handling, code quality, naming, test design, test quality, and architecture) and fix and report as `/engineering:mob-review` does, with the same ticks and prompts |
| `/review-pr` | Review | Resolve a PR from its number, URL, branch, or ticket key, claim its worktree, sync it, run `/engineering:mob-review` there, then give the report path, whose ticks build the `/engineering:post-review-comments` prompt |
| `/post-review-comments` | Review | Post the rows you tick in a review report to the PR: apply your notes, show the drafts, then post them as one comment review and read them back |
| `/apply-review` | Review | Apply the rows you tick in a review report of your own branch: fix test-first, run the gates, commit once, push once, then reply on and resolve the ticked threads. Adds a result run to the report |
| `/sad-path` | Closure | Write a manual QA checklist that tries to break the changed forms and fields, as an HTML report with a setup table first. Each item cites a catalogue ID, and the fail ticks build a `/engineering:fix` prompt |
| `/pickup` | Closure | Confirm an open PR, claim its worktree, sync it by fast-forward only, then assess its open review threads into the review report, whose ticks build the `/engineering:apply-review` prompt |
| `/resolve-feedback` | Closure | Assess review feedback, pasted or from the open threads of a PR, and write a verdict, a recommendation, and a draft reply for each item to a review report. Its ticks build the `/engineering:apply-review` prompt. Applies no fix |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
| `/self-improve` | Maintenance | Mine a repo's fix commits, tracker bugs, review threads, failed CI runs, and the calibration backlog, put each proposal to you, apply the approved persona edits, and write a report and the repo's defect hotspots |
| `/update-personas` | Maintenance | Refresh `persona-best-practice` against installed and current versions, lint any persona's structure, and apply the approved calibration backlog |

### Personas

Each persona has `disable-model-invocation: true`. Start one by name, or let `/engineering:mob-review` start it.

| Persona | Reviews |
|---|---|
| `persona-a11y` | Semantic HTML, ARIA, labels, focus, keyboard |
| `persona-ac-check` | PR coverage of the acceptance criteria in a handoff, a spec, or the ticket |
| `persona-analytics` | Product event tracking: over-tracking, naming, and missing milestones |
| `persona-api-integrity` | Frontend calls against the backend spec, handler, and permission checks |
| `persona-api-spec` | OpenAPI spec and code drift |
| `persona-architecture` | Cross-layer coupling and logic in the wrong layer |
| `persona-async-state` | Races and stale async state |
| `persona-best-practice` | Outdated framework and language APIs |
| `persona-browser-e2e` | A standalone browser E2E suite that runs against a real backend |
| `persona-bundle-size` | Shipped bytes and load timing |
| `persona-charts` | Chart data edge cases: empty, gappy, time zones, axes, tooltips |
| `persona-code-quality` | Extraction, duplication, misplaced code, library reuse, and code smells in any language |
| `persona-comments` | Needless, stale, and what-not-why comments, and dead code |
| `persona-correctness` | Logic errors that give a wrong result or a crash, each with a counterexample |
| `persona-decisions-log` | Conformance with the project's recorded design decisions |
| `persona-design-system` | Design tokens, reinvented components, CSS hygiene, long-value layout |
| `persona-error-handling` | Swallowed failures, context-free throws, duplicate error handlers |
| `persona-file-upload` | File pickers, drop zones, and imports |
| `persona-form-behaviour` | Enter, Escape, and submit, input bounds, and stale hidden fields |
| `persona-github-actions` | Workflow security and best practice |
| `persona-i18n` | Hardcoded strings, dynamic keys, and namespaces |
| `persona-integration-test` | Playwright and MSW integration tests |
| `persona-naming` | File, folder, export, and identifier names, with units |
| `persona-pr-size` | A PR that is too big, and how to split it |
| `persona-production-protector` | Production blast radius: feature gates, defaults, one-way changes, rollback |
| `persona-resilience` | Session expiry, network loss, other tabs, and deploys during a task |
| `persona-security` | XSS, tabnabbing, secrets, and sensitive data sent to logs |
| `persona-shell` | Shell correctness: exit statuses, quoting, pipes, and signals |
| `persona-skills` | Agent-instruction correctness in skills, agents, and `CLAUDE.md` |
| `persona-tanstack` | Query keys, invalidation, and caching |
| `persona-test-design` | What should be tested, rated by risk |
| `persona-test-quality` | How tests are built, in any language: coupling, mocks, and false passes |
| `persona-text-input` | What happens to the characters a user types or pastes |
| `persona-typing` | Casts, type gymnastics, and missing `readonly` |
| `persona-url-state` | What refresh, a shared link, Back, and Forward do |
| `persona-value-display` | Missing, zero, huge, and awkward values on screen |
| `persona-vitest` | Unit-test quality, selectors, builders, and flaky tests |
| `persona-vue-reactivity` | Computed, ref, and watch correctness, and composable call sites |

## Installation

```json
{
  "enabledPlugins": {
    "engineering@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills`.

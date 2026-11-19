# Engineering

Software engineering from an idea to a merged PR. Nine lifecycle commands sit on top. Each one
picks and runs the skills below it, so you can start from the command for your phase and go down a
level when you need control. Framework-agnostic and language-agnostic, except the persona
reviewers, which each review one kind of code.

```
/spec → /plan → /build → /test → /review → /ship
```

## Commands

Each command description starts with ★. The user, the agent, or another skill can start a command.
Between commands the agent does not stop. Inside a command it stops where that skill asks for a
yes, and it stops before each action on the pause list, such as a merge or a ready-for-review PR.

| Command | Phase | Runs |
|---|---|---|
| `/spec` | Define | `/refine-ticket` for a ticket key. For an idea: an interview to an explicit yes, then a spec with lettered ACs |
| `/plan` | Plan | `/start-ticket` with a ticket key or a spec |
| `/build` | Build | Every remaining step of the plan, one fresh subagent per step (or per run of small fix steps). Then a test and review loop until the `/ship` checks pass, then `/happy-path` and `/sad-path`. Open decisions wait in one batch. A review report's prompt adds a fix round |
| `/test` | Verify | `/tdd` for a bug or an untested seam, else `/happy-path`, then `/sad-path` when its guard matches |
| `/constraints` | Verify | Write `CONSTRAINTS.md` with a command behind each rule, then check each branch for a lowered bar |
| `/review` | Review | `/light-review` on the branch, `/mob-review` with `full`, or `/review-pr` for a PR |
| `/webperf` | Verify | Measure a page, fix the worst bottleneck, measure again, keep or revert |
| `/code-simplify` | Review | Simplify the changed code with no change in behaviour, one change and one test run at a time |
| `/ship` | Ship | A go or no-go gate on plan, tests, review, and constraints, then `/create-pr` |

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/work-on` | Router | Run a playbook of the commands from a ticket, an idea, or a map to draft PRs. It stops only at the stops H0 to H5: the map, the spec, the plan, an open decision, an action on the pause list, and the `/retro` picks. |
| `/pick-next-task` | Discovery | Rank your team's open tickets by focus, priority, iteration, and effort. You pick up to three, then each is assigned, moved to in progress, and given its `/plan` command |
| `/refine-ticket` | Discovery | Grill out each ambiguity in a ticket, derive lettered ACs from its user story, and write a plain summary, then write both back to the ticket after one yes |
| `/scope-ticket` | Discovery | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate. On CLARIFY, `/refine-ticket` asks the questions, then the scope runs again. On a direct run, the split path hands off to `/split-ticket` |
| `/split-ticket` | Discovery | Split a ticket that is too big into pieces of 3 points or less, grouped into waves with a merge order. Write the split report, then create one sub-task per piece and a map of the sub-tasks after one yes |
| `/start-ticket` | Discovery | Refine a vague ticket with `/refine-ticket`, scope it, and split a big one with `/split-ticket`. Else claim its worktree, then write the plan with lettered ACs and a test approach for you to approve. On a sub-task, the plan takes its merge and stack order from the split map |
| `/claim` | Discovery | Find or create the worktree for a ticket, a PR, or a branch, then record it in the plan. Needs worktrunk (`wt`) |
| `/prototype` | Discovery | Build a throwaway prototype to answer a design question |
| `/implement` | Implementation | `/do-next` on the plan, one step. With no plan, implement a spec or tickets with `/tdd` at agreed seams |
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
| `/why` | Anytime | Answer why a line, a block, or a file is the way it is, from its commits and PR threads. Cites the author of each source and lists what the record does not answer. Only reads |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |
| `/stand-up` | Anytime | Show your day as one table per epic, from your tickets, PRs, review requests, and branches, then write a news bulletin about the day |
| `/gazette` | Anytime | Print a one-page HTML newspaper for a time window from `/stand-up` and `/codebase-news` across your repos, with the board, the CI weather, and an honour roll |
| `/mob-review` | Review | Run every in-scope persona over a branch or PR and write the ranked findings to an HTML report. On your own branch, it fixes each finding that has a fix, commits once, and reports what stays open. Its ticks on the open rows build the `/engineering:apply-review` prompt, or in a plan the `/engineering:build` prompt. On someone else's branch, it drops the nits, and its ticks build the `/engineering:post-review-comments` prompt. In a plan, it records the report in the review step |
| `/light-review` | Review | Run the essential lanes of the panel (correctness, security, error handling, code quality, naming, test design, test quality, architecture, comments, and skills) and fix and report as `/engineering:mob-review` does, with the same ticks and prompts |
| `/interrogate` | Review | Send panel adversaries to break the change, each in its own worktree. A script re-runs the command of each finding, and only a proven finding that breaks the intent stays in the report. Each other finding goes to the Dropped list with its reason. Applies no fix: the report's ticks build the `/engineering:fix` prompt |
| `/babysit` | Ship | Watch your PRs in the background. A CI or review change on a PR calls the notifier once and moves its chip on line 1 of the status line. A stack watches its lowest open PR |
| `/blast-radius` | Review | Find what a change can break outside its diff. Prove the one fact that makes it safe by a run, and name the rung of the five-rung ladder that it reached and the command that proved it. Gives the verdict `clear` or `risk`. Applies no fix. `/work-on` runs `/interrogate` on `risk` |
| `/benchmark` | Verify | Vet a performance number with seven checks: limiter, tuning, limits, errors, repeatability, relevance, and whether the work ran. Gives the verdict faster, slower, no measurable difference, or inconclusive, with the limiter or the gap. `/webperf` calls it on each measurement |
| `/loop-until` | Verify | Move one measured number to a stated predicate. Each try is one change and one measure, kept as one commit past noise with the gate green, else reverted. The harness is proven to separate cases, then frozen. Each try writes one row to the decision log. It stops at the predicate or on a surfaced dead end |
| `/verify` | Closure | Find the verification drivers that match the diff, with a script, and run each one against the live app. Returns the evidence paths, or `no driver`. `/test`, `/interrogate`, `/blast-radius`, and `/qa-screenshots` call it |
| `/create-verification-skill` | Closure | Write a verification driver for an app: a skill that launches the app, drives it the way a user does, and keeps the evidence. Checks the layout with a script and proves the driver by one run before it hands it over. `/verify` finds the driver from a diff |
| `/maintain-verification-skill` | Closure | Keep a verification driver true as the app changes: one source reader for each feature file, one live pass over every feature, then one commit of proven fixes. The outcome is `clean`, `changed`, or `blocked` |
| `/review-pr` | Review | Resolve a PR from its number, URL, branch, or ticket key, claim its worktree, sync it, run `/engineering:mob-review` there, then give the report path, whose ticks build the `/engineering:post-review-comments` prompt |
| `/post-review-comments` | Review | Post the rows you tick in a review report to the PR: apply your notes, show the drafts, then post them as one comment review and read them back |
| `/apply-review` | Review | Apply the rows you tick in a review report of your own branch: fix test-first, run the gates, commit once, push once, then reply on and resolve the ticked threads. Adds a result run to the report |
| `/sad-path` | Closure | Write a manual QA checklist that tries to break the changed forms and fields, as an HTML report with a setup table first. Each item cites a catalogue ID, and the fail ticks build a `/engineering:fix` prompt |
| `/pickup` | Closure | Confirm an open PR, claim its worktree, sync it by fast-forward only, then assess its open review threads into the review report, whose ticks build the `/engineering:apply-review` prompt |
| `/resolve-feedback` | Closure | Assess review feedback, pasted or from the open threads of a PR, and write a verdict, a recommendation, and a draft reply for each item to a review report. Its ticks build the `/engineering:apply-review` prompt. Applies no fix |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
| `/self-improve` | Maintenance | Mine a repo's fix commits, tracker bugs, review threads, failed CI runs, and the calibration backlog, put each proposal to you, apply the approved persona edits, and write a report and the repo's defect hotspots |
| `/update-personas` | Maintenance | Refresh `persona-best-practice` against installed and current versions, lint any persona's structure, and apply the approved calibration backlog |
| `/retro` | Maintenance | Read a session, find what in the skills, hooks, rules, and steering slowed or misled the agent, then apply and commit the fixes the user picks |
| `/tidy-up` | Maintenance | Delete the local working state of finished work in one repo, and fix the lines in open plans that finished work made stale |

### Personas

Each persona has `disable-model-invocation: true`. Start one by name, or let `/engineering:mob-review` start it.

| Persona | Reviews |
|---|---|
| `persona-a11y` | Semantic HTML, ARIA, labels, focus, keyboard |
| `persona-ac-check` | PR coverage of the acceptance criteria in a plan, a spec, or the ticket |
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

## Principles

The 14 principles come from pstack. Each is a skill with `disable-model-invocation: true`, so it costs no context. Type one, such as `/principle-fix-root-causes`, or let `/work-on` read it by path. The index with the full "when it applies" lines is in [`work-on/SKILL.md`](skills/work-on/SKILL.md).

| Principle | Group | Applies when |
|---|---|---|
| `/principle-redesign-from-first-principles` | Core | A new requirement in an existing design, a rewrite, or a migration |
| `/principle-subtract-before-you-add` | Core | Ordering an addition, a refactor, or a rewrite, or sizing a diff |
| `/principle-minimize-reader-load` | Core | Code that is hard to trace |
| `/principle-experience-first` | Core | A product, UX, or scope tradeoff |
| `/principle-build-the-lever` | Core | Any non-trivial work |
| `/principle-model-the-domain` | Architecture | Stateful logic, or code with many branches |
| `/principle-type-system-discipline` | Architecture | Types, signatures, validation, and adapters |
| `/principle-make-operations-idempotent` | Architecture | Commands and loops that run amid crashes and retries |
| `/principle-separate-before-serializing-shared-state` | Architecture | Concurrent writers to one target |
| `/principle-prove-it-works` | Verification | Before you say a task is done |
| `/principle-fix-root-causes` | Verification | Debugging, and fixes that fail on one premise |
| `/principle-sequence-verifiable-units` | Verification | Multi-step work, and stacked commits and PRs |
| `/principle-guard-the-context-window` | Delegation | Context is filling up |
| `/principle-encode-lessons-in-structure` | Meta | The same instruction written a second time |

## Installation

```json
{
  "enabledPlugins": {
    "engineering@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills`. Install `utility@xxkeefer-skills` and run `/install-rules`
too, so the `pause-list.md` rule stops the agent before a merge, a ready-for-review PR, or a posted
comment.

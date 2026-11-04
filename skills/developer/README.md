# Developer

Engineering workflows from ticket to PR, then review, debugging, and QA. Framework-agnostic and
language-agnostic, except the persona reviewers, which each review one kind of code.

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
| `/mob-review` | Review | Run every in-scope persona over a branch or PR, rank the findings, and ask which clear-cut fixes to apply on your own branch. In a handoff, it adds them as fix steps |
| `/review-pr` | Review | Resolve a PR from its number, URL, branch, or ticket key, claim its worktree, sync it, run `/mob-review` there, then offer `/post-review-comments` |
| `/post-review-comments` | Review | Post the review findings you tick to the PR: show each draft, then post the approved ones as one comment review. Five or more picks go to a handoff |
| `/create-pr` | Closure | Check the review for drift, fill the repo's PR template with an AC table and its gaps, then push and open a draft PR after one yes |
| `/happy-path` | Closure | Manual QA test plan for the current changeset |
| `/sad-path` | Closure | Write a manual QA checklist that tries to break the changed forms and fields. Each item cites a catalogue ID |
| `/pickup` | Closure | Confirm an open PR, claim its worktree, sync it by fast-forward only, then triage its review threads into a handoff |
| `/resolve-feedback` | Closure | Assess code review feedback |
| `/resolve-conflicts` | Closure | Resolve git merge/rebase conflicts with history-aware context |
| `/sync-docs` | Maintenance | Sync docs to code |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
| `/self-improve` | Maintenance | Mine a repo's fix commits, tracker bugs, review threads, failed CI runs, and the calibration backlog, put each proposal to you, apply the approved persona edits, and write a report and the repo's defect hotspots |
| `/update-personas` | Maintenance | Refresh `persona-best-practice` against installed and current versions, lint any persona's structure, and apply the approved calibration backlog |
| `/domain-modeling` | Anytime | Build and sharpen the project's domain model (glossary, ADRs) |
| `/codebase-design` | Anytime | Deep-module vocabulary the architecture skills compose |
| `/codebase-news` | Anytime | Table the notable changes in the current repo over a time period, from the changelogs first, then the commit history |

### Personas

Each persona has `disable-model-invocation: true`. Start one by name, or let `/mob-review` start it.

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
    "developer@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills`.

# Code Review

Persona reviewers, the review panel, and the PR review skills. The `developer` domain calls these
skills by name. Framework-agnostic and language-agnostic, except the persona
reviewers, which each review one kind of code.

## Skills

| Skill | Phase | Purpose |
|---|---|---|
| `/mob-review` | Review | Run every in-scope persona over a branch or PR and write the ranked findings to an HTML report. On someone else's branch, its ticks build the `/code-review:post-review-comments` prompt. On your own branch, its ticks build the `/code-review:apply-review` prompt, or in a handoff the `/developer:run-wave` prompt for another fix round. In a handoff, it records the report in the review step |
| `/light-review` | Review | Run the seven essential lanes of the panel (correctness, security, error handling, code quality, naming, test design, and architecture) and write the findings to the same report as `/code-review:mob-review`, with the same ticks and prompts |
| `/review-pr` | Review | Resolve a PR from its number, URL, branch, or ticket key, claim its worktree, sync it, run `/code-review:mob-review` there, then give the report path, whose ticks build the `/code-review:post-review-comments` prompt |
| `/post-review-comments` | Review | Post the rows you tick in a review report to the PR: apply your notes, show the drafts, then post them as one comment review and read them back |
| `/apply-review` | Review | Apply the rows you tick in a review report of your own branch: fix test-first, run the gates, commit once, push once, then reply on and resolve the ticked threads. Adds a result run to the report |
| `/sad-path` | Closure | Write a manual QA checklist that tries to break the changed forms and fields, as an HTML report. Each item cites a catalogue ID, and the fail ticks build a `/developer:fix` prompt |
| `/pickup` | Closure | Confirm an open PR, claim its worktree, sync it by fast-forward only, then assess its open review threads into the review report, whose ticks build the `/code-review:apply-review` prompt |
| `/resolve-feedback` | Closure | Assess review feedback, pasted or from the open threads of a PR, and write a verdict, a recommendation, and a draft reply for each item to a review report. Its ticks build the `/code-review:apply-review` prompt. Applies no fix |
| `/improve-codebase-architecture` | Maintenance | Scan for deepening opportunities, HTML report, grill through picks |
| `/self-improve` | Maintenance | Mine a repo's fix commits, tracker bugs, review threads, failed CI runs, and the calibration backlog, put each proposal to you, apply the approved persona edits, and write a report and the repo's defect hotspots |
| `/update-personas` | Maintenance | Refresh `persona-best-practice` against installed and current versions, lint any persona's structure, and apply the approved calibration backlog |

### Personas

Each persona has `disable-model-invocation: true`. Start one by name, or let `/code-review:mob-review` start it.

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
    "code-review@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills` and `developer@xxkeefer-skills`.

# Dev Personas

A panel of staff-engineer code reviewers. Each persona reviews one narrow lane of a diff and stays
out of the others. `/mob-review` runs every persona whose guard matches the diff, in parallel, and
merges the findings into one report ranked Change Requested, then Nit, then Future. `/sad-path`
turns the test data of the edge-case personas into a manual QA checklist.

## Skills

| Skill | Purpose |
|---|---|
| `/mob-review` | Run every in-scope persona over a branch or PR, rank the findings, and ask which clear-cut fixes to apply on your own branch. In a handoff, it adds them as fix steps |
| `/sad-path` | Write a manual QA checklist that tries to break the changed forms and fields. Each item cites a catalogue ID |
| `/self-improve` | Mine a repo's fix commits, tracker bugs, review threads, failed CI runs, and the calibration backlog, put each proposal to you, apply the approved persona edits, and write a report and the repo's defect hotspots |
| `/update-personas` | Refresh `persona-best-practice` against installed and current versions, lint any persona's structure, and apply the approved calibration backlog |

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
    "dev-personas@xxkeefer-skills": true
  }
}
```

`primitives` is required.

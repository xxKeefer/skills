# Developer

Opinionated engineering workflows covering the full lifecycle: investigation, planning,
implementation, and closure. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Developer skills reference `/grill-it` and `/write-to-file` from the `primitives` plugin. Both must be installed.

## Workflow

```
spike-it -> task-it -> plan-it -> do-it (uses tdd) -> close-it
                        ^                               ^
                    design-it (explore APIs)      resolve-it (PR feedback)
                    hunt-it (track bugs)

Anytime: explain-it, document-it, improve-it, qa-it
```

## Skills

| Skill | Purpose |
|---|---|
| `/spike-it` | Deep-dive investigation of a problem |
| `/task-it` | Decompose a spike into tracked tickets |
| `/plan-it` | Break a task into ordered, atomic steps |
| `/do-it` | Execute a plan step-by-step via /tdd |
| `/tdd` | Red-green-refactor loop |
| `/close-it` | Commit strategy, PR description, QA test plan |
| `/hunt-it` | Trace a bug from report to root cause |
| `/resolve-it` | Critically assess code review feedback |
| `/design-it` | Generate multiple radically different interface designs |
| `/document-it` | Sync documentation to code changes |
| `/improve-it` | Find architectural improvement opportunities |
| `/qa-it` | Generate manual QA test plans |
| `/explain-it` | Unpack agent reasoning transparently |
| `/setup-guard-rails-typescript` | Pre-commit hooks for formatting, types, and tests |

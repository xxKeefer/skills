# Developer

Engineering workflows from a plan to working code: claim a worktree, prototype, implement
test-first, debug, fix, and run manual QA. Framework-agnostic, language-agnostic -- pure
best-practice software engineering principles.

## Dependencies

Developer skills reference `/grill`, `/write-to-file`, and `/look-up` from the `primitives` plugin;
all must be installed.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

## Review

The [`review`](../review/README.md) domain holds the persona reviewers, the review panels, and the
PR review skills. A developer skill names a review skill with the `review:` prefix, and reads no
file in that domain.

## Composed by other domains

`engineering` and `review` call these skills by name. Before you change one, keep what the last
column names, or change each caller in the same commit.

| Skill | Called by | Must keep |
|---|---|---|
| `claim` | `start-ticket`, `split-ticket`, `squash-bugs`, `review:review-pr`, `review:pickup` | Its return (path, branch, handoff), the `Worktree:` line that `/do-next` reads, and the search for a handoff whose file name holds the key |
| `auto-handoff` | `review:mob-review` | The `D` and `N` entry format in `STEP.md` |
| `codebase-design` | `improve-codebase-architecture` | Its glossary terms |
| `domain-modeling` | `improve-codebase-architecture`, the domain doc that `utility:set-up-dev-workflow-skills` installs | The `CONTEXT.md` and ADR formats |
| `fix` | `diagnose`, the QA checklists of `happy-path` and `review:sad-path` | Its input: a description of what is broken, or a QA report prompt (`@<report> <IDs>`) |
| `tdd` | Each step of a `start-ticket` plan that changes behaviour | These two lines in `SKILL.md`: "A seam that the handoff step names is agreed" and "Test the conditions whose IDs the step names" |

## Loading

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

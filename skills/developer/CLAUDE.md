# Developer

Implementing code, broadly: refine, scope, split, and plan a ticket, claim a worktree, prototype,
implement test-first, debug, fix, run manual QA, and open the PR. Code review comes from
`code-review`. Framework-agnostic, language-agnostic -- pure best-practice software engineering
principles.

## Dependencies

Developer skills reference `/grill`, `/write-to-file`, `/write-report`, `/look-up`, `/do-next`, and
`/update-handoff` from the `primitives` plugin; all must be installed. `start-ticket` names
`/code-review:mob-review` and `/code-review:self-improve`, so install `code-review` too.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

[`TEST-APPROACH.md`](TEST-APPROACH.md) holds the risk and technique method. `start-ticket` and
`create-pr` read it. `tdd` holds the same text in `risk-and-technique.md`, and
`code-review:self-improve` uses the same defect tokens. A change to one file needs the same change
to the others.

## Review

The [`code-review`](../code-review/README.md) domain holds the persona reviewers, the review panels, and the
PR review skills. A developer skill names a review skill with the `code-review:` prefix, and reads no
file in that domain.

## Composed by other skills

Skills in `code-review` and `utility`, and other developer skills, call these skills by
name. Before you change one, keep what the last column names, or change each caller in the same
commit.

| Skill | Called by | Must keep |
|---|---|---|
| `claim` | `start-ticket`, `split-ticket`, `squash-bugs`, `code-review:review-pr`, `code-review:pickup` | Its return (path, branch, handoff), the `Worktree:` line that `/do-next` reads, and the search for a handoff whose file name holds the key |
| `auto-handoff` | `code-review:mob-review` | The `D` and `N` entry format in `STEP.md` |
| `codebase-design` | `code-review:improve-codebase-architecture` | Its glossary terms |
| `domain-modeling` | `code-review:improve-codebase-architecture`, the domain doc that `utility:set-up-dev-workflow-skills` installs | The `CONTEXT.md` and ADR formats |
| `fix` | `diagnose`, the QA checklists of `happy-path` and `code-review:sad-path` | Its input: a description of what is broken, or a QA report prompt (`@<report> <IDs>`) |
| `tdd` | Each step of a `start-ticket` plan that changes behaviour | These two lines in `SKILL.md`: "A seam that the handoff step names is agreed" and "Test the conditions whose IDs the step names" |
| `diagnose` | The user. `squash-bugs` writes its hunt docs to the same path | The hunt doc `hunt_<KEY>.md`, written with `/write-to-file`, doctype `hunt` |
| `happy-path` | `code-review:sad-path`, which adds its run to the same report | Model invocation (no `disable-model-invocation`), and the `/write-report` kind `qa`, so that both runs write to one file |

## Loading

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

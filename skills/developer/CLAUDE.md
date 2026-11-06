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

## Loading

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

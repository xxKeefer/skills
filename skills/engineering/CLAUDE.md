# Engineering

Engineering workflows from ticket to PR: scoping, planning, implementation, and opening the PR,
then review, debugging, and QA. Framework-agnostic, language-agnostic -- pure best-practice
software engineering principles.

## Dependencies

Engineering skills reference `/grill`, `/write-to-file`, `/write-report`, and `/look-up` from the
`primitives` plugin, and `/review:mob-review` from the `review` plugin. Install both domains.

Name a review skill with its `review:` prefix, such as `/review:mob-review`. `developer` holds
skills with the same names.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

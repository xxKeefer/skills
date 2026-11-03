# Dev Personas

A panel of code reviewers. Each `persona-*` skill reviews one narrow lane of a diff, such as
naming, accessibility, or query caching. `mob-review` runs every persona whose guard matches the
diff, in parallel, and merges their findings into one ranked report. `update-personas` keeps the
personas accurate.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

## The agnostic bar

The repo's North Star is everything-agnostic. A persona is a review lane for one kind of code, so
it can name languages, frameworks, libraries, and public tools (Vue, TanStack Query, Spring Boot,
Liquibase, Playwright, Sentry, PostHog, GitHub Actions). A persona names no employer or client
code:

- no company, product, team, or person names
- no internal repo names, file paths, package names, component names, or API names
- no ticket keys, PR numbers, wiki page IDs, or links to private repos
- no history notes that say where a rule was seen. The rule stands on its own

A persona does not restate an employer's internal docs, even with the names removed. No regex
checks this rule, so it binds whoever imports a persona.

Where a rule depends on a project choice (the design-system component for an input, the app's
error taxonomy, the analytics wrapper), describe the role and let the reviewer find the project's
own name in the repo (`CLAUDE.md`, `AGENTS.md`, `package.json`, the code).

The repo's pre-commit hook checks the name rules on every commit. The root `README.md` tells you
how to turn it on. To run it by hand, run `.githooks/pre-commit` from the repo root.

## Rules for editing personas

- A persona's directory name must match its `name:` and its row in the `mob-review` panel table.
- Every `persona-*` keeps `disable-model-invocation: true`. Only `mob-review` or the user starts
  one.
- Keep the section order: Guard, Scope, What you review, Out of lane, Severity, Output.
- Keep the output contract unchanged: the `ReportFindings` paragraph and the
  `{"persona": ...}` JSON line. `mob-review` parses the JSON.
- Never renumber a rule. Findings and other personas cite rules by number. Give a new rule the
  next number in its section. A removed rule leaves a gap.
- Every rule must be checkable against a changed line in a diff.
- A guard change needs the same change to the persona's Guard column in `mob-review`.
- Inside a persona, `$SKILL_DIR` means that persona's own directory. `mob-review` tells each
  subagent the absolute path.

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

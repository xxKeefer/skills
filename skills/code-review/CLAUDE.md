# Code Review

Persona reviewers, the review panel, and the PR review skills. The `developer` domain calls these
skills by name.

## Dependencies

Review skills call `/write-to-file`, `/write-report`, `/look-up`, and `/do-next` from the
`primitives` plugin, and `/claim`, `/codebase-design`, and `/domain-modeling` from the
`developer` plugin. `review-pr` and `pickup` call `/claim`, `improve-codebase-architecture` calls
`/codebase-design` and `/domain-modeling`, and the `sad-path` report builds a `/developer:fix`
prompt, so install both domains.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

### light-review

`light-review` has no steps of its own. It follows the `mob-review` steps with a list of eight
lanes.

- A change to a `mob-review` step also changes `light-review`. Check each change that
  `light-review` makes to that step.
- A persona rename also changes the lane list in `light-review`.

## Personas

The review panel is a set of code reviewers. Each `persona-*` skill reviews one narrow lane of a diff, such as
naming, accessibility, or query caching. `mob-review` runs every persona whose guard matches the
diff, in parallel, and merges their findings into one ranked HTML report. `update-personas` keeps the
personas accurate. `self-improve` mines a repo's fixes, tracker bugs, review threads, CI failures,
and the calibration backlog for persona edits, and `update-personas` applies the ones you approve.
It also writes the repo's defect hotspots, which `persona-test-design` reads.
`sad-path` turns the test data of the edge-case personas into a manual QA checklist in HTML.
The rules below bind the `persona-*` skills only.

### The agnostic bar

The repo's North Star is everything-agnostic. A persona is a review lane for one kind of code, so
it can name languages, frameworks, libraries, and public tools (Vue, TanStack Query, Express,
Prisma, Playwright, Sentry, PostHog, GitHub Actions). A persona names no employer or client
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

### Rules for editing personas

- A persona's directory name must match its `name:` and its row in the `mob-review` panel table.
- Every `persona-*` keeps `disable-model-invocation: true`. Only `mob-review` or the user starts
  one.
- Keep the section order: Guard, Scope, What you review, Out of lane, Severity, Output.
- Every persona follows [`PERSONA-CONTRACT.md`](PERSONA-CONTRACT.md). The first line under the
  frontmatter is this pointer, word for word: "Read
  [`PERSONA-CONTRACT.md`](../../PERSONA-CONTRACT.md) before you start, and follow every rule in
  it."
- Do not copy contract text into a persona. Scope holds only the lane paths and the lane's own
  reads. Output holds the category slug, the anchor when it is not the changed line, what `detail`
  and `suggestion` hold, and any grouping rule.
- `mob-review` parses the contract's JSON. A change to that JSON needs the same change to
  `mob-review` Steps 4 and 5.
- A persona `SKILL.md` over 10 KB is sprawl. When an edit takes it over, move what only some diffs
  need, such as one file type, examples, or stack facts, to `references/`. Leave one line that
  says when to read the file. A moved rule keeps its number. What every diff needs stays inline,
  even when the file stays over 10 KB.
- Never renumber a rule. Findings and other personas cite rules by number. Give a new rule the
  next number in its section. A removed rule leaves a gap.
- Every rule must be checkable against a changed line in a diff.
- A guard change needs the same change to the persona's Guard column in `mob-review`.
- `sad-path` reads the Guard of each lane it lists, and links that persona's
  `references/fixtures.md` and `references/catalogue.md`. A move or rename of those files needs
  the same change in `sad-path`.
- Inside a persona, `$SKILL_DIR` means that persona's own directory. `mob-review` tells each
  subagent the absolute path.

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

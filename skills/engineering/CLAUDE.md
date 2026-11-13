# Engineering

Software engineering from an idea to a merged PR: nine lifecycle commands, and the skills they run.
Framework-agnostic and language-agnostic, except the persona reviewers.
[ADR 0013](../../docs/adr/0013-one-engineering-domain.md) merged `developer` and `code-review`
into this domain.

## Dependencies

Engineering skills call `/grill`, `/write-to-file`, `/write-report`, `/look-up`, `/do-next`, and
`/update-handoff` from the `primitives` plugin, so install it too.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a row there.

[`TEST-APPROACH.md`](TEST-APPROACH.md) holds the risk and technique method. `start-ticket` and
`create-pr` read it. `tdd` holds the same text in `risk-and-technique.md`, and `self-improve` uses
the same defect tokens. A change to one file needs the same change to the others.

## Commands

The nine commands (`spec`, `plan`, `build`, `test`, `constraints`, `review`, `webperf`,
`code-simplify`, `ship`) are the entry points.

- Each command has `disable-model-invocation: true`. Only the user starts one.
- Each description starts with `★ `, so the commands stand out in the terminal list. A skill that is
  not a command has no ★.
- A command picks a skill and runs it by name. It holds no step that a skill below it already holds.
  When a skill changes its input or its return, check each command that runs it.
- `webperf`, `constraints`, and `code-simplify` hold their own steps, because no skill below them
  does the work.

## Composed by other skills

Skills in `utility`, and other engineering skills, call these skills by name. Before you change one, keep what the last column names, or change each caller in the same
commit.

| Skill | Called by | Must keep |
|---|---|---|
| `claim` | `start-ticket`, `split-ticket`, `squash-bugs`, `review-pr`, `pickup` | Its return (path, branch, handoff), the `Worktree:` line that `/do-next` reads, and the search for a handoff whose file name holds the key |
| `run-wave` | `mob-review`, and the prompt of its report in a handoff | The `D` and `N` entry format in `STEP.md`, and the `Handoff` meta key that it reads from the report |
| `codebase-design` | `improve-codebase-architecture` | Its glossary terms |
| `domain-modeling` | `improve-codebase-architecture`, the domain doc that `utility:set-up-dev-workflow-skills` installs | The `CONTEXT.md` and ADR formats |
| `fix` | `diagnose`, the QA checklists of `happy-path` and `sad-path` | Its input: a description of what is broken, or a QA report prompt (`@<report> <IDs>`) |
| `tdd` | Each step of a `start-ticket` plan that changes behaviour | These two lines in `SKILL.md`: "A seam that the handoff step names is agreed" and "Test the conditions whose IDs the step names" |
| `diagnose` | The user. `squash-bugs` writes its hunt docs to the same path | The hunt doc `hunt_<KEY>.md`, written with `/write-to-file`, doctype `hunt` |
| `happy-path` | `sad-path`, which adds its run to the same report | Model invocation (no `disable-model-invocation`), and the `/write-report` kind `qa`, so that both runs write to one file |

## light-review

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

## Loading

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.

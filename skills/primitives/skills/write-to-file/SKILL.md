---
name: write-to-file
description: >
  Write a map, spec, plan, findings, report, or scratch file to `.ai/`, or to the folder that the
  user's instructions name for its doctype. Use whenever a skill or workflow makes a document to
  `@`-reference later.
---

Write the given content to the output folder for its doctype.

## Doctypes

| Doctype | Holds | Template |
|---|---|---|
| `map` | the order of many units, shared decisions, a tick per unit | none yet |
| `spec` | what to build for one change, and why | [`templates/spec.md`](templates/spec.md) |
| `plan` | goal, steps, progress, pending decisions, follow-ups | [`templates/plan.md`](templates/plan.md) |
| `findings` | a question, its answer, the evidence, open points | none yet |
| `report` | a review or audit result, often HTML with a JSON `runs` block and rows to tick | none yet |
| `scratch` | anything | none |

Refuse any other doctype. Write no file, and reply with the six doctypes above. When the caller
names no doctype, use `scratch`.

A file with a template has the template's layout. After you write a `plan`, run
`python3 scripts/check_plan.py <absolute plan path>` from this skill's folder. After you write a
`spec`, run `python3 scripts/check_spec.py <absolute spec path>` from this skill's folder. On exit
1, fix each line that it names, and run it again. Give the last line of the check, the open count,
to the caller.

## Behaviour

1. Check the doctype against the set above.
2. Pick the folder. If the user's instructions (CLAUDE.md, AGENTS.md) name a folder for this
   doctype, use it, with any layout they give, such as one subfolder per ticket or topic.
   Otherwise use `.ai/` in the main worktree root, so all linked worktrees of a repo share one
   folder. The main worktree root is the parent folder of
   `git rev-parse --path-format=absolute --git-common-dir`. Outside a git repo, use `.ai/` in the
   current working directory.
3. Ensure the folder exists
4. Write the file to `{folder}/{filename}`
5. For a `plan` or a `spec`, run its check
6. Report the written path so the user can load it with `@{path}`

**Done when:** the file exists at the path you reported, and a `plan` or a `spec` passes its check. For a
doctype outside the set, you wrote no file and named the set.

## Check a plan

A caller can ask you to check a plan. Run `python3 scripts/check_plan.py <absolute plan path>` from this skill's
folder. Change no line of the plan. Return the exit code, each error line, and the last line, which
gives the count of open decisions. For a file with no YAML header, also say that a migration
request (below) moves it to the plan layout.

**Done when:** you returned the exit code, the errors, and the count of open decisions.

## Check a spec

A caller can ask you to check a spec. Run `python3 scripts/check_spec.py <absolute spec path>` from this skill's
folder. Change no line of the spec. Return the exit code, each error line, and the
`open questions: <n>` line.

**Done when:** you returned the exit code and the errors.

## Migrate a plan

A caller can ask you to migrate a plan in the old layout, which has no YAML header. Run
`python3 scripts/migrate_plan.py <absolute plan path>` from this skill's folder. It changes a file that has a
header in no way. Then run the check, and report each line that it names.

**Done when:** the file has a YAML header, and you reported the result of the check.

## Naming convention

Pattern: `{doctype}_{terse-description}.{ext}`

Examples:

| Doctype | Example filename |
|---|---|
| `plan` | `plan_auth-rewrite.md` |
| `findings` | `findings_bundler-comparison.md` |
| `scratch` | `scratch_api-sketch.md` |

`{terse-description}` is a short kebab-case slug derived from the task description — **unless** the
repo's context defines a tracking mechanism for the work, in which case prefer that identifier so the
file is traceable back to its source of truth.

- If the work has a defined tracker (a Jira/Linear key, a GitHub issue number, a changeset id,
  whatever the project uses), use it: `plan_PROJ-123.md`, `findings_gh-1421.md`.
- Otherwise fall back to the kebab-case slug: `plan_auth-rewrite.md`.

A tracking mechanism counts as "defined" when it's discoverable from context — named in the prompt,
the current branch, an open ticket, or the project's CLAUDE.md/conventions. Don't invent one; only use
a tracker that already exists.

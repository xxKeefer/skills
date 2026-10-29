---
name: write-to-file
description: >
  Write planning, spike, handoff, or intermediary files to `.ai/` at the project root, or to the
  folder that the user's instructions name for the doctype. Model-invocable -- other skills delegate
  file output here instead of managing paths themselves. Use whenever a skill or workflow produces a
  document that needs to persist for later `@`-reference in future prompts.
---

Write the given content to the output folder for its doctype.

## Behaviour

1. Pick the folder. If the user's instructions (CLAUDE.md, AGENTS.md) name a folder for this
   doctype, use it, with any layout they give, such as one subfolder per ticket or topic.
   Otherwise use `.ai/` in the root of the current working directory.
2. Ensure the folder exists
3. Write the file to `{folder}/{filename}`
4. Report the written path so the user can load it with `@{path}`

**Done when:** the file exists at the path you reported.

## Naming convention

Pattern: `{doctype}_{terse-description}.{ext}`

Examples:

| Doctype | Example filename |
|---|---|
| `plan` | `plan_auth-rewrite.md` |
| `handoff` | `handoff_auth-rewrite.md` |
| `research` | `research_bundler-comparison.md` |
| `scratch` | `scratch_api-sketch.md` |

`{terse-description}` is a short kebab-case slug derived from the task description — **unless** the
repo's context defines a tracking mechanism for the work, in which case prefer that identifier so the
file is traceable back to its source of truth.

- If the work has a defined tracker (a Jira/Linear key, a GitHub issue number, a changeset id,
  whatever the project uses), use it: `plan_ENG-29019.md`, `research_gh-1421.md`.
- Otherwise fall back to the kebab-case slug: `plan_auth-rewrite.md`.

A tracking mechanism counts as "defined" when it's discoverable from context — named in the prompt,
the current branch, an open ticket, or the project's CLAUDE.md/conventions. Don't invent one; only use
a tracker that already exists.

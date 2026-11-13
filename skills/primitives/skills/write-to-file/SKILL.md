---
name: write-to-file
description: >
  Write a plan, spike, handoff, or other working file to `.ai/`, or to the folder that the user's
  instructions name for its doctype. Use whenever a skill or workflow makes a document to
  `@`-reference later.
---

Write the given content to the output folder for its doctype.

## Behaviour

1. Pick the folder. If the user's instructions (CLAUDE.md, AGENTS.md) name a folder for this
   doctype, use it, with any layout they give, such as one subfolder per ticket or topic.
   Otherwise use `.ai/` in the main worktree root, so all linked worktrees of a repo share one
   folder. The main worktree root is the parent folder of
   `git rev-parse --path-format=absolute --git-common-dir`. Outside a git repo, use `.ai/` in the
   current working directory.
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
  whatever the project uses), use it: `plan_PROJ-123.md`, `research_gh-1421.md`.
- Otherwise fall back to the kebab-case slug: `plan_auth-rewrite.md`.

A tracking mechanism counts as "defined" when it's discoverable from context — named in the prompt,
the current branch, an open ticket, or the project's CLAUDE.md/conventions. Don't invent one; only use
a tracker that already exists.

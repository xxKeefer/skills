---
name: write-to-file
description: >
  Write planning, spike, or intermediary files to `.ai/` at the project root. Model-invocable --
  other skills delegate file output here instead of managing paths themselves. Use whenever a skill
  or workflow produces a document that needs to persist for later `@`-reference in future prompts.
---

Write the given content to `.ai/` in the root of the current working directory.

## Behaviour

1. Ensure `.ai/` exists at the working directory root
2. Write the file to `.ai/{filename}`
3. Report the written path so the user can load it with `@.ai/{filename}`

## Naming conventions

| Source | Filename pattern |
|---|---|
| `/spike-it` | `spike_{identifier}.md` |
| `/plan-it` | `plan_{identifier}.md` |
| `/task-it` | `tasks_{identifier}.md` |
| Other | `{descriptive_slug}.md` |

`{identifier}` is a ticket key (e.g. `ENG-123`) when available, otherwise a short kebab-case slug
derived from the task description.

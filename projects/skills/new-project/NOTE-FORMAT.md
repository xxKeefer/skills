# Note Format

Task notes live in `tasks/` and are created from kanban cards via the obsidian-kanban
"New note from card" action. Each note is a card's working space -- the card is the handle on the
board, the note is where the detail lives.

The `_template.md` written into `tasks/` during `/new-project` scaffolding is the on-disk template
the plugin uses when creating new card notes (configured via `new-note-template` in the board's
`%% kanban:settings %%` block).

## Template

```md
---
type: project/task
project: "[[{slug}.kanban]]"
status: todo
tags: [project, task]
---

# {Card Title}

## Context

> Why this task exists and how it fits the mission. One short paragraph.

## Acceptance Criteria

- [ ] ...

## Notes

```

## Rules

- **`project` frontmatter is a wikilink to the board.** Use just the filename (`[[{slug}.kanban]]`)
  so Obsidian resolves it without a hardcoded path.
- **`status` mirrors the card's column.** `todo` → `doing` → `done`. Keep it in sync with the board.
- **Card title and note filename must match.** The board links to the note by filename; rename both
  together or the wikilink breaks.
- **Context is mandatory, the rest is optional.** If you can't write a context sentence, the task
  isn't scoped well enough to start.
- **Acceptance Criteria are the definition of done.** When all boxes are checked, move the card to Done.

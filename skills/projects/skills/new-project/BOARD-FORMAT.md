# BOARD-FORMAT.md

The project board is a single markdown file, `<slug>.kanban.md`, in the obsidian-kanban format.
Under the hood it is just headings (columns) and checkboxes (cards) -- fully readable and editable
without the plugin, fully visual with it.

## Template

````md
---
kanban-plugin: board
type: project/board
tags: [project, kanban]
---

## Backlog

- [ ] First task
- [ ] Another task

## Next

- [ ] A task scoped for this week @{YYYY-MM-DD}

## Doing

- [ ] A task in progress

## Done

**Complete**

- [x] A finished task

%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false],"new-note-folder":"{projects-dir}/{slug}/tasks","new-note-template":"{projects-dir}/{slug}/tasks/_template.md"}
```
%%
````

## Rules

- **Columns are `##` headings.** The default four: `Backlog`, `Next`, `Doing`, `Done`. Adjust
  per project, but keep `Next` and `Done`.
- **Cards are checkboxes.** `- [ ] text` for open, `- [x] text` for complete. One card per line.
- **Deadlines use the obsidian-kanban date tag.** Append `@{YYYY-MM-DD}` to a card.
- **The `Done` column starts with a `**Complete**` marker line.** This is the obsidian-kanban
  convention that lets the plugin auto-archive completed cards. Leave it in place.
- **The `%% kanban:settings %%` block must stay at the end.** It is what tells obsidian-kanban to
  render the file as a board rather than a note. Do not drop it.
- **Frontmatter `kanban-plugin: board` is required** for the plugin to recognise the file.
- **Cards can link to task notes.** Use the obsidian-kanban "New note from card" action to promote
  a card into a wikilink: `- [ ] [[Card Title]]`. The note lands in `tasks/` (set via
  `new-note-folder`) using `tasks/_template.md` as its starting content (set via `new-note-template`).
  Both paths in the settings block are vault-relative -- substitute actual paths when writing the
  board during `/new-project`.
- **Card edits are mostly manual.** The user moves and checks off cards by hand. Only
  `/new-project` writes to the board (initial structure); after that, skills only read it.

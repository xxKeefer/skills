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

## This Week

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

- **Columns are `##` headings.** The default four: `Backlog`, `This Week`, `Doing`, `Done`. Adjust
  per project, but keep `This Week` and `Done` -- `/summarize-sprint` and `/project-status` read them.
- **Cards are checkboxes.** `- [ ] text` for open, `- [x] text` for complete. One card per line.
- **Deadlines use the obsidian-kanban date tag.** Append `@{YYYY-MM-DD}` to a card. These are the
  dates `/schedule-goals` mirrors into `occasions.md` and `/project-status` surfaces as upcoming.
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
- **Card edits are mostly manual.** The user moves and checks off cards by hand. Three skills write
  to the board: `/new-project` (initial structure), `/capture-goals` (appends new cards to Backlog
  and triages into This Week during a planning session), and `/close-project` (archives the file).
  All other skills only read the board.

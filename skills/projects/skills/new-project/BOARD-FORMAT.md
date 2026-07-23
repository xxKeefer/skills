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
{"kanban-plugin":"board","list-collapse":[false,false,false,false],"new-note-folder":"{projects-dir}/{slug}/tasks","new-note-template":"{projects-dir}/{slug}/tasks/_template.md","tag-colors":[{"tagKey":"#epic","color":"rgba(255,255,255,1)","backgroundColor":"rgba(68,0,68,1)"},{"tagKey":"#urgent","color":"rgba(255,255,255,1)","backgroundColor":"rgba(204,0,0,1)"},{"tagKey":"#blocked","color":"rgba(255,255,255,1)","backgroundColor":"rgba(96,0,0,1)"},{"tagKey":"#now","color":"rgba(0,0,0,1)","backgroundColor":"rgba(255,229,0,1)"},{"tagKey":"#bug","color":"rgba(255,255,255,1)","backgroundColor":"rgba(161,62,0,1)"},{"tagKey":"#visbug","color":"rgba(255,255,255,1)","backgroundColor":"rgba(161,62,0,1)"},{"tagKey":"#afk","color":"rgba(255,255,255,1)","backgroundColor":"rgba(0,68,68,1)"},{"tagKey":"#hitl","color":"rgba(0,0,0,1)","backgroundColor":"rgba(0,205,205,1)"},{"tagKey":"#techdebt","color":"rgba(0,0,0,1)","backgroundColor":"rgba(255,255,255,1)"},{"tagKey":"#later","color":"rgba(255,255,255,1)","backgroundColor":"rgba(51,51,51,1)"}],"tag-sort":[{"tag":"#epic"},{"tag":"#urgent"},{"tag":"#blocked"},{"tag":"#now"},{"tag":"#bug"},{"tag":"#visbug"},{"tag":"#afk"},{"tag":"#hitl"},{"tag":"#techdebt"},{"tag":"#later"}]}
```
%%
````

## Universal Project Tags

Every board's settings block carries a canonical `tag-colors`/`tag-sort` pair so tags render
consistently across every project without per-board setup. Sort order below (top to bottom) is
the intended `tag-sort` order -- `#epic` first, `#later` last.

| Tag | Signal | Text (hex) | Background (hex) |
|---|---|---|---|
| #epic | Organisation / Sequencing | fff | 440044 |
| #urgent | Priority 0 | fff | cc0000 |
| #blocked | Sequencing, task will ref blockers | fff | 600000 |
| #now | Priority 1 | 000 | ffe500 |
| #bug | Any logic or functionality defects | fff | a13e00 |
| #visbug | Purely visual defects | fff | a13e00 |
| #afk | Agent to complete without human | fff | 004444 |
| #hitl | Human to work on task with/without agent | 000 | 00cdcd |
| #techdebt | Meta work to improve the code | 000 | fff |
| #later | Priority negative 1 | fff | 333 |

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
- **The settings block always carries the canonical `tag-colors`/`tag-sort` pair** (see Universal
  Project Tags above). Skills adding project-specific tags must append to these arrays, not
  replace them.
- **Cards can link to task notes.** Use the obsidian-kanban "New note from card" action to promote
  a card into a wikilink: `- [ ] [[Card Title]]`. The note lands in `tasks/` (set via
  `new-note-folder`) using `tasks/_template.md` as its starting content (set via `new-note-template`).
  Both paths in the settings block are vault-relative -- substitute actual paths when writing the
  board during `/new-project`.
- **Cards can carry a block ID.** obsidian-kanban's "Copy link to card" appends `^{blockid}` to a
  card line and gives you `[[{slug}.kanban#^{blockid}]]` -- an Obsidian-generated, collision-free
  handle for that exact card, sturdier than matching on text. Skills that rewrite a card line must
  preserve its trailing `^{blockid}` if present; other notes may already link to it.
- **Day-to-day card moves are manual.** The user moves and checks off cards by hand. Skills may
  append to the board when invoked for that purpose (`/new-project` scaffolding it, `/promote-card`
  turning a card into a spec + tickets). Appending is always fine; removing or rewriting a card
  someone else added is not -- if a card looks obsolete or wrong, ask first, or replace it with a
  new card that wikilinks back to the old one and states why.

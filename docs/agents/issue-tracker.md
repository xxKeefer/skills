# Issue tracker: Obsidian Kanban

Issues for this repo live as cards on the `agentic-skills` kanban board in the user's Obsidian
vault (obsidian-kanban plugin format).

The board and task-note format are owned by the `projects` domain, not duplicated here -- read
`projects:skills/new-project/BOARD-FORMAT.md` and `projects:skills/new-project/NOTE-FORMAT.md` for
the canonical shape (columns, card tags, block-link targeting, task note frontmatter, the spec/
ticket note split). This file covers only what's specific to using that board as this repo's
tracker.

## Locations

- **Vault**: `~/studio/notes/`
- **Project workspace**: `~/studio/notes/05-projects/agentic-skills/`
- **Board**: `~/studio/notes/05-projects/agentic-skills/agentic-skills.kanban.md`
- **Task notes**: `~/studio/notes/05-projects/agentic-skills/tasks/`

## When a skill says "publish to the issue tracker"

Append a `- [ ]` card to `Backlog` (or the column the user names), per BOARD-FORMAT.md's
append-only rule. If the content is more than one line, write a task note -- spec or ticket, per
NOTE-FORMAT.md -- and make the card a wikilink to it.

`/promote-card` feeds this. It grills a rough thought jotted on the board, with no code context
yet, into a spec, then publishes it the same way.

## When a skill says "fetch the relevant ticket"

Find the card by name on the board; if it's a wikilink, read the task note it points to. Prefer a
block link (`[[agentic-skills.kanban#^<blockid>]]`, from obsidian-kanban's "Copy link to card") if
the user gives one -- unambiguous, per BOARD-FORMAT.md.

## Triage state

Triage roles are inline tags on the card, using the role strings from `triage-labels.md`
(`#needs-triage`, `#needs-info`, `#afk`, `#hitl`, `#wontfix`). Replace the old role tag when the
state changes. A `#wontfix` card moves to the archive.

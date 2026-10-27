# Issue tracker: Obsidian Kanban

Issues for this repo live as cards on a per-project kanban board in the user's Obsidian vault
(obsidian-kanban plugin format). Setup fills in the paths below -- never guess them.

The board and task-note format are owned by the `projects` domain, not duplicated here -- read
`projects:skills/new-project/BOARD-FORMAT.md` and `projects:skills/new-project/NOTE-FORMAT.md` for
the canonical shape (columns, card tags, block-link targeting, task note frontmatter, the spec/
ticket note split). This file covers only what's specific to using that board as a tracker.

## Locations

- **Project workspace**: `<vault>/<projects-dir>/<project-slug>/` — the projects directory is
  found by scanning the vault for a `*projects` directory (e.g. `05-projects/`)
- **Board**: `<workspace>/<project-slug>.kanban.md`
- **Task notes**: `<workspace>/tasks/`

## When a skill says "publish to the issue tracker"

Append a `- [ ]` card to `Backlog` (or the column the user names), per BOARD-FORMAT.md's
append-only rule. If the content is more than one line, write a task note -- spec or ticket, per
NOTE-FORMAT.md -- and make the card a wikilink to it.

`/promote-card` feeds this. It grills a rough thought jotted on the board, with no code context
yet, into a spec, then publishes it the same way.

## When a skill says "fetch the relevant ticket"

Find the card by name on the board; if it's a wikilink, read the task note it points to. Prefer a
block link (`[[<board>#^<blockid>]]`, from obsidian-kanban's "Copy link to card") if the user gives
one -- unambiguous, per BOARD-FORMAT.md.

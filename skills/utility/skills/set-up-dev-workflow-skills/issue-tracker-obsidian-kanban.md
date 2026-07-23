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

Two entry points feed this, depending on how much groundwork is already done:

- **`/to-spec` / `/to-tickets`** -- the investigation already happened in-conversation; these just
  publish the result.
- **`/promote-card`** -- a rough thought jotted on the board with no code context yet; this grills
  it into a spec first, then publishes the same way.

## When a skill says "fetch the relevant ticket"

Find the card by name on the board; if it's a wikilink, read the task note it points to. Prefer a
block link (`[[<board>#^<blockid>]]`, from obsidian-kanban's "Copy link to card") if the user gives
one -- unambiguous, per BOARD-FORMAT.md.

## Triage state

Triage roles are inline tags on the card, using the role strings from `triage-labels.md`
(defaults: `#needs-triage`, `#needs-info`, `#ready-for-agent`, `#ready-for-human`, `#wontfix`).
Replace the old role tag when the state changes. A `#wontfix` card moves to the archive.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a task note; its **child** tickets are wikilinked cards.

- **Map**: `tasks/<effort>-map.md` — the Notes / Decisions-so-far / Fog body, listing children
  in priority order. Its own card sits on the board tagged `#epic`.
- **Child ticket**: a card wikilinking `tasks/<slug>.md`. The note carries a `Type:` line
  (`research`/`prototype`/`grilling`/`task`) and the question in the body.
- **Blocking**: a `Blocked by: [[<note>]], [[<note>]]` line near the top of the child note, plus
  a `#blocked` tag on its card. Unblocked when every listed note's card is under `Done` — remove
  the tag then.
- **Frontier**: first child in map order whose card is not under `Doing`/`Done`, not `#blocked`,
  and unclaimed.
- **Claim**: move the card to `Doing` — the session's first write.
- **Resolve**: append the answer under `## Answer` in the child note, move its card to `Done`,
  then append a context pointer (gist + link) to the map's Decisions-so-far.

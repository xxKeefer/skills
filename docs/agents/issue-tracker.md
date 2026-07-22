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

Two entry points feed this, depending on how much groundwork is already done:

- **`/to-spec` / `/to-tickets`** -- the investigation already happened in-conversation; these just
  publish the result.
- **`/promote-card`** -- a rough thought jotted on the board with no code context yet; this grills
  it into a spec first, then publishes the same way.

## When a skill says "fetch the relevant ticket"

Find the card by name on the board; if it's a wikilink, read the task note it points to. Prefer a
block link (`[[agentic-skills.kanban#^<blockid>]]`, from obsidian-kanban's "Copy link to card") if
the user gives one -- unambiguous, per BOARD-FORMAT.md.

## Triage state

Triage roles are inline tags on the card, using the role strings from `triage-labels.md`
(`#needs-triage`, `#needs-info`, `#afk`, `#hitl`, `#wontfix`). Replace the old role tag when the
state changes. A `#wontfix` card moves to the archive.

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

`#epic` and `#blocked` colours are defined once, in the canonical `tag-colors` palette in
[BOARD-FORMAT.md](../../skills/projects/skills/new-project/BOARD-FORMAT.md#universal-project-tags) --
don't redefine them here.

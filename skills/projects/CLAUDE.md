# Projects -- Long-Running Goal Management

Project management for work that has **no neat time box** -- a goal, a pile of discrete tasks, and
a state that must persist across weeks or months. Where `journal` handles the clock, `projects`
handles the goal.

All artifacts live in the **projects directory** within the user's Obsidian vault.
`/new-project` finds it with `/discover-vault-directory *projects`.

## Design Principles

- **Project-manager tone**: A competent PM surfacing state -- what's done, what's blocked, what's
  next. Informative, terse, no pressure, no agile ceremony.
- **Stateful workspace**: Each project is a directory of files that persist across sessions, modelled
  on the `teach` skill's workspace pattern. The workspace *is* the state.
- **Obsidian-native**: Valid YAML frontmatter, wikilinks, and an obsidian-kanban board per project.
  Boards are plain markdown (headings + checkboxes) -- portable, no Dataview dependency.
- **Manual card edits**: The user adds, moves, and completes Kanban cards by hand. Skills scaffold
  and promote -- they append when invoked for that purpose, but never delete or rewrite a card
  someone else added.
- **Public repo**: No personal specifics in any skill or example.

## Project Workspace

One directory per project under the projects directory:

```
<projects-dir>/<slug>/
  MISSION.md          # why this project exists, definition of done, constraints, out-of-scope
  <slug>.kanban.md    # obsidian-kanban board: Backlog / Next / Doing / Done
  decisions/          # ADR-style records (NNNN-slug.md) that steer next steps
  tasks/              # per-card task notes created via "New note from card" in obsidian-kanban
    _template.md      # note template used by the plugin when creating card notes
  NOTES.md            # working scratchpad
```

Format contracts live in `skills/new-project/`:

- [MISSION-FORMAT.md](skills/new-project/MISSION-FORMAT.md)
- [BOARD-FORMAT.md](skills/new-project/BOARD-FORMAT.md)
- [DECISIONS-FORMAT.md](skills/new-project/DECISIONS-FORMAT.md)
- [NOTE-FORMAT.md](skills/new-project/NOTE-FORMAT.md)

Every other skill reads these as contracts -- read them before touching a workspace.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

## Dependencies

- `primitives` -- `/grill` for mission clarification, `/look-up` for resource gathering,
  `/discover-vault-directory` to find the projects directory.

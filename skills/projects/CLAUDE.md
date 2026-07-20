# Projects -- Long-Running Goal Management

Project management for work that has **no neat time box** -- a goal, a pile of discrete tasks, and
a state that must persist across weeks or months. Where `journal` handles the clock, `projects`
handles the goal.

All artifacts live in the **projects directory** within the user's Obsidian vault.

## Projects Directory Discovery

Skills must never hardcode the projects path. Instead:

1. Scan the vault for a directory matching `*projects` at the root (e.g. `05-projects/`).
2. If found, use that directory for all project workspaces.
3. If not found, ask the user where projects live and store the path to memory.

## Design Principles

- **Project-manager tone**: A competent PM surfacing state -- what's done, what's blocked, what's
  next. Informative, terse, no pressure, no agile ceremony.
- **Stateful workspace**: Each project is a directory of files that persist across sessions, modelled
  on the `teach` skill's workspace pattern. The workspace *is* the state.
- **Obsidian-native**: Valid YAML frontmatter, wikilinks, and an obsidian-kanban board per project.
  Boards are plain markdown (headings + checkboxes) -- portable, no Dataview dependency.
- **Manual card edits**: The user adds, moves, and completes Kanban cards by hand. Skills scaffold
  -- they do not micro-manage the board.
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

| Skill | Purpose |
|---|---|
| `/new-project` | Scaffold a stateful project workspace with mission, Kanban board, and decisions log |

## Dependencies

- `primitives` -- `/grill` for mission clarification, `/look-up` for resource gathering.

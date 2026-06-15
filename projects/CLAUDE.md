# Projects -- Long-Running Goal Management

Project management for work that has **no neat time box** -- a goal, a pile of discrete tasks, and
a state that must persist across weeks or months. Where `journal` handles the clock, `projects`
handles the goal. The two stay decoupled but aware of each other through `occasions.md`.

All artifacts live in the **projects directory** within the user's Obsidian vault.

## Projects Directory Discovery

Skills must never hardcode the projects path. Instead:

1. Scan the vault for a directory matching `*projects` at the root (e.g. `05-projects/`).
2. If found, use that directory for all project workspaces.
3. If not found, ask the user where projects live and store the path to memory.

Skills that write milestones into the journal also discover the **journal directory** the same way
the journal domain does -- scan for a directory containing `occasions.md`.

## Design Principles

- **Project-manager tone**: A competent PM surfacing state -- what's done, what's blocked, what's
  next. Informative, terse, no pressure, no agile ceremony.
- **Stateful workspace**: Each project is a directory of files that persist across sessions, modelled
  on the `teach` skill's workspace pattern. The workspace *is* the state.
- **Obsidian-native**: Valid YAML frontmatter, wikilinks, and an obsidian-kanban board per project.
  Boards are plain markdown (headings + checkboxes) -- portable, no Dataview dependency.
- **Projects -> journal, one-way (v1)**: Projects push milestones into the journal via `occasions.md`.
  The journal stays battle-tested and mostly untouched; it never needs to understand a project's
  schema. A dedicated journal-queries-projects skill is deferred.
- **Manual card edits**: The user adds, moves, and completes Kanban cards by hand. Skills scaffold,
  report, bridge, and archive -- they do not micro-manage the board.
- **Public repo**: No personal specifics in any skill or example. Outputs meant for sharing (the
  sprint one-pager) must be readable by anyone, with no private data.

## Project Workspace

One directory per project under the projects directory:

```
<projects-dir>/<slug>/
  MISSION.md          # why this project exists, definition of done, constraints, out-of-scope
  <slug>.kanban.md    # obsidian-kanban board: Backlog / This Week / Doing / Done
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

## Journal Interface

Projects surface in the journal through `occasions.md`:

1. `/schedule-goals` appends a row to the **Projects** section of `occasions.md` (distinct from the
   user-maintained One Off Events section) and/or a goal into the relevant cascading journal file.
2. The journal's `/update-occasions-config` regenerates `vault_occasions.js`, emitting each project
   milestone with an existing `section` value (`tasks`/`work`) so it renders in the current
   daily/weekly checklist groups -- no journal template changes required.
3. `/close-project` removes a project's Projects rows from `occasions.md`, ending journal injection.

## Cross-Skill Data Flow

```
/new-project      -> scaffolds <slug>/ workspace (MISSION + board + decisions)
/capture-goals    -> facilitates a planning session -> organises a thought dump into board cards
/schedule-goals   -> writes: occasions.md Projects section + cascading journal goal
/project-status   -> reads: board + MISSION -> PM state summary
/summarize-sprint -> reads: board -> generic shareable one-pager (PDF-exportable)
/close-project    -> archives workspace + strips occasions.md Projects rows
```

## Skills

| Skill | Purpose |
|---|---|
| `/new-project` | Scaffold a stateful project workspace with mission, Kanban board, and decisions log |
| `/capture-goals` | Facilitate a planning session: grill the room, organise the thought dump into board cards |
| `/schedule-goals` | Write project milestones into `occasions.md` and goals into cascading journal files |
| `/project-status` | PM-persona check-in: board state, stalled cards, next actions, upcoming dates |
| `/summarize-sprint` | Generic, shareable one-pager of the current goal and timeframed task breakdown |
| `/close-project` | Mark complete, strip journal injection, archive the workspace |

## Dependencies

- `primitives` -- `/grill-it` for mission clarification, `/look-up` for resource gathering.
- `journal` -- the projects interface writes to `occasions.md` and reuses the journal directory
  discovery convention. The `/update-occasions-config` skill (journal domain) parses the Projects
  section this domain writes.

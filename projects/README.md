# Projects

Long-running, goal-oriented project management for Claude Code + Obsidian. For work with no neat
time box: a goal, a pile of discrete tasks, and state that persists across weeks or months. Where
`journal` handles your days, `projects` handles your goals -- decoupled, but aware of each other.

## Skills

| Skill | Purpose |
|---|---|
| `/new-project` | Scaffold a stateful project workspace with mission, Kanban board, and decisions log |
| `/capture-goals` | Facilitate a planning session: grill the room, organise the thought dump into board cards |
| `/refine-task` | Work a thin Kanban card up into a full, context-grounded task note in `tasks/` |
| `/schedule-goals` | Write project milestones into `occasions.md` and goals into cascading journal files |
| `/project-status` | PM-persona check-in: board state, stalled cards, next actions, upcoming dates |
| `/summarize-sprint` | Generic, shareable one-pager of the current goal and timeframed task breakdown |
| `/close-project` | Mark complete, strip journal injection, archive the workspace |

## Workflow

```
/new-project -> /capture-goals -> /schedule-goals -> /project-status -> /summarize-sprint -> /close-project
```

Each project is a stateful directory in your vault's projects folder (modelled on the `teach`
skill): a `MISSION.md`, an obsidian-kanban board, and an ADR-style `decisions/` log.
`/capture-goals` is the recurring heartbeat -- sit down (alone or with a collaborator), dump your
thinking, and the skill turns it into actionable cards. Day-to-day card moves are manual; the skills
scaffold, capture, report, bridge into the journal, and archive.

## Journal Interface

Projects push milestones into the journal via `occasions.md` -- one-way for v1, so the journal stays
untouched. `/schedule-goals` writes a row to a **Projects** section; the journal's
`/update-occasions-config` regenerates the Templater config so the milestone surfaces in your daily
and weekly files. `/close-project` removes those rows when the project is done.

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "projects@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills` (`/grill-it`, `/look-up`) and `journal@xxkeefer-skills` (the
`occasions.md` interface).

## Vault Setup

A projects directory in your Obsidian vault (e.g. `05-projects/`) and the obsidian-kanban plugin
installed for board visualisation. Boards are plain markdown, so they remain readable without it.

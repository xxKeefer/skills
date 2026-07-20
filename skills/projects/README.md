# Projects

Long-running, goal-oriented project management for Claude Code + Obsidian. For work with no neat
time box: a goal, a pile of discrete tasks, and state that persists across weeks or months. Where
`journal` handles your days, `projects` handles your goals.

## Skills

| Skill | Purpose |
|---|---|
| `/new-project` | Scaffold a stateful project workspace with mission, Kanban board, and decisions log |

Each project is a stateful directory in your vault's projects folder (modelled on the `teach`
skill): a `MISSION.md`, an obsidian-kanban board, and an ADR-style `decisions/` log. Day-to-day
card moves are manual.

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "projects@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills` (`/grill`, `/look-up`).

## Vault Setup

A projects directory in your Obsidian vault (e.g. `05-projects/`) and the obsidian-kanban plugin
installed for board visualisation. Boards are plain markdown, so they remain readable without it.

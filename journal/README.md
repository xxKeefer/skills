# Journal

Personal planner skill suite for Claude Code + Obsidian. Cascading goal/reflection system with
secretary/PA tone.

## Skills

| Skill | Purpose |
|---|---|
| `/daily` | Generate daily file with tasks and reflection sections |
| `/weekly` | Generate weekly file with goals, events, and daily links |
| `/monthly` | Generate monthly file with goals and weekly overview |
| `/yearly` | Generate yearly file with aspirations and monthly overview |
| `/reflect` | File-agnostic reflection and link maintenance tool |

## Workflow

```
/yearly -> /monthly -> /weekly -> /daily -> /reflect
```

Goals cascade down: yearly feeds monthly, monthly feeds weekly, weekly feeds daily. Each skill
reads its parent's goals and prompts you to pull items down.

`/reflect` works on any file level -- fixes wikilinks, bubbles patterns from child reflections,
and surfaces incomplete items for carry-forward.

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "xxkeefer-skills@journal": true
  }
}
```

Requires `xxkeefer-skills@primitives` for `/grill-it` dependency.

## Vault Setup

Create a journal directory in your Obsidian vault with:
- `occasions.md` -- chores, events, reminders

Templates for manual fallback are in `templates/`.

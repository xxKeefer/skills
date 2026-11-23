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
| `/broadsheet` | Print this week's HTML newspaper of the vault into the journal folder: the week, the compass of reflections and trends, weather, chore rates, and suggestions to choose from, which build a prompt |
| `/act-on-broadsheet` | Apply the rows chosen on a broadsheet page to the vault: move, archive, or delete notes, set project status, tick goals, and edit templates. Asks before a delete |
| `/bulletin` | Add today's entry to this week's HTML bulletin in the journal folder: how the goals moved since the last entry, today's weather, the events due now and later in the week, chores, and project moves. Newest entry on top |
| `/update-occasions-config` | Migrate an old-layout `occasions.md` after one yes, then sync it into `vault_occasions.js` for Templater |

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
    "journal@xxkeefer-skills": true
  }
}
```

Requires `primitives@xxkeefer-skills` for `/grill` and `/discover-vault-directory`.

## Vault Setup

Create a journal directory at the root of your Obsidian vault with:
- `occasions.md` -- chores, events, reminders

Templates for manual fallback are in `templates/`.

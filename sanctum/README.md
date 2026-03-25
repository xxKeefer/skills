# Sanctum

Agile-inspired life coaching skill suite for Claude Code + Obsidian.

## Skills

| Skill | Purpose | Cadence |
|---|---|---|
| `/smart-goal` | SMART goal grilling for any domain | When activating a domain |
| `/quest` | Actionable plan to achieve a north star | After setting a goal |
| `/vault` | Backlog + north star management | Anytime |
| `/weekly` | Sprint planning (Monday kickoff) | Weekly |
| `/daily` | Morning standup | Daily AM |
| `/reflect` | Evening reflection | Daily PM |
| `/ponder` | Sprint retro | End of sprint |
| `/chronicle` | Monthly/yearly progress arc | Monthly + yearly |

## Workflow

```
/smart-goal → /quest → /vault
                         ↓
                      /weekly (Monday)
                         ↓
              /daily (AM) → /reflect (PM)
                         ↓
                      /ponder (end of sprint)
                         ↓
                      /chronicle (monthly/yearly)
```

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "xxkeefer-skills@sanctum": true
  }
}
```

Requires `xxkeefer-skills` plugin for `/grill-it` dependency.

## Vault Setup

Create `10 - Sanctum/` in your Obsidian vault with seed files:
- `north-stars.md`
- `backlog.md`
- `occasions.md`

Templates for manual fallback are in `templates/`.

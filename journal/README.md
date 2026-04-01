# Journal

Agile-inspired life coaching skill suite for Claude Code + Obsidian.

## Skills

| Skill | Purpose | Cadence |
|---|---|---|
| `/smart-goal` | SMART goal grilling for any domain | When activating a domain |
| `/quest` | Actionable plan to achieve a north star | After setting a goal |
| `/vault` | Backlog + north star management | Anytime |
| `/weekly` | Sprint planning (Monday kickoff) | Weekly |
| `/daily` | Morning standup | Daily AM |
| `/check-in` | Adhoc micro-reflection | Anytime |
| `/reflect` | Evening reflection | Daily PM |
| `/ponder` | Sprint retro | End of sprint |
| `/chronicle` | Monthly/yearly progress arc | Monthly + yearly |

## Workflow

```
/smart-goal -> /quest -> /vault
                         |
                      /weekly (Monday)
                         |
              /daily (AM) -> /check-in (anytime) -> /reflect (PM)
                         |
                      /ponder (end of sprint)
                         |
                      /chronicle (monthly/yearly)
```

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

Create `10 - Sanctum/` in your Obsidian vault with seed files:
- `north-stars.md`
- `backlog.md`
- `occasions.md`

Templates for manual fallback are in `templates/`.

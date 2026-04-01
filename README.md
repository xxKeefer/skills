# xxkeefer-skills

Claude Code skills for idiomatic, agnostic workflows. Organized into domains.

## Domains

| Domain | Skills | Purpose |
|---|---|---|
| **primitives** | grill-it | Foundational building blocks |
| **developer** | spike-it, task-it, plan-it, do-it, tdd, close-it, hunt-it, resolve-it, design-it, document-it, improve-it, qa-it, explain-it | Engineering lifecycle |
| **journal** | smart-goal, quest, vault, weekly, daily, check-in, reflect, ponder, chronicle | Life admin + personal growth |
| **meta** | audit-workflow, learn-it, teach-it | Skills about skills |
| **omen** | (empty) | Creative -- TTRPG, worldbuilding |

## Setup

### Install as a local marketplace

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "xxkeefer-skills": {
      "source": {
        "source": "directory",
        "path": "/path/to/this/repo"
      }
    }
  },
  "enabledPlugins": {
    "xxkeefer-skills@primitives": true,
    "xxkeefer-skills@developer": true,
    "xxkeefer-skills@journal": true,
    "xxkeefer-skills@meta": true,
    "xxkeefer-skills@omen": true
  }
}
```

`primitives` is required by all other domains. Enable whichever domains you need.

### Publishing a new version

1. Bump the version in the relevant domain's `plugin.json` (e.g. `1.0.0` -> `1.0.1`)
2. Commit and push to `main`
3. Restart Claude Code on each consuming machine -- it detects the new HEAD SHA and re-caches

## Attribution

Several skills were inspired by or adapted directly from
[Matt Pocock's skills repo](https://github.com/mattpocock/skills):

- **grill-it** -- taken from Matt's repo
- **design-it** -- taken from Matt's repo
- **improve-it** -- taken from Matt's repo
- **spike-it** -- inspired by Matt's approach to investigation workflows
- **tdd** -- inspired by Matt's TDD skill, particularly the tracer bullet pattern and
  anti-horizontal-slice philosophy

Thanks Matt for sharing these publicly.

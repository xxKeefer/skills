# xxkeefer-skills

Claude Code skills for idiomatic, agnostic workflows. Organized into domains.

## Domains

| Domain | Skills | Purpose |
|---|---|---|
| **primitives** | grill-it, explain, look-up, write-to-file, caveman, handoff, tabular-analysis | Foundational building blocks |
| **developer** | research-it, spike-it, task-it, plan-it, do-it, tdd, tweak-it, hunt-it, fix-it, happy-path, resolve-it, resolve-conflicts, document-it, explain-it | Engineering lifecycle |
| **journal** | yearly, monthly, weekly, daily, reflect, update-occasions-config | Life admin + personal growth |
| **projects** | new-project, capture-goals, schedule-goals, project-status, summarize-sprint, close-project | Long-running goal management |
| **meta** | audit-workflow, write-a-skill, migrate-a-skill, retire-a-skill | Skills about skills |
| **omen** | scaffold-setting, doctor-setting, plan-session, log-session, log-cannon, log-npcs, log-place, log-progression, make-lore, make-blurb, make-summary | Creative -- TTRPG, worldbuilding |
| **scribe** | add-procedure, edit-article, define-concept, define-term, define-language, teach | Capture vault procedures + edit notes |
| **nix-manager** | add-it, remove-it, rice-it, refine-it, debug, explain | NixOS config management |
| **utility** | setup-pre-commit, setup-git-guardrails, setup-skill-tally, configure-obsidian-kanban | Dev-environment setup |
| **experimental** | debrief, do-next, lobotomize, patch-doctor, update-handoff | Skills on probation |
| **deprecated** | design-it, improve-it, intake-it, intake-raw, rebuild-index, research-it, standardise-frontmatter | Awaiting keep/kill decision |

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
    "primitives@xxkeefer-skills": true,
    "developer@xxkeefer-skills": true,
    "journal@xxkeefer-skills": true,
    "projects@xxkeefer-skills": true,
    "meta@xxkeefer-skills": true,
    "omen@xxkeefer-skills": true,
    "scribe@xxkeefer-skills": true,
    "nix-manager@xxkeefer-skills": true,
    "utility@xxkeefer-skills": true,
    "experimental@xxkeefer-skills": true,
    "deprecated@xxkeefer-skills": true
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

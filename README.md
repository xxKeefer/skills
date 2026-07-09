# xxkeefer-skills

Claude Code skills for idiomatic, agnostic workflows. Organized into domains.

## Layout

| Path | Holds |
|---|---|
| `skills/` | The domain plugins -- one directory per domain (see table below). |
| `hooks/` | Claude Code hook holders (e.g. `tool-policy`) -- installable guardrails. |
| `scripts/` | Supporting tooling skills depend on (e.g. `obsidian/` -- journal Templater scripts). |
| `statusline/` | The self-contained Claude Code status line script, installed by `/setup-statusline`. |
| `output-styles/` | Claude Code output styles (e.g. `Terse.md`). |
| `.claude-plugin/` | Marketplace registry (`marketplace.json`). |

## Domains

| Domain | Skills | Purpose |
|---|---|---|
| **primitives** | grill, explain, look-up, write-to-file, caveman, handoff, update-handoff, do-next, tabular-analysis | Foundational building blocks |
| **developer** | research, spike, to-tickets, to-plan, implement, tdd, tweak, diagnose, fix, happy-path, resolve-feedback, resolve-conflicts, sync-docs, explain-reasoning | Engineering lifecycle |
| **journal** | yearly, monthly, weekly, daily, reflect, update-occasions-config | Life admin + personal growth |
| **projects** | new-project, capture-goals, refine-task, schedule-goals, project-status, summarize-sprint, close-project | Long-running goal management |
| **meta** | audit-workflow, write-a-skill, migrate-a-skill, retire-a-skill | Skills about skills |
| **omen** | scaffold-setting, doctor-setting, plan-session, log-session, log-cannon, log-npcs, log-place, log-progression, make-lore, make-blurb, make-summary | Creative -- TTRPG, worldbuilding |
| **scribe** | add-procedure, edit-article, define-concept, define-term, define-language, take-a-note, triage-notes, teach | Capture vault procedures + edit notes |
| **nix-manager** | add, remove, rice, refine, debug, explain | NixOS config management |
| **utility** | setup-pre-commit, setup-git-guardrails, setup-skill-tally, setup-statusline, configure-obsidian-kanban | Dev-environment setup |
| **mattpocock** | grill-with-docs, wayfinder, to-spec, to-tickets, implement, code-review, grilling, domain-modeling, prototype, research, triage, tdd, codebase-design, improve-codebase-architecture, writing-great-skills, setup-matt-pocock-skills | Verbatim vendored copy of Matt Pocock's skills (MIT, v1.1.0) |
| **experimental** | lobotomize, patch-doctor | Skills on probation |
| **deprecated** | debrief | Holding pen for skills awaiting a keep/kill decision |

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
    "mattpocock@xxkeefer-skills": true,
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

This marketplace owes a lot to [Matt Pocock's skills repo](https://github.com/mattpocock/skills)
(MIT licensed):

- The **mattpocock** domain is a verbatim vendored copy of his engineering skills at tag
  `v1.1.0`, with his LICENSE alongside. It is never edited in place -- updates come from
  re-vendoring a newer tag.
- Several of my own skills carry his designs under my names: **grill** and **handoff**
  (his `grilling`/`handoff` v1.1.0 bodies), **tdd** (his reference-only design), and **spike**
  (inspired by his investigation workflows).

Thanks Matt for sharing these publicly.

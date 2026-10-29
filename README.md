# xxkeefer-skills

Claude Code skills for idiomatic, agnostic workflows. Organized into domains.

## Layout

| Path | Holds |
|---|---|
| `skills/` | The domain plugins -- one directory per domain (see table below). Installable assets, such as hooks, the status line, and output styles, live inside their `utility` installer skill. |
| `scripts/` | Supporting tooling skills depend on (e.g. `obsidian/` -- journal Templater scripts). |
| `.claude-plugin/` | Marketplace registry (`marketplace.json`). |

## Domains

| Domain | Purpose |
|---|---|
| [**primitives**](skills/primitives/README.md) | Foundational building blocks |
| [**developer**](skills/developer/README.md) | Engineering lifecycle |
| [**journal**](skills/journal/README.md) | Life admin + personal growth |
| [**projects**](skills/projects/README.md) | Long-running goal management |
| [**meta**](skills/meta/README.md) | Skills about skills |
| [**omen**](skills/omen/README.md) | Creative -- TTRPG, worldbuilding |
| [**scribe**](skills/scribe/README.md) | Capture vault procedures + edit notes |
| [**nix-manager**](skills/nix-manager/README.md) | NixOS config management |
| [**utility**](skills/utility/README.md) | Dev-environment setup |
| [**experimental**](skills/experimental/README.md) | Skills on probation |
| [**deprecated**](skills/deprecated/README.md) | Holding pen for skills awaiting a keep/kill decision |

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

The setup above loads each domain in place from this repo (see
[ADR 0001](docs/adr/0001-how-plugins-load.md)). A new session, or `/reload-plugins` in a running
one, loads an edit. No version bump is needed for that.

1. Bump the version in the relevant domain's `plugin.json` (e.g. `1.0.0` -> `1.0.1`)
2. Commit and push to `main`

An install that copies the plugin into its cache, such as a marketplace added from GitHub, gets an
edit only after the `plugin.json` version changes and the user updates the plugin.

## Attribution

This marketplace owes a lot to [Matt Pocock's skills repo](https://github.com/mattpocock/skills)
(MIT licensed):

- The **developer** domain's `wayfinder`, `to-spec`, `to-tickets`, `triage`, and `code-review`
  (plus the earlier-adopted `implement`, `grill-with-docs`, `domain-modeling`, `codebase-design`,
  `improve-codebase-architecture`, and `prototype`) were adopted from his repo at tag `v1.1.0`,
  with his LICENSE alongside as `skills/developer/LICENSE-mattpocock`. The vendored `mattpocock`
  holding domain was retired 2026-07 once everything worth keeping had been adopted.
- Several of my own skills carry his designs under my names: **grill** and **handoff**
  (his `grilling`/`handoff` v1.1.0 bodies), **tdd** (his reference-only design), and **spike**
  (inspired by his investigation workflows).

Thanks Matt for sharing these publicly.

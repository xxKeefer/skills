# xxkeefer-skills

Claude Code skills for idiomatic, agnostic workflows. Organized into domains.

## Layout

| Path | Holds |
|---|---|
| `skills/` | The domain plugins -- one directory per domain (see table below). Installable assets, such as hooks, the status line, output styles, and rules, live inside their `utility` installer skill. |
| `scripts/` | Supporting tooling skills depend on (e.g. `obsidian/` -- journal Templater scripts). |
| `.claude-plugin/` | Marketplace registry (`marketplace.json`). |
| `.githooks/` | The scrub check: a pre-commit hook that blocks employer content. |

## Domains

| Domain | Purpose |
|---|---|
| [**primitives**](skills/primitives/README.md) | Foundational building blocks |
| [**implement-code**](skills/implement-code/README.md) | Ticket to PR |
| [**dev-personas**](skills/dev-personas/README.md) | Persona code reviewers and the panel that runs them |
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
    "implement-code@xxkeefer-skills": true,
    "dev-personas@xxkeefer-skills": true,
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

### Turn on the scrub check

The pre-commit hook in `.githooks/` blocks a commit when a tracked file matches a pattern for
employer content, such as a ticket key or a custom field ID. Run these commands once per clone:

1. Run `git config core.hooksPath .githooks`.
2. To also block names that must stay private, put one pattern per line in a file outside this
   repo. Then run `git config scrub.patterns <path-to-that-file>`.

The hook checks the whole staged tree. To check a commit, run `.githooks/pre-commit <revision>`.

### Publishing a new version

The setup above loads each domain in place from this repo (see
[ADR 0001](docs/adr/0001-how-plugins-load.md)). A new session, or `/reload-plugins` in a running
one, loads an edit. No version bump is needed for that.

1. Bump the version in the relevant domain's `plugin.json` (e.g. `1.0.0` -> `1.0.1`)
2. Commit and push to `main`

An install that copies the plugin into its cache, such as a marketplace added from GitHub, gets an
edit only after the `plugin.json` version changes and the user updates the plugin.

## Related repos

| Repo | Role |
|---|---|
| [nixos_config](https://github.com/xxKeefer/nixos_config) | System and home-manager config. The `nix-manager` domain manages it |
| [dotfiles](https://github.com/xxKeefer/dotfiles) | Config kept outside nix, linked into `~/.config` |
| [skills](https://github.com/xxKeefer/skills) | This repo. Claude Code skills |

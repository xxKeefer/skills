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
| [**engineering**](skills/engineering/README.md) | Idea to PR -- nine lifecycle commands over the plan, build, test, review, and PR skills |
| [**journal**](skills/journal/README.md) | Life admin + personal growth |
| [**projects**](skills/projects/README.md) | Long-running goal management |
| [**meta**](skills/meta/README.md) | Skills about skills |
| [**scribe**](skills/scribe/README.md) | Capture vault procedures + edit notes |
| [**nix-manager**](skills/nix-manager/README.md) | NixOS config management |
| [**utility**](skills/utility/README.md) | Dev-environment setup |
| [**experimental**](skills/experimental/README.md) | Skills on probation |
| [**deprecated**](skills/deprecated/README.md) | Holding pen for skills awaiting a keep/kill decision |

## The engineering flow

```
/spec → /plan → /build → /test → /review → /ship
```

Each command picks and runs the skills below it, and each description starts with ★. Three commands
sit outside the line: `/constraints`, `/webperf`, and `/code-simplify`. `/build` runs one step.
`/run-wave` runs every remaining step. `/review` and `/plan` share a name with built-in commands.
When the bare name opens the built-in, type `/engineering:review` or `/engineering:plan`. The
[engineering README](skills/engineering/README.md) holds the full table of commands and skills.

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
    "engineering@xxkeefer-skills": true,
    "journal@xxkeefer-skills": true,
    "projects@xxkeefer-skills": true,
    "meta@xxkeefer-skills": true,
    "scribe@xxkeefer-skills": true,
    "nix-manager@xxkeefer-skills": true,
    "utility@xxkeefer-skills": true,
    "experimental@xxkeefer-skills": true,
    "deprecated@xxkeefer-skills": true
  }
}
```

`primitives` is required by all other domains. Enable whichever domains you need.

### Configure the tools on each machine

A skill names a tool by its role: the tracker, the code host, or the browser. It never names a
product. A skill finds the tool in this order:

1. The repo's `## Agent skills` block. [`/set-up-dev-workflow-skills`](skills/utility/skills/set-up-dev-workflow-skills/SKILL.md)
   writes it for each repo.
2. The `## Tools on this machine` block in your global instructions, for example `~/.claude/AGENTS.md`.
3. If neither block names the tool, the skill asks you.

Put one table in the machine block, with the columns Role, Tool, and Notes. A work machine can
look like this:

```markdown
## Tools on this machine

| Role      | Tool                       | Notes                        |
| --------- | -------------------------- | ---------------------------- |
| Tracker   | Jira, through the Atlassian MCP | `~/.claude/tools/tracker.md` |
| Code host | GitHub, through `gh`       | none                         |
| Browser   | Claude in Chrome           | `~/.claude/tools/browser.md` |
```

A home machine can use GitHub Issues as its tracker:

```markdown
## Tools on this machine

| Role      | Tool                   | Notes |
| --------- | ---------------------- | ----- |
| Tracker   | GitHub Issues, through `gh` | none  |
| Code host | GitHub, through `gh`   | none  |
| Browser   | none                   | none  |
```

- The Notes column points to a file outside any repo. Put employer detail, such as project keys,
  field IDs, and team names, only in that file.
- If a role has no tool on a machine, a skill skips the step that needs it and says so.

### Turn on the scrub check

The pre-commit hook in `.githooks/` blocks a commit when a tracked file matches a pattern for
employer content, such as a ticket key or a custom field ID. Run these commands once per clone:

1. Run `git config core.hooksPath .githooks`.
2. To also block names that must stay private, put one pattern per line in a file outside any
   repo, for example `~/.claude/scrub-patterns.txt`. Then run `git config scrub.patterns <path-to-that-file>`.

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

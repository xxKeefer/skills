---
name: configure-obsidian-kanban
description: >
  Install (if missing) and configure the obsidian-community/obsidian-kanban plugin in the user's
  Obsidian vault so its settings line up with the projects domain board format. Use when the user
  says "configure kanban", "set up obsidian-kanban", "install the kanban plugin", or wants project
  boards to render and behave correctly.
---

# Configure Obsidian Kanban

Get the [obsidian-community/obsidian-kanban](https://github.com/mgmeyers/obsidian-kanban) plugin
installed and tuned so the boards the `projects` domain writes (`<slug>.kanban.md`) render and behave
the way those skills assume. This is a one-shot setup task -- run it once per vault.

The contract this skill aligns to is [BOARD-FORMAT.md](../../../projects/skills/new-project/BOARD-FORMAT.md):
`@{YYYY-MM-DD}` date tags, a `**Complete**` marker in Done, and the `%% kanban:settings %%` block.

> **Never commit in the vault.** The user manages the vault's git separately. Write files, then stop
> -- do not stage or commit anything under the vault.

## Step 1: Locate the Vault and Plugin

Find the vault root (the directory containing `.obsidian/`). The plugin lives at:

```
.obsidian/plugins/obsidian-kanban/
  main.js
  manifest.json
  styles.css
```

If you can't find `.obsidian/`, ask the user for the vault path.

## Step 2: Install if Missing

If `.obsidian/plugins/obsidian-kanban/main.js` is absent, install it:

1. Fetch the latest release from the GitHub API:
   `https://api.github.com/repos/mgmeyers/obsidian-kanban/releases/latest`
2. Download the three release assets -- `main.js`, `manifest.json`, `styles.css` -- into
   `.obsidian/plugins/obsidian-kanban/` (create the directory first).
3. Enable the plugin by adding `"obsidian-kanban"` to the array in
   `.obsidian/community-plugins.json` (create the file as `["obsidian-kanban"]` if it doesn't exist).
   Read-modify-write -- don't clobber other enabled plugins.

Tell the user the plugin won't load until Obsidian is reloaded (Cmd/Ctrl-R or restart). If it's
already installed, skip to configuration and note the installed version from `manifest.json`.

## Step 3: Configure Settings

The plugin's global settings live in `.obsidian/plugins/obsidian-kanban/data.json`. **Read-modify-write**
-- merge these keys into whatever is there, leave unrecognised keys untouched, and don't overwrite a
setting the user has deliberately changed without flagging it.

| Setting | Value | Why it matters for the projects boards |
|---|---|---|
| `date-trigger` | `"@"` | Matches the `@{YYYY-MM-DD}` deadline syntax in BOARD-FORMAT |
| `date-format` | `"YYYY-MM-DD"` | The on-disk date format the project skills read and write |
| `date-display-format` | `"YYYY-MM-DD"` | What the rendered card shows |
| `show-relative-date` | `true` | Surfaces "in 3 days" on dated milestone cards |
| `link-date-to-daily-note` | `false` | Deadlines are milestones, not journal day-links |
| `hide-date-in-title` | `false` | Keep deadlines visible on the card face |
| `archive-with-date` | `true` | Completed cards keep their date when auto-archived from Done |
| `show-checkboxes` | `true` | Cards are checkboxes -- the readable-without-the-plugin format |
| `new-line-trigger` | `"enter"` | Predictable card entry during manual edits |

If `data.json` doesn't exist, create it with exactly these keys.

## Step 4: Confirm Board Compatibility

The per-board `%% kanban:settings %%` block (written by `/new-project`) overrides globals per file.
Don't rewrite existing boards. Just confirm the global defaults above don't fight the board format --
the date trigger and format are the ones that must agree, and Step 3 sets them.

## Step 5: Report

> obsidian-kanban **{installed vX.Y.Z | already present vX.Y.Z}** and configured.
> - Settings written: `.obsidian/plugins/obsidian-kanban/data.json`
> - Date syntax aligned to `@{YYYY-MM-DD}`
>
> Reload Obsidian to pick up changes, then open any `<slug>.kanban.md` to verify it renders as a board.

Do not commit -- the vault's git is the user's to manage.

---
name: install-preferred-fonts
description: Install the preferred fonts on this machine, or with --project copy them into a repo as woff2 with a fonts.css. Use when the user says "install fonts" or "install preferred fonts", or a project needs the house fonts.
disable-model-invocation: true
argument-hint: "[--project [path]]"
---

# Install Preferred Fonts

This skill ships four variable font families in [`fonts/`](fonts/), each with its OFL licence. Each
family has one role:

| Role | Family | CSS property |
|---|---|---|
| Body text | Atkinson Hyperlegible Next | `--font-body` |
| Headings | Noto Serif | `--font-heading` |
| Display | Shantell Sans | `--font-display` |
| Monospace | JetBrains Mono | `--font-mono` |

[`fonts/manifest.json`](fonts/manifest.json) lists each face, its axis ranges, and the role stacks.

## Step 1: Pick the mode

With no `--project`, go to Step 2. With `--project`, go to Step 3.

## Step 2: Install on the machine

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/install_fonts.py"
```

The script copies each TTF to `~/.local/share/fonts/preferred-fonts/` on Linux, or to
`~/Library/Fonts/` on macOS, then runs `fc-cache` when it exists. On any other OS it exits 1 and
copies nothing. Tell the user, and stop.

Then check that the system sees each family. On Linux, run `fc-list : family | sort -u` and find
the four names. On macOS, ask the user to look in Font Book. Say that an open app needs a restart
before it lists the fonts.

**Done when:** the script exits 0, and each of the four families shows in the font list.

## Step 3: Install into the project

Find the folder for the fonts. Use the path given after `--project`. With no path, look for the
folder that the project serves static files from, such as `public/`, `static/`, or `assets/`, and
propose `<that folder>/fonts/`. Ask the user to confirm the path.

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/install_fonts.py" --project <path>
```

The script copies each woff2 file and one `<Family>-OFL.txt` per family into the folder. It writes
`fonts.css` there, with one `@font-face` rule per face and the four role properties on `:root`. A
re-run with no change prints `unchanged` for each file.

Find where the project loads its global CSS. Show the user the one line that loads `fonts.css`
there, such as an `@import` or a `<link>`. Apply it after a yes.

**Done when:** the script exits 0, and the user has seen the line that loads `fonts.css`.

## Step 4: Verify

Run the same command again. Each line must say `unchanged`.

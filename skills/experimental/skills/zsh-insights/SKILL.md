---
name: zsh-insights
description: Mine the zsh history for aliases, functions, and scripts, show them in an HTML report, and write the ones you pick to ~/.config/zsh/.
disable-model-invocation: true
---

# zsh Insights

A script counts patterns in the zsh history. Suggest the shortcuts that the counts prove, and write
the ones the user picks as modules.

`$ARGUMENTS` is an optional window: `Nd`, such as `30d`, or `all`. The default is `90d`.

## Layout

| Path | Holds |
|---|---|
| `~/.config/zsh/<topic>.zsh` | One module per topic, such as `git.zsh`, `nav.zsh`, or `wt.zsh` |
| `~/.config/zsh/bin/<name>` | One executable script per file |

The skill knows only these paths. The folder can be a plain folder or a link to a dotfiles checkout.

The **loader** in `.zshrc` sources the modules and puts the scripts on PATH:

```zsh
# Load the zsh modules and scripts in ~/.config/zsh.
export PATH="$HOME/.config/zsh/bin:$PATH"
for f in $HOME/.config/zsh/*.zsh(N); do source "$f"; done
```

## Step 1: Analyse the history

```sh
cache="${XDG_CACHE_HOME:-$HOME/.cache}/zsh-insights"
mkdir -p "$cache"
zsh -ic 'alias -r' > "$cache/aliases.txt" 2>/dev/null
hist=$(zsh -ic 'print -r -- ${HISTFILE:-$HOME/.zsh_history}' 2>/dev/null)
python3 "${CLAUDE_SKILL_DIR}/scripts/zsh_insights.py" analyse \
  --history "$hist" --aliases "$cache/aliases.txt" --window <window> > "$cache/analysis.json"
```

Read only `analysis.json`. The script masks secret-like values there, and the history file itself
can hold secrets.

If `window.timestamps` is `false`, tell the user that the window does not apply. Timestamps need
`setopt EXTENDED_HISTORY`, or `programs.zsh.history.extended = true` in home-manager.

**Done when:** you have read `analysis.json`.

## Step 2: Read the current shortcuts

Read `${ZDOTDIR:-$HOME}/.zshrc`, each `~/.config/zsh/*.zsh`, and the file names in
`~/.config/zsh/bin/`. `aliases.txt` holds the aliases that plugins define.

**Done when:** you have a list of every alias, function, and script name, with its definition.

## Step 3: Draft the suggestions

Turn the lists in `analysis.json` into suggestions. Each suggestion covers a pattern that no current
shortcut covers.

| List | Suggest |
|---|---|
| `commands` | An alias for the fixed text |
| `prefixes` | An alias when the changing part is at the end, because an alias takes trailing arguments. Otherwise a function |
| `sequences` | A function that runs the steps in order, when the steps do one task |

Pick the kind:

- **alias** -- fixed text, or a fixed start with arguments at the end.
- **function** -- arguments in the middle, several steps, or a change to shell state such as `cd`
  or `export`.
- **script** -- a long workflow, or a command that another program calls.

Name by kind. Use short lowercase for frequent aliases, such as `gpf`. Use camelCase verbNoun for
functions, scripts, and rare tasks, such as `syncMain`. Check all names in one call, and rename
each name that does not print `none`:

```sh
zsh -ic 'whence -w name1 name2 ...'
```

Rank by keys saved: uses × (characters replaced − name length). Keep the top 15.

Write 3 to 5 observations about how the user works, in the style of `/insights`. Base each one on a
count in the analysis: top programs, busy hours, change by month, or the most common sequence.

Write `$cache/suggestions.json`. `definition` holds the exact text to write. For a script, `module`
is `bin/<name>`.

```json
{
  "observations": ["You ran `z mono` then `git pull` 49 times in 90 days."],
  "suggestions": [
    {"kind": "alias", "name": "devu", "definition": "alias devu='nx dev:remote portal --site=uat'",
     "module": "nx.zsh", "uses": 49, "all_time": 130, "saved": 1323,
     "why": "Typed 49 times in 90 days."}
  ]
}
```

**Done when:** `whence -w` prints `none` for every name, and `suggestions.json` exists.

## Step 4: Show the report

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/zsh_insights.py" render \
  --analysis "$cache/analysis.json" --suggestions "$cache/suggestions.json" --out "$cache/report.html"
open "$cache/report.html"
```

On Linux, use `xdg-open` in place of `open`.

Give the user the report path. Ask for the numbers to apply, such as `1 3 5`, or `2 as gpl` to
rename one. **Wait for the reply.**

**Done when:** the user has replied.

## Step 5: Write the picks

1. Run `mkdir -p ~/.config/zsh/bin`.
2. Check each renamed pick with `whence -w`, as in Step 3.
3. Append each alias and function to its module. Create the module if it does not exist.
4. Put a one-line comment above each function. Write it as you would name its test.
5. Write each script to `~/.config/zsh/bin/<name>` with a shebang.
6. Run `chmod +x` on each script.
7. Run `zsh -n` on each module you changed.

**Done when:** every pick is in its file, and `zsh -n` passes on each changed module.

## Step 6: Wire the loader

Read `${ZDOTDIR:-$HOME}/.zshrc`. Follow the link if it is one.

- **The file sources `~/.config/zsh`:** go to Step 7.
- **It does not, and `[ -w <file> ]` passes:** append the loader to the end of the file. The end
  comes after any plugin manager, so the modules override plugin aliases.
- **It does not, and the file is not writable:** home-manager owns it. Give the user the snippet in
  [nixos.md](nixos.md), with the loader inside it. Skip Step 7, and tell the user the picks load
  after the rebuild.

**Done when:** `.zshrc` sources `~/.config/zsh`, or the user has the snippet.

## Step 7: Verify

Run `zsh -ic 'whence -w <each pick>'`. Each name must print `alias`, `function`, or `command`.

Tell the user to run `exec zsh` to load the picks in the current shell.

**Done when:** every pick resolves in a new shell.

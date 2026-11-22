---
name: broadsheet
description: >
  Print this week's one-page HTML newspaper of the Obsidian vault into the journal folder: the
  week's story, the compass of filled reflections and trends, today's weather, chore rates, the
  goal ledger, the inbox, stale and archived notes, folder layout, project boards, and an
  editorial. Each suggestion has a choice and a comment, and the page builds two editable prompts:
  vault maintenance for /journal:act-on-broadsheet, and skill suite changes for the engineering
  flow. Use when the user says "broadsheet" or wants a newspaper of their
  vault.
disable-model-invocation: true
argument-hint: "[accent=<colour>] [place=<label or name>]"
---

# Broadsheet

The journal domain's weekly newspaper. The front page tells the last 7 days from the journal. The
inside pages look across the whole vault, and suggest what to file, archive, delete, or
reorganise. The user picks a choice on each suggestion, and the page builds two prompts, which the
user can edit before they copy them. The vault prompt goes to `/journal:act-on-broadsheet`, which
applies it with no review. The suite prompt goes to the engineering flow (`/engineering:spec`,
then plan and build), so each change gets tests and review.

`$SKILL_DIR` is this skill's base directory. The page is [`template.html`](template.html). The
scripts are in `$SKILL_DIR/scripts/`: `edition.py`, `scan_vault.py`, `weather.py`, and
`check_broadsheet.py`.

Write as a secretary: surface the facts, and give each suggestion once. No pressure, no coaching,
no agile words. This skill writes one file, the page. It never moves, edits, archives, or deletes a
note.

## Step 1: Resolve the edition

1. Find the journal folder with `/discover-vault-directory * holding occasions.md`. Run:

   ```sh
   python3 $SKILL_DIR/scripts/edition.py <journal folder>
   ```

   It prints `{path, exists, last_path, last_ids, muted}`. `path` is this week's page,
   `<journal folder>/{YYYY}-wk{ww}-broadsheet.html`, with the ISO week of today. `last_path` is
   last week's page in the journal folder, else in `chronicles/{YYYY}/` with its ISO year, else
   null. `muted` lists
   each row id that the user vetoed, or snoozed to today or later, in `broadsheet-memory.md` in
   the journal folder. `/journal:act-on-broadsheet` writes that file.
2. If `exists` is true, stop. Scan nothing and write nothing. Reply with `path`, and say that this
   week's edition is already printed.
3. Read `~/.claude/broadsheet.md` if it exists. Its layout is in
   [`config.example.md`](config.example.md). An `accent=<colour>` argument overrides its line. A `place=<label or name>` argument replaces
   the places for this run: a label of the config picks that place, and any other value is one
   place name. The skill takes no time period: the lead always covers the last 7 days.
4. Defaults: the paper name is "The Obsidian Oracle". The accent is oxblood, `#8b1e3f`. Stale is
   90 days. Archive is 180 days. No places.
5. The vault root is the parent of the journal folder. Find the inbox with
   `/discover-vault-directory *notes`, and the projects folder with
   `/discover-vault-directory *projects`.

**Done when:** you have the edition JSON, the paper name, the accent, the two day limits, the
places or none, the vault root, and the journal, inbox, and projects folders. Or this week's page
exists, and the user has its path.

## Step 2: Scan the vault and the sky

```sh
python3 $SKILL_DIR/scripts/scan_vault.py <vault root> --journal <journal folder> --stale <days> --archive-days <days>
```

The scanner prints JSON. It reads ages from the vault's git history, and from the file time for a
note with uncommitted changes. `dates_from` says which. Each long list holds at most 40 rows, and
`totals` gives its full count. The window is the last 7 days. [SCAN.md](SCAN.md) names each key.

For each place, run one of these. A place that is a name takes the name. A place that is
coordinates takes both numbers:

```sh
python3 $SKILL_DIR/scripts/weather.py <place name>
python3 $SKILL_DIR/scripts/weather.py <lat> <lon>
```

Each run prints `{available, date, conditions, high, low, rain_chance, unit}`, or `{available: false}`.

**Done when:** the scanner exits 0, you hold its JSON, and you hold the forecast, or you know that
there is no place or no forecast.

## Step 3: Read last week's page

If `last_path` is null, skip this step. Every row is new, and the colophon says that there was no
page last week.

Else read `last_path`. From it, take the lead headline, the compass figures, each story in the
board and the back pages, and `last_ids`.

- A row is a **repeat** when its `data-id` is in `last_ids`. Else it is **new**.
- A story is a repeat when last week's page told the same item.
- A repeat gets one line, unless its facts changed. Then it gets full space, and says what changed.
- Find the trends across the two weeks: the compass figures that moved, and each repeat row that
  got worse, such as a stale note that is now older and still has no link.

**Done when:** each row and story you plan has new or repeat, and you have the two-week trends, or
there was no page last week.

## Step 4: Read the journal

Read the journal files of the last 7 days: the yearly, the monthly, each weekly, and each daily.
Read [`CASCADE.md`](../../CASCADE.md) for the carry-forward rules. From them, find:

- the themes, wins, and misses of the week, for the lead;
- each goal at each level of the cascade, and whether a task at the level below serves it. A goal
  that no task serves, or that carried forward unchanged, is news.

From `reflections`, group the filled reflections by the compass window that each `date` falls in.
Read each one in full. These are the highest-value signal in the journal.

**Done when:** each goal in the week's yearly, monthly, and weekly files is marked served, not
served, or carried, and you have read each filled reflection.

## Step 5: Read the rest of the vault

Each suggestion row gives its reason and what its action does. A bare folder name is not a
suggestion.

1. **Letters:** read each `inbox` note. Suggest one folder for each, from what the folders already
   hold. The reason names the topic of the note and the folder that holds like notes, such as "a
   recipe; the cooking notes live in that folder". The action says "move the note to <folder>".
2. **Stale shelf:** from `stale`, pick the notes most worth a decision. A note with recent
   backlinks is still in use: suggest keep, and give the count of recent backlinks as the reason.
   A note with none is an archive suggestion: give its age and its zero recent backlinks as the
   reason, and say that archive moves it to the archive folder, where its links still work. Never
   suggest archive for a note in a `*knowledge` folder because of its age. The scanner leaves those
   notes off, so add none by hand.
3. **The morgue:** list each `delete_candidate`. The reason is its age in the archive and that no
   note outside the archive links to it. The action says "delete the note", and that
   `/journal:act-on-broadsheet` asks before it deletes. When there is no candidate, give the oldest
   archived notes and their ages, with no action.
4. **Floor plan:** from `folders`, find each folder that its use has outgrown, such as loose notes
   beside subfolders, a flat folder with hundreds of notes, an empty folder, or names in two styles.
   The journal domain wants a flat journal folder named by date, so a journal subfolder is news.
   One exception: `chronicles/{YYYY}/` in the journal folder holds past journal files, so it is
   not news.
   Give each finding its numbers as the reason, and one change as the action.
5. **The board:** for each project in `projects`, by `status`:
   - `active`: read its `*.kanban.md` board. Name the next card, the first open card in the first
     column that is not done. Note the cards that moved in the last 7 days, and the cards that sat
     in their column for all 7 days.
   - `waiting`: give one line, with `until` if it has one, only when `changed_days` is 7 or less.
     Else leave it out.
   - `dormant` and `archived`: leave it out.

   An active project with no edit in 7 days can get a status suggestion, such as "set the status
   to dormant". The reason is its `changed_days`.
6. **Back pages:** from `recent`, read the notes edited in the last 7 days in each folder other
   than the journal, inbox, and projects. Write one item per story: what happened and how it came
   out, such as a recipe tried and how it went. Leave out a note with no story, such as a typo fix
   or a list that only grew. For a want list, such as books, films, or gifts, suggest two or three
   additions that fit the list, each as a suggestion row.

**Done when:** each section of the page has its facts, or a note that it has none, and each
suggestion row has a reason and an action.

## Step 6: Write the editorial

From `activity`, `folders`, `compass`, and Steps 3 to 5: where the writing happens, at what hours,
and in which folders. Then give three to five changes to the folders, the templates, or the
routine that fit that use. Base each change on a number from the scan, and give the number. Each
change is a suggestion row. A change to the skills, the hooks, or a script is a suite row. A
change that only edits a note or a template in the vault is a vault row: write
`data-prompt="vault"` on it. When a suite row follows from a vault row, such as a new template
that a skill must read, write that row's `data-id` in `data-relates` on the suite row.

**Done when:** each suggestion names the number behind it.

## Step 7: Lay out the page

Copy `template.html`, and replace each `{{placeholder}}` with HTML. Use only the template's
classes. The page holds no inline style.

Read [LAYOUT.md](LAYOUT.md). It gives the content of each placeholder, the shape of a suggestion
row, and the `data-id` rules. Follow every rule in it.

**Done when:** each section has content or a line that says it has none, each suggestion row has
the row shape, no row id is in `muted`, and no placeholder is left.

## Step 8: Print

1. Write the page to `path` from Step 1.
2. Run `python3 $SKILL_DIR/scripts/check_broadsheet.py <path>`. On exit 1, fix each line that it
   names, and run it again.
3. Open the page in the default browser.
4. Reply with the path and the lead headline. Say to pick a choice or write a comment on each row
   to act on, edit the two prompts at the foot of the page if needed, copy each from its button,
   and paste the vault prompt into `/journal:act-on-broadsheet` and the suite prompt into a new
   session.

**Done when:** the check prints `ok`, and the user has the path.

---
name: broadsheet
description: >
  Print this week's one-page HTML newspaper of the Obsidian vault into the journal folder: the
  week's story, the compass of filled reflections and trends, today's weather, chore rates, the
  goal ledger, the inbox, stale and archived notes, folder layout, project boards, and an
  editorial. Each suggestion has a choice and a comment, and the page builds a prompt for
  /journal:act-on-broadsheet. Use when the user says "broadsheet" or wants a newspaper of their
  vault.
disable-model-invocation: true
argument-hint: "[accent=<colour>]"
---

# Broadsheet

The journal domain's weekly newspaper. The front page tells the last 7 days from the journal. The
inside pages look across the whole vault, and suggest what to file, archive, delete, or
reorganise. The user picks a choice on each suggestion, and the page builds a prompt that
`/journal:act-on-broadsheet` applies.

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
   [`config.example.md`](config.example.md). An `accent=<colour>` argument overrides its line. The
   skill takes no time period: the lead always covers the last 7 days.
4. Defaults: the paper name is "The Obsidian Oracle". The accent is oxblood, `#8b1e3f`. Stale is
   90 days. Archive is 180 days. No location.
5. The vault root is the parent of the journal folder. Find the inbox with
   `/discover-vault-directory *notes`, and the projects folder with
   `/discover-vault-directory *projects`.

**Done when:** you have the edition JSON, the paper name, the accent, the two day limits, the
location or none, the vault root, and the journal, inbox, and projects folders. Or this week's page
exists, and the user has its path.

## Step 2: Scan the vault and the sky

```sh
python3 $SKILL_DIR/scripts/scan_vault.py <vault root> --journal <journal folder> --stale <days> --archive-days <days>
```

The scanner prints JSON. It reads ages from the vault's git history, and from the file time for a
note with uncommitted changes. `dates_from` says which. Each long list holds at most 40 rows, and
`totals` gives its full count. The window is the last 7 days. The keys:

| Key | Holds |
|---|---|
| `folders` | Each folder two levels deep: note count, subfolders, loose notes, newest and oldest age, edits in the last 7 days |
| `journal.summaries` | The `>` summary line of each daily of the last 7 days |
| `journal.missing_days` | Each of the last 7 days with no daily, not counting today |
| `journal.checklists` | Each chore that `occasions.py` gives as due on a day (the daily list and the due chores), matched to the tasks of that day's daily: times seen, times ticked, and the rate, over the last 7 days |
| `journal.occasions_errors` | Each row of `occasions.md` that `occasions.py` cannot read: `line`, `row`, and `why`. A file in the old layout gives an error for each row and no chores |
| `journal.broken_nav` | Each `up`, `prev`, or `next` in a journal file edited in the last 7 days that names no file |
| `compass` | One row each for 7, 30, 90, and 365 days: `dailies`, `edits`, `chore_rate` (null with no chores), `busiest` (top 3 folders by edits), and `reflections` (a count) |
| `reflections` | Each journal note of the last 365 days with a filled reflect section, newest first: `path`, `level` (daily, weekly, monthly), `date`, and `sections` of `{heading, text}`. The `## 🗓️ Weekly Reflect` of a Sunday daily is its own `weekly` item, dated to the Monday of its week, as a weekly file is |
| `projects` | Each project with a `MISSION.md`: `project`, `path`, `status` (`active`, `dormant`, `waiting`, or `archived`), `until`, and `changed_days`, the age of its newest note |
| `inbox` | Each inbox note with its age and word count |
| `recent` | Each note outside the journal edited in the last 7 days |
| `stale` | Each note past the stale limit, with its backlinks, and its backlinks from notes edited inside the limit. Notes in a `*knowledge` folder are never on it |
| `archive` | Each archived note with its age and its links from outside the archive. `delete_candidate` is true past the archive limit with no such link |
| `activity` | Edits by folder, by hour, and by weekday (Monday first), and the tags of notes edited in the last 7 days |

With a location, run:

```sh
python3 $SKILL_DIR/scripts/weather.py <lat> <lon>
```

It prints `{available, date, conditions, high, low, rain_chance, unit}`, or `{available: false}`.

**Done when:** the scanner exits 0, you hold its JSON, and you hold the forecast, or you know that
there is no location or no forecast.

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
change is a suggestion row.

**Done when:** each suggestion names the number behind it.

## Step 7: Lay out the page

Copy `template.html`, and replace each `{{placeholder}}` with HTML. Use only the template's
classes. The page holds no inline style.

| Placeholder | Content |
| --- | --- |
| `paper_name`, `date`, `window`, `edition` | From Step 1. The window is "The last 7 days". The edition is the ISO week, such as "Week 47 edition" |
| `vault_counts` | Notes in the vault, notes edited in the last 7 days, and dailies written |
| `accent` | The accent from Step 1, as a CSS colour |
| `lead_*` | The week's story from Step 4: a headline, a one-line standfirst, and two to four paragraphs. Name the two-week trends from Step 3 |
| `compass_body` | First, each filled reflection, as a `<blockquote>` with its text and a `<cite>` that links the note and gives its level and date, newest first, grouped by window. Then a `<table>` of the four `compass` rows: window, dailies, edits, chore rate, and busiest folders, with each change since last week's page. The reflections get more space than the table. A window with no filled reflection names none |
| `weather_body` | From `weather.py`: `<p class="forecast">` with the conditions, then the high and low with the unit, and the chance of rain. With `available: false`, "The forecast is not available today." With no location, "Set a location in the config for a forecast." |
| `chores_body` | A table of `journal.checklists`: chore, ticked of seen, and the rate in `<span class="rate">` as a percent. No weather icons. Give a chore seen fewer than three times "Too few days to rate". When `journal.occasions_errors` is not empty, add one line under the table with the count of rows that cannot be read, and say that `/update-occasions-config` fixes them |
| `gaps_body` | The missing days and the broken nav links. A `next` that names a file not yet due is expected, so leave it out |
| `ledger_body` | A table per cascade level, one `<tr class="action">` per goal: goal, served, not served, or carried, and the action |
| `letters_body` | One `<li class="action">` per inbox note, from Step 5 |
| `stale_body` | One `<li class="action">` per Step 5 pick, then the total |
| `morgue_body` | One `<li class="action">` per delete candidate, or the oldest archived notes as plain `<li>`, then the total |
| `editorial_body` | The Step 6 prose, then an `<ol>` with one `<li class="action">` per change |
| `floor_plan_body` | One `<article class="action">` per finding: `<span class="kicker">` with the folder, an `<h3>`, the reason, and the action |
| `honour_roll_body` | Up to three: the longest chore streak, the most-linked new note, and the biggest win of the week |
| `board_body` | One `<article>` per shown project from Step 5, with its next card. A status suggestion is an `<article class="action">` |
| `back_pages_body` | One `<article>` per story from Step 5, with `<span class="kicker">` for the folder. Each want list suggestion is an `<li class="action">` in that article |
| `colophon` | `dates_from`, the limits, last week's page or none, and the time of print |

Each suggestion row has this shape:

```html
<li class="action" data-id="letters:<inbox folder>/<note>.md">
  <a href="obsidian://open?vault=..." target="_blank" rel="noopener">Note title</a>
  <span class="age">12 days</span> <span class="tag">new</span>
  <strong>Why:</strong> the reason. <strong>Do:</strong> what the action does.
  <select class="choice" aria-label="Choice for Note title"></select>
  <details><summary>Comment</summary><textarea class="comment" aria-label="Comment on Note title"></textarea></details>
</li>
```

- Leave the `<select>` empty. The page script adds the choices: do, veto, snooze, and done.
- Mark a new row with `<span class="tag">new</span>`, and a repeat with
  `<span class="age">repeat</span>`. With no page last week, mark nothing.
- The `data-id` is `<section id>:<target>`, so the same suggestion has the same id next week. The
  target is:
  - the vault path of the note, with `.md`, in the letters, stale shelf, and morgue;
  - the vault path of the folder in the floor plan;
  - the project folder name on the board;
  - the want list's vault path, then a short kebab-case name of the item, in the back pages, such
    as `back-pages:<path>.md:the-hobbit`;
  - the journal file name, then a short kebab-case name of the goal, in the ledger, such as
    `the-ledger:2026-wk47-week:finish-the-quilt`;
  - a short kebab-case name of the change in the editorial, such as
    `editorial:shopping-list-above-reflect`.

  When a row is the same suggestion as an id in `last_ids`, use that id. Each id is unique on the
  page: when two rows in one section share a target, add `:<action verb>`. An id holds no space and
  no `|`: write a space in the target as `%20` and a `|` as `%7C`, such as
  `stale-shelf:03-work/old%20plan.md`. Write no other code.
- Leave out each row whose `data-id` is in `muted` from Step 1. Do not name it on the page.
- The row text never holds ` | comment: `, because `/journal:act-on-broadsheet` splits there.
- Each note that the page names is a link: `obsidian://open?vault=<vault folder name>&file=<path
  without .md, URL-encoded>`, with `target="_blank"` and `rel="noopener"`. The `data-id` holds the
  path, so the row text names the note only by its link.
- Write in plain prose with newspaper headlines. Each fact traces to the scan or to a note.

**Done when:** each section has content or a line that says it has none, each suggestion row has
the row shape, no row id is in `muted`, and no placeholder is left.

## Step 8: Print

1. Write the page to `path` from Step 1.
2. Run `python3 $SKILL_DIR/scripts/check_broadsheet.py <path>`. On exit 1, fix each line that it
   names, and run it again.
3. Open the page in the default browser.
4. Reply with the path and the lead headline. Say to pick a choice or write a comment on each row
   to act on, copy the prompt from the bar at the foot of the page, and paste it.

**Done when:** the check prints `ok`, and the user has the path.

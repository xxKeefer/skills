---
name: broadsheet
description: >
  Print a one-page HTML newspaper of the Obsidian vault for a time window: the journal's week, the
  goal ledger, carried tasks, the chore weather, the inbox, stale and archived notes, folder layout,
  link health, and an editorial on how the vault is used. Use when the user says "broadsheet" or
  wants a newspaper of their vault.
disable-model-invocation: true
argument-hint: "[time-period] [accent=<colour>]"
---

# Broadsheet

The journal domain's newspaper. The front page tells the window from the journal. The inside pages
look across the whole vault, and suggest what to file, archive, delete, or reorganise.

`$SKILL_DIR` is this skill's base directory. The page is [`template.html`](template.html). The
scanner is `$SKILL_DIR/scripts/scan_vault.py`, and the check is
`$SKILL_DIR/scripts/check_broadsheet.py`.

Write as a secretary: surface the facts, and give each suggestion once. No pressure, no coaching,
no agile words. This skill writes one file, the page. It never moves, edits, archives, or deletes a
note.

## Step 1: Resolve the edition

1. Read `~/.claude/broadsheet.md` if it exists. Its layout is in
   [`config.example.md`](config.example.md).
2. Let each argument override its config line: a time period, `accent=<colour>`.
3. Defaults: the window is the last 7 days. The paper name is "The Vault Herald". The accent is
   oxblood, `#8b1e3f`. Stale is 90 days. Archive is 180 days.
4. Find the journal folder with `/discover-vault-directory * holding occasions.md`. The vault root
   is its parent. Find the inbox with `/discover-vault-directory *notes`, and the projects folder
   with `/discover-vault-directory *projects`.

**Done when:** you have the window in days, the paper name, the accent, the two day limits, the
vault root, and the journal, inbox, and projects folders.

## Step 2: Scan the vault

```sh
python3 $SKILL_DIR/scripts/scan_vault.py <vault root> --journal <journal folder> --window <days> --stale <days> --archive-days <days>
```

The scanner prints JSON. It reads ages from the vault's git history, and from the file time for a
note with uncommitted changes. `dates_from` says which. Each long list holds at most 40 rows, and
`totals` gives its full count. The keys:

| Key | Holds |
|---|---|
| `folders` | Each folder two levels deep: note count, subfolders, loose notes, newest and oldest age, edits in the window |
| `journal.summaries` | The `>` summary line of each daily in the window |
| `journal.missing_days` | Each day in the window with no daily, not counting today |
| `journal.carried` | Each leaf task left open in 3 or more dailies in a row, with its first and last day |
| `journal.checklists` | Each chore from `occasions.md`: times seen and times ticked in the window |
| `journal.broken_nav` | Each `up`, `prev`, or `next` in a journal file edited in the window that names no file |
| `inbox` | Each inbox note with its age and word count |
| `recent` | Each note outside the journal edited in the window |
| `stale` | Each note past the stale limit, with its backlinks, and its backlinks from notes edited inside the limit |
| `archive` | Each archived note with its age and its links from outside the archive. `delete_candidate` is true past the archive limit with no such link |
| `links` | Unresolved link targets grouped by target, most linked first, and orphans that nothing links to |
| `activity` | Edits by folder, by hour, and by weekday (Monday first), and the tags of notes edited in the window |

**Done when:** the scanner exits 0, and you hold its JSON.

## Step 3: Read the journal

Read the journal files that the window touches: the yearly, the monthly, each weekly, and each
daily, with their reflect sections. Read [`CASCADE.md`](../../CASCADE.md) for the carry-forward
rules. From them, find:

- the themes, wins, and misses of the window, for the lead;
- each goal at each level of the cascade, and whether a task at the level below serves it. A goal
  that no task serves, or that carried forward unchanged, is news.

**Done when:** each goal in the window's yearly, monthly, and weekly files is marked served, not
served, or carried.

## Step 4: Read the rest of the vault

1. **Inbox:** read each `inbox` note. Suggest one folder for each, from what the folders already
   hold.
2. **Stale shelf:** from `stale`, pick the notes most worth a decision. A note with recent
   backlinks is still in use, so say keep. A note with none is an archive suggestion.
3. **The morgue:** list each `delete_candidate`. When there is none, give the oldest archived notes
   and their ages.
4. **Floor plan:** from `folders`, find each folder that its use has outgrown, such as loose notes
   beside subfolders, a flat folder with hundreds of notes, an empty folder, or names in two styles.
   The journal domain wants a flat journal folder named by date, so a journal subfolder is news.
   Give each finding one suggested change.
5. **The board:** read each `*.kanban.md` board in the projects folder that changed in the window,
   and each board whose folder has no edit in the window. Note the cards that moved, the cards in
   their column for the whole window, and the boards with no edits.
6. **Back pages:** from `recent`, read the notes edited in the window in each folder other than the
   journal, inbox, and projects. Write one short item per folder.
7. **Link health:** from `links`, a target that many notes link to is a note that the vault keeps
   asking for. Name the top five. Give the orphan count, with up to five examples.

**Done when:** each section of the page has its facts, or a note that it has none.

## Step 5: Write the editorial

From `activity`, `folders`, and Steps 3 and 4: where the writing happens, at what hours, and in
which folders. Then give three to five changes to the folders, the templates, or the routine that
fit that use. Base each change on a number from the scan, and give the number.

**Done when:** each suggestion names the number behind it.

## Step 6: Lay out the page

Copy `template.html`, and replace each `{{placeholder}}` with HTML. Use only the template's
classes. The page holds no inline style.

| Placeholder | Content |
| --- | --- |
| `paper_name`, `date`, `window`, `edition` | From Step 1. The edition is the date in words, such as "Saturday edition" |
| `vault_counts` | Notes in the vault, notes edited in the window, and dailies written |
| `accent` | The accent from Step 1, as a CSS colour |
| `lead_*` | The window's story from Step 3: a headline, a one-line standfirst, and two to four paragraphs |
| `weather_body` | A table of the checklists: chore, ticked of seen, and a forecast. ☀️ at 80% or more, ⛅ from 50% to 79%, ⛈️ below 50%. Give a chore seen fewer than three times "No reading" |
| `gaps_body` | The missing days and the broken nav links. A `next` that names a file not yet due is expected, so leave it out |
| `ledger_body` | A table per cascade level: goal, and served, not served, or carried |
| `carried_body` | An `<ol class="two">`, one `<li>` per carried task, with its days and dates in `<span class="age">` |
| `letters_body` | One `<li>` per inbox note, with its age and its suggested folder |
| `stale_body` | The Step 4 picks, each with its age and keep or archive, then the total |
| `morgue_body` | The delete candidates, or the oldest archived notes, then the total |
| `editorial_body` | The Step 5 editorial as prose |
| `floor_plan_body` | One `<article>` per finding: `<span class="kicker">` with the folder, an `<h3>`, and the suggestion |
| `link_health_body` | The most-asked-for targets and the orphans |
| `honour_roll_body` | Up to three: the longest checklist streak, the most-linked new note, and the biggest win of the window |
| `board_body` | One `<article>` per board from Step 4 |
| `back_pages_body` | One `<article>` per folder from Step 4, with `<span class="kicker">` for the folder |
| `colophon` | `dates_from`, the window, the limits, and the time of print |

- Each note that the page names is a link: `obsidian://open?vault=<vault folder name>&file=<path
  without .md, URL-encoded>`, with `target="_blank"` and `rel="noopener"`.
- Write in plain prose with newspaper headlines. Each fact traces to the scan or to a note.

**Done when:** each section has content or a line that says it has none, and no placeholder is
left.

## Step 7: Print

1. Write the page to `broadsheet_<YYYY-MM-DD>.html` in the inbox folder.
2. Run `python3 $SKILL_DIR/scripts/check_broadsheet.py <path>`. On exit 1, fix each line that it
   names, and run it again.
3. Open the page in the default browser.
4. Reply with the path and the lead headline.

**Done when:** the check prints `ok`, and the user has the path.

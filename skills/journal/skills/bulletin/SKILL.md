---
name: bulletin
description: >
  Add today's entry to this week's HTML bulletin in the journal folder. The page holds one dated
  entry for each day you run it, newest on top. Each entry gives the week's goals and how they
  moved since the entry below it, how last week ended, a look at next week, a Reflect masonry of
  four cards, and a side column with weather, events, and chores. Use when the user says
  "bulletin" or wants a daily page that shows how the goals change over the week.
disable-model-invocation: true
argument-hint: "[accent=<colour>] [place=<label or name>]"
---

# Bulletin

The journal domain's daily page. One file holds one ISO week. Each run adds one entry with its own
masthead, above the older entries. The older entries are input for the next run: you compare
against the latest one, so the entry says what is new, what changed, and what stayed.

`$SKILL_DIR` is this skill's base directory. The page is [`template.html`](template.html). The
entry shape is in [`LAYOUT.md`](LAYOUT.md). The scripts in `$SKILL_DIR/scripts/` are
`bulletin.py` and `check_bulletin.py`. This skill also calls scripts of its neighbours:
`$SKILL_DIR/../broadsheet/scripts/scan_vault.py`, `$SKILL_DIR/../broadsheet/scripts/weather.py`,
and `$SKILL_DIR/../../scripts/occasions.py`. It copies no code from them.

Write as a secretary: surface the facts, and give each item once. No pressure, no coaching, no
agile words. This skill writes one file, the page. It never edits, moves, or deletes a note. The
page has no suggestion row, no choice control, no prompt, and no script.

## Step 1: Resolve the entry

1. Find the journal folder with `/discover-vault-directory * holding occasions.md`. Run:

   ```sh
   python3 $SKILL_DIR/scripts/bulletin.py state <journal folder>
   ```

   It prints `{path, exists, today_present, days, days_since_last, last_ids, week_start,
   last_week_start, window_days}`.
   `path` is `<journal folder>/{YYYY}-wk{ww}-bulletin.html`, with the ISO week of today. `days`
   lists the dates that have an entry, newest first. `last_ids` lists the `data-id` values of the
   latest entry. `week_start` is the Monday of this week. `last_week_start` is the Monday of last
   week. `window_days` is the days from `last_week_start` to today.
2. If `today_present` is true, stop. Scan nothing and write nothing. Reply with `path`, and say that
   today's entry is already on the page.
3. Read `~/.claude/broadsheet.md` if it exists. Its layout is in
   [`config.example.md`](../broadsheet/config.example.md). An `accent=<colour>` argument overrides
   its line. A `place=<label or name>` argument replaces the places for this run: a label of the
   config picks that place, and any other value is one place name.
4. Defaults: the paper name is "The Obsidian Oracle", so the bulletin is "The Obsidian Oracle
   Bulletin". The accent is oxblood, `#8b1e3f`. No places.
5. The vault root is the parent of the journal folder. Find the inbox with
   `/discover-vault-directory *notes`, and the projects folder with
   `/discover-vault-directory *projects`.
6. The entry number is the count of `days` plus one. When `days_since_last` is above 1, the entry
   covers that many days. Say so in the standfirst. When `days` is empty, this is the first entry
   of the week.

**Done when:** you have the state JSON, the paper name, the accent, the places or none, the vault
root, and the journal, inbox, and projects folders. Or today's entry exists, and the user has the
path.

## Step 2: Scan the vault, the sky, and the calendar

The window covers last week and this week. Pass `window_days` from `state`. Do no date sums.

```sh
python3 $SKILL_DIR/../broadsheet/scripts/scan_vault.py <vault root> --journal <journal folder> --window <window_days>
```

The scanner prints JSON. [`SCAN.md`](../broadsheet/SCAN.md) names each key. Use only what falls
in the window. Sort the items by their dates: the dates from `week_start` on are this week, and
the earlier dates are last week. Name no note older than the window, except as the context of a
goal.

For each place, run one of these. A place that is a name takes the name. A place that is
coordinates takes both numbers:

```sh
python3 $SKILL_DIR/../broadsheet/scripts/weather.py <place name>
python3 $SKILL_DIR/../broadsheet/scripts/weather.py <lat> <lon>
```

Each run prints `{available, date, conditions, high, low, rain_chance, unit}`, or
`{available: false}`. The forecast is for today.

Run `occasions.py` once for today, once for each later day of this week up to Sunday, and once
for each day of next week, Monday to Sunday:

```sh
python3 $SKILL_DIR/../../scripts/occasions.py <journal folder>/occasions.md --date <YYYY-MM-DD>
```

Each run prints `{due, past, errors, old_layout}`. `due` holds the items of that day, by section.
`errors` lists the rows that the script cannot read.

**Done when:** the scanner exits 0, you hold its JSON, you hold the forecast or know that there is
no place or no forecast, and you hold the due items for each day from today to the Sunday of next week.

## Step 3: Read the earlier entries

If `days` is empty, skip this step. Every story is new, and the standfirst says that this is the
first entry of the week.

Else read `path`, and take the latest entry, the first one on the page. From it, take its goal
statuses, its headline, and its stories. `last_ids` lists their `data-id` values.

- A story is **new** when its `data-id` is not in `last_ids`.
- A story is **changed** when its `data-id` is in `last_ids` and its facts differ.
- A story is **unchanged** when its `data-id` is in `last_ids` and its facts are the same. It gets
  one line.
- Find what moved since the latest entry: a goal that changed status, a chore rate that moved, a
  card that changed column.

**Done when:** each story you plan is new, changed, or unchanged, and you know what moved since
the latest entry, or that there is no earlier entry.

## Step 4: Read the journal

Read the weekly and daily files of the window. Read [`CASCADE.md`](../../CASCADE.md) for the
carry-forward rules. Read no yearly or monthly goal. From them, find:

- each goal of this week, and whether a task at the level below serves it. Mark each goal as
  served, not served, or carried;
- what changed in each goal since the latest earlier entry, or that this is the first entry of the
  week;
- how each goal of last week ended: served, not served, or carried into this week;
- the goals that carry into next week, and the ideas for next week;
- the filled reflections of the window, by the map in the Reflect card rule of Step 6.

**Done when:** each goal of this week and of last week has a status, and you have read each filled
reflection of the window.

## Step 5: Read the rest of the window

1. **Chores:** from the journal scan, give the ticks since the Monday of last week for each chore. The scan counts the whole window.
2. **The board:** for each active project in `projects` with `changed_days` inside the window, read
   its Kanban file. A card moved when its column differs from the latest earlier entry. With no
   earlier entry, name the cards of the first column that is not done. Leave out a project with no
   move.
3. **Notes:** from `recent`, name the notes edited in the window, outside the journal, with one
   line on what each one holds. Leave out a note with no story, such as a typo fix.

**Done when:** each section has its facts, or a line that says it has none.

## Step 6: Write the entry

Write the entry to a scratch file outside the vault. Read [`LAYOUT.md`](LAYOUT.md). It gives the
frame, the content of each part, the chart rule, and the `data-id` rules. Follow every rule in it.

The main column has six parts, in the order of `LAYOUT.md`: This week, Last week, Next week, Reflect,
the board, and the notes. The side column holds the weather, the events, and the chores.

- **Last week** gives how last week's goals ended, and a chart of this week against last week, from
  the numbers that the chart rule of `LAYOUT.md` names.
- **Next week** gives the carried goals, the events of each day of next week from `occasions.py`,
  and the ideas. Mark it as a projection.
- **Reflect** is a masonry of four cards. Each item says its week and links its note. Map the
  sources like this: Learning from the learned lines (`What I learned`), Friction from `What caused
  friction`, and What's next from `What is next`, all in `reflections` of the scan, and Ideas from
  the `Thoughts and Ideas` section of the dailies that Step 4 reads. A card with no
  item says so.
- **Charts:** follow the rule of `/show-me`: the smallest visual that makes the point. Write each
  chart by hand as an inline SVG bar chart, because `/show-me` has no SVG form and the page has no
  script. A chart appears only when the scan holds its numbers. `LAYOUT.md` names the suggested
  charts and their sources.

**Done when:** the entry holds each part or a line that says it has none, each story has a
`data-id`, at least one chart is drawn, and no placeholder is left.

## Step 7: Add the entry

1. Run:

   ```sh
   python3 $SKILL_DIR/scripts/bulletin.py add <path> <entry file>
   ```

   The script creates the page from the template when it does not exist. Else it puts the entry
   above the older entries and leaves them as they were. It exits 1 when the page already has an
   entry for today.
2. Replace the accent in the page's `:root` block only when it differs from the template, and only
   when the page is new.
3. Run `python3 $SKILL_DIR/scripts/check_bulletin.py <path>`. On exit 1, fix each line that it
   names, and run it again. Fix the new entry only. Never edit an older entry.
4. Open the page in the default browser.
5. Reply with the path and the headline of the entry.

**Done when:** the check prints `ok`, and the user has the path.

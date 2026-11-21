---
name: weekly
description: Generate the weekly file, with monthly goals, events from occasions, a daily links table, and recurring themes.
disable-model-invocation: true
---

# Weekly

Generate the weekly file. Surface context, don't apply pressure.

`$SKILL_DIR` is this skill's base directory. The occasions script is
`$SKILL_DIR/../../scripts/occasions.py`.

## Step 1: Parse Input

`<user-input>` may contain:

- A **week number** (e.g., "weekly wk14") -- plan that specific week
- A **file path** -- update an existing weekly file
- **Nothing** -- plan the current/next week

Determine the week dates (Monday -> Sunday) and the file name: `YYYY-wkNN-week.md`.

Find the journal directory with `/discover-vault-directory * holding occasions.md`.

## Step 2: Read Context

Read these files from the journal directory:

- `YYYY-MM-mon.md` -- this month's goals (for pull-down)
- Previous week's file (if exists) -- check reflect section
- Previous week's Sunday daily (if exists) -- check its `## 🗓️ Weekly Reflect` section
- This week's existing daily files (if any) -- for theme detection

The user can write the week's reflect in the Sunday daily. When the previous week's file has an
empty `## 🤔 Reflect` and its Sunday daily has text under `## 🗓️ Weekly Reflect`, copy that text
into the previous week's `## 🤔 Reflect`, under the same `###` headings. Change nothing else in
either file. Then use it as last week's reflect.

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- This month's goals (what's active)
- Last week's reflect (what went well, friction, what's next)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Pull Down Monthly Goals

Follow **Pull-down** in [CASCADE.md](../../CASCADE.md), with this month's file as the parent.

Ask:

> Any additional goals for this week?

## Step 5: Assemble Events

Get the events from the occasions script. Do not read the `When` rules yourself. Run the
script once for each date of this week, Monday to Sunday:

```sh
python3 $SKILL_DIR/../../scripts/occasions.py <journal directory>/occasions.md --date <YYYY-MM-DD>
```

Each run prints JSON: `due` (the items due on that date, in `chores`, `work`, and `tasks`),
`errors` (each row it cannot read), and `past`. The events are the `due` items whose row is in
the `## Yearly`, `## Maintenance`, or `## One-off` table.
Find the table of an item by its name in `occasions.md`. Give each event with its date.

When `errors` is not empty, say once: `occasions.md has {N} rows that occasions.py cannot read.
Run /update-occasions-config.` Go on with the rows that it can read.

List the events under the Events section.

Ask:

> Any other events this week?

## Step 6: Build Daily Links Table

Generate the Days table with wikilinks for each day of the week (Mon-Sun). The Day column shows
the date number before the day abbreviation (e.g., "02 Mon", "03 Tue").

Populate the Notes column for each day:

- Match events from `occasions.md` (assembled in Step 5) to their specific day
- If a daily file already exists, pull a short note from it
- Combine both sources -- events first, then existing notes

## Step 7: Detect Recurring Themes

If daily files from the previous week exist, scan their "Thoughts and Ideas" and reflect sections
for recurring themes or ideas that appear 2+ times.

If found, suggest:

> These themes came up multiple times last week:
> - {theme}
>
> Worth promoting any to a standalone note?

If nothing recurs, skip this step silently.

## Step 8: Carry Forward

Follow **Carry-forward** in [CASCADE.md](../../CASCADE.md) on the open goals in last week's file.

## Step 9: Write the Weekly File

Create or update `YYYY-wkNN-week.md` in the journal directory using the format in
[templates/weekly.md](../../templates/weekly.md).

## Step 10: Done

> **Week {NN}** ready. {N} goals, {N} events.

---
name: yearly
description: Generate the yearly file, with a goals dump, a monthly plan table, and reflection sections.
disable-model-invocation: true
---

# Yearly

Generate the yearly file. Lightest-touch skill -- a goals dump and organising structure.

`$SKILL_DIR` is this skill's base directory. The occasions script is
`$SKILL_DIR/../../scripts/occasions.py`.

## Step 1: Parse Input

`<user-input>` may contain:

- A **year** (e.g., "yearly 2027") -- target that year
- A **file path** -- update an existing yearly file
- **Nothing** -- target the current year

Determine the file name: `YYYY.md` (e.g., `2026.md`).

Find the journal directory with `/discover-vault-directory * holding occasions.md`.

Check if the yearly file already exists. If it does, read it and update rather than overwrite.

## Step 2: Read Context

Read these files from the journal directory:

- Previous year's file (if exists) -- check reflect section and goals

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- Last year's reflect (what went well, friction, what's next)
- Last year's goals (what was achieved, what carried over)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Set Goals

If last year's file exists, follow **Carry-forward** in [CASCADE.md](../../CASCADE.md) on its open
goals.

Then ask:

> What are your goals and aspirations for {YYYY}?

This is freeform -- big-picture stuff. Holidays, projects, life changes, learning goals. No
structure enforced beyond a checklist.

## Step 5: Assemble Events

Get the events from the occasions script. Do not read the `When` rules yourself. Run the
script once for each date of this year, from Jan 1 to Dec 31:

```sh
python3 $SKILL_DIR/../../scripts/occasions.py <journal directory>/occasions.md --date <YYYY-MM-DD>
```

Each run prints JSON: `due` (the items due on that date, in `chores`, `work`, and `tasks`),
`errors` (each row it cannot read), and `past`. The events are the `due` items whose row is in
the `## Yearly` or `## One-off` table.
Find the table of an item by its name in `occasions.md`. Give each event with its date.

When `errors` is not empty, say once: `occasions.md has {N} rows that occasions.py cannot read.
Run /update-occasions-config.` Go on with the rows that it can read.

List the events under the Events section.

Ask:

> Any other events or milestones planned for this year?

## Step 6: Build Monthly Plan Table

Generate the Monthly Plans table with wikilinks for all 12 months. If monthly files already
exist, pull a short note from their goals. Otherwise leave Notes empty.

## Step 7: Write the Yearly File

Create or update `YYYY.md` in the journal directory using the format in
[templates/yearly.md](../../templates/yearly.md).

If updating an existing file, preserve any content already written. Only update sections that
need changes.

## Step 8: Done

> **{YYYY}** ready. {N} goals set.

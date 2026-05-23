---
name: daily
description: >
  Generate today's daily file. Assembles chores from occasions, pulls weekly goals into tasks,
  reads yesterday's reflect for at-a-glance context. Use when user says "daily", "what's today",
  or starts their day.
---

# Daily

Generate the daily file. Quick, focused, minimal back-and-forth.

**Input:** optional date or file path, plus freeform notes (ad-hoc tasks, work context).
**Output:** daily file (`YYYY-wkNN-day.md`) in the journal directory.

## Step 1: Parse Input

`<user-input>` may contain:

- A **date** (e.g., "daily monday", "daily 2026-03-24") -- target that day
- A **file path** -- update an existing daily file
- **Freeform notes** -- ad-hoc tasks, work context to fold into the checklist
- **Nothing** -- target today

Determine the day, week number, and file name: `YYYY-wkNN-day.md` (e.g., `2026-wk13-mon.md`).

Locate the journal directory per the journal domain's discovery convention.

Check if the daily file already exists. If it does, read it and update rather than overwrite.

## Step 2: Read Context

Read these files from the journal directory:

- `YYYY-wkNN-week.md` -- this week's goals
- `occasions.md` -- chores and events for today
- Previous day's file (if exists) -- check reflect section for context

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- Yesterday's reflect (what's next, friction, learnings)
- This week's goals (what's active, what's relevant today)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Build the Checklist

See [CHECKLIST_RULES.md](CHECKLIST_RULES.md) for assembly rules.

### Pull Down Weekly Goals

Read the current weekly file's Goals section. Present them:

> This week's goals:
> - [ ] Goal 1
> - [ ] Goal 2
>
> Pull any into today's tasks?

Add selected goals to the Tasks group. Don't pressure -- if they skip, that's fine.

### Confirm

> Here's today's file. Anything to add or drop?

One round of confirmation, then write.

## Step 5: Write the Daily File

Create or update `YYYY-wkNN-day.md` in the journal directory using the format in
`journal/templates/daily.md`.

If updating an existing file, preserve any content already written (checked chores, completed
tasks, notes). Only update sections that need changes.

## Step 6: Done

> **{Dayname} -- wkNN** ready. {N} tasks, {N} chores. {event note if applicable}

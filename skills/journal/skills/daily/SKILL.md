---
name: daily
description: Generate today's daily file, with chores from occasions, weekly goals, and yesterday's open tasks, after one question that ticks what the user did yesterday.
disable-model-invocation: true
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

Find the journal directory with `/discover-vault-directory * holding occasions.md`.

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

Follow **Pull-down** in [CASCADE.md](../../CASCADE.md), with this week's file as the parent.

### Backfill Yesterday

Before the carry-forward, ask one question: which of yesterday's open items did the user do? List
each open item in yesterday's `## 📋 Today`, numbered. List the children of a group, not the group
line:

> Still open from yesterday. Which did you do? (`all`, `none`, numbers, or `skip`)
> 1. {item}
> 2. {item}

- `all`: tick each listed item in yesterday's file.
- Numbers, such as `1 3`: tick only those items.
- `none`, `skip`, or no answer: tick nothing.

When the answer ticks all children of a group, tick the group line too. Change nothing else in
yesterday's file. Ask no question when yesterday has no file or no open item.

### Carry Forward

Follow **Carry-forward** in [CASCADE.md](../../CASCADE.md) on the items in yesterday's file that
are still open after the backfill.

### Confirm

> Here's today's file. Anything to add or drop?

One round of confirmation, then write.

## Step 5: Write the Daily File

Create or update `YYYY-wkNN-day.md` in the journal directory using the format in
[templates/daily.md](../../templates/daily.md).

If updating an existing file, preserve any content already written (checked chores, completed
tasks, notes). Only update sections that need changes.

## Step 6: Done

> **{Dayname} -- wkNN** ready. {N} tasks, {N} chores. {event note if applicable}

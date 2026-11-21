---
name: daily
description: Generate today's daily file, with chores from occasions, weekly goals, and yesterday's open tasks, after one question that ticks what the user did yesterday. Then commits and pushes the vault when it is a git repo.
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

## Step 7: Back Up the Vault

This is the one step in which a journal skill commits in the vault. Run it after the daily file
is written.

1. Find the repo: `git -C <journal directory> rev-parse --show-toplevel`. Go on only when this
   command works and the folder it gives holds `.obsidian/`, so that the repo is the vault and
   not a parent folder. Else skip this step and say nothing.
2. Run `git -C <vault root> remote`. When it prints nothing, skip this step and say nothing.
3. Commit every change: `git -C <vault root> add -A`, then
   `git -C <vault root> commit -m "vault: daily <YYYY-MM-DD>"`, with the date of the daily file.
   When nothing changed, make no commit.
4. Run `git -C <vault root> push`. Never force a push.

When a command in items 3 or 4 fails, give one line, `Backup failed: {first line of the error}`,
and stop the step. The daily file is already written, so the daily is still done. Make no second
try, and do not fix the repo.

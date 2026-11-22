---
name: daily
description: Generate today's daily file, with chores from occasions, weekly goals, and the last daily's open tasks, after one question that ticks what the user did since. Then commits and pushes the vault when it is a git repo.
disable-model-invocation: true
---

# Daily

Generate the daily file. Quick, focused, minimal back-and-forth.

**Input:** optional date or file path, plus freeform notes (ad-hoc tasks, work context).
**Output:** daily file (`YYYY-wkNN-day.md`) in the journal directory.

`$SKILL_DIR` is this skill's base directory. The occasions script is
`$SKILL_DIR/../../scripts/occasions.py`.

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
- The **last daily** (if one exists) -- check its `## 🤔 Reflect` section for context

The last daily is the daily file with the latest date before the target day, not only the file of
the day before. List the daily files (`YYYY-wkNN-day.md`, not `-week`) in the journal directory,
then in `chronicles/{YYYY}/` for the year of the target day and the year before. Get each date
from the file name. When the root and `chronicles/` both hold a file, use the root copy. Note how
many days back it is: 1 for the day before.

### Occasions

Get the day's chores and events from the script. Do not read the `When` rules yourself:

```sh
python3 $SKILL_DIR/../../scripts/occasions.py <journal directory>/occasions.md --date <YYYY-MM-DD>
```

It prints JSON: `daily` (the lines of the `## Daily` list), `due` (the items due on the date, in
`chores`, `work`, and `tasks`), `errors` (each row it cannot read, with its `line` and `why`), and
`past` (each one-off whose date is gone), and `old_layout` (true when the file has no `## Daily`
heading, or a table has a `Type` or `Date/Rule` column). [CHECKLIST_RULES.md](CHECKLIST_RULES.md)
puts `daily` and `due` into the checklist.

When `old_layout` is true, do not give an empty chore list with no word. Say:

> `occasions.md` is in the old layout, so today has no chores from it. Run
> `/update-occasions-config` to migrate it.

Then go on with the other parts of the daily.

In the new layout, give one line for each row in `errors`: `occasions.md line {line}: {why}`. Use
the rows that the script can read.

List each `past` one-off for the user to prune: `Past one-offs in occasions.md: {item} ({when})`.
Delete nothing from `occasions.md`.

Give these lines once, with the Step 6 message.

## Step 3: Build At a Glance

Compose the blockquote summary under the heading. Pull from:

- The last daily's reflect (what's next, friction, learnings)
- This week's goals (what's active, what's relevant today)

Keep it to 2-3 sentences. Factual, no editorialising.

## Step 4: Build the Checklist

See [CHECKLIST_RULES.md](CHECKLIST_RULES.md) for assembly rules.

### Pull Down Weekly Goals

Follow **Pull-down** in [CASCADE.md](../../CASCADE.md), with this week's file as the parent.

### Backfill the Last Daily

Before the carry-forward, ask one question: which of the last daily's open items did the user do?
List each open item in its `## 📋 Today`, numbered. List the children of a group, not the group
line. Name the day and how many days back it is:

> Still open from {day} ({N} days ago). Which did you do? (`all`, `none`, numbers, or `skip`)
> 1. {item}
> 2. {item}

When the last daily is the day before, write `Still open from yesterday.`

- `all`: tick each listed item in the last daily's file.
- Numbers, such as `1 3`: tick only those items.
- `none`, `skip`, or no answer: tick nothing.

When the answer ticks all children of a group, tick the group line too. Change nothing else in
the last daily's file. Ask no question when there is no last daily or it has no open item.

### Carry Forward

Follow **Carry-forward** in [CASCADE.md](../../CASCADE.md) on the items in the last daily's file
that are still open after the backfill. With no last daily, carry nothing forward.

### Confirm

> Here's today's file. Anything to add or drop?

One round of confirmation, then write.

## Step 5: Write the Daily File

Create or update `YYYY-wkNN-day.md` in the journal directory using the format in
[templates/daily.md](../../templates/daily.md).

If updating an existing file, preserve any content already written (checked chores, completed
tasks, notes). Only update sections that need changes.

Keep each free section, such as a shopping list, above `## 🤔 Reflect`. Put nothing but the reflect
bullets and their text in a reflect section.

On a Sunday, add `## 🗓️ Weekly Reflect` after `## 🤔 Reflect`. Under it, copy the three bullets
of the `## 🗓️ Weekly Reflect` section of [templates/daily.md](../../templates/daily.md). The user writes
the week's reflect there, and `/weekly` and `/reflect` copy it into the weekly file. On other
days, leave the section out.

## Step 6: Done

> **{Dayname} -- wkNN** ready. {N} tasks, {N} chores. {event note if applicable}

Then give the occasions lines from Step 2, if any.

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

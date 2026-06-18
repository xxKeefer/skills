---
name: schedule-goals
description: >
  Schedule a project's milestones into the journal. Writes dated milestones into the Projects section
  of occasions.md and/or goals into the relevant cascading journal file (daily/weekly/monthly/yearly).
  Use when the user says "schedule goals", "add a milestone", "set a deadline", or wants a project's
  dates and goals to surface in their journal.
---

# Schedule Goals

The bridge from a project to the journal. A milestone is a **dated** thing the journal should remind
you about; a goal is a **cascading** thing that feeds your planning. This skill writes both, then
regenerates the Templater config so they surface.

## Step 1: Identify the Project

Check `$ARGUMENTS` for a project slug or name. Otherwise discover the projects directory (per the
domain `CLAUDE.md`) and list active projects (those whose `MISSION.md` has `status: active`). Ask
which one.

Read the project's `MISSION.md` and board for context -- the milestones should serve the mission.

## Step 2: Gather Milestones and Goals

Ask what to set. Two distinct outputs:

- **Milestones** -- a dated event the journal surfaces as a reminder. Needs an emoji, a short label,
  and a date. Phrase the label as `{Project}: {milestone}` so it reads clearly in the daily file.
- **Goals** -- a cascading planning item. Needs a target level: daily, weekly, monthly, or yearly.

A single call can produce any mix. Confirm the parsed list before writing.

## Step 3: Write Milestones to occasions.md

Discover the journal directory (scan for `occasions.md`). **Read-modify-write** -- never overwrite.

- If a `## Projects` section exists, append rows to its table.
- If not, create the section using the shape in the journal `occasions.md` template:

  ```
  ## Projects
  | Occasion | Date/Rule | Type | Section |
  |---|---|---|---|
  | 🏗 New House: finance approved | Jul 3 | event | tasks |
  ```

- Default Type `event`, Section `tasks`. Use the date format the config parser understands
  (`Mon DD`, e.g. `Jul 3`).

## Step 4: Write Goals to Journal Files

For each goal, locate the target journal file by the journal naming convention
(`YYYY-wkNN-day.md`, `YYYY-wkNN-week.md`, `YYYY-MM-mon.md`, `YYYY.md`). Append the goal to that
file's Goals (or Tasks, for daily) section as a `- [ ]` item. Read-modify-write. If the target file
doesn't exist yet, tell the user and suggest the matching journal skill (`/weekly`, `/monthly`, etc.)
rather than creating it here.

## Step 5: Regenerate Templater Config

If any milestone was written, offer to run `/update-occasions-config` so the new Projects rows reach
`vault_occasions.js` and surface in daily/weekly files. Don't run it silently -- ask first.

## Step 6: Confirm

Report what was written:

> Set for **{Project}**:
> - Milestones -> `occasions.md` Projects: {list}
> - Goals -> {file}: {list}
>
> {Ran / skipped} `/update-occasions-config`.

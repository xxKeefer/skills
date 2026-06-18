---
name: summarize-sprint
description: >
  Produce a terse, shareable one-pager for a project: the current goal plus a task breakdown by
  timeframe (This Week / This Month / Next Up). Designed to export to PDF and share with anyone,
  including people with no access to the vault. Use when the user says "summarize sprint", "sprint
  summary", "one-pager", "share an update", or wants a clean status to send someone.
---

# Summarize Sprint

A one-page status anyone can read -- a collaborator, a partner, a stakeholder. No vault access, no
Obsidian, no jargon required.

> **Public-facing output.** This document leaves the vault. It must contain **no personal specifics**
> beyond what the recipient already knows, no private notes, no internal decision detail. Keep it to
> the goal and the work.

## Step 1: Identify the Project

Check `$ARGUMENTS` for a slug or name. Otherwise discover the projects directory and list active
projects; ask which one. Read `MISSION.md` and the board.

## Step 2: Build the One-Pager

Translate the board into three timeframe buckets. Map cards by their `@{date}` tag and column:

- **This Week** -- the `This Week` column + anything dated within 7 days.
- **This Month** -- cards dated within the month, or the obvious near-term backlog.
- **Next Up** -- everything beyond this month; the horizon, not the detail.

Lead with the single most important thing: **what we're trying to achieve right now**. Then the
breakdown. Terse -- bullets, not paragraphs.

```md
# {Project Name}

**Goal right now:** {one sentence -- the current focus, drawn from MISSION.md + the board}

## This Week
- {task}
- {task}

## This Month
- {task}

## Next Up
- {task}

_Updated {date}_
```

Strip emoji-as-status and internal labels; write it for a reader who has never seen the board.

## Step 3: Write and Export

Write the one-pager to the project workspace as `sprint-summary.md` (overwrite the previous one --
it's a snapshot, not a log).

Offer to export to PDF. Stay tool-agnostic -- use whatever the environment has. A common path:

```
pandoc sprint-summary.md -o sprint-summary.pdf
```

If no converter is available, say so and hand back the markdown for the user to export themselves.

## Step 4: Confirm

> **Sprint summary for {Project}** -- written to `sprint-summary.md`{, exported to `sprint-summary.pdf`}.
> Goal: {the headline}. Ready to share.

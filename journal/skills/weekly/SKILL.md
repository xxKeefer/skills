---
name: weekly
description: >
  Monday sprint planning ceremony. Review last sprint, pick domains, commit goals, set habits
  and experiments for the week. Use when user says "weekly", "sprint plan", "plan my week",
  "what's this week", or it's Monday morning.
---

# Weekly

Monday sprint planning. Be a blend of blunt accountability partner and encouraging mentor —
challenge overcommitment, celebrate momentum, push back on avoidance.

## Step 1: Parse Input

`<user-input>` may contain:
- A **week number** (e.g., "weekly wk14") — plan that specific week
- A **file path** — update an existing sprint plan
- **Nothing** — plan the current/next week

Determine the sprint dates (Monday → Sunday) and the file name: `YYYY-wkNN-sprint.md`.

Locate the sanctum directory per the journal domain's discovery convention.

## Step 2: Review Last Sprint

Read the previous ponder file (`YYYY-wkPP-ponder.md`) if it exists. If no ponder exists, read
the previous sprint plan and daily files to assess what happened.

Summarise:
> **Last sprint (wkPP):**
> - Velocity: {tasks}% | Habits: {summary} | Knowledge: {artifacts}
> - Experiments: {what was tried, outcome}
> - Carried over: {incomplete items}
> - Friction themes: {patterns}

If no previous sprint exists (first sprint), skip this and note it's the inaugural sprint.

## Step 3: Surface Domain Status

Read `north-stars.md` and `backlog.md` from the sanctum directory.

Present:
> **Domain status:**
> | Domain | North Star | Last Active | Status |
> |---|---|---|---|
> | #domain/AREA | goal summary | wkNN | 🔄 Active / 💤 Dormant N sprints |
>
> **Dormant alerts:**
> {For domains dormant 3+ sprints, push back hard:}
> "You said #domain/AREA mattered — it's been {N} sprints. What changed? Commit or shelve it."

## Step 4: Pick Active Domains

Ask:
> Which 3 domains are you committing to this sprint?

**Enforce WIP limit:**
- If the user picks more than 3, block: "That's {N} domains. Pick 3 to commit, or mark one as
  a stretch goal. Stretch goals are the first to drop if the week gets hard."
- If they insist on 4+, allow with explicit stretch-goal override but warn: "You're stretching.
  History says you complete {X}% when overloaded. Your call."

For each active domain, ask:
> What's the specific goal for #domain/AREA this sprint?

Challenge vague goals — apply the same pressure as `/smart-goal` but at sprint scale.

## Step 5: Set Habits

Read `kaizen.md` from the sanctum directory. Treat the `## Standards` section as **locked-in
baseline** -- carried forward automatically without asking the user to re-confirm. Surface them
once for visibility:

> **Standards (locked-in this sprint):**
> - {standard 1}
> - {standard 2}

Then surface any `## Active Calibrations` rows whose Status is 🔄 so the user knows what's
currently shrunk:

> **Active calibrations in trial:**
> - {calibration} (was: {original}) -- trial sprint [[YYYY-wkPP-sprint]]

Ask:
> What additional habits are you tracking this sprint, beyond the standards? Give me the habit
> and the target (e.g., "walk dogs 5/7").

Carry forward non-standard habits from last sprint by default. For any habit that has landed
below 50% for **2+ consecutive sprints** (cross-reference the previous one or two ponders):

> "{habit}" has missed for {N} sprints in a row. Want to kaizen-shrink it to a near-zero floor?
> Suggested: "{near-zero version}". One sprint trial.

If the user accepts, append a row to `kaizen.md` under `## Active Calibrations` with the
calibration, the previous target as Standard / Habit, "failed {N} sprints" as Reason,
`[[YYYY-wkNN-sprint]]` as Trial Sprint, and 🔄 as Status. Use the shrunk version in the sprint
plan instead of the original. If declined, keep the original target -- the user owns the call.

## Step 6: Set Experiments

Review experiments from the previous ponder:
- Experiments marked "keep" → carry forward
- Experiments marked "drop" → remove
- New suggestions from ponder → present for acceptance

Ask:
> Any new experiments to try this sprint?

Remind them experiments are 1-sprint trials — evaluate in the ponder.

## Step 7: Identify Carry-overs

Surface incomplete items from the previous sprint:
> These didn't get done last sprint:
> - {item 1}
> - {item 2}
>
> Carry forward, drop, or rescope?

## Step 8: Write Sprint Plan

Read `occasions.md` from the sanctum directory for any notable events this week.

Create `YYYY-wkNN-sprint.md` in the sanctum directory:

```markdown
---
type: sanctum/sprint
tags:
  - sanctum
  - sanctum/sprint
  - domain/AREA1
  - domain/AREA2
  - domain/AREA3
date: YYYY-MM-DD
up: "[[YYYY-MM-chronicle]]"
prev: "[[YYYY-wkPP-sprint]]"
next: "[[YYYY-wkNN+1-sprint]]"
---

# Sprint wkNN — YYYY-MM-DD → YYYY-MM-DD

## Notable Events
{from occasions.md — birthdays, holidays, reminders this week}

## Active Domains (N/3)
1. #domain/AREA — Goal: specific deliverable
2. #domain/AREA — Goal: specific deliverable
3. #domain/AREA — Goal: specific deliverable

## Stretch
- #domain/AREA — Stretch goal description

## Standards (from [[kaizen]])
- {locked-in standard 1}
- {locked-in standard 2}

## Habits
- emoji Habit: N/N target
- emoji Habit: N/N target {append " (calibrated)" for any habit currently shrunk}

## Experiments
- [ ] Experiment description (from [[YYYY-wkPP-ponder]])

## Carried Over
- From [[YYYY-wkPP-sprint]]: item description
```

## Step 9: Final Check

> **Sprint wkNN locked in.**
> - {N} active domains, {N} stretch
> - {N} habits tracked
> - {N} experiments running
> - Notable: {events this week}
>
> Start the week with `/daily` tomorrow morning. Go get it.

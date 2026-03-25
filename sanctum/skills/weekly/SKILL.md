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

Read `10 - Sanctum/north-stars.md` and `10 - Sanctum/backlog.md`.

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

Ask:
> What habits are you tracking this sprint? Give me the habit and the target (e.g., "walk dogs 5/7").

Carry forward habits from last sprint by default. Flag if a habit has been failing:
> "You've hit {habit} only {N}% of the time over the last 3 sprints. Adjust the target or
> recommit?"

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

Read `10 - Sanctum/occasions.md` for any notable events this week.

Create `10 - Sanctum/YYYY-wkNN-sprint.md`:

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

## Habits
- emoji Habit: N/N target
- emoji Habit: N/N target

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

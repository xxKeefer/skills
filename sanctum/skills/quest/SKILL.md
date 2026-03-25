---
name: quest
description: >
  Map an actionable route to achieve a north star — milestones, resources, practice schedule,
  knowledge outputs. Use when user says "quest", "map the route", "how do I get there", "plan
  the goal", or has just set a north star via /smart-goal.
---

# Quest

Map the route from where the user is now to their north star. Be a blend of blunt accountability
partner and encouraging mentor — challenge unrealistic timelines, celebrate thoughtful planning.

## Step 1: Identify the North Star

`<user-input>` may contain a domain name or north star reference.

Read `10 - Sanctum/north-stars.md` to find the active north star for the domain.

If no domain given or no active north star found, ask:

> Which north star are we mapping a quest for? Give me a domain name, or run `/smart-goal` first
> to set one.

Check if a quest file already exists (`10 - Sanctum/quest-<domain>.md`). If so:

> There's already a quest for #domain/AREA. Update it, or start fresh?

## Step 2: Assess Starting Point

Ask the user:

> Where are you right now with #domain/AREA? What do you already know, have, or have done?

Use `/grill-it` mechanics to get an honest assessment. Push back on both overconfidence and
underestimation. This grounds the milestones in reality.

## Step 3: Map Milestones

Break the north star into 3–5 milestones. Each milestone should be:
- **Demo-able** — a visible deliverable or capability
- **Sequential** — each builds on the last
- **Time-bound** — target sprint week

Present them:

> **Quest: {north star goal}**
>
> - **M1 — {name}** (by wkNN): {deliverable}
> - **M2 — {name}** (by wkNN): {deliverable}
> - **M3 — {name}** (by wkNN): {deliverable}
>
> Does this path make sense? Too aggressive? Too slow?

Iterate until the user agrees. Challenge if milestones are too vague or if the timeline doesn't
add up to the north star's target date.

## Step 4: Identify Resources

Ask:

> What resources will help you get there? Courses, books, people, tools, references?

Suggest resources if the user is unsure. Draw on:
- Existing backlog items for the domain
- Common learning paths for the skill area
- The user's preferred learning style (courses → notes → build something)

## Step 5: Define Practice Schedule

Ask:

> How often can you realistically work on this per sprint? Be honest — overcommitting here is
> how goals die.

Push for a concrete cadence:
- Number of sessions per sprint
- Minimum session length
- Specific days if helpful

Cross-check against the user's current sprint load. If they're already running 3 active domains,
flag the time pressure.

## Step 6: Define Knowledge Outputs

Ask:

> What artifacts will you produce along the way? Notes, essays, tools, sessions run?

Knowledge outputs serve two purposes:
- Evidence of progress for `/chronicle`
- Reusable reference material in the vault

Link them as wikilinks to expected future notes.

## Step 7: Write the Quest File

Create `10 - Sanctum/quest-<domain>.md` with:

```markdown
---
type: sanctum/quest
tags:
  - sanctum
  - sanctum/quest
  - domain/AREA
aliases:
  - quest AREA
up: "[[north-stars]]"
---

# Quest: {north star goal}

**North Star**: {full SMART goal statement}
**Domain**: #domain/AREA

## Milestones
{from Step 3}

## Resources
{from Step 4}

## Practice Schedule
{from Step 5}

## Knowledge Outputs
{from Step 6}

## Progress Log
| Sprint | Milestone | Notes |
|---|---|---|
```

Update `10 - Sanctum/north-stars.md` — set the Quest column for this domain to `[[quest-AREA]]`.

## Step 8: Suggest Next Steps

> Quest mapped. Next:
> - `/vault` — add supporting tasks to the backlog
> - `/weekly` — commit this domain to your next sprint
> - Start working — the first milestone is {M1 name} by wk{NN}

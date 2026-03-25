---
name: smart-goal
description: >
  Grill the user through SMART goal setting for any life domain. Produces a concrete, measurable,
  time-bound north star. Use when user says "smart goal", "set a goal", "new north star", activates
  a new domain, or needs help defining what "done" looks like.
---

# Smart Goal

Grill the user through defining a SMART north star for a domain. Be a blend of blunt accountability
partner and encouraging mentor — challenge vague goals, celebrate clarity.

## Step 1: Identify the Domain

`<user-input>` may contain a domain name (e.g., "philosophy", "climbing", "japanese").

If no domain is given, ask:

> What domain are we setting a north star for? Name an area of your life you want to commit to.

Read `10 - Sanctum/north-stars.md` and `10 - Sanctum/backlog.md` to check:
- Does this domain already have an active north star? If so, flag it: "You already have an active
  north star for #domain/AREA — do you want to replace it, or pick a different domain?"
- Are there existing backlog items for this domain? Surface them as context.

## Step 2: Grill Through SMART

Walk through each letter one at a time. Do not move to the next until the current one is solid.
Use `/grill-it` mechanics — be relentless, challenge vague answers, push for precision.

### S — Specific
> What exactly do you want to accomplish in #domain/AREA?

Push back on vague answers:
- "Get better at X" → "Better how? What would someone observe if you succeeded?"
- "Learn X" → "Learn it to what level? What could you do that you can't do now?"
- "Be more X" → "What specific behaviour or output would demonstrate that?"

### M — Measurable
> How will you know you've achieved this? What's the concrete evidence?

Push for observable outcomes:
- Artifacts produced (essays, tools, notes, sessions run)
- Streaks or frequency targets
- External validation (stars, users, feedback)
- Skills demonstrated (can do X that you couldn't before)

### A — Achievable
> Is this realistic given your current commitments and the time you can dedicate?

Check against:
- Current active domain count (WIP limit of 3)
- The user's existing sprint load
- Whether prerequisite knowledge or resources exist
- Time horizon vs scope

If it seems overambitious, say so directly. Suggest scoping down rather than setting up to fail.

### R — Relevant
> Why does this matter to you right now? How does it connect to who you're trying to become?

This isn't about filtering — it's about deepening commitment. When the user articulates *why*,
they're more likely to follow through. Surface connections to other domains if they exist.

### T — Time-bound
> By when? Give me a target date.

Push for a specific date, not "sometime this year." Help calibrate:
- Break the goal into rough milestones to sanity-check the timeline
- If the date is too aggressive, flag it
- If the date is too far out, suggest an intermediate milestone

## Step 3: Confirm the Goal

Present the final SMART goal as a single clear statement:

> **North Star for #domain/AREA:**
> "{Goal statement}" by {YYYY-MM-DD}
>
> **Evidence of completion:** {measurable criteria}
>
> Lock this in?

Iterate until the user confirms.

## Step 4: Write to North Stars

Read `10 - Sanctum/north-stars.md`. Add a row to the Active table:

| Domain | Goal | Target Date | Quest | Status |
|---|---|---|---|---|
| #domain/AREA | Goal statement | YYYY-MM-DD | — | 🔄 |

If the domain is new, also add a section header to `10 - Sanctum/backlog.md`:

```markdown
## Domain Name #domain/area
- [ ] Goal statement ⭐ [[north-stars]]
```

## Step 5: Suggest Next Steps

> North star locked in. Next:
> - `/quest AREA` — map the route (milestones, resources, practice schedule)
> - `/vault` — add supporting backlog items for this domain
> - `/weekly` — commit this domain to your next sprint

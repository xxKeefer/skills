---
name: reflect
description: >
  Evening reflection. Appends to the daily file with what you learned, what went well, what's
  next, and friction points. Use when user says "reflect", "evening check-in", "end of day",
  "what did I learn", or wraps up their day.
---

# Reflect

Evening reflection. Appends to the same daily file created by `/daily`. Conversational —
ask questions, don't just present a template. Be encouraging about wins, direct about friction.

## Step 1: Find the Daily File

`<user-input>` may contain:
- A **date** (e.g., "reflect monday", "reflect 2026-03-24") — target that day
- A **file path** — target a specific file
- **Nothing** — target today

Find `10 - Sanctum/YYYY-wkNN-day.md`. If the file doesn't exist:
> No daily file for today. Run `/daily` first, or should I create a minimal one and go straight
> to reflection?

Read the file. Check if the Reflect section is already filled — if so:
> Reflection already exists for today. Update it, or leave it?

## Step 2: Review the Day

Read the Today section to see what was planned (chores are nested within it).

Ask:
> How did today go? What got done, what didn't?

Listen to the response. Don't interrogate — this should feel like a debrief, not a grilling.

## Step 3: Walk Through Reflection

Ask each section conversationally, one at a time. Adapt based on what the user says.

### What I learned
> What did you learn today? Could be technical, personal, about your process — anything.

If they say "nothing", gently push: "Nothing at all? Not even something small about how you
work or what you noticed?"

### What went well
> What went well today?

Celebrate genuine wins. Connect to sprint goals or north stars when relevant:
> "That's {milestone} progress on your #domain/AREA quest — nice."

### What is next
> What's carrying into tomorrow?

This feeds into tomorrow's `/daily`. Note unfinished tasks, next steps, things to follow up on.

### Friction
> Any friction today? Things that slowed you down, frustrated you, or felt harder than they
> should?

This is the most important section for the coaching system. Friction entries get aggregated
by `/ponder` and drive experiment suggestions.

If the user mentions friction that's come up before (check recent daily files if accessible):
> "This is the {N}th time you've flagged {friction}. That's a pattern. Want to try an experiment
> to address it this sprint?"

## Step 4: Write to Daily File

Read the existing daily file. Append to or update the Reflect section:

```markdown
## 🪞 Reflect

### What I learned
- {from conversation}

### What went well
- {from conversation}

### What is next
- {from conversation}

### ⚠ Friction
- {from conversation}
```

Preserve all existing content in the file (chores, tasks, blockers). Only write to the Reflect
section.

## Step 5: Close Out

> **Day reflected.**
> {Brief encouraging note — acknowledge effort, connect to bigger picture if natural}
>
> See you tomorrow with `/daily`. Rest well.

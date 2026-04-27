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

Locate the sanctum directory per the journal domain's discovery convention, then find `YYYY-wkNN-day.md` within it. If the file doesn't exist:
> No daily file for today. Run `/daily` first, or should I create a minimal one and go straight
> to reflection?

Read the file. Check if the Reflect section is already filled — if so:
> Reflection already exists for today. Update it, or leave it?

## Step 2: Review the Day

Read the Today section to see what was planned (chores are nested within it). Also read the
`## 🌱 Today's kaizen` section if present — this is the morning intent to evaluate.

Ask:
> How did today go? What got done, what didn't?

Listen to the response. Don't interrogate — this should feel like a debrief, not a grilling.

## Step 2.5: Close the One-Day PDCA

If the daily file has a `## 🌱 Today's kaizen` line with a real intent (not `skipped`), surface
it and ask:

> Your morning intent was: "{intent}". How did it land — worked, partial, or dropped?

Record the outcome by appending an `**Outcome:** worked | partial | dropped — short note` line
beneath the intent in the daily file. If the morning intent was `skipped`, skip this step.

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

If the user mentions friction that's come up before (scan recent daily files in the sanctum for
similar Friction entries — at least the last 3-5 days):

> "This is the {N}th time you've flagged {friction}. Let's run a quick 5 Whys."

Then walk through five `Why?` prompts, one at a time, each building on the previous answer. Stop
early if the root cause becomes obvious before five. Record the chain in the daily file's
Friction section as a nested block:

```markdown
- {friction summary}
  - **Why 1:** {answer}
  - **Why 2:** {answer}
  - **Why 3:** {answer}
  - **Root cause:** {plain statement}
  - **Counter-measure:** {smallest possible next action}
```

Also append the same 5 Whys block to `kaizen.md` under the `## 5 Whys Log` section with a dated
heading: `### YYYY-MM-DD -- {friction label}`.

### Tiny improvement
> One tiny improvement you noticed today? Could be the kaizen intent paying off, or something
> serendipitous. Skip-able.

If the user names one, append a row to `kaizen.md` under `## Improvement Log`:

| Date | Domain | Tiny improvement | Triggered by |
|---|---|---|---|
| YYYY-MM-DD | #domain/AREA (best guess from context, or blank) | one-line description | morning intent / friction / serendipity |

If they skip, do nothing — the row is optional.

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

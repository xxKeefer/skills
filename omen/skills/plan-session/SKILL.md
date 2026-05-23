---
name: plan-session
description: >
  Plan the next game session. Synthesises campaign state -- canon, character arcs, NPC schemes,
  recent sessions -- against the DM's rough direction to pitch compelling session concepts. Produces
  lean outlines with detail on demand. Use when user says "plan session", "plan next game", "what
  should happen next", or wants to prep an upcoming session.
---

# Plan Session

Help the DM design a compelling, gamified session by synthesising the full campaign state into
actionable pitches and outlines.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Get the DM's Direction

`$ARGUMENTS` may contain:

- A rough direction ("I want to push KD's arc forward", "time for consequences from session 2")
- A game type preference ("something light", "big dramatic moment")
- Nothing -- ask:

> What's on your mind for the next session? Rough direction, character focus, vibe -- anything.

## Step 3: Deep Read the Campaign State

Read broadly across the campaign to build a full picture. All of:

- **Canon timeline** (`lore/_cannon.md`) -- recent events and unresolved threads
- **Recent session logs** (`logs/`) -- what just happened, how it ended, player feedback/questions
  if recorded
- **Character progressions** (`characters/`) -- where each PC is at, recent spotlight history,
  active goals and motives
- **Player index** (`lore/_players.md`) -- character motives and relationships
- **NPC index** (`lore/_npcs.md`) and standalone NPC lore files -- active schemes, checklists,
  unresolved plans
- **Places** (`lore/_places.md`) and standalone location files -- environments with untapped
  potential
- **Blurb** (`blurb.md`) -- campaign tone and genre

### What to look for

- **Spotlight debt** -- which PCs haven't been central recently? Infer from the narrative in
  session logs and character progressions, not from counting sessions
- **Ripe NPC plans** -- which NPC checklist items are ready to fire or collide with PC goals?
- **Unresolved tensions** -- cliffhangers, unanswered questions, simmering conflicts
- **Cross-over opportunities** -- where do separate character arcs intersect naturally through
  NPC schemes or shared stakes?
- **Resolved arcs** -- has a PC's current tension just wrapped up, making space for another PC
  to step into the spotlight?
- **Pacing** -- was the last session heavy or light? What does the table need next?

## Step 4: Pitch 3-4 Options

Present 3-4 pitches. Each pitch is 2-3 sentences covering:

- **What happens** -- the core narrative situation
- **Who's in the spotlight** -- primary PC(s) and which NPCs drive the action
- **Why now** -- what makes this the right moment for this story beat
- **Suggested game type** -- Transition, Continuation, Fork, Climax, or Reflect
- **Suggested act structure** -- a brief shape (e.g. "3-act: cold open into investigation,
  confrontation, fallout" or "4-act: quiet build, reveal, scramble, cliffhanger")

### Pitch variety

Offer a **mix** of:

- Different narrative threads as the session focus
- Different approaches to the same thread
- Different game types and pacing

### Creative priorities (in order)

1. **Compelling narrative** -- above all, the story must be engaging
2. **NPC-driven beats** -- stories powered by NPC motivations and PC backstory payoffs are prized
3. **Cross-over opportunities** -- moments where separate character arcs collide or interweave
4. **PC spotlight rotation** -- shift focus to the PC whose arc is most ripe, not just whoever is
   "due"
5. **Ensemble progression** -- even background PCs should move forward in small ways
6. **Act structure variety** -- break predictability. Don't default to the same shape every session

### Act structure suggestions

Don't pick from a fixed menu -- let the story dictate the shape. Some possibilities:

- **3-act** -- setup, confrontation, resolution. Clean and punchy
- **4-act** -- hook, rising tension, climax, denouement. Room to breathe
- **5-act** -- hook, test, investigation, climax, resolution. Full dramatic arc
- **Cold open + 2** -- drop in mid-action, then play out consequences
- **Slow burn** -- 2 long scenes with mounting pressure, no release until next session
- **Parallel threads** -- cut between two groups/storylines converging
- **Bottle episode** -- single location, single pressure, character-driven

Format:

> **Pitch 1: {Title}**
> {2-3 sentences}
> *Type: {game type} | Shape: {act structure}*
>
> **Pitch 2: {Title}**
> ...

Then ask:

> Pick one, combine elements, or redirect?

## Step 5: Generate Outline

Once the DM picks or combines, generate a scene-by-scene skeleton using the chosen act structure.

Each scene:

```markdown
### Scene {N}: {Title}

**Purpose:** {one sentence -- what this scene accomplishes narratively}
**Core question:** {the dramatic question this scene poses to the players}
**Exit cue:** {what triggers the transition to the next scene}
```

Keep it lean. No guardian, beats, or skill checks at this level.

Present the outline and ask:

> Outline for **{session title}**. Want to drill into any scene?

## Step 6: Detail on Demand

When the DM asks to flesh out a scene, expand it to full prep:

```markdown
### Scene {N}: {Title}

**Purpose:** {what this scene accomplishes}
**Location/Situation:** {where and what's happening when the scene starts}
**Guardian/Obstacle:** {what stands in the players' way}

**Must-hit beats:**
- {beat 1}
  - *Fumble:* {what happens on a bad roll}
  - *Success:* {what happens on a good roll}
  - *Critical:* {what happens on an exceptional roll}
- {beat 2}
  - ...

**Core question:** {dramatic question}
**Exit cue:** {transition trigger}
```

Only generate detail for scenes the DM asks about. Don't over-prep.

## Step 7: Create the Session Log File

Once the DM is satisfied, offer to scaffold the session log file:

> Want me to create the log file in `logs/`?

If yes, create the file with proper frontmatter and the outline content:

```yaml
---
tags:
  - omen/<campaign>
up: "[[log]]"
prev: "[[previous-session]]"
next:
campaign: <campaign>
group: <Group>
type: session-log
episode: "{session title}"
blurb: "{one-line teaser}"
---
```

Include the outline scenes under a `## Scenes` section. Leave `## Plot`, `## Questions`, and
`## Reflections` sections empty for post-game use.

---
name: make-blurb
description: >
  Generate a spoiler-free hype blurb from an unplayed session's planning notes. Reads DM-only
  planning, distills a teaser paragraph that builds anticipation without revealing secrets. Use when
  user says "make blurb", "write a teaser", "hype the next session", or has planning notes ready
  for an upcoming game.
---

# Make Blurb

Write a short hype paragraph for an upcoming session -- spoiler-free, evocative, builds
anticipation.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Session Planning

`$ARGUMENTS` may contain:

- A path or wikilink to an unplayed session log with planning notes
- Nothing -- check `logs/` for the latest session file and confirm it's unplayed

Read the session log file. This will contain DM-only planning: plot beats, NPC intentions, secret
reveals, encounter setups.

## Step 3: Read Campaign Context

Read `blurb.md` to match the campaign's established tone and voice.

Read the last few entries in `lore/_cannon.md` to understand where the story left off.

## Step 4: Identify What's Safe to Tease

Classify the planning content:

- **Safe** -- tensions already visible to players, unresolved cliffhangers, character goals in
  play, locations they're heading to
- **Spoiler** -- hidden NPC motives, secret reveals, surprise encounters, plot twists, anything
  the players don't yet know

The blurb draws ONLY from safe material.

## Step 5: Draft the Blurb

Write a single paragraph (3-5 sentences) that:

- Matches the campaign's genre and tone
- References the current narrative tension without resolving it
- Hints at stakes without revealing outcomes
- Uses character names and locations the players already know
- Reads like a TV episode teaser or back-of-book blurb
- Ends on a hook

## Step 6: Present for Review

> **Blurb for {session}:**
>
> {the blurb}
>
> Safe to share with players? Edit or approve.

The DM must sign off -- they know what's truly safe to reveal.

## Step 7: Append to Canon

Add the approved blurb to `lore/_cannon.md` under a heading:

```markdown
### Upcoming -- {Session Reference}

{blurb}
```

## Step 8: Confirm

> **Blurb posted.** Added to {campaign} canon as upcoming teaser.

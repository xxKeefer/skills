---
name: make-summary
description: >
  Create a narrative summary from a completed session log. Turns session notes into a 1-3 paragraph
  story retelling and appends it to _cannon.md. Use when user says "make summary", "write the
  story", "summarise the session", or wants a narrative recap of a completed game.
---

# Make Summary

Turn a completed session into a short narrative retelling.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Session Log

`$ARGUMENTS` may contain:

- A path or wikilink to a completed session log
- A session number -- find the matching file in `logs/`
- Nothing -- find the most recent session and confirm it's complete

Read the session log file in full. If the session hasn't been played yet, say so and suggest
`/make-blurb` instead.

## Step 3: Read Campaign Context

Read `blurb.md` to match the campaign's genre and voice.

Read recent entries in `lore/_cannon.md` to understand the narrative flow leading into this
session.

## Step 4: Write the Summary

Craft a 1-3 paragraph narrative retelling that:

- Reads like prose fiction, not a play-by-play
- Matches the campaign's genre and tone (cyberpunk noir, high fantasy, space opera -- whatever
  fits)
- Covers the key beats in chronological order
- Uses character names naturally -- both PCs and NPCs
- Weaves in `[[wikilinks]]` for NPCs, places, and organisations
- Captures the emotional weight of pivotal moments
- Ends on whatever note the session ended on -- cliffhanger, resolution, quiet beat

Keep it tight. Three paragraphs maximum. This is a recap, not a novelisation.

## Step 5: Present for Review

> **Summary of {session}:**
>
> {the narrative}
>
> Reads right? Edit or approve.

## Step 6: Append to Canon

Replace any existing "Upcoming" blurb for this session in `lore/_cannon.md` (if `/make-blurb` was
used earlier), or append after the last entry:

```markdown
### {Session Reference} -- {Date}

{narrative summary}
```

## Step 7: Confirm

> **Summary posted.** {session} narrative added to {campaign} canon.

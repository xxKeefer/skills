---
name: log-cannon
description: >
  Extract canon events from a session log and append them to the campaign's timeline. Reads a
  session log, identifies narratively significant events, and adds timestamped entries to _cannon.md
  with wikilinks. Use when user says "log canon", "update the timeline", "add to cannon", or after
  logging a session.
---

# Log Cannon

Extract significant narrative events from a session and append them to the campaign's canon
timeline.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Session Log

`$ARGUMENTS` may contain:

- A path or wikilink to a session log file
- A session number -- find the matching file in `logs/`
- Nothing -- list recent sessions and ask which one to process

Read the session log file in full.

## Step 3: Read Existing Canon

Read `lore/_cannon.md` to understand:

- The current timeline and latest entries
- Existing wikilinks and naming conventions used in this campaign
- What's already been logged (avoid duplicates)

## Step 4: Read Existing Indexes

Scan `lore/_npcs.md` and `lore/_places.md` to know which NPCs and places already have entries.
This ensures wikilinks point to known names and use established aliases.

## Step 5: Extract Canon Events

Analyse the session log for events that are **narratively significant** -- moments that change the
state of the world, alter relationships, reveal secrets, or create consequences. Not every action
is canon.

Signals of canon weight:

- **Decisions** that close off alternatives (Fork/Climax game types are inherently canon-heavy)
- **Reveals** -- information the players or characters didn't have before
- **Relationship shifts** -- alliances formed, betrayals, deaths, new enemies
- **World-state changes** -- locations destroyed, factions moved, power shifts
- **Character milestones** -- goals achieved, trauma, transformation

For each event, draft a terse dot-point entry:

- Use `[[wikilinks]]` for every NPC, place, organisation, or concept that has or should have a
  lore entry
- Keep entries factual and chronological
- Write from an omniscient narrator perspective, not a player perspective
- One line per event -- dense but readable

## Step 6: Present for Review

Show the extracted events to the user before writing:

> **Canon from {session}** -- {N} events extracted:
>
> - event 1
> - event 2
> - ...
>
> Add all, edit, or drop any?

## Step 7: Append to Canon

Add the approved events to `lore/_cannon.md` under a heading for this session:

```markdown
### {Session Reference} -- {Date}
- event 1
- event 2
```

Append after the last existing session block.

## Step 8: Confirm

> **Canon updated.** {N} events from {session} added to {campaign} timeline.

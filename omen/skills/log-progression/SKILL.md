---
name: log-progression
description: >
  Update player character progression files from a session log. Analyses the session for narratively
  significant moments per character and appends to their individual files. Use when user says "log
  progression", "update characters", "character arcs", or after logging a session.
---

# Log Progression

Analyse a session log and update each player character's progression file with narratively
significant events.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Session Log

`$ARGUMENTS` may contain:

- A path or wikilink to a session log file
- A session number -- find the matching file in `logs/`
- Nothing -- list recent sessions and ask which one to process

Read the session log file in full.

## Step 3: Read the Player Index and Character Files

Read `lore/_players.md` to get the roster -- names, players, motives.

Read each character's individual file in `characters/`. If a character file doesn't exist yet,
note it for creation.

## Step 4: Analyse the Session per Character

For each player character, extract moments that carry **narrative weight** for that specific
character. Not every event matters to every character.

Signals of progression:

- **Relationship changes** -- new ally, new enemy, trust gained or lost, bonding moments
- **Decisions with consequences** -- choices that shape who the character is becoming
- **Goal progress** -- steps toward or away from their stated motive
- **Reveals** -- learning something that changes the character's understanding
- **Trauma or growth** -- moments that challenge or reinforce the character's identity
- **Off-screen significance** -- events the character doesn't know about but that affect them
  (mark these clearly, e.g. "Unknown to {character}:")

Keep entries terse. One line per moment, factual, with wikilinks.

## Step 5: Present for Review

> **Progression from {session}:**
>
> **{Character 1} ({Player}):**
> - moment 1
> - moment 2
>
> **{Character 2} ({Player}):**
> - moment 1
>
> Add all, edit, or drop any?

## Step 6: Update Character Files

### Existing character files

Append a new section under a session heading:

```markdown
### {Session Reference} -- {Date}
- moment 1
- moment 2
```

Append after the last existing session block.

### New character files

If a character file doesn't exist in `characters/`, create it:

```markdown
---
tags:
  - omen/<campaign>/pc
campaign: <campaign>
group: <Group>
type: pc
up: "[[_players]]"
---

# {Character Name}

**Player:** {player name}
**Motive:** {main motive from _players.md}

## Progression

### {Session Reference} -- {Date}
- moment 1
- moment 2
```

## Step 7: Confirm

> **Progression updated.** {N} characters updated from {session}.

# Omen -- TTRPG Campaign Management

Creative skills for TTRPG campaign logging, lore management, and session planning. All artifacts
live in **setting directories** within the user's Obsidian vault.

## Campaign Discovery

Skills must never hardcode campaign paths. Instead:

1. Scan `07-omen/` in the vault for directories containing setting state files (`log.md` plus a
   `lore/` subdirectory with `_cannon.md`).
2. If multiple campaigns found, ask the user which one.
3. If none found, ask the user where the campaign lives.

## Setting Folder Structure

Each campaign setting follows this layout:

```
<setting>/
  index.md          # Map of content and how-to guide
  blurb.md          # Tone-setting overview (genre, plot, characters)
  log.md            # Session index table
  lore/
    _cannon.md      # Chronological timeline of canon events
    _npcs.md        # NPC index (alphabetical headings)
    _places.md      # Location index (alphabetical headings)
    _players.md     # Player character index
  logs/             # Individual session log files
  characters/       # Individual player character progression files
  lore/             # Standalone lore files (spun off from indexes)
  assets/           # Images and non-text media
```

## Frontmatter Schema

Lore files use this YAML frontmatter:

```yaml
tags:
  - omen/<campaign>/<type>    # e.g. omen/crown/npc
aliases: []                    # alternative names
related: []                    # wikilinks to related entries
blurb: ""                      # one-line description
campaign: <campaign>           # setting name (e.g. crown)
group: <Group>                 # display group (e.g. Crown)
type: <type>                   # npc | location | lore | session-log
```

Session log files use:

```yaml
tags:
  - omen/<campaign>
up: "[[log]]"
prev: "[[previous-session]]"  # or None
next: "[[next-session]]"      # or empty
campaign: <campaign>
group: <Group>
type: session-log
```

## Game Types

Sessions are classified by narrative function:

| Type | Purpose |
|---|---|
| Transition | Set up, explore, define tensions. New chapters, wind-downs, plot turns |
| Continuation | Follow-on exploration and tension building |
| Fork | A dilemma -- players choose alignment, pushing narrative in a specific direction. Canon-defining |
| Climax | Highly dramatic scene bringing the story to a head. Canon-defining |
| Reflect | Light-hearted filler for character bonding |

## Lore Type Templates

### NPC

Structured sections: appearance, voice, role/faction, What They Want, What They Can Do, How
They'll Act, What They Fear, What's Their Plan (with checklist items for background plotting).

### Location

Structured sections: What/Where/Who overview, What It Looks Like, What Happens Here, What Else Is
Here (sub-locations, companies, narrative description).

### Organization / Concept

Narrative paragraphs with heavy wikilinks. Aliases in frontmatter for cross-referencing.

## Wikilinks

All cross-references use Obsidian `[[wikilink]]` syntax. When creating or updating entries, link
to any NPC, place, organization, or canon event that exists in the setting. Use aliases where
natural (e.g. `[[Alfred Technologies Conglomerate|ATC]]`).

## Tone

Co-DM and creative collaborator. Match the campaign's genre and voice when writing narrative
content. Keep index entries terse and factual. Keep lore files rich and evocative.

## Skills

| Skill | Purpose |
|---|---|
| `/log-session` | Log a game session to the session index |
| `/log-cannon` | Extract canon events from a session log |
| `/log-npcs` | Catalog NPCs from a session log |
| `/log-place` | Catalog places from a session log |
| `/log-progression` | Update character arcs from a session log |
| `/make-lore` | Spin off a heading into a standalone lore file |
| `/make-blurb` | Generate hype blurb from session planning |
| `/make-summary` | Narrative summary from a completed session |
| `/plan-session` | Plan a new session by game type |
| `/scaffold-setting` | Bootstrap a new campaign setting with standard structure |
| `/doctor-setting` | Migrate an existing campaign to the standard structure |

## Dependencies

Omen skills are self-contained. No dependency on other domains.

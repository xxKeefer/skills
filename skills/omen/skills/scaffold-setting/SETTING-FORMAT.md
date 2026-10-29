# Setting Format

The contract for an omen campaign setting. Omen skills read this file before they touch a setting.

## Campaign Discovery

Find the campaign with `/discover-vault-directory *omen/* holding log.md lore/_cannon.md`.

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

## File Templates

The standard files of a new setting. Replace each `{placeholder}` with the setting's values.

### index.md

```markdown
# {Setting Name}

Map of content for the {Setting Name} campaign.

## Structure

| File/Folder | Purpose |
|---|---|
| [[index]] | This file |
| [[log]] | Session index with summary |
| [[blurb]] | Setting overview -- genre, tone, plot |
| [[_cannon]] | Chronological timeline of canon events |
| [[_npcs]] | NPC index |
| [[_places]] | Location index |
| [[_players]] | Player character index |
| /assets | Images and non-text media |
| /logs | Individual session log files |
| /lore | Standalone lore files |
| /characters | Player character progression files |
```

### blurb.md

```markdown
---
tags:
  - omen/{campaign-tag}
campaign: {campaign-tag}
group: {Group}
type: blurb
---

{Genre/tone description if provided, otherwise a placeholder:}
{A tone-setting paragraph that illuminates the setting, genre, player characters, and main plot.}
```

### log.md

```markdown
| Date | Session | Type | Summary |
|------|---------|------|---------|
|      |         |      |         |
```

### lore/_cannon.md

```markdown
---
tags:
  - omen/{campaign-tag}/cannon
campaign: {campaign-tag}
group: {Group}
type: cannon
---

# {Setting Name} -- Canon Timeline
```

### lore/_npcs.md

```markdown
---
tags:
  - omen/{campaign-tag}/npc-index
campaign: {campaign-tag}
group: {Group}
type: npc-index
---

# NPCs
```

### lore/_places.md

```markdown
---
tags:
  - omen/{campaign-tag}/place-index
campaign: {campaign-tag}
group: {Group}
type: place-index
---

# Places
```

### lore/_players.md

If player characters were provided:

```markdown
---
tags:
  - omen/{campaign-tag}/player-index
campaign: {campaign-tag}
group: {Group}
type: player-index
---

# Players

| Player | Character | Main Motive |
|--------|-----------|-------------|
| {player} | **{character}** | {motive} |
```

If no PCs provided, generate the table with an empty row.

### characters/{Character Name}.md

One file per player character:

```markdown
---
tags:
  - omen/{campaign-tag}/pc
campaign: {campaign-tag}
group: {Group}
type: pc
up: "[[_players]]"
---

# {Character Name}

**Player:** {player name}
**Motive:** {main motive}

## Progression
```

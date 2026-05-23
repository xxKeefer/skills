---
name: make-lore
description: >
  Spin off an index heading into a standalone lore file. Takes an index file and a heading that has
  grown too large, creates a rich lore file in /lore with proper frontmatter, moves the content, and
  replaces the original with a wikilink. Use when user says "make lore", "spin off", "this entry is
  too big", or wants to promote an NPC/place to a full lore file.
---

# Make Lore

Promote an index entry into a standalone lore file.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Source

`$ARGUMENTS` may contain:

- An index file and heading name (e.g. `_npcs.md Akemi Sunshine`)
- Just a heading name -- search across `_npcs.md`, `_places.md`, `_cannon.md` for it
- Nothing -- ask what to spin off

Read the source index file. Locate the heading and all content under it.

## Step 3: Determine Lore Type

Infer from the source index:

| Source | Type | Template |
|---|---|---|
| `_npcs.md` | npc | NPC template |
| `_places.md` | location | Location template |
| `_cannon.md` | lore | Narrative lore |
| `_players.md` | pc | Character file (redirect to `characters/`) |

## Step 4: Gather Context

Read related entries across the campaign indexes to enrich the lore file:

- Cross-references in `_cannon.md` mentioning this entity
- Related NPCs or places that link to it
- Session logs where it appeared prominently

Present a summary of what you'll include:

> **Spinning off {name} into lore/{name}.md**
> - Source: {index file} ({N} paragraphs)
> - Cross-references found: {list}
> - Template: {type}
>
> Proceed?

## Step 5: Create the Lore File

Write `lore/{Name}.md` with frontmatter matching the campaign's schema:

```yaml
---
tags:
  - omen/<campaign>/<type>
aliases: []
related: []
blurb: ""
campaign: <campaign>
group: <Group>
type: <type>
---
```

Populate aliases from any known alternative names. Populate related from cross-references found.
Write a blurb -- one line capturing the essence.

### Body by type

**NPC:** Expand using the NPC template from CLAUDE.md -- appearance, voice, role/faction, What
They Want, What They Can Do, How They'll Act, What They Fear, What's Their Plan. Use existing
content as the foundation, flesh out where the source material supports it. Don't invent details
the campaign hasn't established.

**Location:** Expand using the Location template -- What/Where/Who, What It Looks Like, What
Happens Here, What Else Is Here. Same rule: flesh out from existing material, don't invent.

**Lore:** Narrative paragraphs with wikilinks. Organise chronologically or thematically as fits
the content.

## Step 6: Update the Source Index

Replace the content under the original heading with a wikilink to the new file:

```markdown
## {Name}

See [[{Name}]]
```

Keep the heading so the index remains scannable.

## Step 7: Confirm

> **Lore created.** `lore/{Name}.md` ({type}) -- source index updated with wikilink.

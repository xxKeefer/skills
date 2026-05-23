---
name: log-npcs
description: >
  Catalog NPCs from a session log into the campaign's NPC index. New NPCs get a heading with a
  summary. Existing NPCs get new information appended. Use when user says "log npcs", "update npcs",
  "catalog characters", or after logging a session.
---

# Log NPCs

Extract NPCs from a session log and update the campaign's `_npcs.md` index.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Session Log

`$ARGUMENTS` may contain:

- A path or wikilink to a session log file
- A session number -- find the matching file in `logs/`
- Nothing -- list recent sessions and ask which one to process

Read the session log file in full.

## Step 3: Read the NPC Index

Read `lore/_npcs.md` to understand:

- Which NPCs already have entries (by heading)
- The format and voice used for existing entries
- Alphabetical ordering of headings

Also check `lore/` for standalone NPC lore files -- if an NPC already has their own file, note it.

## Step 4: Extract NPCs from the Session

Identify every NPC that appeared, was mentioned, or was revealed in the session. For each:

- **Name** -- use the name as it appears in play. Note aliases
- **What happened** -- terse summary of their role in this session
- **New or existing** -- does this NPC already have a heading in `_npcs.md`?

Skip player characters -- they belong in `_players.md`.

## Step 5: Present for Review

> **NPCs from {session}:**
>
> **New:**
> - {NPC name} -- {one-line summary}
>
> **Updated:**
> - {NPC name} -- {what's new this session}
>
> Add all, edit, or drop any?

## Step 6: Update the Index

### New NPCs

Insert a new heading in `_npcs.md` in **alphabetical order** among existing headings:

```markdown
## {NPC Name}

{One-line summary of who they are and their role. Wikilink to related places, factions, or other
NPCs.}
```

### Existing NPCs

Append a new paragraph under the existing heading with the new information from this session.
Prefix with the session reference for traceability:

```markdown
**{Session Reference}:** {What happened with this NPC in this session.}
```

If an NPC has a standalone lore file in `lore/`, append there instead and note the wikilink under
the index heading if not already present.

## Step 7: Wikilink Hygiene

Ensure all NPC entries wikilink to:

- Places they're associated with
- Other NPCs they interact with
- Factions or organisations they belong to

Only link to entries that exist or will be created in this pass.

## Step 8: Confirm

> **NPCs updated.** {N} new, {M} updated in {campaign} index.

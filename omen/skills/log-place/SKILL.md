---
name: log-place
description: >
  Catalog places from a session log into the campaign's location index. New places get a heading
  with a summary. Existing places get new information appended. Use when user says "log places",
  "update locations", "catalog places", or after logging a session.
---

# Log Place

Extract locations from a session log and update the campaign's `_places.md` index.

## Step 1: Discover the Campaign

Follow the campaign discovery convention from the omen domain CLAUDE.md.

## Step 2: Identify the Session Log

`$ARGUMENTS` may contain:

- A path or wikilink to a session log file
- A session number -- find the matching file in `logs/`
- Nothing -- list recent sessions and ask which one to process

Read the session log file in full.

## Step 3: Read the Places Index

Read `lore/_places.md` to understand:

- Which places already have entries (by heading)
- The format and voice used for existing entries
- Alphabetical ordering of headings

Also check `lore/` for standalone location lore files -- if a place already has its own file, note
it.

## Step 4: Extract Places from the Session

Identify every location that was visited, mentioned, or revealed in the session. For each:

- **Name** -- use the name as it appears in play. Note aliases
- **What happened** -- terse summary of what occurred here or what was learned about it
- **New or existing** -- does this place already have a heading in `_places.md`?

Include locations at all scales -- districts, buildings, rooms, planets -- whatever the campaign
operates at.

## Step 5: Present for Review

> **Places from {session}:**
>
> **New:**
> - {Place name} -- {one-line summary}
>
> **Updated:**
> - {Place name} -- {what's new this session}
>
> Add all, edit, or drop any?

## Step 6: Update the Index

### New Places

Insert a new heading in `_places.md` in **alphabetical order** among existing headings:

```markdown
## {Place Name}

{One-line summary of what this place is and why it matters. Wikilink to related NPCs, factions, or
parent locations.}
```

### Existing Places

Append a new paragraph under the existing heading with new information from this session. Prefix
with the session reference:

```markdown
**{Session Reference}:** {What happened at or was revealed about this place.}
```

If a place has a standalone lore file in `lore/`, append there instead and note the wikilink under
the index heading if not already present.

## Step 7: Wikilink Hygiene

Ensure all place entries wikilink to:

- NPCs associated with the location
- Parent or child locations (e.g. district -> city)
- Factions or organisations operating there

Only link to entries that exist or will be created in this pass.

## Step 8: Confirm

> **Places updated.** {N} new, {M} updated in {campaign} index.

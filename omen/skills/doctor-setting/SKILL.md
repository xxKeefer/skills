---
name: doctor-setting
description: >
  Migrate an existing campaign to the standard omen setting structure. Audits the current state,
  creates missing files and directories, extracts content from hybrid files, generates indexes from
  standalone lore, and backfills canon from session logs. Phased with DM approval between each step.
  Use when user says "doctor setting", "fix my campaign", "migrate to standard", or has a messy
  setting folder that needs organising.
---

# Doctor Setting

Migrate an existing campaign to the standard omen setting structure. Works in phases -- audit,
structure, extract, review -- with DM approval between each.

## Step 1: Discover the Target

`$ARGUMENTS` may contain:

- A path to a campaign directory
- A campaign name -- search `07-omen/` for it
- Nothing -- list directories in `07-omen/` and ask which one to doctor

## Phase 1: Audit

Read the entire setting directory. For every file:

- Read its frontmatter (if any)
- Classify it: lore (npc/location/faction/concept), session log, player info, rules, asset, index,
  blurb, hybrid, or unknown
- Note its current location vs where it should live in the standard structure

### Report

Present a full gap analysis:

> **Audit: {Setting Name}**
>
> **Standard files:**
> | File | Status |
> |---|---|
> | index.md | {exists / missing} |
> | blurb.md | {exists / missing} |
> | log.md | {exists / missing} |
> | lore/_cannon.md | {exists / missing} |
> | lore/_npcs.md | {exists / missing} |
> | lore/_places.md | {exists / missing} |
> | lore/_players.md | {exists / missing} |
> | characters/ | {exists+populated / exists+empty / missing} |
> | logs/ | {exists+populated / exists+empty / missing} |
> | assets/ | {exists+populated / exists+empty / missing} |
>
> **Content found:**
> - {N} lore files ({breakdown by type})
> - {N} session logs
> - {N} hybrid files (need splitting)
> - {N} non-standard files (will be left as-is)
>
> **Frontmatter health:**
> - {N} files with complete frontmatter
> - {N} files with partial frontmatter (list missing fields)
> - {N} files with no frontmatter
>
> **Planned actions:**
> - Create: {list of files/dirs to create}
> - Split: {list of hybrid files to decompose}
> - Generate: {list of indexes to build from existing content}
> - Extract: {what to backfill from session logs}
> - Leave: {non-standard files staying put}
>
> Proceed to structuring phase?

## Phase 2: Structure

Create all missing directories and empty standard files. Use the same templates as
`/scaffold-setting` for file contents.

Infer `campaign`, `group`, and tag values from existing frontmatter in the setting. If
inconsistent, ask the DM which values to standardise on.

### Frontmatter normalisation

For every existing file, check and fix frontmatter:

- **Missing fields** -- add `tags`, `campaign`, `group`, `type`, `aliases`, `related`, `blurb`
  where absent
- **Inconsistent tags** -- normalise to `omen/{campaign}/{type}` pattern
- **Missing aliases** -- if the file content or other files reference this entity by alternative
  names, populate aliases
- **Missing related** -- scan for `[[wikilinks]]` in the file body and add referenced entities to
  the `related` field
- **Missing blurb** -- generate a one-line summary from the file content

Present changes per file:

> **Frontmatter fixes:**
>
> **{filename}:**
> - Added: `blurb: "{generated}"`
> - Added: `aliases: ["{alias1}", "{alias2}"]`
> - Fixed: `tags: omen/crown/npc` (was: missing)
>
> **{filename}:**
> - ...
>
> Apply all, edit, or skip any?

## Phase 3: Extract

Work through each extraction task sequentially, presenting results for approval.

### 3a: Split hybrid files

For files serving multiple purposes (e.g. a combined session log + player index):

1. Identify the distinct content blocks and their target destinations
2. Present the split plan:

> **Splitting: {filename}**
>
> - Player table + backstories -> `lore/_players.md` + individual files in `characters/`
> - Session index table -> `log.md`
> - Setting description -> `blurb.md` (if blurb.md is empty)
>
> The original file will be kept until you confirm deletion. Proceed?

3. Create the target files with proper frontmatter
4. For character files created in `characters/`, ensure frontmatter includes `up: "[[_players]]"`
   and wikilinks to related NPCs, places, and factions
5. After all splits confirmed, ask before removing the original:

> **{filename}** has been fully split. Delete the original? (y/n)

### 3b: Generate indexes from standalone lore files

Scan all files in `lore/` and build index entries grouped by type:

**For `_npcs.md`:**

Read every file with `type: npc`. For each, create an alphabetically ordered heading:

```markdown
## {NPC Name}

{blurb from frontmatter, or generate one from content}. See [[{NPC Name}]]
```

**For `_places.md`:**

Same pattern for files with `type: location`.

**For factions, concepts, and other lore types:**

These don't have a dedicated index. Ensure they're well-linked via `related` fields in
frontmatter and wikilinks in `_cannon.md` and other indexes.

Present the generated indexes:

> **Generated `_npcs.md`** -- {N} entries
> **Generated `_places.md`** -- {N} entries
>
> {preview of each}
>
> Approve, edit, or regenerate?

### 3c: Backfill canon from session logs

Read every session log in `logs/`. For each completed session (has a Plot section or equivalent
narrative content):

1. Extract narratively significant events (same criteria as `/log-cannon`)
2. Build a timeline entry per session

Present the full canon timeline:

> **Generated `_cannon.md`** -- {N} events across {M} sessions
>
> ### {Session 1} -- {Date}
> - event 1
> - event 2
>
> ### {Session 2} -- {Date}
> - event 1
>
> Approve, edit, or regenerate?

### 3d: Wikilink pass

After all content is in place, do a cross-referencing sweep:

1. For every file in `lore/`, `characters/`, and the index files:
   - Scan body text for entity names that match other files (including aliases)
   - Add `[[wikilinks]]` where missing
   - Update `related` frontmatter fields with bidirectional references
2. Ensure every standalone lore file is linked from at least one index

Present a summary of links added:

> **Wikilink pass:** {N} links added across {M} files
>
> Notable new connections:
> - {entity A} <-> {entity B} (found in {context})
> - ...
>
> Apply?

## Phase 4: Review

Present the final state of the setting:

> **Doctor complete: {Setting Name}**
>
> **Files created:** {N}
> **Files updated:** {N} (frontmatter fixes + wikilinks)
> **Files split:** {N} -> {M}
> **Files left as-is:** {N}
>
> **Structure:**
> ```
> {tree view of final directory}
> ```
>
> **Frontmatter coverage:** {percentage} of files fully tagged
> **Wikilink density:** {N} cross-references across {M} files
>
> Anything to adjust, or are we good?

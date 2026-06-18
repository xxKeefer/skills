---
name: scaffold-setting
description: >
  Generate the folder structure and initial files for a new campaign setting. Creates all
  directories, index files, and templates so the DM can start logging immediately. Use when user
  says "new campaign", "scaffold setting", "set up a new game", or wants to start a fresh setting.
---

# Scaffold Setting

Bootstrap a new campaign setting with the standard omen folder structure.

## Step 1: Detect Starting Point

Check `$ARGUMENTS` for a path or setting name. Then inspect the target directory:

- **Empty or non-existent** -- fresh scaffold. Go to Step 1a.
- **Contains a single `blurb.md`** (or similar seed file) -- inflate from blurb. Go to Step 1b.
- **Contains existing content** -- this is a migration, not a scaffold. Redirect to
  `/doctor-setting`.

### Step 1a: Gather Setting Details (fresh)

Ask if not provided:

> What's the setting called? Give me a name and a one-line pitch.

Collect:

- **Setting name** -- used for the directory name (kebab-case) and display name
- **Campaign tag** -- short lowercase slug for frontmatter (e.g. `crown`, `thread`)
- **Group name** -- display name for the `group` frontmatter field (e.g. `Crown`, `Thread`)
- **Genre/tone** -- for the blurb and to set the creative direction

Optionally ask:

> Any player characters to set up? Names, players, motives -- or skip for now.

### Step 1b: Inflate from Blurb (seed file found)

Read the seed file. Extract whatever is available:

- **Setting name** -- from the filename, frontmatter, or first heading
- **Campaign tag / group** -- from frontmatter if present, otherwise derive from the setting name
- **Genre/tone/plot** -- from the file body
- **Characters** -- if the blurb mentions PCs, extract names, players, motives
- **NPCs, places, factions** -- if the blurb names them, queue them for index entries and
  placeholder lore files

Present what was extracted:

> **Inflating from {filename}:**
>
> - Setting: {name}
> - Campaign tag: {tag}
> - Genre: {inferred genre}
> - Characters found: {list or "none"}
> - Entities mentioned: {NPCs, places, factions or "none"}
>
> I'll scaffold the full structure and seed indexes with these. Proceed?

The seed file's content becomes `blurb.md` (with proper frontmatter added if missing).

## Step 2: Confirm Structure

Present what will be created:

> **Scaffolding: {Setting Name}**
>
> ```
> 07-omen/{setting-name}/
>   index.md
>   blurb.md
>   log.md
>   lore/
>     _cannon.md
>     _npcs.md
>     _places.md
>     _players.md
>   logs/
>   characters/
>   assets/
> ```
>
> Proceed?

## Step 3: Create the Directory Structure

Create all directories under the vault's `07-omen/` path:

- `{setting-name}/`
- `{setting-name}/lore/`
- `{setting-name}/logs/`
- `{setting-name}/characters/`
- `{setting-name}/assets/`

## Step 4: Generate Files

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

## Step 5: Scaffold Characters (if provided)

For each player character, create a file in `characters/`:

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

## Step 6: Seed from Blurb (inflate mode only)

If entities were extracted from the seed file in Step 1b:

- **NPCs mentioned** -- add a heading + one-line blurb to `_npcs.md` for each
- **Places mentioned** -- add a heading + one-line blurb to `_places.md` for each
- **Factions/orgs mentioned** -- create placeholder lore files in `lore/` with frontmatter and a
  one-line description pulled from the blurb context

Wikilink everything that references each other.

## Step 7: Confirm

> **{Setting Name} scaffolded.** {N} files created in `07-omen/{setting-name}/`.
> Ready to run `/plan-session` or start logging.

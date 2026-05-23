# Plan: Omen Domain Skills

Build the omen domain's skill suite -- TTRPG campaign logging, lore management, and session
planning workflows for Obsidian.

## Context

- **Example setting** (`notes/02-omen/dev/example setting/index.md`) defines the ideal folder
  structure and skill wishlist
- **Crown setting** (`notes/02-omen/crown/`) is a live cyberpunk campaign with rich lore,
  structured frontmatter, and session logs -- the reference implementation
- **Omen plugin** (`code/skills/omen/`) exists as an empty shell ready for skills

## Step 1: Establish the Omen CLAUDE.md and campaign discovery convention

**What:** Define the omen domain's architecture in CLAUDE.md -- campaign discovery (analogous to
journal's sanctum discovery), frontmatter schema (tags, aliases, related, blurb, campaign, group,
type), file naming conventions, the setting folder structure, and the skill catalog. This is the
foundation all skills build on.
**Files:** `omen/CLAUDE.md`
**Done when:** CLAUDE.md documents discovery convention, frontmatter schema, game types, and skill
catalog

## Step 2: `log-session` -- Log a game session to the session index

**What:** First skill. Takes a session log file as input, extracts date/type/summary, appends a row
to the setting's `log.md` index table. Establishes the campaign discovery pattern in practice.
**Files:** `omen/skills/log-session/SKILL.md`
**Done when:** Skill can locate a campaign's log.md and append a session entry

## Step 3: `log-cannon` -- Extract canon events from a session

**What:** Reads a session log, identifies significant narrative events, appends timestamped entries
to `_cannon.md` with wikilinks to NPCs, places, and other lore.
**Files:** `omen/skills/log-cannon/SKILL.md`
**Done when:** Skill extracts canon events and appends them with proper wikilinks

## Step 4: `log-npcs` -- Catalog NPCs from a session

**What:** Reads a session log, identifies NPCs mentioned. New NPCs get a heading in `_npcs.md`
(alphabetical) with a summary. Existing NPCs get new information appended under their heading.
**Files:** `omen/skills/log-npcs/SKILL.md`
**Done when:** Skill creates/updates NPC entries in the index with proper formatting

## Step 5: `log-place` -- Catalog places from a session

**What:** Same pattern as `log-npcs` but for locations in `_places.md`.
**Files:** `omen/skills/log-place/SKILL.md`
**Done when:** Skill creates/updates place entries in the index

## Step 6: `log-progression` -- Update character arcs from a session

**What:** For each player character in `_players.md`, analyze the session log for narratively
significant moments and append to their individual character file in `/characters`.
**Files:** `omen/skills/log-progression/SKILL.md`
**Done when:** Skill updates character files with session-relevant progression notes

## Step 7: `make-lore` -- Spin off a heading into a standalone lore file

**What:** Takes an index file and a heading that's grown too large. Creates a new lore file in
`/lore` with proper frontmatter (matching crown's pattern), moves content there, replaces the
original with a wikilink.
**Files:** `omen/skills/make-lore/SKILL.md`
**Done when:** Skill creates lore file with correct frontmatter and replaces source content with a
link

## Step 8: `make-blurb` -- Generate hype blurb from session planning

**What:** Reads an unplayed session log's planning notes, writes a spoiler-free teaser paragraph to
`_cannon.md`. DM planning stays hidden.
**Files:** `omen/skills/make-blurb/SKILL.md`
**Done when:** Skill produces a spoiler-free blurb from DM-only planning notes

## Step 9: `make-summary` -- Narrative summary from a completed session

**What:** Takes a completed session log, writes a 1-3 paragraph narrative retelling, appends to
`_cannon.md`.
**Files:** `omen/skills/make-summary/SKILL.md`
**Done when:** Skill produces a story-style summary from session notes

## Step 10: `plan-session` -- Plan a new session by game type

**What:** Given a game type (Transition, Continuation, Fork, Climax, Reflect), reads recent canon,
active character arcs, and unresolved threads to help the DM plan the next session. Creates a new
log file with planning notes and proper frontmatter.
**Files:** `omen/skills/plan-session/SKILL.md`
**Done when:** Skill scaffolds a new session log with DM planning structured by game type

## Ordering Rationale

1. CLAUDE.md first -- all skills depend on the conventions it establishes
2. `log-session` first skill -- simplest, establishes discovery pattern
3. `log-cannon` through `log-progression` -- core logging pipeline, each building on the pattern
4. `make-*` skills -- depend on having logged data to work with
5. `plan-session` last -- reads everything the other skills produce

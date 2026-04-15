# Wiki

Raw note intake, knowledge management, and vault indexing for Obsidian. Skills in this domain run
from the Obsidian vault root. "Vault" = the Obsidian vault.

## Vault Conventions

### INDEX.md Files

Every vault directory gets an `INDEX.md` maintained by agents:

```markdown
---
description: One-line purpose of this directory
conventions: brief notes on naming, structure rules
---

# {Directory Name}

{2-3 sentences on what belongs here and what doesn't}

## Structure

{Description of any subdirectory conventions}
```

### Canonical Knowledge Frontmatter

```yaml
---
up: "[[broader-topic]]"
related: ["[[child-1]]", "[[child-2]]"]
also: ["[[sibling]]", "[[cross-cutting]]"]
aliases: ["alt name 1", "alt name 2"]
tags: ["knowledge", "topic1", "topic2"]
---
```

- `up` -- single wikilink to a more general parent document
- `related` -- wikilinks to subtopics split off from this doc (down)
- `also` -- lateral connections: siblings, cross-cutting knowledge
- `aliases` -- alternative names for Obsidian search/linking
- `tags` -- flat, per vault tag taxonomy (`#knowledge` + topic tags)
- No `source` in frontmatter -- sources live at the bottom of the document under a `## Sources`
  heading
- No inheritance -- each new doc starts with fresh frontmatter

### Absorb-and-Split Algorithm (Wikipedia Model)

1. Find the most relevant existing knowledge doc for the raw note's topic
2. Insert content under the most relevant heading
3. If that section exceeds ~500 lines, split the largest subsection into a new doc:
   - New doc gets its own fresh frontmatter
   - Parent doc keeps a brief summary + `Main article: [[new-doc]]` wikilink where content was
   - Parent adds new doc to `related` in frontmatter
   - New doc sets `up: [[parent]]`
4. Apply recursively -- if the new doc itself is too large, split again
5. If the overall document exceeds ~2000 lines, look for the largest L1/L2 heading to split out
6. If no existing knowledge doc matches, create a new one with a declarative, descriptive name
   (follow existing naming conventions in the knowledge folder)

### Classification Routing

| Classification | Destination | Action |
|---|---|---|
| Knowledge (reference material) | `03-knowledge/` | Absorb into existing doc or create new |
| Fleeting/personal | `04-notes/` | File to directory root |
| Project-related | `05-projects/` | File to directory root |
| Work-related | `00-raw/hitl/` | Never auto-file to work -- HITL only |
| Low confidence | `00-raw/hitl/` | Agent unsure of classification |

### Source Tracking

While a raw note is being processed, sources appear at the bottom of the knowledge doc:

```markdown
## Sources

- https://some-url.com -- external reference
- conversation, 2026-04-15 -- agent session
```

If the raw note is deleted after full absorption, strip its reference from sources. External URLs
and other sources persist.

## Dependencies

Wiki skills reference `/grill-it` from the `primitives` plugin for HITL coaching mechanics. Both
plugins must be installed.

## Skills

| Skill | Purpose |
|---|---|
| `/intake-raw` | AFK batch -- process all notes in `00-raw/`, classify, route, absorb-and-split |
| `/intake-it` | HITL single note -- process one `00-raw/hitl/` note with human guidance |
| `/standardise-frontmatter` | AFK -- normalise knowledge note frontmatter to canonical shape |
| `/edit-article` | HITL -- structural and prose editing for Obsidian notes |
| `/rebuild-index` | AFK -- generate or rebuild INDEX.md for a given directory |

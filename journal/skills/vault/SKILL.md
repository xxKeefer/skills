---
name: vault
description: >
  Manage the life backlog and north stars. View, add, remove, reprioritise items across all
  domains. Use when user says "vault", "backlog", "show my goals", "add to backlog", "what's
  on my plate", or wants to manage what they're working toward.
---

# Vault

The vault is the single source of truth for everything the user wants to do across all life
domains. Be a blend of blunt accountability partner and encouraging mentor.

## Step 1: Parse Input

`<user-input>` may contain:
- A **domain filter** (e.g., "vault se", "vault philosophy") — show only that domain
- An **action** (e.g., "add", "remove", "reprioritise")
- **Nothing** — show the full backlog overview

Locate the sanctum directory per the journal domain's discovery convention. Read `backlog.md` and `north-stars.md` from it.

## Step 2: Present Current State

Show a summary:

> **Vault Overview**
>
> **Active North Stars** ({N}/{total domains}):
> {list from north-stars.md with status and target dates}
>
> **Backlog** ({N} items across {N} domains):
> {condensed view — domain headers with item counts, north star items highlighted}
>
> **Dormant domains** (no activity in 3+ sprints):
> {list with last active sprint — push back hard: "You said X mattered — what changed?"}

If a domain filter was given, show only that domain's items in full.

## Step 3: Handle Actions

### Add items
Ask:
> What domain and what's the item?

If the domain doesn't exist yet, create a new section in `backlog.md`:
```markdown
## Domain Name #domain/area
- [ ] Item description
```

Use `#domain/<area>` tags and `[[wikilinks]]` where appropriate.

### Remove items
Confirm before removing:
> Remove "{item}" from #domain/AREA? This can't be undone.

### Complete items
Move the item to checked and add sprint reference:
```markdown
- [x] Item description ✅ [[YYYY-wkNN-ponder]]
```

### Reprioritise
Reorder items within a domain section. Items closer to the top are higher priority.

### Promote to north star
If the user wants to make a backlog item a north star:
> This needs to be a SMART goal. Run `/smart-goal AREA` to define it properly.

### Shelve a domain
Mark all items in a domain as shelved. Add a note:
```markdown
## Domain Name #domain/area (shelved wkNN)
```

Remove any active north star for that domain from `north-stars.md` and note the reason.

## Step 4: Write Changes

Update `backlog.md` and/or `north-stars.md` in the sanctum directory with changes.

Show what changed:
> **Updated vault:**
> - Added: {items}
> - Removed: {items}
> - Completed: {items}
> - Reprioritised: {domain}

## Step 5: Coach Observations

After any vault interaction, surface relevant observations:
- Domains with no north star: "No north star for #domain/AREA — want to set one?"
- Domains with many items but no activity: "Lots of ideas for AREA but no sprint commitment lately."
- Overloaded domains: "AREA has {N} items. Consider pruning or splitting into sub-domains."
- Completed north stars without a replacement: "You achieved your #domain/AREA goal! Ready for a new one?"

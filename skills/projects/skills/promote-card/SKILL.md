---
name: promote-card
description: >
  Promote a bare board card into one fully-specced ticket note with a phased plan that /do-next
  runs one phase at a time. Use when the user says "promote this card", "spec this card", "turn
  this into a ticket", or points at a dot point on a project board that needs scoping before work
  starts.
---

# Promote Card

Turn a bare card -- a dot point with no wikilink -- into one ticket note. The card is the handle.
The ticket is the handoff that `/do-next` runs against, one phase per session.

If the project's repo has an Obsidian Kanban tracker configured, this writes exactly what
`docs/agents/issue-tracker.md` describes.

## Step 1: Locate the Card

Find the project (from `$ARGUMENTS` or ask) and its board, `{slug}.kanban.md`.

Prefer a block link over free text -- obsidian-kanban's "Copy link to card" gives
`[[{slug}.kanban#^{blockid}]]`, an ID Obsidian itself generates collision-free. If `$ARGUMENTS`
contains one, grep the board for a line ending in `^{blockid}` -- that match is unambiguous, skip
straight to Step 2.

Otherwise grep the board for the card's text, taken verbatim from what the user gave you. If
nothing matches exactly, ask the user to paste the literal line -- or better, the block link -- rather
than guessing at a fuzzy match. If more than one line matches, ask which column it's in. If the
matched line is already a wikilink (`[[...]]`), it's already been promoted -- stop and point at the
existing note.

Once matched, that line (text and any trailing `^{blockid}`) is how this run refers to the card for
the rest of the skill -- don't paraphrase it.

## Step 2: Grill the Spec

Invoke `/grill` on the card's text to develop it into a full spec:

- **What** -- the concrete change, in enough detail to slice into phases.
- **Why** -- how it serves the project's mission.
- **Acceptance criteria** -- observable, checkable conditions.
- **Constraints and out-of-scope** -- anything that bounds the approach.

Resolve everything in-session. No open questions carried into the note.

## Step 3: Match Board Tags

Read the card's own inline tags, if any, and the board's tag vocabulary (`tag-colors` /
`tag-sort` in the `%% kanban:settings %%` block). Carry over the card's existing tags by default;
confirm with the user if the grilled spec suggests a different or additional fit (e.g. the card had
no tags but is clearly `#techdebt`).

If the confirmed tag isn't already in the board's `tag-colors`/`tag-sort` arrays, it's a new
project-specific tag -- ask the user for a text/background colour (or propose a sensible default)
and append one entry to each array in the `%% kanban:settings %%` block. Append only: never reorder
or replace the canonical entries already there (see BOARD-FORMAT.md's Universal Project Tags rule).

## Step 4: Plan the Phases

Slice the spec into numbered phases. Each phase is one vertical slice, sized so `/implement` can
run it end to end in one session. Give each phase a done line the agent can check. A spec that fits
in one session gets a plan with one phase.

**Done when:** each acceptance criterion is reached by a phase, and each phase has a checkable done
line.

## Step 5: Write the Ticket Note

Write one note, `tasks/{Card Title}.md`, per [NOTE-FORMAT.md](../new-project/NOTE-FORMAT.md). Tags:
the matched tags. Context: the grilled spec. Acceptance Criteria: the spec's criteria. Plan: the
phases from Step 4. Progress: empty.

The filename is the note's permanent handle from here on -- Obsidian resolves the wikilink by it.

**Done when:** the note holds every section of the ticket format, and every phase from Step 4.

## Step 6: Update the Board

Replace the original card line (the exact text matched in Step 1) with the ticket's wikilink and
matched tags: `- [ ] [[Card Title]] #tag`. Keep a trailing `^{blockid}` if the original line had
one -- other notes may already link to that anchor. Leave every other card as it is.

**Done when:** the original card line links to the ticket note, and no other card changed.

## Step 7: Confirm

Report the ticket note, its phases, the board line changed, and the `/do-next @{note path}` command
that runs phase 1.

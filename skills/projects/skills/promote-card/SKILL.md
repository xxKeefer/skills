---
name: promote-card
description: >
  Promote a bare board card into a fully-specced, implementable unit of work. Grills the card into
  a spec, splits the spec into one-shot tickets sized for /implement, and writes both as task notes
  the board wikilinks out to. Use when the user says "promote this card", "spec this card", "turn
  this into tickets", or points at a dot point on a project board that needs scoping before work
  starts.
---

# Promote Card

Turn a bare card -- a dot point with no wikilink -- into a spec and the tickets that implement it.
The card is the handle; the ticket is the oneshotable handoff `/implement` runs against.

The vault-native counterpart to `developer:to-spec`/`to-tickets`: those assume the investigation
already happened in-conversation and just publish it; this one starts from a jotted thought with no
code context yet and grills it first. Both land in the same place -- if the project's repo has an
Obsidian Kanban tracker configured, this writes exactly what `docs/agents/issue-tracker.md`
describes.

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

- **What** -- the concrete change, in enough detail to slice into independent pieces.
- **Why** -- how it serves the project's mission.
- **Acceptance criteria** -- observable, checkable conditions.
- **Constraints and out-of-scope** -- anything that bounds the approach.

Resolve everything in-session. No open questions carried into the note.

## Step 3: Match Board Tags

Read the card's own inline tags, if any, and the board's tag vocabulary (`tag-colors` /
`tag-sort` in the `%% kanban:settings %%` block). Carry over the card's existing tags by default;
confirm with the user if the grilled spec suggests a different or additional fit (e.g. the card had
no tags but is clearly `#techdebt`).

## Step 4: Decide the Split

Judge whether the spec is already one-shot -- a scope `/implement` could run end to end without
further clarification. If yes, skip the spec note: this promotes straight to a single ticket (Step
5), no parent.

Otherwise, split the spec into 1..N tickets, each independently implementable and self-contained.
Don't over-split -- a spec that only needs one slice gets one ticket with a spec parent, not several
artificial ones.

## Step 5: Write the Notes

Per [NOTE-FORMAT.md](../new-project/NOTE-FORMAT.md):

- **Spec note** (only if Step 4 produced one) -- `tasks/{Card Title}.md`. Tags: `spec` + matched
  tags. Context: the grilled spec. Acceptance Criteria: a wikilink per ticket, checked off as
  tickets close.
- **Ticket notes** -- `tasks/{Ticket Title}.md` each. Tags: matched tags (never `spec`). Context:
  opens with a wikilink back to the spec note, if there is one, then the ticket's own scope.
  Acceptance Criteria: that ticket's one-shot slice.

Each note's filename is its permanent handle from here on -- Obsidian resolves the wikilink by it.

## Step 6: Update the Board

Append, never delete or rewrite a card someone else added:

- Replace the original card line (the exact text matched in Step 1) with the spec's wikilink and
  matched tags: `- [ ] [[Card Title]] #spec #tag`. If Step 4 skipped the spec, replace it with the
  single ticket's wikilink instead. Keep a trailing `^{blockid}` if the original line had one --
  other notes may already link to that anchor.
- Add one new card per ticket in the same column, each `- [ ] [[Ticket Title]] #tag`.

## Step 7: Confirm

Report what was written: the spec (if any), each ticket, and the board lines changed.

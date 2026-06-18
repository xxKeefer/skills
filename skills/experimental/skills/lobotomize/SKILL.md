---
name: lobotomize
description: >
  Review the agent's persistent memories in a table and purge the ones that have outlived their
  use. Surfaces each memory's name, age, and reason for existing, then deletes the ones the user
  multi-selects — scrubbing the index and any backlinks so nothing dangles. Use when the user says
  "lobotomize", "purge memories", "clean up memory", "forget stuff", or "prune what you remember".
---

# Lobotomize

Prune the agent's long-term memory. Show every memory with its age and purpose, let the user pick
which to forget, then hard-delete the chosen ones and clean up after them.

## Step 1: Locate the memory store

Find the memory directory for the current project — the folder holding one-fact-per-file memories
and a `MEMORY.md` index. Enumerate every memory file in it, excluding `MEMORY.md` itself.

- No memory directory, or it holds only `MEMORY.md` (or nothing) → tell the user there's nothing to
  prune and stop.

**Done when:** you have the path to the store and the list of memory files.

## Step 2: Gather each memory's facts

Read every memory file and the `MEMORY.md` index. For each memory collect:

- **Name** — the frontmatter `name:` slug (fall back to the filename).
- **Age** — the file's last-modified timestamp expressed relative to today (e.g. `3d`, `2w`, `5mo`).
- **Why it exists** — a one-line gloss of its purpose, drawn from the frontmatter `description:`,
  the `MEMORY.md` hook, and the body (`type`, the `**Why:**` line for feedback/project memories).

Do not guess a purpose you can't support from the file — say `unclear` and let that be a signal
for purging.

**Done when:** every memory has a name, an age, and a purpose line.

## Step 3: Render the table

Delegate to `/tabular-analysis` to present the comparison. Pass the memories as the topic and these
exact pipe-delimited columns:

```
Memory | Age | Why it exists
```

Order rows oldest-first — stale memories are the likeliest purge candidates and should lead.

**Done when:** the table is shown, one row per memory.

## Step 4: Let the user choose what to purge

Present the memory names as a **multi-select** — the user ticks the ones to forget. Nothing is
selected by default; an empty selection means "keep everything."

If the selection tool caps the number of options, batch the names across several prompts rather
than silently dropping any. Always offer a "purge nothing" escape.

- Empty selection → report that nothing was purged and stop.

**Done when:** you have the confirmed set of memory names to delete.

## Step 5: Purge and scrub

This is a hard delete — git history and the user's backups are the only safety net. For each
selected memory:

1. **Delete** the memory file.
2. **De-index** — remove its line from `MEMORY.md`.
3. **Unlink** — find `[[name]]` backlinks to it in surviving memories and strip or neutralise them
   so no reference dangles.

**Done when:** every selected memory is gone and no trace of it remains in the store.

## Step 6: Report

List what was purged (name + why) and what was scrubbed (index lines removed, backlinks cleaned).
Keep it to a few lines — the deletions are the deliverable, not prose.

**Done when:** the user can see exactly what was forgotten.

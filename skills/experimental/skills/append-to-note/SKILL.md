---
name: append-to-note
description: >
  Append something from the current conversation to an existing note in the user's Obsidian
  notes, in that note's own style. Use when the user says "add this to my X note" or "append this
  to <note>".
argument-hint: "<path to an existing note>"
---

# Append to a Note

Distill something worth keeping from the conversation and add it to the note that the user names,
in that note's style. To capture a fresh note in the vault inbox instead, use `/take-a-note`.

## Step 1: Decide What to Capture

The content is whatever the user wants noted — usually the most recent useful thing in the
conversation: a how-to, a finding, an exact command, a decision and its reasoning.

- If it's obvious from context, proceed.
- If two or more things could be meant, **ask** which one in a single line before continuing.

Distill it into clean, note-ready markdown. Write a reference entry, not a transcript — drop the
back-and-forth, keep the durable facts. Tables, fenced code, and callouts are encouraged where
they sharpen it.

**Done when:** you have one idea, distilled into note-ready markdown.

## Step 2: Resolve the Note

- `$ARGUMENTS` holds a path to an existing note: use it.
- No path, or the path does not exist: ask "Which note?" in one line, then wait.

**Done when:** you have the path of one note that exists.

## Step 3: Learn the Note

1. Read the **full** target note.
2. Learn its conventions before writing a word: frontmatter shape, heading style (emoji
   prefixes?), table formatting, callout types in use (e.g. `[!dont]`, `[!brain]`), list and
   quote style.
3. Find the **most relevant insertion point** — the section the content belongs under. If none
   fits, add a new section at the end with a heading that matches the note's heading style.

**Done when:** you can name the insertion point and the conventions that the addition follows.

## Step 4: Checkpoint, then Insert

1. Draft the addition in the note's *exact* style. The existing note wins over any default of
   yours.
2. **Checkpoint** — show the user the proposed location and the rendered addition. A curated note
   is higher stakes than a raw capture, so wait for approval. Adjust on feedback.
3. Insert with a targeted edit. Leave all surrounding content byte-for-byte intact.

**Done when:** the user approved the addition, and it is in the note with all other content
unchanged.

## Principles

- **Match, don't impose.** The target note's style is law.
- **Distill, don't dump.** A note is a reference, not a conversation log.
- **Straight quotes only** — no smart quotes or unicode bullets (vault rule). Em dashes and emojis
  are fine.

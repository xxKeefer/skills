---
name: take-a-note
description: >
  Capture something from the current conversation into the user's Obsidian notes. With a file
  path, append it to the most relevant part of that note, matching the note's existing style.
  With no path, drop a fresh note into the vault's 00-notes/ for later triage. Use when the user
  says "take a note", "note this", "capture this", "jot this down", or "add this to my notes".
argument-hint: "[optional path to an existing note to append to]"
---

# Take a Note

Distill something worth keeping from the conversation and persist it. Two modes, decided by
whether `$ARGUMENTS` contains a file path.

## Step 1: Decide What to Capture

The content is whatever the user wants noted — usually the most recent useful thing in the
conversation: a how-to, a finding, an exact command, a decision and its reasoning.

- If it's obvious from context, proceed.
- If two or more things could be meant, **ask** which one in a single line before continuing.

Distill it into clean, note-ready markdown. Write a reference entry, not a transcript — drop the
back-and-forth, keep the durable facts. Tables, fenced code, and callouts are encouraged where
they sharpen it.

## Step 2: Pick the Mode

- `$ARGUMENTS` contains a path to an existing note → **Append mode** (Step 3)
- No path → **Capture mode** (Step 4)

## Step 3: Append Mode

1. Read the **full** target note.
2. Learn its conventions before writing a word: frontmatter shape, heading style (emoji
   prefixes?), table formatting, callout types in use (e.g. `[!dont]`, `[!brain]`), list and
   quote style.
3. Find the **most relevant insertion point** — the section the content belongs under. If none
   fits, add a new section at the end with a heading that matches the note's heading style.
4. Draft the addition in the note's *exact* style. The existing note wins over any default of
   yours.
5. **Checkpoint** — show the user the proposed location and the rendered addition. Adjust on
   feedback; otherwise confirm.
6. Insert with a targeted edit. Leave all surrounding content byte-for-byte intact.

## Step 4: Capture Mode (no path)

1. Locate the vault: scan the home directory for a folder containing `.obsidian/`; the first
   match is the vault root. If none is found, warn the user and stop.
2. Write to `{vault}/00-notes/{slug}-{YYYYMMDD}.md` — a short kebab-case slug plus the date,
   matching how existing 00-notes captures are named.
3. Frontmatter + the `#raw` tag (vault inbox convention):
   ```yaml
   ---
   source: {conversation | https://... | tool:name}
   created: {YYYY-MM-DD}
   ---

   #raw
   ```
4. Body = the distilled content. Keep it atomic (one idea). Use `[[wikilinks]]` and `#tags` where
   natural.
5. Print the full path written.

## Principles

- **Match, don't impose.** In append mode the target note's style is law.
- **Distill, don't dump.** A note is a reference, not a conversation log.
- **Straight quotes only** — no smart quotes or unicode bullets (vault rule). Em dashes and emojis
  are fine.
- **Append mode confirms; capture mode just writes.** Editing a curated note is higher stakes than
  dropping a raw note for later triage.

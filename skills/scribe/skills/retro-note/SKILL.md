---
name: retro-note
description: >
  Append a thought from the current conversation to the user's rolling retro log in their Obsidian
  vault, as a dated bullet, so it surfaces at the next retro. Use when the user says "retro note",
  "note for retro", "log this for retro", "add to retro", or wants to park an observation for the
  next retrospective.
---

# Retro Note

Capture one observation worth raising at the next retro and append it to the retro log. Fast,
low-ceremony — the inverse of distilling a curated note. One thought per invocation.

## Step 1 — Distill the thought

The content is whatever the user wants logged — usually the most recent useful thing in the
conversation: a friction point, a win, a decision, a "we should change this".

- If it's obvious from context, proceed.
- If two or more things could be meant, **ask** which one in a single line before continuing.

Reduce it to a **short description** — one line, the kind a person scans in a standup. Strip the
back-and-forth. If (and only if) detail would be lost, draft one or two **indented sub-bullets**
under it. Most entries are a single line with no sub-bullets.

## Step 2 — Locate the retro log

1. Find the vault root the way `/discover-vault-directory` does. If there is no vault, warn the
   user and stop.
2. Find the log note: search the vault for a note whose name contains `retro` (case-insensitive).
   - One match → that's the log.
   - Several → ask which one in a single line.
   - None → create `{vault}/retro-log.md` with an `# Retro Log` heading.

## Step 3 — Append the entry

Add the entry as a new bullet at the **end** of the log's list:

```
- **{DD-MMM}:** {short description}
  - {optional detail}
  - {optional detail}
```

- `{DD-MMM}` is **today's** date, e.g. `23-Jun`.
- Indent sub-bullets two spaces under the dated bullet.
- Append only — leave every existing line byte-for-byte intact.
- Match the log's existing style if it already has entries (the note wins over this template).

## Step 4 — Report

Print the entry you appended and the note path. No checkpoint — this is a raw capture for later
triage, not a curated note.

## Principles

- **One thought per call.** Don't batch unrelated observations into one entry.
- **Scannable, not complete.** The bullet is a memory hook for the retro, not a record of the
  discussion.
- **Straight quotes only** — no smart quotes or unicode bullets (vault rule).
- **Append, never rewrite.** The log accumulates until the user clears it after a retro.

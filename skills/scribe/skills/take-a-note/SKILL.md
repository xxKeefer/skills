---
name: take-a-note
description: >
  Capture something from the current conversation as a fresh note in the vault's notes inbox, for
  later triage. Use when the user says "take a note", "note this", "capture this", or "jot this
  down".
---

# Take a Note

Distill something worth keeping from the conversation into a raw note in the vault inbox. To add
it to an existing note instead, use `/append-to-note`.

## Step 1: Decide What to Capture

The content is whatever the user wants noted — usually the most recent useful thing in the
conversation: a how-to, a finding, an exact command, a decision and its reasoning.

- If it's obvious from context, proceed.
- If two or more things could be meant, **ask** which one in a single line before continuing.

Distill it into clean, note-ready markdown. Write a reference entry, not a transcript — drop the
back-and-forth, keep the durable facts. Tables, fenced code, and callouts are encouraged where
they sharpen it.

**Done when:** you have one idea, distilled into note-ready markdown.

## Step 2: Write the Note

Write without a checkpoint. A raw note waits for `/triage-notes`, so the user reviews it there.

1. Find the inbox with `/discover-vault-directory *notes`.
2. Write to `{inbox}/{slug}-{YYYYMMDD}.md` — a short kebab-case slug plus the date,
   matching how existing inbox captures are named.
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

**Done when:** the note is in the inbox with its frontmatter and `#raw` tag, and you printed its
path.

## Principles

- **Distill, don't dump.** A note is a reference, not a conversation log.
- **Straight quotes only** — no smart quotes or unicode bullets (vault rule). Em dashes and emojis
  are fine.

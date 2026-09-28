---
name: orwells-six
description: >
  Proof-read a document against Orwell's six rules from "Politics and the English Language" --
  stale figures, long words, cuttable words, passive voice, jargon, and the barbarism guardrail --
  proposing numbered findings for approval before any edit lands, ending with a table of every
  change. Use when the user says "orwell", "orwells six", "orwell's rules", or wants a document's
  prose tightened.
---

# Orwell's Six

One lens over one document: does each sentence say its thing in the fewest plain words? The rules
come from George Orwell's "Politics and the English Language" (1946). For all four lenses in
order, use `/proof-read`.

Hard rules:

- Preserve Obsidian syntax: frontmatter, wikilinks (`[[note]]`), callouts, tags, embeds.
- Never edit code blocks, tables, ASCII diagrams, or link targets.
- Preserve the author's voice: edit for clarity, not to rewrite in your own voice.
- A **term of art** survives: a word the document defines, or one the stated audience reads
  without friction (`idempotent`, `fail closed`). Name the survivors in the findings so the human
  can veto the exemption.

## Read

Resolve the target from the arguments: a file path, a note title to search for, or content in the
conversation. If none resolves, use **AskUserQuestion** to ask for one.

State the audience (from the arguments, or inferred) before the audit. It decides the terms of
art.

## Audit

Number every finding and group them by rule:

- **Rule 1** -- a metaphor, simile, or figure the reader has seen in print many times ("move the
  needle", "lets both sides win"). Replace it with the literal claim.
- **Rule 2** -- a long word where a short one does ("utilize" -> "use", "optionality" -> "the
  option").
- **Rule 3** -- every word that can come out ("explicitly out of scope", "in order to", "actual
  deliverable").
- **Rule 4** -- the passive where the active works and the actor is known.
- **Rule 5** -- a foreign phrase, scientific word, or jargon word with an everyday equivalent,
  minus the terms of art ("leverage" -> "use", "per se").
- **Rule 6** -- the guardrail: break any rule sooner than write something barbarous. Keep what a
  fix would make worse, and list each keep with its reason.

## Gate and apply

Gate with **AskUserQuestion**: apply all, pick findings by number, or stop.

Apply what was approved. Complete when every finding is applied or declined.

## Summary

One row per applied edit, Before/After truncated to the changed span:

| Rule | Location | Before | After |
| ---- | -------- | ------ | ----- |

Close with one line counting declined findings.

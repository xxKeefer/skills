---
name: asd-ste100
description: >
  Proof-read a document against ASD-STE100 Simplified Technical English -- words, verbs, sentences,
  punctuation, structure -- proposing numbered findings for approval in a chosen mode before any
  edit lands, ending with a table of every change. Use when the user says "ste", "asd-ste100",
  "simplified technical english", or wants a document made hard to misread for native and
  non-native readers.
---

# ASD-STE100

One lens over one document: can every reader, native or not, read each sentence one way only?
ASD-STE100 is the controlled-language spec that aerospace uses for maintenance docs. For all four
lenses in order, use `/proof-read`.

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

- **Words** -- one word with two meanings (flag "ships" meaning both "delivers in v1" and "is
  included"), one thing with two names, a long word with a short common one ("utilize" ->
  "use"), metaphor, idiom, and phrasal verbs ("spin up").
- **Noun clusters** -- over three words (proper names exempt).
- **Verbs** -- passive voice with a known actor ("two alternatives were rejected" -> "we rejected
  two"), a noun doing a verb's job ("perform an analysis" -> "analyze"), stacked auxiliaries
  ("may help to improve"), and "-ing" main verbs where a simple tense works.
- **Sentences** -- over 25 words (20 for instructions), more than one instruction, contractions,
  missing articles, and verbless fragments ("Result: ...", "No app code.").
- **Punctuation** -- semicolons, and em dashes as prose connectors (structural separators in
  glossaries and tables stay).
- **Structure** -- a paragraph with two topics or over six sentences, and a procedure that is not
  a numbered list of imperative steps with each condition before its command. A warning starts
  with the command, then gives the reason.

## Gate and apply

Gate with one **AskUserQuestion** call, two questions:

1. **Findings** -- apply all, pick by number, or stop.
2. **Mode** -- **STE-flavored** (recommended -- caps, actors, plain verbs, but the register
   survives), **strict** (every rule everywhere; reads like a spec), or **strict for reference
   sections only** (glossaries, procedures, delivery plans).

Apply what was approved in the chosen mode. Complete when every finding is applied or declined.

## Summary

One row per applied edit, Before/After truncated to the changed span:

| Rule | Location | Before | After |
| ---- | -------- | ------ | ----- |

Close with one line counting declined findings.

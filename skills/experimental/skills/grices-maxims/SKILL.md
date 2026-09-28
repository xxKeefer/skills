---
name: grices-maxims
description: >
  Proof-read a document against Grice's maxims -- Quantity, Quality, Relation, Manner, plus
  unintended implicature -- proposing numbered findings for approval before any edit lands, ending
  with a table of every change. Use when the user says "grice", "grices maxims", "what does this
  imply", or wants a document checked for what it says, leaves out, and implies.
---

# Grice's Maxims

One lens over one document: does each claim give the reader what they need, and nothing that
misleads? Grice's maxims ("Logic and Conversation", 1975) describe what a reader assumes a
cooperative writer does. Where the text breaks one, the reader infers a meaning the author may not
intend. For all four lenses in order, use `/proof-read`.

Hard rules:

- Preserve Obsidian syntax: frontmatter, wikilinks (`[[note]]`), callouts, tags, embeds.
- Never edit code blocks, tables, ASCII diagrams, or link targets.
- Preserve the author's voice: edit for clarity, not to rewrite in your own voice.
- Only the author can supply a missing fact or the evidence for a claim. Ask for it; never invent
  it.

## Read

Resolve the target from the arguments: a file path, a note title to search for, or content in the
conversation. If none resolves, use **AskUserQuestion** to ask for one.

Before the audit, state the audience (from the arguments, or inferred), the document's purpose in
one sentence, and what each section contributes to it. Every judgement calibrates to these three.

## Audit

Number every finding and group them by maxim:

- **Quantity (enough)** -- a claim the reader cannot act on without a missing fact, caveat, or
  condition.
- **Quantity (no more)** -- a sentence, aside, or section the audience does not need, or a point
  made twice.
- **Quality** -- a claim stated with more certainty than its evidence supports, or two claims that
  contradict each other. Offer three fixes: cite the evidence, soften the claim to match it, or
  cut it.
- **Relation** -- a sentence or paragraph that does not serve its section's contribution.
- **Manner** -- a term the audience does not know and the document does not define, a referent
  with two candidates ("this", "it"), a sentence with two readings, or steps out of the order the
  reader does them.
- **Implicature** -- what the text implies but the author likely does not mean: "some" read as
  "not all", "faster on Linux" read as "not faster elsewhere", "we did X and errors dropped" read
  as cause.

A **term of art** is not obscure: a word the document defines, or one the stated audience reads
without friction (`idempotent`, `fail closed`). Name the terms you exempted so the human can veto
the exemption.

## Gate and apply

Gate with **AskUserQuestion**: apply all, pick findings by number, or stop.

For an approved Quantity gap or Quality claim, ask the author for the fact first. If the author
has none, soften or cut instead.

Apply what was approved. Complete when every finding is applied or declined.

## Summary

One row per applied edit, Before/After truncated to the changed span:

| Maxim | Location | Before | After |
| ----- | -------- | ------ | ----- |

Close with one line counting declined findings.

---
name: proof-read
description: >
  Proof-read a document in three gated passes -- structural analysis, an ASD-STE100 pass, then
  Orwell's six rules -- each proposing findings for y/n approval before any edit lands, ending
  with a table of every change. Use when the user says "proof read", "proofread", or wants a
  document hardened for a mixed technical audience.
---

# Proof-Read

Three lenses over one document, strictly in order: **structure**, **STE**, **Orwell**. Each lens
proposes findings, the human gates them, then the edits land. A later lens edits only its
**delta** -- what earlier lenses could not see -- so nothing is reported or fixed twice.

Hard rules for every pass:

- Preserve Obsidian syntax: frontmatter, wikilinks (`[[note]]`), callouts, tags, embeds.
- Never edit code blocks, tables, ASCII diagrams, or link targets.
- Preserve the author's voice: edit for clarity, not to rewrite in your own voice.
- A **term of art** survives every lens: a word the document defines, or one the stated audience
  reads without friction (`idempotent`, `fail closed`). Name the survivors in each pass's
  findings so the human can veto the exemption.

## Read

Resolve the target from the arguments: a file path, a note title to search for, or content in the
conversation. If none resolves, use **AskUserQuestion** to ask for one.

Note the audience if the arguments state one; otherwise infer it and declare it in the Pass 1
analysis -- every later judgement calibrates to it.

## Pass 1: Structure

Build the model: thesis (one sentence), what each section contributes, a DAG of section
dependencies, gaps, and redundancy -- especially the same mechanics restated in two places. A
section must never reference a concept introduced later; propose a reorder if one does.

Present the analysis (thesis, section count, flow verdict, issues found), then gate with
**AskUserQuestion**: apply all, pick issues, or skip the pass.

Apply what was approved. The pass is complete when every issue is applied or declined.

## Pass 2: STE (ASD-STE100)

Audit against the STE rules and present findings grouped by rule:

- Sentences over 25 words (20 for instructions).
- Passive voice with a known actor ("two alternatives were rejected" -> "we rejected two").
- Em dashes as prose connectors (structural separators in glossaries and tables stay).
- Verbless fragments ("Result: ...", "No app code.").
- Noun clusters over three words (proper names exempt).
- Metaphor and idiom, minus the terms of art.
- One word, one meaning (flag "ships" meaning both "delivers in v1" and "is included").

Gate with **AskUserQuestion** on mode, then apply: **STE-flavored** (recommended -- caps, actors,
plain verbs, but the register survives), **strict** (every rule everywhere; reads like a spec),
or **strict for reference sections only** (glossaries, procedures, delivery plans).

Complete when every finding is applied or declined.

## Pass 3: Orwell

STE already spent Orwell's rules on voice and jargon; hunt the remaining delta:

- **Rule 1** -- stale figures the STE pass classed as tolerable ("lets both sides win").
- **Rule 2** -- long words with short equivalents ("optionality" -> "the option").
- **Rule 3** -- every word that can come out ("explicitly out of scope", "quietly queues",
  "actual deliverable").
- **Rule 6** -- the guardrail: break any rule sooner than write something barbarous. Keep what a
  cut would make worse, and say which keeps you made.

Present the delta only, gate y/n with **AskUserQuestion**, apply.

## Summary

One row per applied edit across all passes, Before/After truncated to the changed span:

| Pass | Location | Before | After |
| ---- | -------- | ------ | ----- |

Close with one line counting declined findings, and recommend stopping: three lenses is the full
treatment -- a fourth pass trades voice for diminishing returns.

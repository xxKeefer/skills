---
name: define-term
description: >
  Add a single term to a CONTEXT.md glossary under a concept the user specifies. Lightweight
  alternative to /define-concept -- one term, corpus-evidence lookup, human verification, insert.
  Use when the user says "define term", "add X to the context", "glossary this", or wants to
  capture one term without a full concept mining pass.
---

# Define Term

Add one term to a `CONTEXT.md`. The user must say which context (file) and which section it
belongs under -- if they don't, ask before doing anything else.

The corpus -- code, vault notes, lore, session logs, docs -- is wherever the term's meaning is
evidenced. Only the evidence source changes; the mechanics are identical.

## Step 1: Locate the CONTEXT.md

The glossary is a markdown file canonically named `CONTEXT.md`, one per context.

1. Check memory and user instructions for a stated location -- a user preference wins.
2. Otherwise glob for `CONTEXT.md` (legacy names: `ubiquitous-language.md`, `ubiquitous.md`,
   `GLOSSARY.md`) near the material.
3. Multiple matches: ask the user which context to update.
4. No match: suggest running `/define-concept` instead -- a context file needs a frame and at
   least one core term before single terms make sense.

## Step 2: Resolve the Section

The term must land somewhere in the file. Classify it:

- **Core term** -- a structural noun; gets a prose `### {Term}` entry under `## Core Terms`.
- **Action** -- a verb the concept supports; goes under `## Actions`.
- **Qualifier** -- a state, constraint, or flavour; a row in the `## Qualifiers` table.
- **Relationship** -- how it links to another concept; a row in the `## Relationships` table.

If the user named a section, honour it. If not, propose the classification and confirm. Do not guess
silently.

## Step 3: Gather Evidence

Search the corpus for the term (types, schemas, constants, i18n strings, headings, frontmatter,
named entities, comments, tests, logs). Draft a definition from usage. If the term doesn't appear
in the corpus, draft from the user's description and say so.

## Step 4: Verify

Present as plain markdown text (never an interactive picker):

> **Proposed term: `{Term}`** -- under `## {Section}`
>
> **Definition:** {proposed definition}
> **Found in:** {sources, or "not in corpus -- from your description"}
>
> **Accept**, **edit**, or **reject**?

Honour edits verbatim. Record any 🚩 needs-review flag the user raises, including the reason.

## Step 5: Insert

- **Core term** -- add a prose `### {Term}` entry: define what it IS, fold in composition and
  cross-links via anchors. **Action** -- add to the Actions prose/list. **Qualifier** /
  **Relationship** -- add a terse row to the matching table, creating the table if missing.
- One best term per concept -- if it's a synonym of an existing entry, say so and offer to list it
  as one to avoid rather than add a duplicate.
- Add any 🚩 to the Flagged for Review section.
- Refresh the **Last updated** line.
- Touch nothing else in the file.

## Step 6: Summary

> **Term added:** `{Term}` under `## {Section}` {flags if any}
>
> File: `{path}`

## Guiding Principles

- **Restraint** -- the file only carries terms of value for aligning humans and agents. If the term
  is implementation trivia or session-local shorthand, say so and suggest skipping.
- **Human verifies** -- never insert without explicit approval.
- **Definitions describe what something IS**, not what it does. No entry without a clear definition.

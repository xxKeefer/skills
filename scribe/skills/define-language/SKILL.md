---
name: define-language
description: >
  Compare the current conversation against a CONTEXT.md glossary and propose additions or
  corrections. Invokable at any point in a session. The file is the source of truth -- suggest
  edits with restraint. Use when the user says "define language", "sync the context", "update the
  glossary", or after a discussion that surfaced new or drifted terminology.
---

# Define Language

Audit the conversation so far against a `CONTEXT.md`. Propose changes; the human decides. The file
is a curated source of truth, not a transcript -- maintain it carefully and with restraint.

This works for any context file regardless of corpus -- code, vault, lore, docs. It maintains an
existing file; it does not create one.

## Step 1: Locate the CONTEXT.md

The glossary is a markdown file canonically named `CONTEXT.md`, one per context.

1. Check memory and user instructions for a stated location -- a user preference wins.
2. Otherwise glob for `CONTEXT.md` (legacy names: `ubiquitous-language.md`, `ubiquitous.md`,
   `GLOSSARY.md`) near the material under discussion.
3. Multiple matches: ask the user which context this conversation applies to.
4. No match: suggest `/define-concept` to bootstrap one -- this skill maintains an existing file.

Read the file in full before comparing.

## Step 2: Mine the Conversation

Review the conversation for:

- **Terms the file already defines** -- check whether usage matched the definition; mismatches are
  either a conversation error (no change) or evidence the definition has drifted (propose an edit).
- **New terms** -- words used with specific meaning that the file lacks.
- **Synonyms and homonyms** -- words colliding with or duplicating existing entries.
- **Resolved flags** -- did the conversation settle anything currently marked 🚩?

## Step 3: Triage Against the Bar

The file only carries terms of value for aligning humans and agents. Before proposing anything:

- **Additions** -- more relaxed, but still restrained. Skip session-local shorthand, trivia, and
  one-off phrasing. Would a future agent or teammate misalign without this entry? If not, drop it.
- **Edits to existing entries** -- the file is the source of truth; an existing definition outranks
  conversational usage. Propose an edit only when the conversation produced genuinely better
  understanding (a user correction, an expert statement, a resolved 🚩) -- not merely different
  wording.
- **Flag resolutions** -- conversation explicitly settled a 🚩: propose removing the flag and
  updating the entry.

If nothing clears the bar, say so and stop -- an empty result is a valid outcome.

## Step 4: Propose Changes

Present each proposal one at a time, as plain markdown text (never an interactive picker). State the
change type and target section:

> **{Add | Edit | Resolve flag}: `{Term}`** -- under `## {Section}`
>
> **{Proposed definition | Current → proposed definition}**
> **Why:** {what in the conversation justifies this}
>
> **Accept**, **edit**, or **reject**?

For edits, always show the current definition alongside the proposed one.

## Step 5: Apply

For each accepted change:

- Place it in the right section: prose `### {Term}` under `## Core Terms`, the Actions list, or a
  row in the `## Qualifiers` / `## Relationships` table -- matching the file's existing shape.
- One best term per concept; flag duplicates as synonyms to avoid rather than adding them.
- Keep 🚩 flags and the Flagged for Review section in sync.
- Refresh the **Last updated** line.
- Leave everything not explicitly accepted untouched.

## Step 6: Summary

> **Context updated:** {N} added, {N} edited, {N} flags resolved, {N} proposals rejected
>
> File: `{path}`

## Guiding Principles

- **The file is the source of truth** -- it outranks conversational usage. Edit only when genuinely
  warranted; never silently rewrite definitions to match a single conversation.
- **Adding is more relaxed than editing** -- but both pass the alignment-value bar.
- **Human verifies every change** -- propose, don't apply unilaterally.
- **Empty result is success** -- most conversations don't move the file. Don't invent changes to
  look useful.

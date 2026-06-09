---
name: update-language
description: >
  Compare the current conversation against the ubiquitous language glossary and propose
  additions or corrections. Invokable at any point in a session. The glossary is the source
  of truth -- suggest edits with restraint. Use when the user says "update language",
  "sync the glossary", "ubiquitous language", "capture these terms", or after a discussion
  that surfaced new or drifted domain terminology.
---

# Update Language

Audit the conversation so far against the glossary. Propose changes; the human decides.
The glossary is a curated source of truth, not a transcript -- maintain it carefully and
with restraint.

## Step 1: Locate the Glossary

The glossary is a markdown file, canonically named `ubiquitous-language.md` (legacy names:
`ubiquitous.md`, `UBIQUITOUS_LANGUAGE.md`, `GLOSSARY.md`).

1. Check memory and user instructions for a stated glossary location -- a user preference wins.
2. Otherwise grep/glob the repo for the filename candidates.
3. Multiple matches: ask the user which glossary applies to this conversation.
4. No match: suggest `/define-concept` to bootstrap one -- this skill maintains an existing
   glossary, it does not create one.

Read the glossary in full before comparing.

## Step 2: Mine the Conversation

Review the conversation for:

- **Terms used that the glossary already defines** -- check whether usage matched the
  definition; mismatches are either a conversation error (no glossary change) or evidence
  the definition has drifted (propose an edit)
- **New terms** -- domain words used with specific meaning that the glossary lacks
- **Synonyms and homonyms** -- words colliding with or duplicating existing entries
- **Resolved flags** -- did the conversation settle anything currently marked 🚩?

## Step 3: Triage Against the Bar

The glossary only carries terms of value for aligning humans and agents on concepts. Before
proposing anything, filter:

- **Additions** -- more relaxed, but still restrained. Skip session-local shorthand,
  implementation trivia, and one-off phrasing. Would a future agent or teammate misalign
  without this entry? If not, drop it.
- **Edits to existing entries** -- the glossary is the source of truth; an existing
  definition outranks conversational usage. Propose an edit only when the conversation
  produced genuinely better understanding (a user correction, a domain-expert statement,
  a resolved 🚩) -- not merely different wording.
- **Flag resolutions** -- conversation explicitly settled a 🚩: propose removing the flag
  and updating the entry.

If nothing clears the bar, say so and stop -- an empty result is a valid outcome.

## Step 4: Propose Changes

Present each proposal one at a time, as plain markdown text (never an interactive picker).
State the change type:

> **{Add | Edit | Resolve flag}: `{Term}`** -- under `{Concept}` / `{sub-heading}`
>
> **{Proposed definition | Current → proposed definition}**
> **Why:** {what in the conversation justifies this}
>
> **Accept**, **edit**, or **reject**?

For edits, always show the current definition alongside the proposed one.

## Step 5: Apply

For each accepted change:

- Place additions in the correct concept section and sub-heading (Core Terms / Actions /
  Qualifiers / Relationships); use `General` only for terms confirmed to apply across
  concepts; tag suspected-general terms **[generic?]**
- Keep 🚩 flags and the Flagged for Review section in sync
- Refresh the **Last updated** line
- Leave everything not explicitly accepted untouched

## Step 6: Summary

> **Glossary updated:** {N} added, {N} edited, {N} flags resolved, {N} proposals rejected
>
> File: `{path}`

## Guiding Principles

- **Glossary is the source of truth** -- it outranks conversational usage. Edit only when
  genuinely warranted; never silently rewrite definitions to match a single conversation.
- **Adding is more relaxed than editing** -- but both pass the alignment-value bar.
- **Human verifies every change** -- propose, don't apply unilaterally.
- **Empty result is success** -- most conversations don't move the glossary. Don't invent
  changes to look useful.

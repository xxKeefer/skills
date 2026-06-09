---
name: define-term
description: >
  Add a single term to the ubiquitous language glossary under a concept the user specifies.
  Lightweight alternative to /define-concept -- one term, code-evidence lookup, human
  verification, insert. Use when the user says "define term", "add X to the glossary",
  "glossary this", or wants to capture one term without a full concept mining pass.
---

# Define Term

Add one term to the glossary. The user must specify which concept the term belongs under --
if they don't, ask before doing anything else.

## Step 1: Locate the Glossary

The glossary is a markdown file, canonically named `ubiquitous-language.md` (legacy names:
`ubiquitous.md`, `UBIQUITOUS_LANGUAGE.md`, `GLOSSARY.md`).

1. Check memory and user instructions for a stated glossary location -- a user preference wins.
2. Otherwise grep/glob the repo for the filename candidates.
3. Multiple matches: ask the user which glossary to update.
4. No match: suggest running `/define-concept` instead -- a glossary needs at least one
   concept section before single terms make sense.

## Step 2: Resolve the Concept

The term must land under a concept:

- User named a concept that exists in the glossary (or `General`) -- proceed.
- User named a concept with no section yet -- confirm: add a new concept section with just
  this term, or run `/define-concept` for a full pass?
- User named no concept -- ask. Do not guess.

## Step 3: Gather Evidence

Search the codebase for the term (types, schemas, constants, i18n strings, comments, tests).
Draft a definition from usage. If the term doesn't appear in code, draft from the user's
description and say so.

## Step 4: Verify

Present as plain markdown text (never an interactive picker):

> **Proposed term: `{Term}`** -- under `{Concept}` / `{sub-heading}`
>
> **Definition:** {proposed definition}
> **Found in:** {file:line sources, or "not in code -- from your description"}
>
> **Accept**, **edit**, or **reject**?

Honour edits verbatim. Record any 🚩 needs-review flag the user raises, including the reason.

## Step 5: Insert

- Place the term in the correct sub-heading table (Core Terms / Actions / Qualifiers /
  Relationships) under the concept, creating the sub-heading if missing
- If the term applies beyond its concept, tag it **[generic?]** (promotion candidate) or put
  it under `General` if the user confirms it is generic
- Add any 🚩 to the Flagged for Review section
- Refresh the **Last updated** line
- Touch nothing else in the file

## Step 6: Summary

> **Term added:** `{Term}` under `{Concept}` {flags if any}
>
> File: `{path}`

## Guiding Principles

- **Restraint** -- the glossary only carries terms of value for aligning humans and agents
  on concepts. If the term is implementation trivia or session-local shorthand, say so and
  suggest skipping.
- **Human verifies** -- never insert without explicit approval.
- **Definitions over labels** -- no entry without a clear definition.

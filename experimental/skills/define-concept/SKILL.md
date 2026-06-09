---
name: define-concept
description: >
  Mine the codebase for all terminology around a single domain concept (e.g. a product, an
  aggregate, a workflow) and add it to the ubiquitous language glossary as its own section.
  Every proposed term is verified by the human one at a time. Use when the user says
  "define concept", "document the concept of X", "mine terms for X", or wants to build out
  the glossary one concept at a time.
---

# Define Concept

Deep-dive a single domain concept: mine the codebase for its nouns, verbs, qualifiers, and
relationships, verify every term with the human, and write the result into the glossary as
a dedicated concept section. Nothing gets added without approval.

## Step 1: Locate the Glossary

The glossary is a markdown file, canonically named `ubiquitous-language.md` (legacy names:
`ubiquitous.md`, `UBIQUITOUS_LANGUAGE.md`, `GLOSSARY.md`).

1. Check memory and user instructions for a stated glossary location -- a user preference wins.
2. Otherwise grep/glob the repo for the filename candidates.
3. Multiple matches: ask the user which glossary this concept belongs in.
4. No match: ask the user where it should live (suggest an existing documentation folder
   near the code being mined), then create it with the skeleton in Step 6.

## Step 2: Explore the Codebase

Scan for terminology around the target concept. Use parallel Explore subagents on large
codebases -- one sweep per category works well:

- **Core nouns** -- what the concept IS: type/interface definitions, schemas, constants,
  enums, comments/docstrings, i18n strings, README/docs
- **Actions** -- what can be DONE to it: API/SDK methods, store actions, component action
  menus, test descriptions; distinguish lifecycle verbs from state-toggle verbs from
  approval-flow verbs
- **Relationships & qualifiers** -- how it connects to other concepts: parent/child fields,
  product-type unions, status/state enums (capture enum values verbatim), flags that gate
  behaviour

Focus on domain logic, not infrastructure. Have each agent return term + draft definition +
source (file:line).

## Step 3: Build the Candidate List

Deduplicate across sweeps and group into:

- **Core nouns** -- entities, value objects, structural parts
- **Core verbs** -- commands, events, processes
- **Qualifiers** -- states, statuses, flavours
- **Relationships** -- how the concept connects to others

Sort by how fundamental the term is. Present the user a brief count-by-category summary,
then start the loop.

## Step 4: Human Verification Loop

Present candidates **one at a time**, as plain markdown text -- never an interactive picker
(pickers hide the definition while the user decides):

> **Proposed term: `{Term}`**
>
> **Definition:** {proposed definition based on code usage}
> **Found in:** {file:line sources}
>
> **Accept**, **edit**, or **reject**?

- **Accept** -- record as-is
- **Edit** -- user corrects the name and/or definition; record their version
- **Reject** -- skip
- Any answer may also add a **🚩 needs review** flag (uncertain domain knowledge, synonym
  to confirm, scope question) -- record the flag reason verbatim
- The user may volunteer **new terms** mid-loop -- record them attributed as user-added

After each decision, immediately move to the next term. Keep the pace brisk. If the user
gets impatient, offer a numbered bulk list ("accept 1-5, reject 6, edit 7: ...").

### Scope marking

While verifying, classify each term's scope:

- **General** -- applies across all concepts (e.g. lifecycle states, lock/unlock, approval
  workflows). These go to the glossary's top-level General section.
- **Concept-specific** -- only meaningful for this concept.
- **[generic?]** -- suspected general but only verified through this concept's lens so far.
  Keep under the concept section with the marker; promote later when confirmed.

## Step 5: Flag Ambiguities

During the loop, surface:

- Same word, different meanings (homonyms)
- Different words, same meaning (synonyms)
- Code usage contradicting plain-English or colloquial team usage

Ask the user to resolve each; unresolved ones go to the Flagged for Review section with 🚩.

## Step 6: Write the Glossary

Structure (create if new, merge into if existing):

```markdown
# Ubiquitous Language -- {Project}

**Last updated:** {YYYY-MM-DD}

**Structure:** terms that apply across all concepts live under **General**; concept-specific
terms live under their concept heading. Terms marked **[generic?]** are promotion candidates.
🚩 = needs domain-expert review.

## General

### Core Terms
| Term | Definition |
| --- | --- |

### Actions
| Term | Definition |
| --- | --- |

## {Concept}

### Core Terms
### Actions
### Qualifiers
### Relationships

## Flagged for Review
1. ...
```

Rules:

- Each concept gets its own top-level `## {Concept}` section with the repeating sub-headings
  (Core Terms / Actions / Qualifiers / Relationships) -- include only the sub-headings that
  have content
- General terms discovered during this pass go under `## General`, not the concept section
- Always refresh the **Last updated** line
- Preserve all existing sections and entries untouched unless the user approved a change

## Step 7: Summary

> **Concept `{Concept}` defined:** {N} terms accepted ({N} user-edited, {N} flagged 🚩),
> {N} rejected
>
> File: `{path}`
>
> Use `/define-term` to add single terms later, `/update-language` to keep the glossary in
> sync with future conversations.

## Guiding Principles

- **Human verifies every entry** -- the codebase suggests, the human decides. Code names are
  often wrong, outdated, or misleading. The glossary captures what terms *should* mean.
- **Restraint** -- only terms of value for aligning humans and agents on concepts get
  promoted to the glossary. Implementation trivia stays out.
- **One at a time by default** -- forces real consideration. Bulk mode is an escape hatch.
- **Definitions over labels** -- an entry without a clear definition is useless.
- **Code is evidence, not truth** -- divergence between code and glossary is a refactoring
  signal, not a glossary bug.

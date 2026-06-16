---
name: define-concept
description: >
  Mine a corpus -- code, vault notes, lore, session logs, docs -- for all terminology around a
  single concept and write it into a CONTEXT.md glossary as a self-contained context file. Every
  proposed term is verified by the human one at a time. Use when the user says "define concept",
  "document the concept of X", "mine terms for X", or wants to capture the language of one concept.
---

# Define Concept

Deep-dive a single concept: mine the corpus for its nouns, verbs, qualifiers, and relationships,
verify every term with the human, and write the result into a `CONTEXT.md` as one self-contained
context. Nothing gets added without approval.

The corpus is whatever source material defines the concept -- a codebase, an Obsidian vault, a
campaign's lore files, session logs, design docs, a transcript. The mechanics are identical; only
the evidence source changes.

## Step 1: Locate the CONTEXT.md

The glossary is a markdown file canonically named `CONTEXT.md`. One `CONTEXT.md` holds one context.
A repo or vault with several contexts keeps each in its own `CONTEXT.md` and (optionally) a
`CONTEXT-MAP.md` at the root that links them.

1. Check memory and user instructions for a stated location -- a user preference wins.
2. Otherwise glob for `CONTEXT.md` (legacy names: `ubiquitous-language.md`, `ubiquitous.md`,
   `GLOSSARY.md`) near the material being mined.
3. Multiple matches: ask the user which context this concept belongs to, or whether it's a new one.
4. No match: ask where it should live (suggest a folder beside the material), then create it with
   the skeleton in Step 6.

## Step 2: Explore the Corpus

Scan for terminology around the target concept. Use parallel Explore subagents on large corpora --
one sweep per category works well. Adapt the evidence source to the corpus:

- **Core nouns** -- what the concept IS: type/schema/constant definitions, headings, frontmatter,
  i18n strings, glossary entries, named entities in lore/notes.
- **Actions** -- what can be DONE to/with it: methods, store actions, menu items, ritual/spell
  verbs, documented procedures, test descriptions. Distinguish lifecycle verbs from state-toggle
  verbs from approval-flow verbs.
- **Relationships & qualifiers** -- how it connects: parent/child links, unions/variants,
  status/state enums (capture values verbatim), flags or conditions that gate behaviour.

Focus on domain meaning, not infrastructure. Have each agent return term + draft definition +
source (`file:line`, note title, or log timestamp).

## Step 3: Build the Candidate List

Deduplicate across sweeps and group into:

- **Core nouns** -- entities, value objects, structural parts
- **Core verbs** -- commands, events, processes
- **Qualifiers** -- states, statuses, flavours, constraints
- **Relationships** -- how the concept connects to others

Sort by how fundamental the term is. Present a brief count-by-category summary, then start the loop.

## Step 4: Human Verification Loop

Present candidates **one at a time**, as plain markdown text -- never an interactive picker
(pickers hide the definition while the user decides):

> **Proposed term: `{Term}`**
>
> **Definition:** {proposed definition based on corpus usage}
> **Found in:** {sources}
>
> **Accept**, **edit**, or **reject**?

- **Accept** -- record as-is
- **Edit** -- user corrects the name and/or definition; record their version
- **Reject** -- skip
- Any answer may also add a **🚩 needs review** flag (uncertain knowledge, synonym to confirm,
  scope question) -- record the flag reason verbatim
- The user may volunteer **new terms** mid-loop -- record them attributed as user-added

After each decision, move straight to the next term. Keep the pace brisk. If the user gets
impatient, offer a numbered bulk list ("accept 1-5, reject 6, edit 7: ...").

### Sort each term by weight

As you verify, note how much room each term needs in Step 6:

- **Prose** -- structural nouns central to the concept that carry composition or cross-references.
  These earn a `### {Term}` entry.
- **Table** -- terse, list-like terms (states, constraints, flavours, links, verbs) that fit a one-
  line definition.

Let the natural groupings emerge from the terms themselves rather than pre-deciding a section list
-- you'll name the sections in Step 6 to match what you actually collected.

## Step 5: Flag Ambiguities

During the loop, surface:

- Same word, different meanings (homonyms)
- Different words, same meaning (synonyms) -- pick the one best term, list the rest to avoid
- Corpus usage contradicting plain-English or colloquial team usage

Ask the user to resolve each; unresolved ones go to the Flagged for Review section with 🚩.

## Step 6: Write the CONTEXT.md

One file, one context. **Form follows the material** -- shape the document around what the corpus
actually contains, not around a fixed template. The example below is a common shape, not a required
one; rename, add, drop, or reorder sections so the structure reads honestly.

```markdown
# {Subject} — Context

**Last updated:** {YYYY-MM-DD}

{1-3 sentence framing: what this context covers and any scope note, e.g. "this module is
product-agnostic" or "covers the northern kingdoms only".}

## The core model

> **{One-line essential truth of the concept.}**

{Short prose elaboration of that statement.}

## Core Terms

### {Term}

{Prose definition: what it IS, not what it does. Fold in customer-facing labels, composition
("a Flow Exporter is a Source and a Collector"), and cross-links to other terms via anchors.}

## {Supporting section}

| Term | Definition |
| --- | --- |

## Flagged for Review

1. ...
```

Invariants -- hold these regardless of how the sections are arranged:

- **Title, `Last updated`, and a framing line** always open the file. Refresh `Last updated` on
  every write.
- **The structural nouns get prose** -- one `### {Term}` each, with room for composition and
  cross-references. This is usually a `## Core Terms` section but name it to fit.
- **Terse, list-like terms go in tables** -- a `| Term | Definition |` table per coherent group.
  Name the group for what it holds (`## Qualifiers`, `## Relationships`, `## Actions`, `## Where
  things live`, whatever is true). Don't force a term into an ill-fitting bucket; if a section name
  would lie, rename the section.
- **The core model callout is optional but valued** -- use it when one sentence captures the
  essence.
- Cross-link related terms with anchors (`[Reserved IP](#reserved-ip)` ... `<a id="reserved-ip"></a>`).
- **🚩 items collect in a Flagged for Review section.**
- Preserve existing sections and entries untouched unless the user approved a change -- and follow
  the file's own established section names when merging into an existing CONTEXT.md.

## Step 7: Summary

> **Concept `{Subject}` defined:** {N} terms accepted ({N} user-edited, {N} flagged 🚩),
> {N} rejected
>
> File: `{path}`
>
> Use `/define-term` to add single terms later, `/define-language` to keep the file in sync with
> future conversations.

## Guiding Principles

- **Human verifies every entry** -- the corpus suggests, the human decides. Source names are often
  wrong, outdated, or misleading. The file captures what terms *should* mean.
- **Definitions describe what something IS**, not what it does. One best term per concept; list
  rejected synonyms so they don't creep back.
- **Restraint** -- only terms of value for aligning humans and agents get in. Implementation trivia
  and general concepts (timeouts, generic utilities) stay out.
- **One at a time by default** -- forces real consideration. Bulk mode is an escape hatch.
- **Source is evidence, not truth** -- divergence between the corpus and the file is a signal worth
  surfacing, not a file bug.

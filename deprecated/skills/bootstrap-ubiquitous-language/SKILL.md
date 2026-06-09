---
name: bootstrap-ubiquitous-language
description: >
  Bootstrap a ubiquitous language glossary for a brownfield project by mining the codebase for
  domain terms. Each proposed entry is verified by the human one at a time. Use when the user says
  "bootstrap ubiquitous language", "bootstrap glossary", "seed glossary", "extract domain terms",
  or wants to create an initial glossary from an existing codebase.
---

# Bootstrap Ubiquitous Language

Mine a brownfield codebase for domain terminology and build a glossary from scratch. Every
proposed term goes through human verification -- nothing gets added without approval.

## Step 1: Explore the Codebase

Scan broadly for domain terminology signals:

- **Module and directory names** -- these often encode domain concepts
- **Type/class/interface names** -- especially in domain layers
- **Function/method names** -- verbs that describe domain operations
- **Constants and enums** -- named domain values
- **Comments and docstrings** -- natural language descriptions of concepts
- **README and docs** -- existing explanations
- **Test descriptions** -- often the clearest articulation of behaviour
- **Existing glossary** -- check for `UBIQUITOUS_LANGUAGE.md`, `ubiquitous.md`, or similar

Use Explore subagents for large codebases. Focus on domain logic, not infrastructure.

## Step 2: Build the Candidate List

Group discovered terms into categories:

- **Core nouns** -- the things the system works with (entities, value objects, aggregates)
- **Core verbs** -- the operations the system performs (commands, events, processes)
- **Qualifiers** -- states, statuses, types that modify core concepts
- **Relationships** -- how concepts connect (owns, produces, triggers, depends on)

For each candidate, draft:

```
**{Term}** -- {proposed definition based on usage in code}
Source: {where you found it -- module name, test description, etc.}
```

Sort by how fundamental the term is -- core concepts first, qualifiers last.

## Step 3: Human Verification Loop

Present candidates **one at a time**. For each:

> **Proposed term: `{Term}`**
>
> **Definition:** {proposed definition}
> **Found in:** {source context}
>
> **Accept**, **edit**, or **reject**?

Based on response:

- **Accept** -- add to glossary as-is
- **Edit** -- user provides corrected definition, add that instead
- **Reject** -- skip, do not add

After each decision, immediately move to the next term. Keep the pace brisk -- don't
elaborate or discuss unless the user asks.

### Batching shortcut

If the user gets impatient with one-at-a-time, offer:

> Want me to show the remaining {N} terms as a numbered list so you can bulk accept/reject?

In bulk mode, present all remaining terms numbered. User responds with something like
"accept 1-5, reject 6, edit 7: {new definition}".

## Step 4: Flag Ambiguities

During verification, flag terms where:

- The codebase uses the same word for different concepts
- Multiple words are used for the same concept (synonyms)
- A term's usage in code contradicts its plain English meaning

Present each ambiguity and ask the user to resolve:

> **Ambiguity: `{term}`**
>
> Used as {meaning A} in {context} and {meaning B} in {context}.
> Which meaning should own this term? What should the other be called?

## Step 5: Write the Glossary

After all candidates are processed, use `/write-to-file` to create the glossary.

Follow the same structure as `/ubiquitous-language`:

- Core Concepts table
- Relationships table
- Example Dialogue (generate from accepted terms)
- Flagged Ambiguities (any unresolved from Step 4)

## Step 6: Summary

> **Glossary bootstrapped:** {N} terms accepted, {N} rejected, {N} ambiguities flagged
>
> File: `{path}`
>
> Run `/ubiquitous-language` after future conversations to keep it current.

## Guiding Principles

- **Human verifies every entry** -- the codebase suggests, the human decides. Code names
  are often wrong, outdated, or misleading. The glossary captures what terms *should* mean,
  not what the code currently calls them.
- **One at a time by default** -- forces the human to actually consider each term instead
  of rubber-stamping a batch. Bulk mode is an escape hatch, not the default.
- **Definitions over labels** -- a glossary entry without a clear definition is useless.
  "User" is not a glossary entry. "User: a person with an active account who can create
  and manage projects" is.
- **Code is evidence, not truth** -- the codebase shows how terms are used, but the glossary
  captures how they *should* be used. Divergence is a refactoring signal, not a glossary bug.

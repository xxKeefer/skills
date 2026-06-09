---
name: ubiquitous-language
description: >
  Extract and formalise domain terminology from conversations into a UBIQUITOUS_LANGUAGE.md glossary.
  DDD-inspired. Use when the user says "ubiquitous language", "define terms", "glossary",
  "domain language", or wants to capture and standardise project terminology.
---

# Ubiquitous Language

Extract domain terminology from the current conversation and formalise it into a glossary file.
Based on Domain-Driven Design's ubiquitous language practice.

## Step 1: Scan for Terminology

Review the conversation (and optionally the codebase) for:

- **Domain terms** -- nouns and verbs that carry specific meaning in this project
- **Ambiguous terms** -- words used inconsistently or with multiple meanings
- **Implicit concepts** -- ideas referenced but never named explicitly
- **Relationships** -- how terms relate to each other (is-a, has-a, produces, consumes)

## Step 2: Identify Problems

Flag terminology issues:

- **Synonyms** -- different words used for the same concept (pick one)
- **Homonyms** -- same word used for different concepts (disambiguate)
- **Missing terms** -- concepts that need a name
- **Stale terms** -- old terminology that no longer matches the code

Present findings:

> **Terminology audit:**
>
> **New terms:** {list}
> **Ambiguous:** {term} -- used as both {meaning A} and {meaning B}
> **Synonyms:** {term A} and {term B} mean the same thing -- recommend {pick}
> **Missing:** {concept that needs a name}
>
> Agree with these? Adjust before I write the glossary.

## Step 3: Check for Existing Glossary

Look for `UBIQUITOUS_LANGUAGE.md` or `ubiquitous.md` in the project root or common locations.

- **Exists:** read it, incorporate new terms, update definitions, preserve existing structure
- **Doesn't exist:** create a new one

## Step 4: Write the Glossary

Use `/write-to-file` to write `UBIQUITOUS_LANGUAGE.md` (or update the existing one).

### Structure

```markdown
# Ubiquitous Language

Shared terminology for {project name}.

## Core Concepts

| Term | Definition |
|---|---|
| **{Term}** | {concise definition} |

## Relationships

| Subject | Relationship | Object |
|---|---|---|
| {Term A} | produces | {Term B} |
| {Term C} | is a | {Term D} |

## Example Dialogue

> "When a {term A} triggers a {term B}, the {term C} should..."

Shows how terms work together in context.

## Flagged Ambiguities

| Term | Issue | Resolution |
|---|---|---|
| {term} | used as both X and Y | standardise on X; use Z for Y |
```

### Re-running behaviour

When updating an existing glossary:

- **Add** new terms in alphabetical order within their group
- **Update** definitions that have drifted from current usage
- **Preserve** terms not mentioned in this conversation
- **Flag** terms in the file that contradict current conversation usage

## Step 5: Summary

Present what was added/changed:

> **Glossary updated:** {N} new terms, {N} updated, {N} ambiguities flagged
>
> File: `{path}`

---
name: standardise-frontmatter
description: >
  Normalise a knowledge note's frontmatter to the canonical shape defined in the wiki domain spec.
  Adds missing fields, corrects types, flags non-canonical fields. Preserves document content.
  Use when the user says "standardise frontmatter", "fix frontmatter", "normalise frontmatter",
  or wants to bring a knowledge note's metadata into conformance.
---

# Standardise Frontmatter

Normalise knowledge note frontmatter to the canonical shape.

## Step 1: Identify Target Note

`$ARGUMENTS` should contain a file path to a knowledge note.

If no path provided, use **AskUserQuestion**:

> Which knowledge note should I standardise? Give me a file path.

Read the full note.

## Step 2: Parse Current Frontmatter

Extract the YAML frontmatter (between `---` fences). Identify:

- **Present fields** -- what exists and its current type/value
- **Missing fields** -- which canonical fields are absent
- **Non-canonical fields** -- fields not in the canonical spec
- **Type mismatches** -- e.g. `related` as a string instead of a list of wikilinks

Canonical fields (from wiki domain spec):

| Field | Type | Description |
|---|---|---|
| `up` | single wikilink string | Link to broader parent topic |
| `related` | list of wikilink strings | Subtopics split off from this doc |
| `also` | list of wikilink strings | Lateral connections |
| `aliases` | list of strings | Alternative names |
| `tags` | list of strings | Must include `"knowledge"` + topic tags |

## Step 3: Build Normalised Frontmatter

Apply these rules:

1. **Missing fields** -- add with sensible defaults:
   - `up`: `""` (empty string -- user must fill in)
   - `related`: `[]`
   - `also`: `[]`
   - `aliases`: `[]`
   - `tags`: `["knowledge"]` (preserve any existing topic tags)

2. **Type normalisation**:
   - Ensure `related`, `also`, `aliases`, `tags` are arrays
   - Ensure wikilink fields use `"[[name]]"` format
   - Ensure `up` is a single string, not an array

3. **Non-canonical fields** -- flag for user review:
   - `source` field -- remove; add content to `## Sources` section at document bottom
   - Other unknown fields -- list them and ask user whether to keep or remove

4. **Preserve** -- document body content must remain untouched

## Step 4: Apply and Report

Write the updated note. Report changes:

> **Frontmatter standardised for `{filename}`**
>
> - **Added:** {list of fields added}
> - **Normalised:** {list of fields with type corrections}
> - **Flagged:** {list of non-canonical fields, if any}
> - **No changes needed:** {if already conformant}

---
name: rebuild-index
description: >
  Generate or rebuild the INDEX.md for a given vault directory. Scans directory contents and
  produces a conformant index per the wiki domain spec. Works as both a bootstrap tool (first-time
  creation) and a maintenance tool (rebuild after content drift). Use when the user says "rebuild
  index", "update index", "generate index", or wants to refresh a directory's INDEX.md.
---

# Rebuild Index

Generate or rebuild `INDEX.md` for a vault directory.

## Step 1: Identify Target Directory

`$ARGUMENTS` should contain a directory path relative to the vault root.

If no path provided, use **AskUserQuestion**:

> Which directory should I generate an INDEX.md for? Give me a path relative to the vault root.

Confirm the directory exists before proceeding.

## Step 2: Scan Directory Contents

Read the directory contents:

- List all files and subdirectories (one level deep)
- For each markdown file, read its frontmatter and first heading
- For each subdirectory, check if it has its own INDEX.md
- Note any naming conventions or patterns in existing files

## Step 3: Determine Directory Purpose

Infer the directory's purpose from:

- Its name and position in the vault hierarchy
- The content of its files (frontmatter, headings, tags)
- Any existing INDEX.md (if rebuilding)
- Parent directory conventions

## Step 4: Generate INDEX.md

Write the index following the canonical format:

```markdown
---
description: One-line purpose of this directory
conventions: brief notes on naming, structure rules
---

# {Directory Name}

{2-3 sentences on what belongs here and what doesn't}

## Structure

{Description of any subdirectory conventions}
```

Rules:

- `description` -- concise, factual, one line
- `conventions` -- naming patterns, file types, organisation rules observed in existing content
- Body text -- what belongs here, what doesn't, how files relate to each other
- Structure section -- describe subdirectory layout if subdirectories exist; omit if flat

## Step 5: Write and Report

Write the INDEX.md to the target directory. Report what was generated:

> **INDEX.md generated for `{directory}`**
>
> - **Files scanned:** {N}
> - **Subdirectories:** {N}
> - **Status:** {created | rebuilt}

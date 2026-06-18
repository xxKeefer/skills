---
name: edit-article
description: >
  Edit and improve a written article or note. Obsidian-aware -- preserves wikilinks, frontmatter,
  and callouts. DAG-based section ordering, 240 char paragraph cap. Use when the user says
  "edit article", "edit this", "improve this writing", "polish this", or wants structural and
  prose editing on a note or article.
---

# Edit Article

Structural and prose editing for articles and notes. Obsidian-native -- preserves vault syntax.

## Step 1: Read the Article

`$ARGUMENTS` may contain:

- **File path** -- read the file directly
- **Note title** -- search the vault for it
- **Nothing** -- check conversation context for pasted content

If no article found, use **AskUserQuestion**:

> What article should I edit? Give me a file path, note title, or paste the content.

Read the full article. Note:

- **Frontmatter** (YAML between `---` fences) -- preserve exactly
- **Wikilinks** (`[[note name]]`, `[[note|alias]]`) -- preserve exactly
- **Callouts** (`> [!type]`) -- preserve syntax
- **Tags** (`#tag/subtag`) -- preserve exactly
- **Embeds** (`![[file]]`) -- preserve exactly

## Step 2: Analyse Structure

Build a mental model of the article:

- **Thesis** -- what's the main argument or point?
- **Sections** -- what does each section contribute?
- **Flow** -- does the order make sense? Build a DAG of section dependencies
  (which sections require understanding of earlier ones)
- **Gaps** -- what's missing? What questions does the reader have after each section?
- **Redundancy** -- what's repeated or could be consolidated?

Present your analysis:

> **Article: `{title}`**
>
> **Thesis:** {one sentence}
> **Sections:** {N} -- {brief assessment of flow}
> **Issues found:**
> - {issue 1}
> - {issue 2}
>
> Proceed with edits, or discuss first?

## Step 3: Reorder Sections (if needed)

Use the DAG from Step 2. If sections are out of dependency order:

1. Present the proposed new order with reasoning
2. Wait for approval
3. Reorder

A section should never reference concepts introduced in a later section.

## Step 4: Edit Prose

Work through each section applying these rules:

### Paragraph cap

No paragraph exceeds **240 characters**. Split long paragraphs. Prefer short, punchy sentences.

### Prose rules

- **Active voice** over passive
- **Concrete** over abstract -- show, don't tell
- **Cut filler** -- "basically", "actually", "in order to", "it should be noted that"
- **One idea per paragraph**
- **Transitions** -- each paragraph should flow from the previous one
- **Consistent tense** -- don't shift between present and past without reason

### Preserve

- Author's voice and style -- edit for clarity, not to rewrite in your own voice
- Technical accuracy -- don't "simplify" correct statements into incorrect ones
- All Obsidian syntax (wikilinks, callouts, embeds, tags, frontmatter)

## Step 5: Present Edits

Present the edited article in full. Summarise what changed:

> **Changes:**
> - {section reordered / merged / split}
> - {N paragraphs shortened}
> - {specific prose fixes}
>
> Review the edits -- want me to adjust anything?

If the user approves, write the file back using the original path.

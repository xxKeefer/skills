---
name: intake-it
description: >
  HITL single-note intake. Takes a 00-raw/hitl/ file path and user instruction, processes the note
  with human guidance on classification and placement. Same routing and absorb-and-split logic as
  intake-raw but interactive. Use when the user says "intake this", "process this note", "file this",
  or wants to manually process a single raw note with guidance.
---

# Intake It

HITL single-note intake from `00-raw/hitl/`.

## Step 1: Identify the Note

`$ARGUMENTS` should contain:

- **File path** -- path to a note in `00-raw/hitl/`
- **User instruction** (optional) -- guidance on how to classify or place the note

If no file path provided, use **AskUserQuestion**:

> Which note in `00-raw/hitl/` should I process? Give me the file path.

Read the full note.

## Step 2: Present the Note

Show the user a summary:

> **Note: `{filename}`**
>
> **Content preview:** {first 5 lines or key content}
> **My suggested classification:** {knowledge | fleeting | project | work}
> **Suggested destination:** {target path}
> **Reasoning:** {why this classification}
>
> Agree, or redirect?

If the user provided an instruction in `$ARGUMENTS`, use it to inform the classification but still
present the summary for confirmation.

## Step 3: Route Based on User Decision

Apply the user's classification decision:

- **Knowledge** -- proceed to Step 4 (absorb-and-split)
- **Fleeting/personal** -- move to `04-notes/` root
- **Project-related** -- move to `05-projects/` root
- **Work-related** -- move to the user-specified work location (ask if unclear)
- **Other** -- follow user instruction

## Step 4: Absorb Knowledge Notes (if applicable)

If classified as knowledge, apply absorb-and-split with human guidance:

1. Search `03-knowledge/` for the most relevant existing doc
2. Present the match (or lack thereof) to the user:

> **Best match:** `{filename}` -- {reason}
> **Section:** `{heading}` -- content would go here
>
> Absorb here, pick a different doc, or create new?

3. On user approval -- absorb content, applying splits if needed
4. On redirect -- follow user's placement instruction
5. On "create new" -- generate a new knowledge doc with canonical frontmatter

## Step 5: Post-Intake Cleanup

- **Fully absorbed** -- delete the raw file
- **Partially absorbed** -- move to `98-archive/`
- Follow user instruction if they want a different outcome

## Step 6: Report

> **Intake complete for `{filename}`**
>
> - **Classification:** {classification}
> - **Action:** {absorbed into X | filed to Y | created Z}
> - **Splits:** {N, if any}

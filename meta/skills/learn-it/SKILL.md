---
name: learn-it
description: >
  Analyze the current conversation to extract repeatable patterns and codify them into a new skill.
  Use when the user says "learn this", "make a skill from this", "extract a skill", "turn this into
  a skill", or wants to capture a workflow they just performed so it can be reused.
---

# Learn It

Extract a repeatable pattern from the current conversation and turn it into a skill. This is a
HITL wrapper around `/write-a-skill` -- it provides conversation context that write-a-skill
wouldn't otherwise have.

## Step 1: Scan the Conversation

Review the full conversation history. Look for:

- **Repeated sequences** -- steps performed in a consistent order
- **Decision points** -- where choices shaped the workflow
- **Inputs and outputs** -- what went in and what came out
- **Tool patterns** -- which tools, in what order, with what arguments
- **Clarification loops** -- where ambiguity was resolved through questions
- **Checkpoints** -- where the user reviewed and approved before continuing

## Step 2: Identify the Core Pattern

Distill what you found into:

- **One-sentence purpose** -- what does this workflow accomplish?
- **Trigger phrases** -- when would a user invoke this?
- **Inputs** -- what does the skill need to start?
- **Steps** -- the ordered sequence, including decision branches
- **Outputs** -- what does the skill produce?
- **Principles** -- recurring rules or constraints observed

Present the summary:

> **Pattern detected: `{name}`**
>
> **Purpose:** {one sentence}
> **Triggers:** {trigger phrases}
> **Inputs:** {what it needs}
> **Steps:** {N} steps
> **Outputs:** {what it produces}
>
> Does this capture it? Adjust anything before I write the skill.

Wait for confirmation. Iterate if needed.

## Step 3: Hand Off to /write-a-skill

Pass the confirmed pattern as context to `/write-a-skill`, including:

- The distilled pattern from Step 2
- The target domain (ask the user if not obvious)
- Any conversation examples that illustrate the workflow

Let `/write-a-skill` handle the actual skill authoring, quality checks, and review.

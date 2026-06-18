---
name: explain-it
description: >
  Explain the reasoning behind decisions, conclusions, or suggestions made in the current
  conversation. The user points at something the AI said or did, and the AI unpacks its reasoning
  transparently until shared understanding is reached. Use when the user says "explain it",
  "explain that", "why did you", "walk me through", "I don't follow", "justify that", or
  questions a decision made earlier in the conversation.
---

# Explain It

Unpack your reasoning on demand. The user points at something you said, recommended, or did --
you explain why until they're satisfied.

## Step 1: Identify What Needs Explaining

`$ARGUMENTS` may contain:

- **A quote or paraphrase** of something from the conversation
- **A reference to a step, decision, or suggestion** (e.g. "step 3", "that refactor", "the type change")
- **A general "why"** about the overall approach

If `$ARGUMENTS` is empty or ambiguous, use **AskUserQuestion**:

> What part of the conversation do you want me to explain? Point me at a decision, suggestion,
> or anything that isn't sitting right.

## Step 2: Explain via /explain

Invoke `/explain` with the identified target. When constructing the explanation layers, frame
them as self-reasoning:

- **What:** the decision or action you took
- **How:** the chain of reasoning -- what you observed, what you inferred, what you assumed
- **Why:** alternatives you considered and why you rejected them

For each link in the reasoning chain, make explicit:

- **Observed** -- code, context, or constraint that informed the decision
- **Inferred** -- conclusion drawn and why that inference follows
- **Assumed** -- anything taken as given without verifying (flag honestly)
- **Uncertainty** -- where you could be wrong

## Step 3: Revise if Wrong

If explaining your reasoning reveals a flaw, correct course immediately. The user called
`/explain-it` because something felt off -- they may be right.

## Guiding Principles

- **Transparency over persuasion.** The goal is shared understanding, not winning the argument.
- **Revise in the open.** If you realise you were wrong, say so and offer the corrected position.

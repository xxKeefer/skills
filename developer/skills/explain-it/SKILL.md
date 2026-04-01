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

Unpack your reasoning on demand. The user points at something you said, recommended, or did —
you explain why until they're satisfied.

## Step 1: Identify What Needs Explaining

`$ARGUMENTS` may contain:

- **A quote or paraphrase** of something from the conversation
- **A reference to a step, decision, or suggestion** (e.g. "step 3", "that refactor", "the type change")
- **A general "why"** about the overall approach

If `$ARGUMENTS` is empty or ambiguous, use **AskUserQuestion**:

> What part of the conversation do you want me to explain? Point me at a decision, suggestion,
> or anything that isn't sitting right.

## Step 2: Reconstruct Your Reasoning

Walk back through the chain of reasoning that led to the conclusion. For each link in the chain,
make explicit:

- **What you observed** — the code, context, or constraint that informed the decision
- **What you inferred** — the conclusion you drew and why that inference follows
- **What you assumed** — anything you took as given without verifying. Flag these honestly.
- **What alternatives you considered** — other approaches and why you rejected them
- **What you don't know** — gaps in your reasoning, things you could be wrong about

Present this as a structured walkthrough, not a wall of text:

```
## Why: <one-line summary of the decision>

**Observed:** <what I saw in the code/context>
**Inferred:** <the conclusion I drew>
**Assumed:** <what I took as given — flag if unverified>
**Alternatives considered:** <what else I looked at and why I didn't go that way>
**Uncertainty:** <where I could be wrong>
```

Drop sections that add no value. If you considered no alternatives, don't include that section.
If you assumed nothing, skip it.

## Step 3: Check Understanding

After explaining, ask:

> Does that track? Or is there a specific part you want me to dig deeper on?

## Step 4: Go Deeper (if needed)

If the user pushes back or asks follow-ups:

1. **Don't get defensive.** If they found a flaw in your reasoning, acknowledge it directly.
2. **Re-examine from their angle.** Their question may reveal an assumption you didn't notice.
3. **Show your work.** If the reasoning depends on a code path, trace it explicitly — file, line,
   data flow. Don't hand-wave.
4. **Revise if wrong.** If the explanation reveals your original conclusion was flawed, say so and
   offer the corrected position. Do not cling to a bad call.

Repeat Steps 3-4 until the user is satisfied or you've exhausted what you can explain.

## Guiding Principles

- **Transparency over persuasion.** The goal is shared understanding, not winning the argument.
  If your reasoning has holes, exposing them is the point.
- **Distinguish fact from inference.** Be ruthlessly clear about what you read in the code vs
  what you concluded from it. Never present inference as observation.
- **Admit uncertainty.** "I don't know" and "I guessed" are valid answers. Dressing up a guess
  as a deduction erodes trust.
- **Trace to source.** When explaining a code-related decision, point at the specific file, line,
  or symbol. Abstract explanations without grounding are useless.
- **Revise in the open.** If explaining your reasoning makes you realise you were wrong, correct
  course immediately. The user called /explain-it because something felt off — they may be right.

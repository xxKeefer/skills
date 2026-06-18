---
name: resolve-it
description: >
  Critically assess code review feedback before applying fixes. Accepts feedback from AI reviewers
  (e.g. GitHub Copilot, CodeRabbit), human reviewers, or directly as arguments. Use when user says
  "resolve it", "address feedback", "resolve feedback", pastes review comments, or wants to evaluate
  PR suggestions. Do NOT blindly trust the reviewer — analyze validity, trade-offs, and alternatives first.
---

# Resolve It

Evaluate code review feedback critically before acting on it.

## Step 1: Parse Input

`$ARGUMENTS` may contain:

- **Inline feedback** — review comments pasted or typed directly
- **PR URL or number** — fetch comments from the PR
- **Nothing** — use **AskUserQuestion**: "Paste the feedback, or give me a PR URL/number."

Feedback can come from any source:

- **AI reviewers** (GitHub Copilot, CodeRabbit, etc.) — treat with healthy skepticism; they hallucinate, misread control flow, and over-engineer
- **Human reviewers** — treat with more trust but still assess independently; humans can be wrong about unfamiliar code
- **Self-review notes** — the user's own observations they want a second opinion on

Identify each distinct piece of feedback (a comment, suggestion, or requested change).

## Step 2: For Each Piece of Feedback

### 2a. Read the source file

Read the file and surrounding context to fully understand the code.

### 2b. Assess validity

Determine if the feedback is:

- **Valid** — identifies a real issue (bug, unhandled error, race condition, etc.)
- **Partially valid** — correct observation but wrong fix, or low-impact nitpick
- **Invalid** — misunderstands the code, suggests something worse, or is irrelevant

### 2c. Present analysis to user

For each item, provide a concise summary:

```
## Feedback: <one-line summary>

**Source:** <reviewer name or "AI reviewer" or "self">
**Verdict:** Valid | Partially valid | Invalid

**Why:** <1-2 sentences explaining the reasoning>

**Pros of fixing:**
- <bullet>

**Cons of fixing:**
- <bullet>

**Alternatives:**
- <alternative approach if any>

**Recommendation:** <what you'd do and why>
```

Drop sections that add no value (e.g. skip "Alternatives" if there are none, skip "Cons" if the fix is clearly good).

## Step 3: Batch Decision

After presenting all items, ask:

> Apply all recommended fixes? Or pick specific items: [list numbers]

## Step 4: Apply Fixes (if approved)

For each approved fix:

1. Make the change
2. Run relevant tests
3. Report results

If multiple fixes touch the same file, apply them together to avoid conflicts.

## Critical Evaluation Rules

- **Do not trust the reviewer by default.** AI reviewers hallucinate, misread control flow, and suggest over-engineered fixes. Human reviewers may not have full context.
- **Check if the "problem" actually exists.** Trace the code path — does the error scenario the reviewer warns about actually happen?
- **Evaluate the suggested fix itself.** Even if the problem is real, the suggested fix may introduce new issues, be unnecessarily complex, or miss the better solution.
- **Consider the context.** A fire-and-forget dispatch might be intentional. A missing null check might be guarded upstream. Read before judging.
- **Flag when the fix is cosmetic.** If the only benefit is "cleaner code" with no behavioral change, say so — the user can decide if it's worth the diff noise.
- **Weigh reviewer authority.** A senior teammate's architectural feedback carries more weight than an AI nitpick about variable naming. Adjust your confidence accordingly.

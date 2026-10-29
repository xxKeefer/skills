---
name: resolve-feedback
disable-model-invocation: true
description: Assess review feedback from AI or human reviewers, pasted or from a PR, before you apply any fix.
---

# Resolve Feedback

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

**Done when:** you have listed each distinct piece of feedback (a comment, suggestion, or requested change) and its source.

## Step 2: For Each Piece of Feedback

### 2a. Read the source file

Read the file and surrounding context to fully understand the code.

### 2b. Assess validity

Trace each claim in the code before you accept it. Then determine if the feedback is:

- **Valid** — identifies a real issue (bug, unhandled error, race condition, etc.)
- **Partially valid** — correct observation but wrong fix, or low-impact nitpick
- **Invalid** — misunderstands the code, suggests something worse, or is irrelevant

If the fix only makes the code cleaner and changes no behaviour, call it cosmetic in the verdict. The user decides if it is worth the diff.

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

**Done when:** every piece of feedback has a verdict, and the user has its analysis.

## Step 3: Batch Decision

After presenting all items, ask:

> Apply all recommended fixes? Or pick specific items: [list numbers]

**Done when:** the user has picked the fixes to apply, or none.

## Step 4: Apply Fixes (if approved)

For each approved fix:

1. Make the change
2. Run relevant tests
3. Report results

If multiple fixes touch the same file, apply them together to avoid conflicts.

**Done when:** every approved fix is made and its tests pass.

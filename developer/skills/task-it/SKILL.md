---
name: task-it
description: >
  Turn a /spike-it output into GitHub issues ready for /plan-it or /do-it. Decomposes the spike into
  demo-able blocks of work, gets user approval, creates the issues, then edits the spike into a
  tracking issue. Use when the user says "task it", "create tickets", "break into tickets", "make the
  tickets", or wants to turn a spike or feature breakdown into tracked issues.
---

# Task It

Decompose a `/spike-it` output into GitHub issues, get approval, then create them and turn the spike
into a tracking issue.

## Step 1: Parse Input

`$ARGUMENTS` may contain:

- **Spike issue reference** (e.g. `#42`) — fetch from GitHub via `gh`
- **Spike file path** (e.g. `.ai/spike_some-feature.md`) — read the file
- **Nothing** — check the current conversation for a `/spike-it` output

If no spike context is found, use **AskUserQuestion**:

> What are we breaking into tickets? Give me a spike issue number, spike file path, or description.

Read the spike. Extract:

- **Scope items** (the "In scope" checklist)
- **Acceptance criteria**
- **Technical considerations**
- **Approach / broad strokes**

Summarise what you found back to the user.

## Step 2: Decompose into Issues

Break the spike into issues. Each issue should be a **demo-able block of work** — something worth
showing at the end of a sprint. `/plan-it` handles the fine-grained decomposition within an issue;
`/task-it` defines the deliverable units.

For each issue, draft:

```
### Issue N: {conventional prefix}: {summary}

**Type:** feat | fix | refactor | chore
**Summary:** 1 sentence
**Description:** 2-4 sentences — what changes from the user's perspective
**Acceptance Criteria:**
- [ ] Testable behaviour 1
- [ ] Testable behaviour 2
**Depends on:** Issue N (if any)
**Labels:** [relevant labels from spike]
```

### Sizing guidance

- Each issue should be **completable in 1-3 days** by a developer with agent tooling
- An issue is too big if it touches more than one feature area that could be demoed independently
- An issue is too small if it has no visible or testable outcome on its own
- Order issues by dependency — note which ones block others

## Step 3: Present for Approval

Show the full issue list:

> **{N} issues from spike `{spike name}`:**
>
> 1. **{prefix}: {summary}** — {type} — {1-line description}
> 2. **{prefix}: {summary}** — {type} — {1-line description}
> ...
>
> Dependency order: 1 -> 2 -> 3 (4 and 5 independent)

Ask: **"Adjust any issues, or approve to create?"**

Iterate until the user approves. They may want to merge, split, reorder, or drop issues.

## Step 4: Create the Issues

For each approved issue, create it via `gh issue create`:

1. **Title:** `{type}: {summary}` using conventional prefixes
2. **Body:** description + acceptance criteria + `**Spike:** #N` cross-reference at the top
3. **Labels:** from the issue draft

After creating all issues, present:

> **Created {N} issues:**
>
> 1. #N — {summary}
> 2. #N — {summary}
> ...

## Step 5: Edit Spike into Tracking Issue

Edit the spike issue (fallback: plan issue if no spike) to append a task list at the bottom:

```markdown
## Tasks

- [ ] #N — {summary}
- [ ] #N — {summary}
- [ ] #N — {summary}
```

Use `gh issue edit` to append this to the spike issue body. This turns the spike into a tracking
issue — GitHub will show progress as child issues are closed.

Present the final state:

> **Tracking issue:** #N (spike)
> **Work issues:** #N, #N, #N
>
> Pick one to `/plan-it` or `/do-it`?

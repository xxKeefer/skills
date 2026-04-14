---
name: task-it
description: >
  Turn a /spike-it output into tracker tickets ready for /plan-it or /do-it. Decomposes the spike
  into demo-able blocks of work, gets user approval, resolves the epic, then creates the tickets in
  the issue tracker. Use when the user says "task it", "create tickets", "break into tickets",
  "make the tickets", or wants to turn a spike or feature breakdown into tracked issues.
---

# Task It

Decompose a `/spike-it` output into vertical-slice GitHub issues with HITL/AFK classification,
get approval, create them in dependency order, and turn the spike into a tracking issue. The final
issue is always a mandatory HITL QA verification task.

## Step 1: Parse Input

`$ARGUMENTS` may contain:

- **Spike issue reference** (e.g. `#42`) -- fetch from GitHub via `gh`
- **Spike file path** (e.g. `.ai/spike_some-feature.md`) -- read the file
- **Nothing** -- check the current conversation for a `/spike-it` output

If no spike context is found, use **AskUserQuestion**:

> What are we breaking into tickets? Give me a spike issue number, spike file path, or description.

Read the spike. Extract:

- **Scope items** (the "In scope" checklist)
- **Acceptance criteria**
- **Technical considerations**
- **Approach / broad strokes**

Summarise what you found back to the user.

## Step 2: Decompose into Vertical Slices

Break the spike into issues. Each issue is a **vertical slice** -- it cuts through all layers
end-to-end, is demo-able or verifiable on its own, and is worth showing at end of sprint.
`/plan-it` handles fine-grained decomposition within an issue; `/task-it` defines the deliverable
units.

For each issue, draft:

```
### Issue N: {conventional prefix}: {summary}

**Type:** feat | fix | refactor | chore
**Mode:** HITL | AFK
**Summary:** 1 sentence
**Description:** 2-4 sentences -- what changes from the user's perspective. No file paths.
  Use domain language. Describe behaviours, not implementation.
**Acceptance Criteria:**
- [ ] Observable, testable behaviour 1
- [ ] Observable, testable behaviour 2
**Depends on:** Issue N (if any)
**Blocked by:** Issue N (if any -- use when strict ordering required)
**Labels:** [relevant labels from spike]
```

### Slice classification

- **AFK** -- fully specified, an agent can implement and merge without human interaction.
  Prefer AFK where possible to maximise parallelism.
- **HITL** -- requires human judgment, design review, or architectural decision.

### Durability principles

Issue bodies must survive radical codebase changes:

- **No file paths or line numbers** -- they go stale
- **Describe behaviours and contracts**, not implementation structure
- **Use the project's domain language** (check `UBIQUITOUS_LANGUAGE.md` if it exists)
- **Acceptance criteria = observable, testable behaviours**

### Sizing guidance

- Each issue should be **completable in 1-3 days** by a developer with agent tooling
- Too big if it touches more than one feature area that could be demoed independently
- Too small if it has no visible or testable outcome on its own
- Prefer many thin slices over few thick ones
- Order issues by dependency -- note which ones block others

### Mandatory final issue: QA Verification

The last issue in every decomposition is a HITL QA verification task:

```
### Issue N: chore: manual QA verification

**Type:** chore
**Mode:** HITL
**Summary:** Verify all slices work together end-to-end
**Description:** Run through every user-observable change enabled by this spike.
  Confirm each slice integrates correctly and nothing was missed.
**Acceptance Criteria:** (generated per Step 2a below)
**Depends on:** all other issues
**Labels:** qa
```

### Step 2a: Generate the QA checklist

The QA task body contains a detailed checklist covering every user-observable change. Structure it
as checkboxes grouped by **feature flow**, then by **view/page** within each flow.

```markdown
## QA Checklist

### Flow 1: {Actor} -- {Goal}

#### {View / Page / Screen}

- [ ] {action} -> {expected observable outcome}
- [ ] {action} -> {expected observable outcome}

#### {Next View / Page}

- [ ] {action} -> {expected observable outcome}

### Flow 2: {Actor} -- {Goal}

#### {View / Page / Screen}

- [ ] {action} -> {expected observable outcome}

### Edge Cases

- [ ] {scenario} -> {expected outcome}
- [ ] {scenario} -> {expected outcome}
```

To generate:

1. **Enumerate every distinct actor** touched by the spike (provider/consumer, admin/user, etc.)
2. **For each actor, trace the full journey starting from zero** -- first step is creating or
   provisioning the resource, not interacting with something that already exists
3. **Group steps by the view/page/screen** where they happen
4. **Every observable change gets a checkbox** -- be exhaustive, not terse
5. **Order flows by dependency chain** -- what makes the feature exist precedes what uses it
6. Add edge cases at the end (non-obvious scenarios that could break)

## Step 3: Present for Approval

Show the full issue list with mode classification:

> **{N} issues from spike `{spike name}`:**
>
> 1. **{prefix}: {summary}** -- {type} -- {mode} -- {1-line description}
> 2. **{prefix}: {summary}** -- {type} -- {mode} -- {1-line description}
> ...
> N. **chore: manual QA verification** -- chore -- HITL
>
> Dependency order: 1 -> 2 -> 3 (4 and 5 independent) -> N (QA)

Ask: **"Adjust any issues, or approve to create?"**

Iterate until the user approves. They may want to merge, split, reorder, reclassify HITL/AFK,
or drop issues. The QA task is mandatory -- it cannot be dropped.

## Step 4: Create the Issues

Create issues in dependency order so real issue numbers can be referenced in `Blocked by` fields.

For each approved issue, create via `gh issue create`:

1. **Title:** `{type}: {summary}` using conventional prefixes
2. **Body:**

```markdown
## Parent Spike

#{spike-issue-number}

## Description

{description}

## Acceptance Criteria

- [ ] {criterion}

## Blocked By

#{blocker-issue-number} (if any)
```

3. **Labels:** from the issue draft

After creating all issues, present:

> **Created {N} issues:**
>
> 1. #N -- {summary} (AFK)
> 2. #N -- {summary} (HITL)
> ...

## Step 5: Edit Spike into Tracking Issue

Edit the spike issue (fallback: plan issue if no spike) to append a task list at the bottom:

```markdown
## Tasks

- [ ] #N -- {summary} (AFK)
- [ ] #N -- {summary} (AFK)
- [ ] #N -- {summary} (HITL)
- [ ] #N -- manual QA verification (HITL)
```

Use `gh issue edit` to append this to the spike issue body. This turns the spike into a tracking
issue -- GitHub will show progress as child issues are closed.

Present the final state:

> **Tracking issue:** #N (spike)
> **Work issues:** #N, #N, #N
> **QA issue:** #N
>
> Pick one to `/plan-it` or `/do-it`?

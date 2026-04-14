---
name: refactor-it
description: >
  Interview-driven refactor planning. Uses /grill-it to fully understand the problem, explores the
  repo to verify assertions, presents alternatives, hammers out scope, checks test coverage, and
  breaks the plan into tiny commits. Creates a GitHub issue with the full refactor plan. Use when
  the user says "refactor it", "refactor this", "clean this up", "restructure", or wants to improve
  existing code with a structured plan.
---

# Refactor It

Plan a refactor from problem statement to tiny-commit breakdown. Each commit leaves the code
working. Output is a GitHub issue with the full plan.

## Step 1: Understand the Problem

`$ARGUMENTS` may contain:

- **Issue reference** (e.g. `#42`) -- fetch from GitHub via `gh`
- **Module or area name** -- what the user wants to refactor
- **Description** -- what's wrong and why it needs to change

If unclear, use **AskUserQuestion**:

> What are we refactoring and why? Give me an issue, module name, or description.

## Step 2: Interview

Invoke `/grill-it` to fully understand:

- **What's the pain?** -- what specifically is hard to work with?
- **Why now?** -- what triggered this refactor? New feature blocked? Repeated bugs?
- **What's the desired end state?** -- how should the code look/behave after?
- **Scope boundaries** -- what's in and out?
- **Constraints** -- backwards compatibility? Feature flags? Migration path?
- **Success criteria** -- how do you know the refactor is done?

All questions resolved before proceeding.

## Step 3: Explore the Repo

Verify the user's assertions against reality:

1. **Find the code** -- locate the modules, interfaces, and contracts involved
2. **Assess current state** -- understand the existing structure and its trade-offs
3. **Check test coverage** -- what's tested? What's not? What tests will break?
4. **Identify dependents** -- what code depends on the interfaces being refactored?
5. **Look for patterns** -- is this problem repeated elsewhere? Should the refactor cover those too?

Present findings. Flag anything that contradicts the user's assumptions.

## Step 4: Present Alternatives

Propose 2-3 approaches with trade-offs:

> **Option A: {name}**
> {1-2 sentences}
> Trade-off: {what you gain vs what you lose}
>
> **Option B: {name}**
> {1-2 sentences}
> Trade-off: {what you gain vs what you lose}
>
> **Recommendation:** {which and why}

Discuss until the user picks an approach. If the user has a strong preference already, skip
straight to confirming their approach.

## Step 5: Break into Tiny Commits

Each commit must leave the code in a working state (Martin Fowler principle). No commit
introduces a regression.

For each commit, define:

```
### Commit N: {description}

**What changes:** 1-2 sentences -- behavioural description, not file paths
**Tests:** what tests change, get added, or should still pass
**Verification:** how to confirm this commit is correct in isolation
```

Order commits to minimise risk:

1. Add new structure alongside old (parallel)
2. Migrate callers one by one
3. Remove old structure
4. Clean up

## Step 6: Create the GitHub Issue

Create via `gh issue create`. Issue body uses durability principles -- no file paths.

```markdown
## Problem Statement

Why this refactor is needed. What pain it solves. What triggered it.

## Solution

The chosen approach from Step 4. High-level description of the end state.

## Commits

1. **{description}** -- {what changes}
2. **{description}** -- {what changes}
3. ...

## Decision Document

Key decisions made during the interview (Step 2) and alternatives considered (Step 4).
Captures *why* this approach was chosen so future readers understand the reasoning.

- **Decision:** {what was decided}
  **Alternatives considered:** {what was rejected and why}

## Testing Decisions

- What existing tests cover the affected area
- What new tests are needed
- What tests will change during the refactor

## Out of Scope

- Things explicitly excluded from this refactor
- Related improvements deferred to future work

## Acceptance Criteria

- [ ] {observable behaviour preserved or improved}
- [ ] All existing tests pass after each commit
- [ ] No commit introduces a regression
```

Label as `refactor`.

## Step 7: Confirm

> **Refactor plan: `{summary}`**
>
> **Issue:** #N
> **Commits:** {N} (each leaves code working)
>
> Ready to `/plan-it` or `/do-it`, or adjust?

## Guiding Principles

- **Every commit works** -- no "break it now, fix it later" commits
- **Parallel first, migrate, then remove** -- safest ordering for refactors
- **Verify assertions** -- explore the repo before trusting the user's mental model
- **Capture decisions** -- the Decision Document is as important as the plan itself
- **Durability** -- no file paths in issue body, domain language, behavioural descriptions

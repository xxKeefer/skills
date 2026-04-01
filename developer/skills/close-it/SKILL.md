---
name: close-it
description: >
  Wrap up a task: commit strategy, PR description with QA test plan, ready to copy-paste. Use when
  the user says "close it", "ship it", "wrap it up", "create a PR", "close out", or is done coding
  and wants to commit and prepare a PR description.
---

# Close It

Wrap up the current work: commits and a copy-paste-ready PR description with embedded QA test plan.

## Step 1: Assess the Branch

Run these in parallel:

```bash
git branch --show-current
git log --oneline main..HEAD
git diff --stat main..HEAD
git status
```

If there are no changes compared to main, tell the user and stop.

Extract from the diff:

- **Projects affected**
- **Change type** (feat, fix, refactor, test, chore)
- **Ticket key** from branch name or commit messages

## Step 2: Commit Strategy

If there are uncommitted changes, propose how to commit them.

**Single commit** when all changes serve one purpose:

```
git add <files>
git commit -m "type(scope): TICKET summary"
```

**Multiple commits** when changes span distinct concerns:

```
# Commit 1: description
git add <files>
git commit -m "type(scope): TICKET summary"

# Commit 2: description
git add <files>
git commit -m "type(scope): TICKET summary"
```

If a file has changes belonging to different commits, use `git add -p` with hunk instructions.

Present the commands and ask: **"Run these commits, or adjust?"**

Wait for confirmation. Execute only when approved.

## Step 3: Generate PR Description

After commits are clean, generate the PR description from the [template](PR_TEMPLATE.md).

Rules for the PR body:

- **Remove** any section with no relevant content — no empty sections
- **Delete** unchecked checkbox lines — never leave `[ ]` in output
- **Mark** applicable items with `[x]`
- **Screenshots**: only include if UI changed; suggest what to capture
- **Keep it terse** — every line adds value or gets cut

### QA Test Plan (embedded in PR body)

Generate the Manual Test Plan section within the PR description. Rules:

- One bullet per testable behaviour
- **Action → expected result** format
- Happy path first, then edge cases, then error states
- No component names, API endpoints, or framework specifics
- Terse — assume QA knows the app

## Step 4: Present Output

Output two sections:

### 1. Git Commands

If the user hasn't committed yet, the exact commands to run. If already committed, just note the push command:

```bash
git push -u origin $(git branch --show-current)
```

### 2. PR Description

The complete PR description, ready to copy into the GitHub PR form.

---

After presenting, ask: **"Adjust anything, or should I run the commits?"**

Do NOT automatically create commits, push, or open a PR. Wait for explicit instruction.

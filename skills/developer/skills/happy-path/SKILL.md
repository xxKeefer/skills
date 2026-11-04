---
name: happy-path
description: >
  Generate a manual QA test plan for the current changeset. Reads recent git changes to understand
  what was built, then produces a concise checklist the human can walk through. Use when user says
  "happy path", "qa plan", "test plan", "what should I test", or wants to manually verify before
  closing out.
---

# Happy Path

Produce a manual QA checklist for the current changeset.

## Step 1: Read the Changeset

Find the changeset:

1. If `$ARGUMENTS` holds a commit range, use it.
2. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. It prints
   `origin/<name>`. Fall back to `main`.
3. Off the default branch, diff against `git merge-base HEAD <default>`.
4. On the default branch, use the uncommitted diff, `git diff HEAD`.
5. If that diff is empty, ask the user for a range.

Read the `--stat` of the changeset to identify changed files, then its diff to understand what
changed. If `$ARGUMENTS` contains resource links, invoke `/look-up` for additional context.

## Step 2: Produce the Test Plan

Output a flat checklist grouped by feature or area. Each item is a concrete action + expected
result the human can verify in under a minute.

Format:

```
## QA: {short description of changeset}

### {area}
- [ ] {do X} → {expect Y}
- [ ] {do A} → {expect B}

### {area}
- [ ] {do X} → {expect Y}
```

Rules:
- Happy path first, obvious edge cases only if high risk
- No setup instructions the human already knows
- No automated-test-level detail — this is for eyes-on-screen verification
- Keep it under 15 items total. To stay under the cap, merge related changes into one item.

**Done when:** every user-visible change in the diff maps to a checkbox.

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

1. Run `git diff HEAD~3 --stat` to identify changed files
2. Run `git diff HEAD~3` to understand what changed
3. If `$ARGUMENTS` contains resource links, invoke `/look-up` for additional context

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
- Keep it under 15 items total

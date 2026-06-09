---
name: hunt-it
description: >
  Hunt down a bug from user-reported feedback, observed symptoms, or error logs. Combines critical
  assessment of the report (like /resolve-it) with structured investigation and a fix plan (like
  /plan-it). Use when the user says "hunt it", "hunt this bug", "track this down", "find the bug",
  "debug this", pastes an error or bug report, or wants to go from symptom to root cause to fix.
---

# Hunt It

Go from bug report to root cause to fix plan. Assess the report critically, investigate the
codebase, isolate the fault, then produce a plan to fix it.

## Step 1: Parse the Report

`$ARGUMENTS` may contain any combination of:

- **Error messages or stack traces** — pasted directly
- **Bug report / user feedback** — description of observed vs expected behaviour
- **Issue references** (e.g. `#42`) — fetch from GitHub via `gh`
- **PR URL or number** — fetch context from the PR
- **Log output** — runtime logs showing the failure
- **Screenshots or reproduction steps** — user-provided observations

If `$ARGUMENTS` is empty, use **AskUserQuestion**:

> What's the bug? Give me an error, stack trace, ticket, reproduction steps, or description.

## Step 2: Assess the Report

Do NOT take the report at face value. Apply critical evaluation:

- **Verify the symptom is real.** Can you reproduce the described behaviour from the code? Trace the
  code path — does the reported scenario actually occur?
- **Separate observation from interpretation.** The reporter says "X is broken" — but is X actually
  the problem, or is the failure upstream?
- **Check for stale information.** Has the code changed since the report was filed? Is the bug
  already fixed?
- **Identify what's missing.** What does the report NOT tell you? What assumptions is the reporter
  making?
- **Gauge confidence.** Rate how well-specified the bug is:
  - **Clear** — exact reproduction steps, expected vs actual, specific error
  - **Partial** — symptom described but cause unclear, missing reproduction steps
  - **Vague** — "it doesn't work", no specifics

Present your assessment:

```
## Bug Assessment

**Symptom:** <one-line summary of the reported problem>
**Confidence:** Clear | Partial | Vague
**Reporter's interpretation:** <what they think is wrong>
**My read:** <what I think is actually going on, or "aligned" if I agree>
**Missing info:** <what I'd need to confirm — or "none">
```

If confidence is **Vague**, use **AskUserQuestion** to get specifics before proceeding. Ask targeted
questions — not an open "tell me more".

## Step 3: Investigate

Search the codebase to trace the bug. Work from symptom to cause:

1. **Locate the symptom** — find the code path that produces the observed behaviour (error message,
   wrong output, crash site)
2. **Trace upstream** — follow data flow and control flow backward from the symptom. Where does the
   bad state originate?
3. **Check boundaries** — inspect inputs, type conversions, edge cases, error handling at each layer
4. **Look for related issues** — search for similar patterns elsewhere that may have the same flaw
5. **Read existing tests** — what's covered? What's missing? Is there a test that should have caught
   this?

Use Explore subagents for broad searches. Use targeted Grep/Glob for specific symbols.

After investigation, present findings:

```
## Root Cause

**Location:** <file:line or module>
**What happens:** <1-2 sentences — the actual fault>
**Why:** <1-2 sentences — why the fault exists (missing guard, wrong assumption, race condition, etc.)>
**Blast radius:** <what else is affected by the same root cause>
```

If the root cause is unclear, present your best hypothesis and what evidence supports or contradicts
it. Ask the user if they can confirm or provide additional context.

## Step 4: Create the GitHub Issue

Always create a GitHub issue as the output -- investigation findings and fix plan live in the
issue, not just the conversation. Use `gh issue create`.

Assess complexity to determine issue structure:

**Simple** (ALL true: scope is 1-3 files, fix is obvious, no architectural decisions):

Create a short issue and offer to `/do-it` immediately.

**Complex** -- create a full issue with TDD fix plan.

### Issue template

Use durability principles: no file paths or line numbers in the issue body. Describe modules,
behaviours, and contracts instead.

```markdown
## Problem

**Symptom:** one-line summary
**Confidence:** Clear | Partial | Vague
**Actual behavior:** what happens
**Expected behavior:** what should happen
**Reproduction:** steps if applicable

## Root Cause Analysis

Describe the modules, behaviours, and contracts involved -- NOT file paths or line numbers.
What assumption is wrong? What contract is violated?

## TDD Fix Plan

1. **RED**: test that captures the bug
   **GREEN**: minimal change to pass

2. **RED**: next behaviour (if multi-step)
   **GREEN**: minimal change

**REFACTOR**: cleanup if needed

## Acceptance Criteria

- [ ] Failing test captures the reported symptom
- [ ] Fix addresses root cause, not just symptom
- [ ] All new tests pass
- [ ] Existing tests still pass
- [ ] Blast radius checked -- no remaining instances of the faulty pattern
```

Label the issue as `bug`.

## Step 5: Confirm

Present the issue URL and summary:

> **Bug hunt: `{summary}`**
>
> **Issue:** #N
> **Root cause:** {one-line}
> **Fix:** {simple: 1-liner | complex: N RED-GREEN cycles}
>
> Ready to `/do-it`, or adjust anything?

Wait for the user. If they want changes, edit the issue. If they want to execute, suggest `/do-it`.

## Guiding Principles

- **Prove, don't guess.** Every claim about root cause must be backed by a code path you traced.
  If you're hypothesising, say so explicitly.
- **One bug at a time.** If investigation reveals multiple bugs, isolate each one. Fix the reported
  bug first; file the others as separate work.
- **The first failing test is the most important step.** A bug without a regression test is a bug
  that comes back. The fix plan always starts with RED.
- **Suspect the report.** Bug reports are symptoms filtered through human interpretation. The
  reporter may be wrong about what's broken, where it's broken, or why. Verify independently.
- **Check the fix doesn't mask the bug.** A fix that silences the symptom without addressing the
  cause is not a fix. Trace all the way to the root.

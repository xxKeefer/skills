---
name: tdd
description:
  Test-driven development with the red → green loop. Use when the user wants to build a feature or
  fix a bug test-first (TDD), mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

Principle: **principle-test-behavior-not-implementation** ([`../principle-test-behavior-not-implementation/SKILL.md`](../principle-test-behavior-not-implementation/SKILL.md)). Read its file before you apply it, and name it in the reply when it shaped a choice.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Agreement on the seams puts the test effort on the critical paths and the complex logic, not on every edge case.

- A seam that the plan step names is agreed. Test at it, and ask nothing about it. Test the conditions whose IDs the step names.
- Confirm each other seam with the user before you write a test at it. Ask: "What is the public interface, and which seams do we test?"

To rate the risk, derive the test conditions, and pick the level of each test, use [`TEST-APPROACH.md`](../../TEST-APPROACH.md).

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **A test that was never red is a smell.** When a new test passes on its first run, test the same fact in another way that goes red first. Else, break the code that the test covers, see the test go red, and restore the code. If the test does not go red, delete it.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage, not the red → green implementation cycle.

## When to skip a test

TDD is the default. Skip a test only for one of these reasons:

- **Expensive.** The test costs far more to write or run than the risk it covers.
- **Integration-heavy.** The test needs live services, a device, or a setup that the repo cannot run.
- **Unclear.** The expected behaviour is not known yet, so a test would only guess.

A skip never replaces the check. Use the closest real check instead: run the real artifact and read
the result. When the repo has a `/verify` driver for the change, run it.

A skip is never silent. The plan step stays in the plan. Mark it `[-]`, and add the reason under it:

```
- [-] **3. Step title.**
  - Skipped: <reason>. Check used: <the closest real check, and its result>.
```

`/sitrep` shows each skipped step. If the plan has no step for the change, add one before you skip it.

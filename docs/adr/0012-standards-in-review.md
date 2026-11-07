# 0012 Coding standards live in review

**Status:** Accepted, 2026-11-07. Builds on ADR 0011.

## Context

The implementation skills carried coding standards of their own. `sync-docs` checked comments and
names. `tdd` listed test anti-patterns, with `tests.md` and `mocking.md` behind them. The
`squash-bugs` fix step said which layer owns a fix. The review panel checks the same things, so
each standard lived in two places, and an implementation step spent effort on rules that a review
checks again anyway.

## Decision

Implementation skills make the code work. The review step holds the coding standards, and a fix
round after the review applies them.

- `sync-docs`, `tdd`, and `squash-bugs` drop their standards. `tdd` keeps the seams and the rules of
  the red-green loop, because a diff cannot show how the tests were written.
- A new `persona-test-quality` reviews tests in any language: coupling to the implementation, mocks
  of the project's own code, expected values that restate the code, and tests that pass when the
  feature breaks. `tests.md` and `mocking.md` move to its `references/`. It runs in `mob-review`
  and `light-review`.
- In a handoff, the review report's prompt runs `/developer:run-wave`. It adds a fix step for each
  ticked row and a new review step, then runs them. The user reads each report, and loops:

  ```
  plan → run-wave → review → tick rows → run-wave → review → ... → tick nothing → draft PR
  ```

- The user decides when to stop, in each round. Ticking nothing ends the loop.
- `run-wave` runs the push step itself, through `/create-pr`, which opens a draft PR. It never marks
  the PR ready.

## Consequences

- An implementation step can write code that breaks a standard. The review catches it, so expect a
  fix round on most tickets.
- Each round costs a full review. `light-review` is the cheaper round when the change is small.
- A standard that no persona checks is now checked nowhere. Before you cut a standard from an
  implementation skill, name the persona that owns it.
- Outside a handoff, the ticks still build the `/code-review:apply-review` prompt.

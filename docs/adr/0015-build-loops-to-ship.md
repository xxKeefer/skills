# 0015 Build loops to ship

**Status:** Accepted, 2026-11-13. Replaces the `build` line of ADR 0013.

## Context

ADR 0013 made `/build` run one step with `/do-next`, and kept `/run-wave` as the skill that runs
every step. So the command for the build phase did the smaller job, and the larger job had a name
outside the lifecycle line. After the build steps, the user still started `/test` and `/review` by
hand, and ran `/run-wave` again for each fix round.

An `implement` skill already existed. It implemented a spec or tickets with `/tdd`, and no command
ran it.

## Decision

- `/implement` runs one step of a plan handoff with `/do-next`. With no handoff, it implements a
  spec or tickets with `/tdd`, as the old skill did. It is not a command, so the model can call it.
- `/build` takes the steps of `/run-wave` and its `STEP.md`. It runs every remaining step, then
  loops a test step and a review step until the branch passes the `/ship` checks. `/run-wave` is
  gone.
- The test step runs the test suite, and adds a test for each changed behaviour that no test
  covers. The manual QA checklists of `/happy-path` and `/sad-path` cannot run with no user, so
  `/build` writes them once, after the loop.
- A new round starts only when the review's fix commit changes runtime behaviour. The loop stops
  after three review steps in one run.
- A Change Requested row that stays open needs the user, because the review already fixed each row
  that has a fix. It becomes a `D` entry, and the loop stops.
- `/build` never runs the push step. `/ship` checks the branch and opens the PR.

## Consequences

- One command takes a plan handoff to a branch that is ready for `/ship`.
- A review report's prompt runs `/engineering:build`, not `/engineering:run-wave`.
- `/ship` accepts a review of an earlier head when each later commit is a review fix step. A fix
  round that changes no behaviour adds no new review.
- The engineering plugin goes to 2.0.0, because `/run-wave` is gone.

---
name: principle-never-block-on-the-human
description: "Folded into /work-on."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Never Block on the Human

The user supervises later, not in the loop. Stay unblocked. Make a reasonable decision, proceed, and let the user correct course after the fact. Code changes are reversible and reviewable, so a wrong decision usually costs less than a block.

- Proceed, then present. Do the work and show the result. Do not ask "should I do X?" Do X, and say why.
- Make the system heal itself. When you see a problem, record it and fix it in the next round.
- Reversible work proceeds with no stop. This covers code, notes, and splitting a task.
- Product direction comes from the user. Execution does not wait for it.

The stop is on the action, not on the task. The pause list in the `pause-list.md` rule holds each action that stops for a yes from the user: an action whose output another person reads, such as a merge, a deploy, a force-push to a shared branch, a posted comment, or a message to a person. Stop at those. Run everything else with no stop.

When you cannot decide, do not block the run. Write a `D` entry under `## Pending Decisions` in the plan, and continue with the steps that do not depend on it.

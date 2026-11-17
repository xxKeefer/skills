---
name: principle-make-operations-idempotent
description: "Apply when you design commands, lifecycle steps, or loops that run amid crashes, restarts, and retries. Converge to the same end state whatever an earlier run left behind."
disable-model-invocation: true
---

# Make Operations Idempotent

Design each operation that changes state so that it reaches the correct state however many times it runs, and wherever the last run stopped.

Derive each step from the state that exists, not from what the last run meant to do. Read the current state, compare it to the goal, and apply only the difference.

Anything that a run leaves behind must be recognisable as stale by the next run. This covers a lock, a temporary file, a half-written record, and a claimed job. The evidence must hold wherever the last run could have stopped. Write to a temporary path, then rename it into place.

Ask two questions. What happens if this runs twice? What happens if the last run crashed at each possible point? If the answer depends on what the run left behind, add a reconciliation step.

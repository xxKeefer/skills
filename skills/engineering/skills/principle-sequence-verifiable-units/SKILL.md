---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break the work into small units that each end in a check, and verify each one before the next."
disable-model-invocation: true
---

# Sequence Work into Verifiable Units

Order the work as small units. Each unit ends in a state that you can check. Do not move on until the current unit is green.

In a sweep, a migration, or a run of similar edits, each unit is a bracket: a known-good state, one change, the check, then the next unit. Run the check for each unit even when a tool makes the edits.

Deliver in the order that proves the work. Put the failing test before the fix. Put the subtraction before the reshape. Put the baseline before the treatment. Each commit lands on its own.

Scaffold first. After you remove dead code, do the work that helps every later unit, such as CI, tests, and shared types, before the features.

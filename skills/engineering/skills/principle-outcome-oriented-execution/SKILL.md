---
name: principle-outcome-oriented-execution
description: "Apply during a planned rewrite or migration with explicit phase boundaries. Converge on the target architecture, and do not keep a stable middle state with throwaway compatibility code."
disable-model-invocation: true
---

# Outcome-Oriented Execution

Aim for the intended end state that you can verify. Do not keep every middle state smooth.

**Why:** a plan that keeps every middle step fully stable often adds compatibility code that becomes long-lived debt. Converge on the target architecture, and prove it is correct at explicit verification points.

**Core rule:**

- Put the integrity of the end state before the stability of the middle.
- Break the middle only when the break is planned, scoped, and reversible.

**Guardrails:**

- Use this for a planned rewrite or migration with explicit phase boundaries.
- Declare where a temporary break is acceptable.
- Keep high-signal checks on the areas that you change during the migration.
- Require full static and runtime checks when the plan is complete.

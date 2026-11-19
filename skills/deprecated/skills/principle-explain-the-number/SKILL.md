---
name: principle-explain-the-number
description: "Folded into /benchmark."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Explain the Number

- **Write the decision before you run.** Name the result that would change the decision, and name the noise floor. Stop when the spread between runs is larger than the effect.
- **Ask why the number is not double.** Name the resource or code path that bounds the result, from a profile or counters taken during a run. A guess from the code is not a limiter.
- **List what else the number could measure.** Examples are errors, skipped or cached work, code that never ran, an untuned side, noise, and a part too small to matter. Rule out each one with evidence.
- **Keep the run count, the spread, and the limiter with the number.**

For an eval result, ask three things. Did every run do the task? Does the gap hold across trials and models? Does the scenario matter?

---
name: principle-fix-root-causes
description: "Apply when you debug, or when two or more fixes that share one premise have failed the same gate. Trace each symptom back to the first place the system went wrong, and fix it there. Test a shared premise before the next fix."
disable-model-invocation: true
---

# Fix Root Causes

Fix the fault, not the place where it showed. The root cause is the first place where the system did something it should not do, or failed to handle a state that it should handle.

- Reproduce first. Ask why until the answer is a wrong decision in the code. When you are stuck, add instrumentation and read the actual state.
- Ask if the state that caused the symptom is legitimate. If it is, handle it where the code broke. If it should never exist, a check there hides the bug, so find what made it. Guards, retries, swallowed errors, clamped values, and discarded state are the usual ways to hide a bug.
- Fix the pattern, not the instance. Find every place with the same fault.
- If the deciding fact took a deep dig, propose the cheap, always-on signal that would have shown it at first look.

## When fixes keep failing

When two or more fixes that share one premise have failed the same gate, suspect the premise. Do not suspect the fixes.

- Write the premise down. It is the one sentence that every failed fix assumed.
- Test it before the next fix. Find an observation that comes out differently if the premise is false, and make it. Look at how the failures spread, not only at how large they are.
- If the evidence contradicts the premise, look for what the failures share that the premise did not predict. If one part always lands on the losing side, change what puts it there. Do not add a mechanism that cleans up after it.

Do not start the next fix until the premise is written down and tested.

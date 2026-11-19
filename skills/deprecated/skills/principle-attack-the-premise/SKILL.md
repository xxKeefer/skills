---
name: principle-attack-the-premise
description: "Merged into principle-fix-root-causes."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Attack the Premise

When two or more fixes that share one premise have failed the same gate, suspect the premise. Do not suspect the fixes.

- Write the premise down. It is the one sentence that every failed fix assumed.
- Test it before the next fix. Find an observation that comes out differently if the premise is false, and make it. Look at how the failures spread, not only at how large they are.
- If the evidence contradicts the premise, look for what the failures share that the premise did not predict. If one part always lands on the losing side, change what puts it there. Do not add a mechanism that cleans up after it.

Do not start the next fix until the premise is written down and tested.

---
name: principle-foundational-thinking
description: "Retired. Its rules live in principle-model-the-domain, principle-sequence-verifiable-units, and principle-separate-before-serializing-shared-state."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Foundational Thinking

Get the data shape right before you write logic. Define the core types early. Trace every access pattern. Choose the structures that match the dominant paths. Remove duplication in the structure, not in every line.

Before you share state between actors, ask what happens if another actor changes it at the same time. If the answer is not "nothing", isolate the state.

Scaffold first. Do the work that helps every later phase (CI, tests, shared types) before the features, after you remove dead code. Keep commits small and single-purpose.

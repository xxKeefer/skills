---
name: principle-foundational-thinking
description: "Apply before you write logic: when you choose core types and data structures, order scaffold and feature work, or ask what concurrent actors share."
disable-model-invocation: true
---

# Foundational Thinking

Get the data shape right before you write logic. Define the core types early. Trace every access pattern. Choose the structures that match the dominant paths. Remove duplication in the structure, not in every line.

Before you share state between actors, ask what happens if another actor changes it at the same time. If the answer is not "nothing", isolate the state.

Scaffold first. Do the work that helps every later phase (CI, tests, shared types) before the features, after you remove dead code. Keep commits small and single-purpose.

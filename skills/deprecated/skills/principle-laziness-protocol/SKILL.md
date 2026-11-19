---
name: principle-laziness-protocol
description: "Merged into principle-subtract-before-you-add."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth, and pass the result as a simple flag.
- **Minimise the diff.** Make the smallest change that solves the problem. Fewer lines beat elegant boilerplate.

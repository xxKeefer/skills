---
name: principle-laziness-protocol
description: "Apply when you refactor, size a diff, or want to add an abstraction, a layer, or a signal that threads through the code. Prefer deletion and the smallest change that solves the problem."
disable-model-invocation: true
---

# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth, and pass the result as a simple flag.
- **Minimise the diff.** Make the smallest change that solves the problem. Fewer lines beat elegant boilerplate.

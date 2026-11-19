---
name: principle-subtract-before-you-add
description: "Apply when you order an addition, a refactor, or a rewrite, size a diff, or want to add an abstraction, a layer, or a signal that threads through the code. Remove dead weight first, then make the smallest change on the simpler base."
disable-model-invocation: true
---

# Subtract Before You Add

When a system changes, remove complexity first. Then build. Default to subtraction.

Treat simplification as a continual investment. Leave the design a little simpler and a little more capable, behind the same surface or a smaller one.

- Put removal before construction.
- Cut before you polish. Reach the minimum before you invest in quality.
- Design for the usage that you see, not for speculative edge cases.
- Add no validator, parser, or guard beyond what the spec needs.
- Simplify prompts. Remove redundant instructions and excess templates.
- When a reference has no new content, delete it. Do not leave a stub.
- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth, and pass the result as a simple flag.
- **Minimise the diff.** Make the smallest change that solves the problem. Fewer lines beat elegant boilerplate.

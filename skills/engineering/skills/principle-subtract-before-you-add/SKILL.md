---
name: principle-subtract-before-you-add
description: "Apply when you order an addition, a refactor, or a rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
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

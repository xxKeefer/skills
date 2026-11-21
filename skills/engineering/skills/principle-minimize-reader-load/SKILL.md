---
name: principle-minimize-reader-load
description: "Apply when you review or shape code that is hard to trace. Count the layers between the question and the answer, and the hidden state a reader must hold. Collapse one-caller wrappers and shrink mutable scope."
disable-model-invocation: true
---

# Minimize Reader Load

Reader load is the work that a reader does to understand code. It has two independent axes: the layers to trace between the question and the answer, and the hidden or mutable state to keep in mind. Guard both.

- Collapse layers that only forward. Examples are a wrapper with one caller, an adapter with no second implementation, and a pass-through method. Inline them.
- Shrink the scope of state. Prefer returns to mutations, locals to fields, fields to module state, and module state to globals. Derive a value instead of syncing it.
- Name an invariant once at the boundary, not in every consumer.

The test: can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds? If not, cut layers or cut state.

---
name: principle-boundary-discipline
description: "Apply when wiring validation, error handling, or framework adapters. Put guards at system boundaries, trust internal types, and keep business logic in pure functions."
disable-model-invocation: true
---

# Boundary Discipline

Validate, narrow types, and handle errors where data crosses a system boundary. The boundaries are CLI arguments, config files, external APIs, and the network. Inside the boundary, trust the types. Do not validate again and do not add redundant null checks.

- Parse raw data into domain types at the boundary.
- Keep transport and framework types out of the public surface.
- Put business logic in pure functions with no framework dependency. The shell that calls them stays thin.

Ask two questions:

- Does this data cross a boundary right now? If not, the validation is redundant.
- Can this be a pure function that the shell calls? If yes, extract it.

---
name: principle-type-system-discipline
description: "Apply when you design types, review a function signature, write code in a statically typed language, or wire validation, error handling, or framework adapters. Make illegal states impossible to represent, guard at system boundaries, and trust internal types."
disable-model-invocation: true
---

# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants.

- **Brand semantic primitives.** If two arguments share a primitive type but mean different things, give each its own type. Validate once, when you create the value.
- **External data is untyped until parsed.** JSON, RPC payloads, CLI arguments, config, environment variables, and database rows go through a parse function at the boundary. The function returns the typed model.
- **Make illegal states impossible to represent.** Use a union of variants, and handle every variant.
- **Derive types from the authoritative schema.** When a schema file owns a shape, derive the type from it. Do not write a parallel type by hand.

## Boundaries

Validate, narrow types, and handle errors where data crosses a system boundary. The boundaries are CLI arguments, config files, external APIs, and the network. Inside the boundary, trust the types. Do not validate again and do not add redundant null checks.

- Keep transport and framework types out of the public surface.
- Put business logic in pure functions with no framework dependency. The shell that calls them stays thin.

Ask two questions:

- Does this data cross a boundary right now? If not, the validation is redundant.
- Can this be a pure function that the shell calls? If yes, extract it.

For TypeScript, follow the `typescript-conventions` rule.

---
name: principle-type-system-discipline
description: "Apply when you design types, review a function signature, or write code in a statically typed language. Make illegal states impossible to represent, and parse external data at the boundary."
disable-model-invocation: true
---

# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants.

- **Brand semantic primitives.** If two arguments share a primitive type but mean different things, give each its own type. Validate once, when you create the value.
- **External data is untyped until parsed.** JSON, RPC payloads, CLI arguments, config, environment variables, and database rows go through a parse function at the boundary. The function returns the typed model.
- **Make illegal states impossible to represent.** Use a union of variants, and handle every variant.
- **Derive types from the authoritative schema.** When a schema file owns a shape, derive the type from it. Do not write a parallel type by hand.

For TypeScript, follow the `typescript-conventions` rule.

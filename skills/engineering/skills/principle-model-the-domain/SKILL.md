---
name: principle-model-the-domain
description: "Apply when you write stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure, not in scattered conditionals."
disable-model-invocation: true
---

# Model the Domain

Encode the domain in a data structure, not in scattered conditionals. The right structure makes an invalid state impossible to represent, and it deletes branches.

Get the data shape right before you write logic. Define the core types early, trace every access pattern, and choose the structures that match the dominant paths. Remove duplication in the structure, not in every line.

Use a state machine, not scattered booleans or phase checks. Use a typed model, not loose parameters. Use a map, a registry, or a discriminated union, not branching spread over files. Use a reducer, not ad hoc mutations. Use an index, a queue, or a normalised collection where the access pattern needs one.

Do not force it. Keep plain code when the shape is clear, local, and unlikely to grow. Distrust an abstraction that adds indirection and removes no branch or invalid state.

The sign that you skipped this principle: a feature that grows an if/else chain by one more branch, or a second boolean that must stay in sync with the first.

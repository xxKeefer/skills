---
name: principle-separate-before-serializing-shared-state
description: "Apply when concurrent actors share state, or might write to the same file, branch, key, or object. Remove the sharing first. Serialise access only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate Before Serializing Shared State

Before you share state between actors, ask what happens if another actor changes it at the same time. If the answer is not "nothing", isolate the state.

When concurrent actors might write the same file, branch, key, or object, ask first if they need one shared object. They may only publish independent facts. Give each actor its own file, key, branch, or state folder by default, and merge only where the state is read. Two workers that write their own field into one `state.json` still share a mutation.

Serialise access only when one shared write target is a real invariant. Use a structure: a lockfile, a single writer, sequential phases, or compare-and-swap. An instruction is not concurrency control. Treat "we need a lock" as a smell to check first.

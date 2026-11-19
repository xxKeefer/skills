---
name: principle-test-behavior-not-implementation
description: "Folded into /tdd."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Test Behavior, Not Implementation

A test is a claim about what the users of the code can observe through its interface. That means return values, errors, state they can read back, and effects on outside systems. Private helpers, internal call order, and middle data are implementation.

Judge each test against two imagined edits:

- **Break the behaviour.** Use a wrong value, or a skipped or doubled effect. If the test still passes, it proves nothing. The usual causes are a loose assertion, an expected value that the code under test computes, and an assertion on data that the test built.
- **Change the internals** and keep every observable result. If the test fails, it is pinned to the implementation.

Keep a test that catches the first edit and survives the second. Rewrite or delete the others.

- Drive the code through its public interface with a concrete input. Take the expected value from the requirement.
- What an external service receives is behaviour. A call to an internal helper is not.
- Pair "this never happens" with a case where it does happen.
- Assert the error type that callers branch on, not the message.

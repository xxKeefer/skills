---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Merged into principle-redesign-from-first-principles."
disable-model-invocation: true
deprecated: 2026-11-19
---

# Migrate Callers Then Delete Legacy APIs

When a new internal API replaces an old one, migrate every caller and delete the old API in the same wave. Do not keep a compatibility layer.

- Update the tests to assert the new contract. Delete the tests that only protect details of the old implementation.

This applies when all of these hold:

- No external user depends on backward compatibility.
- The project can absorb a coordinated breaking change.
- The new API is part of a simplification or a refactor.

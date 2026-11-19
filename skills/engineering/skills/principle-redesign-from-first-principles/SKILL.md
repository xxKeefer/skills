---
name: principle-redesign-from-first-principles
description: "Apply when you fit a new requirement into an existing design, run a planned rewrite or migration, or add a new internal API while old callers exist. Redesign as if the requirement had been a base assumption, converge on the target, and delete the old API in the same wave."
disable-model-invocation: true
---

# Redesign From First Principles

When you fit a change into a design, do not bolt it on. Redesign as if the requirement had been a base assumption from the start.

- Read all the affected files, and understand the current design.
- Ask: if we wrote this from scratch with this requirement, what would we build?
- Carry the change through every reference: types, docs, examples, and rationale sections.
- Think about the whole redesign, then deliver it in small steps.

This method keeps your options open when you change an existing design.

## Converge on the end state

In a planned rewrite or migration with explicit phase boundaries, aim for the end state that you can verify. Do not keep every middle state smooth, because compatibility code for a middle state becomes long-lived debt.

- Put the integrity of the end state before the stability of the middle.
- Break the middle only when the break is planned, scoped, and reversible. Declare where a temporary break is acceptable.
- Keep high-signal checks on the areas that you change during the migration.
- Require full static and runtime checks when the plan is complete.

## Migrate callers, then delete the old API

When a new internal API replaces an old one, migrate every caller and delete the old API in the same wave. Do not keep a compatibility layer. Update the tests to assert the new contract, and delete the tests that only protect details of the old implementation.

This applies when all of these hold: no external user depends on backward compatibility, the project can absorb a coordinated breaking change, and the new API is part of a simplification or a refactor.

---
doctype: spec
ticket: none
status: confirmed
goal: "`/install-rules` installs the TypeScript rule."
---

# Spec: TypeScript rules

## Intent

- Outcome: `install-rules/rules/typescript-conventions.md` holds the type rules: branded primitives, discriminated unions, exhaustive checks with `never`, `satisfies` before `as`, parse at the boundary, and the simplest total type. Each rule cites the principle behind it.
- User: the user, and any agent that edits a TypeScript file. `principle-type-system-discipline` already says "For TypeScript, follow the `typescript-conventions` rule", but the rule has no type section.
- Why now: map unit 23 (r1.14).
- Success: `/install-rules` installs the rule, and the installed file holds each type rule.
- Constraint: a rule is the one exception to everything-agnostic, so it can name TypeScript. It names no employer code. It loads only for `paths:` that match TypeScript files.
- Out of scope: a change to the other rule files, to `install-rules/SKILL.md`, or to a principle.

## Decisions

- Extend the existing `typescript-conventions.md`, and make no new file: the unit names that path, and a second TypeScript rule would load twice for the same files.
- Cite each principle by name, such as `principle-type-system-discipline`, not by a relative path: the rule installs to `~/.claude/rules/`, where a path to a skill folder does not resolve. The user can type the name as a command.
- Map Decisions, Principles: the agent reads a principle by path before it applies it, and cites only a principle it read.

## Acceptance criteria

- [ ] **A.** Read `typescript-conventions.md` → it has a type section with six rules: branded primitives, discriminated unions, exhaustive checks with `never`, `satisfies` before `as`, parse at the boundary, and the simplest total type.
- [ ] **B.** Read `typescript-conventions.md` → each of the six rules names the principle behind it.
- [ ] **C.** Run the `/install-rules` steps → the installed `typescript-conventions.md` matches the source, byte for byte.

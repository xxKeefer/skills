# persona-best-practice: deps versioning rules

**Deps versioning**
- Flag imports from a **different major** than the installed one, e.g. `import … from 'zod/v4'` while zod is pinned to v3 (the `zod/v4` path doesn't exist → build/typecheck fails). Match the installed major.
- **A repo may run two majors of one library on purpose** (e.g. zod 3 and zod 4, with zod 4 reached through an npm alias such as `zod4`, declared in specific packages). Check `package.json` first. An import from the alias in a package whose `package.json` declares it is **correct: do not flag it**. Flag only the broken shapes: an import from the alias in a package that does *not* declare it (unresolvable specifier), and a v4-only zod API (`z.interface`, `z.strictObject` top-level, the `@zod/mini` entry) called on a plain `'zod'` import that resolves to v3. Change Requested.

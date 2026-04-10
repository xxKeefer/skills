---
name: setup-guard-rails-typescript
description: >
  Set up pre-commit hooks with Husky and lint-staged to enforce formatting, type checking, and tests
  before every commit. Gives agents deterministic feedback loops they cannot bypass. Use when user
  says "setup guard rails", "add pre-commit hooks", "enforce feedback loops", or wants to prevent
  agents from committing broken code in a TypeScript project.
---

# Setup Guard Rails (TypeScript)

Install pre-commit hooks that deterministically enforce code quality on every commit. Agents cannot
bypass these -- a failing typecheck or test blocks the commit and reports the error back.

## Step 1: Assess Current State

Check what already exists:

- **Package manager** -- detect pnpm/npm/yarn from lockfile
- **TypeScript** -- confirm `tsconfig.json` exists
- **Test runner** -- look for vitest/jest config
- **Formatter** -- check for prettier/biome config
- **Existing hooks** -- check for `.husky/` or other git hook setups
- **Scripts** -- check `package.json` for `typecheck` and `test` scripts

If TypeScript or a test runner is missing, stop and tell the user -- this skill assumes both are
present. If a `typecheck` script is missing, add `"typecheck": "tsc"` to `package.json` scripts.
If a `test` script is missing, add one for the detected test runner (e.g. `"test": "vitest"`).

## Step 2: Install Dependencies

Install `husky` and `lint-staged` as dev dependencies using the detected package manager.

Run `husky init` to scaffold the `.husky/` directory.

## Step 3: Configure lint-staged

Create `.lintstagedrc` (or add to `package.json` -- match existing project conventions):

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

Adapt to the project:

- If biome is used instead of prettier, swap the command
- If ESLint is configured, add it before the formatter

## Step 4: Configure the Pre-Commit Hook

Write `.husky/pre-commit` to run three checks in order:

1. **`npx lint-staged`** -- format staged files
2. **Type check** -- `npm run typecheck` (adapt to package manager)
3. **Tests** -- `npm run test` (adapt to package manager)

If the project has a monorepo structure, scope the typecheck and tests to affected packages where
possible.

## Step 5: Verify

1. Do a dry run -- stage a file and commit to confirm all three hooks execute and pass
2. Introduce a deliberate type error, attempt to commit, confirm it's blocked
3. Revert the type error

Report which checks are now enforced and confirm the hook is working.

## Step 6: Commit

Commit all setup files (husky config, lint-staged config, package.json changes, lockfile).

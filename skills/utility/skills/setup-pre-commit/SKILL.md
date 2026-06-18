---
name: setup-pre-commit
description: >
  Detect project language and toolchain, then configure pre-commit hooks that enforce formatting,
  type checking, and tests. Gives agents deterministic feedback loops they cannot bypass. Use when
  user says "setup pre-commit", "setup guard rails", "add pre-commit hooks", "enforce feedback
  loops", or wants to prevent agents from committing broken code.
---

# Setup Pre-Commit

Detect the project's language and toolchain, then install pre-commit hooks that deterministically
enforce code quality on every commit. Agents cannot bypass these -- a failing check blocks the
commit and reports the error back.

## Step 1: Detect Project Stack

Scan the project root to determine:

- **Language** -- look for `tsconfig.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`,
  `requirements.txt`, `mix.exs`, `Gemfile`, etc.
- **Package manager** -- lockfiles (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`,
  `Cargo.lock`, `go.sum`, `poetry.lock`, etc.)
- **Formatter** -- prettier, biome, rustfmt, gofmt, black, ruff, mix format, etc.
- **Linter** -- eslint, clippy, golangci-lint, ruff, credo, rubocop, etc.
- **Type checker** -- tsc, mypy, pyright, dialyzer, etc. (if applicable)
- **Test runner** -- vitest, jest, cargo test, go test, pytest, mix test, rspec, etc.
- **Existing hooks** -- `.husky/`, `.pre-commit-config.yaml`, `.lefthook.yml`, git hooks dir
- **Existing scripts** -- check for `typecheck`, `test`, `lint`, `format` scripts/tasks

Present findings and proposed hook strategy:

> **Detected:** {language} with {package manager}
> **Formatter:** {tool} | none detected
> **Linter:** {tool} | none detected
> **Type checker:** {tool} | not applicable
> **Test runner:** {tool} | none detected
> **Existing hooks:** {tool} | none
>
> **Proposed checks:**
> 1. {format step}
> 2. {lint step}
> 3. {typecheck step} (if applicable)
> 4. {test step}
>
> Proceed?

If critical tools are missing (no test runner, no formatter), flag it and ask how to proceed.

## Step 2: Install Hook Infrastructure

Based on detected stack:

### JavaScript / TypeScript
- Install `husky` + `lint-staged` via detected package manager
- Run `husky init`

### Python
- Install `pre-commit` framework (`pip install pre-commit` or add to dev dependencies)
- Run `pre-commit install`

### Rust
- Use `cargo-husky` or a shell-based git hook

### Go
- Use `lefthook` or a shell-based git hook

### Other
- Fall back to a shell script in `.git/hooks/pre-commit` or use `lefthook`/`pre-commit` framework

## Step 3: Configure Checks

Configure the hook to run checks in order:

1. **Format** -- staged files only where possible (lint-staged, pre-commit framework)
2. **Lint** -- if a linter exists
3. **Type check** -- if applicable to the language
4. **Tests** -- run the test suite

Adapt to project conventions -- use existing scripts/tasks where they exist rather than
inventing new ones. If a monorepo, scope checks to affected packages where possible.

## Step 4: Verify

1. Stage a file and commit -- confirm all hooks execute and pass
2. Introduce a deliberate error (type error, lint violation, or failing test)
3. Attempt to commit -- confirm it's blocked with a clear error message
4. Revert the deliberate error

Report which checks are enforced and confirm the hook is working.

## Step 5: Commit

Commit all setup files (hook config, formatter config if new, package/dependency changes,
lockfile updates).

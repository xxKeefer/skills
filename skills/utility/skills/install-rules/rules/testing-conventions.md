---
paths:
  - "**/*.spec.ts"
  - "**/*.test.ts"
  - "**/*.mocks.ts"
  - "**/tests/**"
---

## Testing Rules

- Test behaviour, not styling. **NEVER** assert on CSS classes, Tailwind tokens, or rendered `innerHTML` to check appearance.
- Visual/style regressions belong to snapshot testing, not unit tests.
- Assert what the user perceives: roles, accessible names, text, enabled/disabled state, ARIA attributes, emitted events.
- For a disabled control, assert the disabled state via the accessibility tree (`toBeDisabled()`, `aria-disabled`), not the class that styles it.
- **`vitest --related` no longer exists.** Vitest 4 removed the flag, and the command crashes with `CACError: Unknown option --related`. Scope a run by explicit spec path, by directory, or with `--changed origin/main`.

### MSW Handlers and Mock Fixtures

- MSW handler files live with the integration mocks (e.g. `tests/integration/mocks/handlers/`), never under `src/`. `msw` is a devDependency — a handler file under `src/` becomes a bundle trap for any production import that reaches it.
- Colocated `src/**/*.mocks.ts` files hold **fixtures and builders only** and must not import `msw`.
- **Never re-export contract/API types from a `*.mocks.ts` file.** Import types from their source module so production code never routes through mock files.
- Unit specs may import handlers from the integration handlers folder and register them with their own `setupServer()`.
- Stateful handlers (in-memory dbs) are not registered in the shared `mocks/server.ts` — seed a fresh db per test instead.

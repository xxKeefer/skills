# TypeScript: modern-API reference (written against 6.0.2)

This file was written against TS **6.0.2**. Flag legacy patterns where a
first-class modern form exists.

## Type-only imports

`import type { X }` or inline `import { type X }` for type-only imports
(verbatim-module-syntax / `isolatedModules` expectations). Mixing a type into a value import
that gets erased → **Nit**.

```ts
import type { IconDefinition } from '@fortawesome/...'   // ✅
import { type Ref, ref } from 'vue'                       // ✅ inline
```

## `satisfies` over widening annotation

Use `satisfies T` when literal inference should be preserved (config objects, route records,
CVA variant maps) instead of a widening `: T` annotation. → **Nit**.

```ts
const routes = [{ path: '/', name: 'home' }] satisfies RouteRecordRaw[]  // ✅ keeps literals
```

## No `enum`

Prefer an `as const` object + derived union, or a plain string-literal union, over `enum`
(enums emit runtime code, aren't tree-shakeable, and have nominal-typing surprises). Using
`enum` in changed code → **Change Requested**.

```ts
// ✅
const Variant = { primary: 'primary', danger: 'danger' } as const
type Variant = (typeof Variant)[keyof typeof Variant]
// ❌  enum Variant { primary, danger }
```

## Other 6.0-era niceties

- `const` type parameters (`<const T>`) to preserve literal inference in generic helpers.
- `using` / `await using` for deterministic disposal (Disposable/AsyncDisposable).
- Prefer `NoInfer<T>` to block unwanted inference sites over manual workarounds.

## Not yet: TypeScript 7

TypeScript 7 is the native (Go) compiler port (`microsoft/typescript-go`), shipped as
`typescript@7`, previewed as `@typescript/native-preview`. If the project is on 6.x, **do not
write v7 rules into review findings**. Checklist for whoever does the bump:

- Compiler is a different binary (`tsgo`); confirm every type-check target, editor
  integration, and Vite/`vue-tsc` plugin resolves it.
- `vue-tsc` / Volar must support the native compiler before Vue SFC typecheck can move.
- Confirm 6.x-era flags in the shared tsconfigs still exist under 7.
- Land it as a tracked dependency upgrade, not as a drive-by.

## Not your lane

Runtime structure, immutability, `es-toolkit` vs hand-rolled → `persona-code-quality`.

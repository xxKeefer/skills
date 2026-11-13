# TanStack Query (Vue): modern-API reference (written against 5.81.2)

This file was written against `@tanstack/vue-query` **5.81.2**; later releases share the major, so every rule below
holds. This file is a currency reference only.

> **Lane boundary:** deep TanStack review (query-key correctness, invalidation bugs,
> `staleTime`/`gcTime` misuse, optimistic updates, API-client usage in `queryFn`) belongs to
> **`persona-tanstack`**, not this persona. `persona-best-practice` only flags a v4→v5 API-shape
> regression if it appears in the diff and no other persona is running. When `persona-tanstack`
> is in the panel, defer entirely.

## v5 API shape (what "current" looks like)

- **Single object argument:** `useQuery({ queryKey, queryFn })`, never the v4 positional
  `useQuery(key, fn, opts)`.
- **`queryOptions()` helper** for shared, typed query definitions reused across `useQuery` /
  `prefetchQuery` / `invalidateQueries`.
- **Status names:** `isPending` (not v4 `isLoading` for the initial-fetch flag), `isPending`
  on mutations, `gcTime` (not v4 `cacheTime`).
- **`throwOnError`** (not v4 `useErrorBoundary`).

```ts
// ✅ v5
const opts = queryOptions({ queryKey: ['user', id], queryFn: () => api.getUser(id) })
const { data, isPending } = useQuery(opts)
```

A v4 positional signature / `cacheTime` / `isLoading`-as-pending in changed lines → hand to
`persona-tanstack`; only raise it yourself if that persona is absent from the run.

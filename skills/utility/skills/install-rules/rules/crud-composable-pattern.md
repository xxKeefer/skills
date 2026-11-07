---
paths:
  - "**/composables/**/*.ts"
  - "**/use*.ts"
---

# CRUD Composable Pattern (TanStack Query)

## Principles

1. **Composable owns all TanStack Query concerns** — consumers never see `useMutation`, `useQuery`, `mutateAsync`, or query keys
2. **Namespace-style API** — return object reads like a resource: `filters.create(data)`, `filters.remove(id)`
3. **Toast notifications live inside the composable** — success/error feedback is not the consumer's job. Only one layer toasts a mutation error. If the app's `QueryClient` toasts in a global `MutationCache.onError`, leave out the `onError` toasts here, because both handlers fire for one failure.
4. **Query invalidation is automatic** — mutations invalidate the list query on success
5. **Each `queryFn` reads its inputs from its own `queryKey`** — never from a ref. If a ref changes and an inactive query then refetches (`refetchQueries`, or `refetchType: 'all'`), a `queryFn` that reads the ref caches another parent's data under the old key. Type the key as a tuple with `as const`. Give the destructured key parts new names, so that they do not shadow the factory parameters (`no-shadow`).
6. **Factories take `MaybeRef`, not `MaybeRefOrGetter`** — Vue Query unwraps a ref in the key type, but not a getter. The composable accepts `MaybeRefOrGetter` and calls `toRef` once to make a getter into a ref.

## Return Shape

```ts
return { all, byId, create, update, remove, isSaving }
```

| Member | Type | Description |
|---|---|---|
| `all` | `Ref<T[] \| undefined>` | Reactive list from `useQuery` |
| `byId` | `(id: number) => Promise<T>` | Fetch single item via `queryClient.fetchQuery` |
| `create` | `(data: Req) => Promise<T>` | Plain async wrapper around create mutation |
| `update` | `(id: number, data: Req) => Promise<T>` | Plain async wrapper around update mutation |
| `remove` | `(id: number) => Promise<void>` | Plain async wrapper around delete mutation |
| `isSaving` | `ComputedRef<boolean>` | `true` while create or update is in-flight |

## Internal Structure

```ts
import { computed, toRef } from 'vue'
import type { MaybeRef, MaybeRefOrGetter } from 'vue'
import { queryOptions, useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { useI18n } from 'vue-i18n'
import { showToast } from '@/ui/toast'
import { api } from '@/api'
import type { ThingRequest } from '@/api/schemas/thing'

// --- Query option factories (NOT exported) ---

const thingsQuery = (parentId: MaybeRef<string>) =>
  queryOptions({
    queryKey: ['things', parentId] as const,
    queryFn: ({ queryKey: [, parent] }) => api.things(parent).list(),
    staleTime: 1000 * 60 * 5,
  })

const thingQuery = (parentId: MaybeRef<string>, thingId: MaybeRef<number>) =>
  queryOptions({
    queryKey: ['thing', parentId, thingId] as const,
    queryFn: ({ queryKey: [, parent, id] }) => api.things(parent).get(id),
    staleTime: 1000 * 60 * 5,
  })

// --- Composable ---

export function useThings(parentId: MaybeRefOrGetter<string>) {
  const queryClient = useQueryClient()
  const { t } = useI18n({ useScope: 'global' })
  const parent = toRef(parentId)
  const listQueryKey = ['things', parent]

  // List query
  const { data: all } = useQuery(thingsQuery(parent))

  // Mutations (internal only)
  const createMutation = useMutation({
    mutationFn: (data: ThingRequest) =>
      api.things(parent.value).create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listQueryKey })
      showToast({ heading: t('general.success-creating', { thing: t('things.thing') }), variant: 'success' })
    },
    onError: (error: Error) => showToast({ heading: error.message, variant: 'danger' }),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ThingRequest }) =>
      api.things(parent.value).update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listQueryKey })
      showToast({ heading: t('general.success-updating', { thing: t('things.thing') }), variant: 'success' })
    },
    onError: (error: Error) => showToast({ heading: error.message, variant: 'danger' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.things(parent.value).delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listQueryKey })
      showToast({ heading: t('general.success-deleting', { thing: t('things.thing') }), variant: 'success' })
    },
    onError: (error: Error) => showToast({ heading: error.message, variant: 'danger' }),
  })

  // Public API — plain async functions, no mutation objects leak
  const byId = (id: number) => queryClient.fetchQuery(thingQuery(parent, id))
  const create = (data: ThingRequest) => createMutation.mutateAsync(data)
  const update = (id: number, data: ThingRequest) => updateMutation.mutateAsync({ id, data })
  const remove = (id: number) => deleteMutation.mutateAsync(id)
  const isSaving = computed(() => createMutation.isPending.value || updateMutation.isPending.value)

  return { all, byId, create, update, remove, isSaving }
}
```

`byId` returns cached data while it is fresh (5 minutes in the example). For a read that must reach the server, such as a check before a save, pass `staleTime: 0`: `queryClient.fetchQuery({ ...thingQuery(parent, id), staleTime: 0 })`.

## Consumer Usage

```vue
<script setup lang="ts">
const things = useThings(computed(() => props.parentId))

// List
things.all.value ?? []

// Fetch one
const item = await things.byId(id)

// Create / Update / Delete
await things.create(data)
await things.update(id, data)
await things.remove(id)

// Loading state
things.isSaving.value
</script>
```

Consumers handle **only UI state** (editor open/closed, selected item, dirty flags). They never touch query keys, mutations, or toast calls.

## Consumer Typing at the Boundary

When the consumer has a unified payload type for create and update:

```ts
type ThingPayload = ThingRequest & { id?: number }

async function handleSave(payload: ThingPayload) {
  const { id, ...data } = payload
  if (id != null) {
    await things.update(id, data)
  } else {
    await things.create(data)
  }
}
```

Use `!= null` guard (catches both `undefined` and `null`) — no type casts needed.

# persona-tanstack diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-A8: `refetch()` after setting a filter, or `queryKey: ['services']` while the filters are read only inside `queryFn` → Put every request input in the query key [default: nit] (rule 2)
- NV-I4: `placeholderData: keepPreviousData` with no use of `isPlaceholderData` in the template or pager → Dim results and disable Next while `isPlaceholderData` [default: nit]
- NV-J3: Mutation invalidating only the exact list key or the detail key, leaving the count query or other pages stale → Invalidate the shared list key prefix [default: nit] (rule 3)
- NV-J6: Paginated `useQuery` with `page` in the key and no `placeholderData`, or a spinner that replaces the table → `placeholderData: keepPreviousData` and a stable min-height [default: nit]
- NV-O1: Mutation with no `invalidateQueries`/`setQueryData` on the list prefix, or `staleTime: Infinity` on an editable list → Invalidate the list key prefix on success [default: nit] (rule 3)
- NV-O2: `onMutate` with `setQueryData` and no `cancelQueries`, rollback or `onSettled` invalidation → `cancelQueries`, snapshot, roll back in `onError`, invalidate in `onSettled` [default: nit] (rule 4)
- NV-O3: Detail `initialData` from `getQueryData(listKey)?.find(...)` with no `initialDataUpdatedAt` → `placeholderData` for list-seeded detail [default: nit]
- NV-O5: Company-scoped query key with no company id, where a company switch doesn't `queryClient.clear()` → Put the company id in the key, or clear on switch [default: change-requested] (rule 2)

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-O2: `:key="index"` in a draggable list, or an optimistic reorder mutation with no `onError` rollback → Key by ID; roll back in `onError`, invalidate in `onSettled` [default: nit] (rule 4)

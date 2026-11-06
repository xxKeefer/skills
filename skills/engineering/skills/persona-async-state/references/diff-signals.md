# persona-async-state diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-C1: `async onSubmit() { await api.create(...) }` with no `if (isPending) return`, or `:disabled="loading"` set after an `await` → Synchronous pending guard before the first `await` [default: change-requested]
- FM-C2: Manual `loading = true; await post(); loading = false` with no `finally`, or `await mutateAsync()` with no `try` → Use `isPending`, or reset the flag in `finally` [default: change-requested]
- FM-G6: `watch(data, d => form.x = d.default)` applying server defaults with no dirty or touched check → Apply defaults only to untouched fields, or once [default: change-requested]
- FM-H8: `watch(query.data, d => Object.assign(form, d))` with `refetchOnWindowFocus` left on, so a refetch overwrites edits → Initialise once, or only when not dirty [default: change-requested]
- FM-N3: `watch(() => query.data.value, v => resetForm(...))` with no `meta.dirty` guard, and fields enabled while `isPending` → Render the form after load; never reset dirty fields [default: change-requested]

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-I3: `watch(search, async v => { list.value = await api.search(v) })`, or a `useQuery` key that omits the term plus `refetch()` → Term in the query key; forward `signal`; abort stale calls [default: nit] (rule 1)
- NV-K5: `error` ref set in a `catch` or `onError` on a list and never cleared on the next success → Derive the banner from the current query's `isError` [default: nit]
- NV-P5: Mutation `onSuccess` that calls `router.push` or toasts with no check the user is still on the origin route → Compare the captured route before navigating [default: nit]

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-B7: `ref([])` or `!data?.length` driving the empty state with no `isPending` gate, so "No records" flashes before data → Render loading, then error, then empty, then data [default: nit]
- DS-B8: `.catch(() => [])` or `data.value ?? []` in a template with no `isError` branch → Separate error state with a retry action [default: nit] (rule 10)
- DS-B9: `v-if="isFetching"` swapping the table for a spinner on refetch, or old rows kept with no busy indicator → Keep previous data dimmed; skeleton only on first load [default: nit]
- DS-B10: Skeleton whose rows, columns or heights differ from the real content; `<img>` with no `width`, `height` or `aspect-*` → Match the skeleton to the layout and reserve image space [default: nit]

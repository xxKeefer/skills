# persona-error-handling diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-C3: `await mutateAsync(...)` with no surrounding `try` and no `onError` toast or field mapping → Use `mutate` with `onError`, or catch and show it [default: nit]
- FM-N9: `await Promise.all(ids.map(mutateAsync))` with one toast and no per-item result handling → `Promise.allSettled` and a "8 updated, 2 failed" summary [default: change-requested]

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-B10: `await router.push(x)` followed by a success toast or form reset with no check of the returned result → Check `isNavigationFailure(result)` before acting [default: nit] (rule 18)
- NV-D3: Query data read with `!` (`data.value!.name`), no `isError` branch on a detail page, or no `/:pathMatch(.*)*` route → Explicit not-found state; catch-all route; don't retry 404s [default: change-requested]

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-K1: `useQuery({ onError: toast })` or `watch(error, toast)` inside a shared composable while a global `QueryCache({ onError })` also toasts → Rely on the one global `QueryCache.onError` [default: nit] (rule 6)

## [persona-resilience catalogue](../../persona-resilience/references/catalogue.md)

- RS-D9: `await (await fetch(u)).json()` with no `res.ok` check, or `{{ error.message }}` rendered in a template → Check `res.ok`; map `TypeError` to one friendly network message [default: nit] (rule 12)

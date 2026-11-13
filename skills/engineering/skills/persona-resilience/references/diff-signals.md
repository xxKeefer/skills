# persona-resilience diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-resilience catalogue](catalogue.md)

- RS-A1: 401 interceptor or session-expiry handler calling `window.location =` or `router.push('/login')` on a screen with form input, no draft save or in-place re-login → Save a scoped sessionStorage draft, re-login in place, then replay [default: nit] (rule 1)
- RS-A2: Session countdown built as `setInterval(() => remaining.value--, 1000)`, or an expiry with no warning component at all → Compute remaining time from the wall-clock expiry on each tick [default: nit]
- RS-A3: `if (status === 401) await refresh()` or logout inside a per-request interceptor, with no module-level in-flight promise or "already handling" flag → Share one in-flight refresh promise; queue and replay the rest [default: change-requested] (rule 2)
- RS-A4: `new QueryClient()` with no `retry` function, or `retry: 3` / `retry: true`, so 401, 403 and 404 retry with backoff → Use a shared retry function that never retries 4xx [default: nit] (rule 3)
- RS-A5: Profile, role or permissions query with `staleTime: Infinity` and `refetchOnWindowFocus: false`, or permissions copied into a store at login → Refetch permissions on window focus and on any 403 [default: nit] (rule 4)
- RS-A6: Logout that only clears the store and redirects, with no `pageshow` listener checking `event.persisted` → On `pageshow` with `persisted`, check the session and redirect [default: change-requested]
- RS-A7: Token refresh scheduled once with `setTimeout(refresh, expiresIn - 60s)`, no `visibilitychange` handler, no cross-tab sharing of the new token → Refresh on `visibilitychange`; Web Lock plus `BroadcastChannel` across tabs [default: change-requested] (rule 1)
- RS-B1: New logout path that clears only this tab's state and does not post through the app's session broadcast helper → Broadcast the logout; every tab clears its cache and redirects [default: nit] (rule 5)
- RS-B2: Active company or token read once from `localStorage` into a store or module variable, request headers built from another source, no `storage`/`BroadcastChannel` listener → Broadcast a session-changed message; reset the cache on identity change [default: change-requested] (rule 5)
- RS-B3: Mutation payload spreading the whole loaded object (`{ ...service, name }`, `update(id, { ...original, ...values })`) with no ETag, `If-Match` or version → Send only changed fields (PATCH), or send `If-Match` [default: change-requested] (rule 6)
- RS-B4: Mutation error handled by one catch-all toast with no branch on `status === 409 || status === 412` → Show "changed since you opened it", offer reload, keep edits [default: nit] (rule 6)
- RS-B5: Basket in `pinia-plugin-persistedstate` or `useStorage` with no `storage` listener, and checkout submitting the local basket without refetching → Keep the basket on the server; refetch before checkout [default: change-requested] (rule 9)
- RS-B6: `window.addEventListener('storage', ...)` as the only path that updates local state after this tab's own `setItem` → Update local state on write; listener only for other tabs [default: nit] (rule 5)
- RS-B7: Order, service or payment create with no idempotency key, or a key generated per request rather than per draft → Generate one idempotency key per draft and keep it [default: change-requested] (rule 7)
- RS-C1: `localStorage.*` or `JSON.parse(localStorage.getItem(k))` at module scope, in `main.ts` or in `setup`, with no try/catch → One guarded storage helper with memory fallback and zod parse [default: change-requested] (rule 8)
- RS-C2: Change to a type persisted through `useStorage` or a persisted store, with no version bump or migration → Version stored data; parse with zod `.catch()` fallback [default: change-requested] (rule 8)
- RS-C3: `useLocalStorage('draft', ...)`, `useStorage('order-draft', ...)` or `localStorage.setItem('cart', ...)` with a constant key, or a draft not cleared on logout → Key by user, company and draft ID; clear on logout [default: change-requested] (rule 9)
- RS-D1: New spinner or disabled state driven only by `isPending` or `isFetching`, with no `fetchStatus === 'paused'` or `isPaused` check → Show an offline or paused state with what happens next [default: nit] (rule 10)
- RS-D2: `loading.value = true` with no `finally`, a blocking overlay with no Cancel, or a raw `fetch`/axios instance bypassing the project's API client timeout → Use the API client or `AbortSignal.timeout`; reset in `finally` [default: change-requested] (rule 11)
- RS-D3: Loading UI tied to `isLoading` (first load only) and not `isFetching`, so a refetch after a click shows nothing → Show progress on the clicked control while `isFetching` [default: nit] (rule 11)
- RS-D4: Fixed `refetchInterval` number with no stop on error, a `retry` or `retryDelay` that ignores the `Retry-After` header → `refetchInterval` as a function that backs off on error [default: nit] (rule 12)
- RS-D5: `computed(() => a.isError || b.isError || c.isError)` gating the whole page template → An error state and retry per section; render what loaded [default: nit]
- RS-D6: Hand-rolled `setInterval` status poll, `refetchIntervalInBackground: true`, or `refetchOnWindowFocus: false` on a status query → Refetch on focus or `visibilitychange` [default: nit] (rule 12)
- RS-D7: Timeout, 408 or status 0 branch on a non-idempotent create that shows "failed" and re-enables Submit, or mutation `retry` on a create → Say the result is unknown; check by idempotency key first [default: change-requested] (rule 7)
- RS-D8: `queryFn` that doesn't pass the context `signal` to `fetch`, or results written to a store from `onSuccess`, so the old record's response lands → Pass the queryFn `signal`; keep the route ID in the key [default: nit] (rule 14)
- RS-D10: `response.json()` in an error path with no content-type check, or no branch for a 503 maintenance response → Check content type; show an unavailable state with `Retry-After` [default: change-requested] (rule 10)
- RS-E1: Chunk-error handling, `router.onError` or a new app entry that misses `vite:preloadError`, swallows the error, or reloads with no loop guard → Reload once on `vite:preloadError`, with a loop guard [default: change-requested] (rule 13)
- RS-E2: `QueryCache({ onError: toast })` or an interceptor with no `isCancelledError` / `axios.isCancel` / `AbortError` filter; catch around an aborted fetch setting an error ref → Filter cancellations out of user-facing errors; log at debug [default: nit] (rule 14)

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-C7: `useMutation({ retry: 3 })` or any non-zero `retry` on a non-idempotent POST → `retry: 0` for creates, or send an idempotency key [default: change-requested] (rule 7)

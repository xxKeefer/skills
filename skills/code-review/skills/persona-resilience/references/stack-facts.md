# Stack facts for resilience fixes

Stack facts to use in fixes. Check each against the project before you rely on it:
- The project's HTTP client may set a request timeout and join it with the caller's signal. Check whether a timeout, a network failure, and a caller abort each give a distinct error, and whether 401 and status 0 stay out of error reporting.
- Check how the authenticated client routes a 401, whether it handles 403, and whether the app refreshes tokens or sends the user back through a hosted login redirect.
- A session guard that keeps the route usually does not keep the form. Check whether the app saves form drafts.
- Each app may have its own 401 path and `QueryClient` config. Check whether it shares one retry function (no retry on a parse error or on a 4xx other than 408 and 429, at most 3 tries) or retries every error, 4xx included, with a global toast on every query error.
- A session-expiry guard that throws a `CanceledError` inside the queryFn, rather than through the signal, gives TanStack an ordinary failure (likely retried, with the global toast stacked on the session toast; verify).
- Cross-tab sync usually goes through one `BroadcastChannel` helper with `session-ended` and `session-changed` messages consumed in the auth store. Check for `storage` listeners.
- Check for a `vite:preloadError` handler in each app. A failed dynamic import is an unhandled rejection, so a `window` `error` listener for chunk errors probably never fires (verify). `router.onError` may only clear an overlay.
- Check whether any write sends `If-Match`, an ETag, or a version, whether anything reads `navigator.onLine`, and whether the app sets `networkMode`, `onlineManager`, or `focusManager`.

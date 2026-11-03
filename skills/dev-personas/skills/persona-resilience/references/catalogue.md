# persona-resilience catalogue: sessions, tabs, network and deploys

Scope: a Vue 3 and TypeScript single-page app (vue-router, TanStack Query, and Reka UI) under stress: session and auth changes mid-task, multiple tabs, browser storage, network conditions, stale bundles after a deploy, and cancelled requests.

Each item has: **Bug** (what the user sees), **Cause**, **Test** (concrete steps and inputs), **Spot** (what to look for in a diff), **Fix**, and **Sources**. Test setups live in `fixtures.md`.

`[uncertain]` marks a claim the cited source doesn't fully back. Check it before you rely on it.

---

## A. Session and auth mid-task

### RS-A1. Token expires mid-form, and re-login throws away what was typed
- **Bug:** The user spends 10 to 20 minutes on a long order form. The token expires and Submit returns 401. The app redirects to login, and after login the user lands on the dashboard or on an empty form. NV-E1 (persona-url-state) covers losing the URL; this item covers losing the form contents.
- **Cause:** A global 401 interceptor does a hard redirect (`window.location =` or `router.push('/login')`), and the form state lives only in component memory. There is no in-place re-authentication and no draft.
- **Test:** Open a form, fill it, then delete or expire the access token (see fixtures), and submit. Repeat with a token refresh that fails (block the refresh endpoint). Check what the form holds after login.
- **Spot:** An axios or fetch 401 interceptor that calls `window.location =` or `router.push('/login')` with no in-place re-auth path; long forms with no draft persistence.
- **Fix:** Refresh silently and replay the request. If a full re-login is needed, do it in place (modal or popup) and replay. Keep a draft in sessionStorage, scoped to the user and company, and restore it after login (see RS-C3 for scoping). If the session did time out, say so plainly.
- **Sources:** [WCAG 2.2 Understanding 2.2.5 Re-authenticating](https://www.w3.org/WAI/WCAG22/Understanding/re-authenticating.html), [WCAG 2.2 Understanding 2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html), [DWP Design System: Manage a session timeout](https://design-system.dwp.gov.uk/patterns/manage-a-session-timeout), [Front-End Checklist](https://github.com/thedaviddias/Front-End-Checklist), [Hendrickson, Lyndsay and Emery: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### RS-A2. No timeout warning, or a countdown that drifts in a background tab
- **Bug:** The session ends with no warning. Or a warning countdown shows the wrong time when the user comes back to the tab, because timers in hidden tabs only run once a second (once a minute after 5 minutes in Chrome).
- **Cause:** No warning dialog at all, or a countdown built as `remaining--` inside `setInterval`, which drifts when the browser throttles the tab.
- **Test:** Configure a short session. Background the tab past the warning point, wait, then return. Compare the countdown with the real expiry time. Use a screen reader and check how often the countdown is announced.
- **Spot:** `setInterval(() => remaining.value--, 1000)`; a countdown inside an `aria-live` region that updates every second; no warning component at all.
- **Fix:** Warn at least 2 minutes before expiry, with a one-click "stay signed in" (WCAG 2.2.1 needs at least 20 seconds and a simple action). Compute the remaining time from the wall-clock expiry on every tick. Announce it at intervals (the MOJ pattern uses every 15 seconds), not on every tick.
- **Sources:** [DWP Design System: Manage a session timeout](https://design-system.dwp.gov.uk/patterns/manage-a-session-timeout), [MOJ Design Patterns: Timeout warning](https://design-patterns.service.justice.gov.uk/components/timeout-warning), [WCAG 2.2 Understanding 2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html), [Chrome: Timer throttling in Chrome 88](https://developer.chrome.com/blog/timer-throttling-in-chrome-88)

### RS-A3. Parallel 401s start parallel refreshes and trip reuse detection
- **Bug:** A dashboard with 8 queries makes 8 refresh calls at once. With refresh-token rotation, the second use of the same refresh token looks like reuse, the server revokes the whole token family, and the user is signed out.
- **Cause:** Each request handles its own 401 and calls `refresh()`. There is no single shared refresh promise.
- **Test:** Expire the access token (see fixtures), then load a page with many parallel queries. Count the calls to the token endpoint in the Network panel. Check whether the user stays signed in.
- **Spot:** `if (status === 401) await refresh()` inside a per-request interceptor with no module-level in-flight promise.
- **Fix:** Keep one in-flight refresh promise. Queue the failed requests behind it and replay them when it resolves. Sign out only if that shared refresh fails.
- **Sources:** [Auth0: Refresh token rotation](https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation)

### RS-A4. 401 or 403 retried with backoff, or shown as a generic error
- **Bug:** A 403 takes about 7 seconds to show "Something went wrong", because TanStack's default 3 retries with exponential backoff (1 s, 2 s, 4 s) run first. The message never says the user lacks access.
- **Cause:** The default `retry: 3` applies to every error, including 4xx. The error UI does not tell 401 from 403 from 5xx.
- **Test:** Mock a 403 and then a 401 on a page query. Time how long the error takes to show and read the message. Count the requests in the Network panel.
- **Spot:** `new QueryClient()` defaults with no `retry` function; error components that only read `isError`.
- **Fix:** `retry: (count, err) => isServerError(err) && count < 2`. Map 401 to re-authentication (RS-A1) and 403 to "You don't have access to …". Re-authenticating won't fix a 403, so don't offer it.
- **Sources:** [TanStack Query (Vue): Query retries](https://tanstack.com/query/latest/docs/framework/vue/guides/query-retries), [MDN: 403 Forbidden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

### RS-A5. Role change mid-session isn't picked up
- **Bug:** An admin removes a user's ordering rights. The Order button stays enabled for that user until a hard reload, and then the order fails with a 403 at the end of the flow (compare FM-O8 (persona-form-behaviour)).
- **Cause:** Permissions are read once at login and kept with `staleTime: Infinity`, or stored once in Pinia and never refreshed.
- **Test:** Sign in as user A in one browser and as an admin in another. Remove a permission from A. Without reloading, switch back to A's tab, focus it, and try the action.
- **Spot:** The profile or permissions query with `staleTime: Infinity` and `refetchOnWindowFocus: false`; permissions copied into a store at login.
- **Fix:** Keep the profile as a query that refetches on window focus. Refetch permissions on any 403 and update the UI, rather than only showing an error.
- **Sources:** [TanStack Query (Vue): Window focus refetching](https://tanstack.com/query/latest/docs/framework/vue/guides/window-focus-refetching), [MDN: 403 Forbidden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

### RS-A6. Back after logout shows authenticated pages from the back/forward cache
- **Bug:** On a shared machine, the next person presses Back after logout and sees the previous user's dashboard, with data. NV-O4 (persona-url-state) covers bfcache staleness; this is the security angle.
- **Cause:** The browser restores the page from the back/forward cache. No `pageshow` handler checks whether the session still exists.
- **Test:** Sign in, open a page with customer data, log out, press Back. Check DevTools > Application > Back/forward cache to confirm the page was restored from the cache.
- **Spot:** No `pageshow` listener checking `event.persisted`; logout that only clears the store and redirects.
- **Fix:** On `pageshow` with `persisted === true`, check the session and reload or redirect to login. Use `Cache-Control: no-store` only on truly sensitive pages, because it disables the cache for everyone.
- **Sources:** [web.dev: Back/forward cache](https://web.dev/articles/bfcache)

### RS-A7. A background tab misses its refresh and logs out on return
- **Bug:** The user comes back to a tab after lunch, and the first click signs them out, even though another tab kept the session alive.
- **Cause:** Each tab schedules `setTimeout(refresh, expiresIn - 60s)`. Hidden-tab throttling delays the timer, and the tabs don't share the refreshed token.
- **Test:** Open two tabs. Leave one hidden for longer than the token lifetime while you keep using the other. Return to the hidden tab and click something that calls the API.
- **Spot:** A refresh timer set once with `setTimeout`; no `visibilitychange` handler; no cross-tab sharing of the new token.
- **Fix:** Check and refresh on `visibilitychange`. Use a Web Lock so only one tab refreshes at a time, and share the result with the others (storage event or `BroadcastChannel`).
- **Sources:** [MDN: Web Locks API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API), [MDN: visibilitychange event](https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilitychange_event), [Chrome: Timer throttling in Chrome 88](https://developer.chrome.com/blog/timer-throttling-in-chrome-88)

---

## B. Multiple tabs and concurrent edits

### RS-B1. Logout in another tab leaves this tab looking usable
- **Bug:** The user signs out in tab A. Tab B still shows customer data and lets them build a whole order before it fails at random on submit.
- **Cause:** Nothing tells the other tabs about the logout. Each tab keeps its own in-memory store and query cache.
- **Test:** Open two tabs. Log out in one. In the other, without reloading, browse, open a form, and submit.
- **Spot:** No `BroadcastChannel` or `storage` listener for auth changes; logout that clears only the current tab's state.
- **Fix:** Broadcast the logout. Every tab clears its query cache and redirects to login (or shows a "you signed out in another tab" blocker).
- **Sources:** [MDN: BroadcastChannel](https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel), [MDN: Window storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event), [Hendrickson, Lyndsay and Emery: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### RS-B2. A different user or company in another tab, and this tab mixes identities
- **Bug:** The user switches company, or a different user signs in, in tab B. Tab A still shows company A's services, but its next request goes out with company B's context (header, cookie, or token), so an order or edit lands in the wrong company or account. NV-O5 (persona-url-state) is the same-tab version.
- **Cause:** The active company or token sits in localStorage or a cookie shared by every tab, while each tab caches its own in-memory copy for the UI. Nothing listens for cross-tab changes. The `storage` event does fire in other same-origin tabs, but not in the tab that made the change.
- **Test:** Open two tabs. In one, switch company, or log out and log in as another user. In the other, without reloading, edit and save a record, then check which company or account the change landed in.
- **Spot:** The active company read once into a Pinia store from localStorage; request headers built from a different source than what the UI shows; query keys with no user or company ID; the token read from localStorage on each request; no `storage` or `BroadcastChannel` listener.
- **Fix:** Listen for `storage` or a `BroadcastChannel` message. On an identity or company change, reset the query cache and either reload or show a "your session changed in another tab" blocker. Build the request context from the same store the UI shows.
- **Sources:** [MDN: Window storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event), [MDN: BroadcastChannel](https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel), [Hendrickson, Lyndsay and Emery: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### RS-B3. Two tabs or two users edit the same record, and the last write silently wins
- **Bug:** A colleague changes a service's rate limit in tab A. The user, in tab B with an older copy, renames the same service and saves. B's PUT sends the whole object and reverts the rate limit. Or the colleague deleted it, and B's save fails with a generic error. FM-H8 (persona-form-behaviour) is the same-tab refetch problem; this is the cross-tab or cross-user one.
- **Cause:** A full-object PUT built from stale form state, with no `If-Match`, ETag, or version field.
- **Test:** Open the same edit form in two tabs, or as two users. Save one field in A, then save a different field in B, and reload. Repeat with A deleting the record.
- **Spot:** A mutation payload that spreads the whole loaded object (`{ ...service, name }`, `api.update(id, { ...original, ...values })`); no version or ETag in the request.
- **Fix:** Send only the changed fields (PATCH). Send `If-Match` with the ETag, or a version field, so the server returns 412 or 409. Then handle the conflict as in RS-B4.
- **Sources:** [MDN: If-Match (lost update problem)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Match), [Kaner, Falk and Nguyen: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [Hendrickson, Lyndsay and Emery: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### RS-B4. A 409 or 412 conflict shown as a generic error
- **Bug:** "Save failed" with no way forward. Retrying hits the same conflict, and the user eventually gives up and loses their edits.
- **Cause:** The error handler treats every non-2xx response the same way.
- **Test:** Mock a 409 and a 412 on save (see fixtures). Read the message, try to retry, and check whether the user's edits survive.
- **Spot:** One catch-all error toast for mutations; no branch on `status === 409 || status === 412`.
- **Fix:** Show a specific "This changed since you opened it" message, offer "Load latest", and keep the user's edits so they can apply them again.
- **Sources:** [MDN: 412 Precondition Failed](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/412)

### RS-B5. A basket open in two tabs diverges
- **Bug:** A port added in tab A is missing in tab B. Checkout in B orders a stale basket, and the badge counts in the two tabs differ.
- **Cause:** A persisted Pinia store that rehydrates from storage only on page load.
- **Test:** Open two tabs. Add an item in A. In B, without reloading, check the badge, open the basket, and check out.
- **Spot:** `pinia-plugin-persistedstate` or `useStorage` for the basket with no `storage` listener; checkout that submits the local basket without refetching.
- **Fix:** Listen for `storage` events and rehydrate, or keep the basket on the server and refetch it on focus and before checkout.
- **Sources:** [MDN: Window storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event)

### RS-B6. The `storage` event is expected in the tab that wrote the value
- **Bug:** A preference toggle updates every other tab but not the one where it was changed.
- **Cause:** The `storage` event does not fire in the window that made the change, and the code updates its own state only from that listener.
- **Test:** Change a stored preference (theme, density, column settings) and check the current tab and a second tab.
- **Spot:** A `window.addEventListener('storage', …)` handler that is the only path updating local state after `setItem`.
- **Fix:** Update local state directly when writing, and use the listener only for changes from other tabs.
- **Sources:** [MDN: Window storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event)

### RS-B7. The same order submitted from two tabs
- **Bug:** The user duplicates the checkout tab (or reopens it from history) and submits in both. Two services are created. FM-C1 (persona-form-behaviour) is a double click in one tab.
- **Cause:** Nothing ties the submission to the draft, so the server can't tell a repeat from a new order.
- **Test:** Reach the final order step, duplicate the tab, and submit in both. Count the created services.
- **Spot:** An order create call with no idempotency key; a key generated per request rather than per draft.
- **Fix:** Generate an idempotency key per draft and keep it with the draft. The server rejects or returns the original result for a repeat.
- **Sources:** [Stripe: Idempotent requests](https://docs.stripe.com/api/idempotent_requests)

---

## C. Browser storage and persisted state

### RS-C1. localStorage is blocked, full, or corrupt, and the app falls over
- **Bug:** With cookies or site data blocked, in private browsing (some browsers give a zero quota), or with storage full, the app shows a blank screen at boot. Or a preference toggle throws and stops the rest of its handler, so the form never submits. A corrupted stored value has the same effect.
- **Cause:** Unguarded `localStorage.getItem` or `setItem`. MDN says reading `localStorage` throws `SecurityError` when the user has set the browser to stop the page persisting data, and blocked cookies are likely treated that way. `setItem` can also throw when the quota is full [uncertain: not stated on the localStorage page; see MDN Storage.setItem]. `JSON.parse` of a corrupted value also throws.
- **Test:** Block site data for the origin, fill storage to the quota, and put invalid JSON in each persisted key (see fixtures). Then boot the app, toggle preferences, and submit forms.
- **Spot:** Direct `localStorage.*` or `JSON.parse(localStorage.getItem(k))` at module scope, in `main.ts`, or in `setup`, with no try/catch.
- **Fix:** One storage wrapper that feature-tests with try/catch (MDN's `storageAvailable`), catches errors, falls back to memory, and validates parsed values with zod.
- **Sources:** [MDN: Window.localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), [MDN: Using the Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API), [Front-End Checklist](https://github.com/thedaviddias/Front-End-Checklist), [Hendrickson, Lyndsay and Emery: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### RS-C2. The persisted state shape changes between releases
- **Bug:** After a deploy, users with old saved filters or column settings get a blank table or a broken page.
- **Cause:** Stored data has no version, and the new code reads it as if it had the new shape.
- **Test:** Seed the previous release's stored shape (see fixtures), then load the page on the new build.
- **Spot:** A change to a type that is persisted through `useStorage` or a persisted store, with no version bump or migration.
- **Fix:** Version the stored data. Parse it with zod and a `.catch()` fallback to defaults, and migrate known old versions.
- **Sources:** [Zod API: .catch()](https://zod.dev/api)

### RS-C3. A draft in localStorage is shared across tabs, users, and companies, and survives logout
- **Bug:** Two tabs each start a new order. Both write the same `orderDraft` key, so whichever autosaved last wins, and on refresh tab A restores tab B's draft. Or a draft started under company A is restored after switching to company B. Or the next user of a shared machine sees the last user's draft order or filters. Tokens kept in localStorage can be read by any XSS.
- **Cause:** A fixed storage key with no user, company, or draft ID in it, no cross-tab awareness, and nothing cleared on logout. Session identifiers stored in localStorage.
- **Test:** Two tabs with different drafts, then refresh each. Start a draft in company A, switch to B, and open the form. Log out and log in as another user on the same browser.
- **Spot:** `useLocalStorage('draft', …)`, `useStorage('order-draft', …)`, or `localStorage.setItem('cart', …)` with a constant key; access or refresh tokens in localStorage.
- **Fix:** Key drafts by user, company, and draft ID, or use sessionStorage for per-tab drafts. Clear them on logout and company switch. Never store session identifiers in localStorage.
- **Sources:** [OWASP HTML5 Security Cheat Sheet: Local Storage](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html), [MDN: Window storage event](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event), [Kaner, Falk and Nguyen: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

---

## D. Network conditions

### RS-D1. Offline: the query or mutation pauses and the spinner runs forever
- **Bug:** With Wi-Fi dropped, the user presses Save. The spinner runs with no error and no "you're offline" message. A first page load shows a spinner forever. When the network comes back, the save fires unexpectedly, possibly after the user has changed the form or left the page.
- **Cause:** In the default `networkMode: 'online'`, queries and mutations don't fire without a network connection. `fetchStatus` becomes `paused` while `status` stays `pending`. UI that keys only on `isPending` or `isFetching` shows a spinner with no reason.
- **Test:** DevTools > Network > Offline, then load a page, save a form, and refetch. Restore the network and watch what fires.
- **Spot:** Spinners driven only by `isPending` or `isFetching`; no use of `fetchStatus === 'paused'` or `isPaused`; no online-state indicator.
- **Fix:** Show an offline banner and a paused state ("You're offline. We'll retry when you reconnect."). Decide on purpose whether a paused mutation should resume or be cancelled when the network returns.
- **Sources:** [TanStack Query (Vue): Network Mode](https://tanstack.com/query/latest/docs/framework/vue/guides/network-mode), [Hendrickson, Lyndsay and Emery: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### RS-D2. No request timeout: a hung request leaves an endless spinner or a blocking overlay with no way out
- **Bug:** A hung backend gives an endless spinner. A full-screen loading overlay (during order submit, a company switch, or a report export) stays forever when the request hangs or the promise never settles. Esc, Back, and Cancel do nothing, and the only way out is reloading the page.
- **Cause:** `fetch` has no timeout of its own. The overlay flag is cleared only on success, not in `finally`. The dialog is `:closable="false"` while loading.
- **Test:** Block the request URL in DevTools mid-submit, or return a response that never ends from a mock. Try Esc, Back, and Cancel.
- **Spot:** `loading.value = true` without a `finally`; an overlay with no Cancel; fetch with no `AbortSignal.timeout`.
- **Fix:** Pass `signal: AbortSignal.timeout(ms)`, clear loading flags in `finally`, and show a "taking longer than expected" state with retry. Provide a Cancel that aborts the request and says whether the action may still complete on the server (see RS-D7).
- **Sources:** [MDN: AbortSignal.timeout()](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static), [Kaner, Falk and Nguyen: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### RS-D3. A slow response gives no feedback, so users click again
- **Bug:** On Slow 3G, a click on a tab or filter shows nothing for 3 seconds, so the user clicks again, or clicks something else.
- **Cause:** Loading state shown only for the first load, or only after the data area empties.
- **Test:** DevTools throttling to Slow 3G (or a custom 2,000 ms latency profile). Click tabs, filters, and buttons and note how long before anything changes.
- **Spot:** Loading UI tied to `isLoading` (first load only) and not to `isFetching`; buttons with no pending state.
- **Fix:** Show progress after about 1 second, and sooner on the clicked control itself. Show percent done for anything over 10 seconds.
- **Sources:** [NN/g: Response Times, the 3 important limits](https://www.nngroup.com/articles/response-times-3-important-limits/)

### RS-D4. A retry storm during an outage
- **Bug:** With the API down, every query retries, polling keeps going, and focus refetches pile on. The page makes hundreds of calls and the UI flickers between loading and error.
- **Cause:** Default retries on every error, a fixed `refetchInterval` that ignores errors, and `Retry-After` ignored.
- **Test:** Mock every API call as 503 with `Retry-After: 120` (see fixtures). Leave a page with polling open for 2 minutes, switch tabs a few times, and count requests.
- **Spot:** A fixed `refetchInterval` number; no `retry` or `retryDelay` function; no read of the `Retry-After` header.
- **Fix:** A `retry` function that stops on 4xx and respects `Retry-After`. Back off or stop polling while queries are failing (`refetchInterval` as a function of the query state).
- **Sources:** [TanStack Query (Vue): Query retries](https://tanstack.com/query/latest/docs/framework/vue/guides/query-retries), [MDN: Retry-After](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After)

### RS-D5. One failed widget blanks the whole page
- **Bug:** The telemetry endpoint fails, and the whole service page shows "Error" instead of only the chart.
- **Cause:** One combined `isError` across parallel queries decides what the page renders.
- **Test:** Block one secondary request (telemetry, pricing, notices) and load the page. Check what else still renders.
- **Spot:** `const isError = computed(() => a.isError || b.isError || c.isError)` gating the whole template.
- **Fix:** An error state and a retry per section. Render what did load.
- **Sources:** [TanStack Query (Vue): Parallel queries](https://tanstack.com/query/latest/docs/framework/vue/guides/parallel-queries), [NN/g: Error-message guidelines](https://www.nngroup.com/articles/error-message-guidelines/)

### RS-D6. A status poll is stale when the tab comes back
- **Bug:** A "Deploying" badge stays stale for a whole poll interval after the user comes back to the tab, because timers in hidden tabs were throttled.
- **Cause:** Polling that relies on `setInterval` timing, with no refetch when the tab becomes visible.
- **Test:** Start a provisioning action, hide the tab for 10 minutes while the status changes, then return. Note how long the badge takes to update.
- **Spot:** A custom `setInterval` poll; `refetchOnWindowFocus: false` on status queries.
- **Fix:** Refetch on focus or `visibilitychange`. Don't rely on interval timing in hidden tabs.
- **Sources:** [TanStack Query (Vue): Window focus refetching](https://tanstack.com/query/latest/docs/framework/vue/guides/window-focus-refetching), [Chrome: Timer throttling in Chrome 88](https://developer.chrome.com/blog/timer-throttling-in-chrome-88)

### RS-D7. A client timeout is reported as a failure though the server committed
- **Bug:** "Order failed". The user retries and ends up with two services. FM-C7 (persona-form-behaviour) is the duplicate; this item is the false "failed" message.
- **Cause:** A timeout or dropped connection after the server committed is treated the same as a rejected request.
- **Test:** Add a delay on the response longer than the client timeout, while the server still completes (mock or proxy). Read the message, then check the server record.
- **Spot:** A timeout or network error branch that shows "failed" for a non-idempotent create.
- **Fix:** Say "We couldn't confirm your order". Check its status by idempotency key (RS-B7) before allowing a retry.
- **Sources:** [Stripe: Idempotent requests](https://docs.stripe.com/api/idempotent_requests)

### RS-D8. A late response from the previous record lands in the new view
- **Bug:** The user switches fast from service A to service B, and A's slow telemetry is drawn on B's chart. NV-I3 (persona-url-state) is the search-results version.
- **Cause:** The record ID is not in the query key, or the fetch ignores the query's abort signal, so the old response writes into shared state.
- **Test:** Add 2 to 3 seconds of latency. Open service A, then switch to B at once. Check the chart, the header, and the details for A's data.
- **Spot:** Query keys that leave out the route ID; a `queryFn` that doesn't pass `signal` to `fetch`; results written to a store from `onSuccess`.
- **Fix:** Put the ID in the query key. Pass the `signal` from the query function context to `fetch` so stale requests abort.
- **Sources:** [TanStack Query (Vue): Query cancellation](https://tanstack.com/query/latest/docs/framework/vue/guides/query-cancellation), [TanStack Query (Vue): Query keys](https://tanstack.com/query/latest/docs/framework/vue/guides/query-keys)

### RS-D9. Raw network errors shown, or HTTP errors treated as success
- **Bug:** Users see "TypeError: Failed to fetch". Or a 500 error body is rendered as data, because `fetch` doesn't reject on HTTP errors.
- **Cause:** No `res.ok` check; the raw `error.message` shown to the user.
- **Test:** Go offline and trigger a request; mock a 500 with a JSON error body and with an HTML body.
- **Spot:** `await (await fetch(u)).json()` with no `res.ok` check; `{{ error.message }}` in a template.
- **Fix:** Check `res.ok`. Map `TypeError` to one friendly network message, and treat `AbortError` as silent (RS-E2).
- **Sources:** [MDN: fetch()](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch)

### RS-D10. A planned outage or 503 isn't handled
- **Bug:** A 503 HTML maintenance page is parsed as JSON and crashes the app. Users aren't told when the service is back or what happens to their unfinished work.
- **Cause:** Error handling assumes a JSON body, and there is no unavailable state.
- **Test:** Mock a 503 with an HTML body and a `Retry-After` header (see fixtures) during a page load and during a form submit.
- **Spot:** `response.json()` in an error path with no content-type check; no handling for 503.
- **Fix:** A dedicated unavailable state that shows the return time (from `Retry-After`) and says what happens to unsaved input.
- **Sources:** [GOV.UK Design System: Service unavailable pages](https://design-system.service.gov.uk/patterns/service-unavailable-pages/), [MDN: Retry-After](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After)

---

## E. Deploys and cancelled requests

### RS-E1. A lazy route chunk is gone after a deploy, so navigation fails
- **Bug:** A tab left open across a release shows a blank page, does nothing on click, or sits on an error when the user navigates to a lazy route. Sometimes the error reads "text/html is not a valid JavaScript MIME type" (Chrome) or "Importing a module script failed" (Safari).
- **Cause:** The deploy removed the old hashed chunks. The next dynamic import requests a file that no longer exists, or the server returns `index.html` for it. `index.html` cached without `no-cache` makes it worse.
- **Test:** Build, open the app, rebuild with new hashes, delete the old assets, then navigate to a route not yet loaded (see fixtures). Also block one chunk URL in DevTools.
- **Spot:** No `vite:preloadError` handler and no `router.onError` handling of chunk errors; `index.html` served without `Cache-Control: no-cache`; a CDN that rewrites unknown asset paths to `index.html`.
- **Fix:** Handle `vite:preloadError` (and router chunk errors) by reloading once to the target URL, with a guard against reload loops. Serve `index.html` with `Cache-Control: no-cache`, return a real 404 for missing assets, and keep the previous release's assets for a while.
- **Sources:** [Vite: Building for production, load error handling (`vite:preloadError`)](https://vite.dev/guide/build#load-error-handling)

### RS-E2. Cancelled or aborted requests are reported as errors
- **Bug:** Navigating away quickly, changing a filter mid-fetch, a debounced search superseding itself, or logging out produces "Something went wrong" toasts or error boxes for requests the app cancelled itself. Users learn to ignore error toasts.
- **Cause:** A global `onError` or axios interceptor toasts every rejection, including `CancelledError`, `AbortError`, `ERR_CANCELED`, and the 401s during logout. In TanStack Query, a cancelled query's `CancelledError` reaches observers such as `onError` unless `silent` is set. With `revert` and prior data it restores the previous state, and it throws only if there was no prior data.
- **Test:** Throttle the network and click through navigation quickly. Change filters rapidly. Type fast in a debounced search. Log out while queries are in flight. Watch for toasts and error states.
- **Spot:** `QueryCache({ onError: toast })` or an interceptor with no `isCancelledError`, `axios.isCancel`, or `name === 'AbortError'` filter; a catch block around an aborted fetch that sets an error ref.
- **Fix:** Filter cancellation and auth-teardown errors out of user-facing reporting. Still log them at debug level.
- **Sources:** [TanStack Query (Vue): Query Cancellation](https://tanstack.com/query/latest/docs/framework/vue/guides/query-cancellation), [MDN: AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController), [Axios: Cancellation](https://axios-http.com/docs/cancellation), [Kaner, Falk and Nguyen: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

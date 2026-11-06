# persona-url-state catalogue: URL state, history and lists

Stack assumed: Vue 3 + TypeScript SPA, vue-router 4, TanStack Query (Vue), and Reka UI.
Each item: **Bug** (what the user sees), **Cause**, **Test** (concrete steps), **Spot** (diff pattern), **Fix**, and **Ref**.
`[uncertain]` marks claims not verified against a primary source.

## Sources (short keys used below)

| Key | URL |
| --- | --- |
| VR-SCROLL | https://router.vuejs.org/guide/advanced/scroll-behavior.html |
| VR-DYN | https://router.vuejs.org/guide/essentials/dynamic-matching.html |
| VR-NAV | https://router.vuejs.org/guide/essentials/navigation.html |
| VR-FAIL | https://router.vuejs.org/guide/advanced/navigation-failures.html |
| VR-MIG | https://router.vuejs.org/guide/migration/ |
| VR-API | https://router.vuejs.org/api/#LocationQuery |
| VR-QUERY-SRC | https://github.com/vuejs/router/blob/main/packages/router/src/query.ts |
| VR-LINK-SRC | https://github.com/vuejs/router/blob/main/packages/router/src/RouterLink.ts (`guardEvent`) |
| VR-LINK-EXT | https://router.vuejs.org/guide/advanced/extending-router-link.html |
| VR-CHANGELOG | https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md (4.1.4, 2022-08-22: "Discarded invalid param(s)") |
| NUQS | https://nuqs.dev/docs/options |
| TS-BLOG | https://tanstack.com/blog/search-params-are-state |
| TSQ-PAGE | https://tanstack.com/query/latest/docs/framework/vue/guides/paginated-queries |
| TSQ-CANCEL | https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation |
| TKDODO-KEYS | https://tkdodo.eu/blog/effective-react-query-keys |
| BAYMARD-BACK | https://baymard.com/blog/back-button-expectations |
| BAYMARD-RETURN | https://baymard.com/research-articles/return-same-place |
| NNG-OVERLAYS | https://www.nngroup.com/articles/overuse-of-overlays/ |
| NNG-MENTAL | https://www.nngroup.com/articles/mental-models/ |
| NNG-DISMISS | https://www.nngroup.com/articles/accidental-overlay-dismissal/ |
| MDN-SORT | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort |
| MDN-COLLATOR | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator |
| MDN-SCROLLRESTORE | https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration |
| HIST-LIMIT | https://azukiazusa.dev/en/blog/history-replacestate-rate-limit ; https://bugzilla.mozilla.org/show_bug.cgi?id=1995636 ; https://github.com/joliss/history-throttled |

Verified facts the reviewer can rely on:

- vue-router `parseQuery` turns a repeated key into an array, decodes `+` as a space, and gives `null` for a key with no `=` (VR-QUERY-SRC). So `route.query.x` is `string | null | (string | null)[] | undefined` (VR-API).
- `stringifyQuery` writes `null` as a bare key (`?a`) and drops `undefined` (VR-QUERY-SRC). Pass `undefined` to remove a key, not `null` and not `''`.
- vue-router reuses the component instance when only params change, so some lifecycle hooks do not run. Use `watch(() => route.params.id)` or `onBeforeRouteUpdate` (VR-DYN).
- `router.push`/`replace` resolve to a navigation failure (aborted, cancelled, or duplicated) instead of throwing (VR-FAIL).
- `params` are ignored when `path` is given (VR-NAV). Since 4.1.4, params not in the route path are discarded with a warning (VR-CHANGELOG).
- `RouterLink`'s `guardEvent` leaves meta/ctrl/shift/alt-click, non-primary buttons, `defaultPrevented`, and `target="_blank"` to the browser (VR-LINK-SRC). A hand-rolled `@click="router.push()"` loses all of that.
- `savedPosition` is only set on popstate (back/forward). Defining `scrollBehavior` sets `history.scrollRestoration = 'manual'` (VR-SCROLL).
- Browsers rate-limit `pushState`/`replaceState`: Chrome silently no-ops after roughly 200 calls in a short window, Firefox and Safari throw; Safari's threshold is stricter (HIST-LIMIT, numbers anecdotal). nuqs throttles to 50 ms (120 ms on Safari) by default (NUQS).
- Baymard: 59% of sites get at least one back-button expectation wrong; 37% fail overlays, 27% fail filter/sort; Back after filters "should begin removing the applied filters" (BAYMARD-BACK). 13% of sites return users to the top of the list from a product page (BAYMARD-RETURN, figure from search snippet `[uncertain]`, verify on page).
- `Array.prototype.sort` is stable since ES2019; default sort compares as strings; `undefined` goes last without calling compareFn, `null` does not (MDN-SORT).

---

## A. URL as the source of truth

### NV-A1. View state not in the URL
- **Bug:** Refresh, shared link, or Back loses filter/search/sort/page/tab. Support cannot reproduce "what I was looking at".
- **Cause:** State lives in `ref()`/Pinia only.
- **Test:** Set a filter, search, sort, page 3, tab 2. Copy the URL, open in a new incognito window (after login). Refresh. Go to a detail page and press Back. All five should match.
- **Spot:** `const page = ref(1)`, `const search = ref('')`, `const activeTab = ref('…')` in a list or tabbed page with no `route.query` read/write. Pinia store holding list filters.
- **Fix:** Derive state from `route.query` through a typed composable (`useRouteQuery`-style getter/setter with parse + serialise). Keep short-lived UI state (hover, an open dropdown) out of the URL.
- **Ref:** [TS-BLOG](https://tanstack.com/blog/search-params-are-state); [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations); https://robertgreiner.com/how-we-forgot-the-url/
- **In the design system**: Look for the standard helpers: a data-table column-filter composable that syncs a `queryParam` through `useRouteQuery` in `replace` mode with typed codecs, and a data-table search composable (`searchQueryParam`). Sort and pagination may not be URL-backed.

### NV-A2. Two sources of truth drift (ref initialised once from query)
- **Bug:** Back/forward changes the URL but the filters/table do not change; or the table changes and the chips don't.
- **Cause:** `const status = ref(route.query.status)` copies once in `setup`; later URL changes are not observed (and the component is reused, see NV-D1).
- **Test:** Apply filter A, then B. Press Back. URL shows A; check the UI and the network request also show A.
- **Spot:** `ref(route.query.x)` / `ref(route.params.x)` with no watcher; `onMounted(() => { filters.value = route.query })`.
- **Fix:** `computed({ get: () => parse(route.query.x), set: v => router.replace({ query: { ...route.query, x: serialise(v) } }) })`.
- **Ref:** [VR-DYN](https://router.vuejs.org/guide/essentials/dynamic-matching.html)

### NV-A3. Query write clobbers other params
- **Bug:** Changing sort wipes the search term, or changing page drops the tab.
- **Cause:** `router.push({ query: { sort } })` replaces the whole query object.
- **Test:** Search "abc", then change sort. `q=abc` must survive.
- **Spot:** `query: { page }` without `...route.query`.
- **Fix:** Always merge: `{ ...route.query, sort }`. Centralise in one helper.
- **Ref:** [TS-BLOG](https://tanstack.com/blog/search-params-are-state) ("writing search params, safely and atomically")

### NV-A4. Non-atomic multi-param write (lost update)
- **Bug:** Setting filter and resetting page in one action leaves one of them stale; occasional navigation "cancelled".
- **Cause:** Two sequential `router.replace` calls in the same tick each spread the *old* `route.query` (route isn't updated until navigation resolves), so the second overwrites the first. The second navigation also cancels the first (VR-FAIL).
- **Test:** Change a filter while on page 3; confirm the URL has the new filter and `page` removed (or 1) in one entry.
- **Spot:** Two setters from a `useRouteQuery` helper called back to back: `status.value = x; page.value = 1`.
- **Fix:** Batch into one `router.replace({ query: { ...route.query, status: x, page: undefined } })`, or a helper that queues writes in a microtask (as `@vueuse/router` `useRouteQuery` does `[uncertain]`, verify version).
- **Ref:** [VR-FAIL](https://router.vuejs.org/guide/advanced/navigation-failures.html); [TS-BLOG](https://tanstack.com/blog/search-params-are-state)

### NV-A5. Default values written to URL / URL noise
- **Bug:** Landing on `/services` immediately becomes `/services?page=1&sort=name&dir=asc&q=`; links look different from what users share; Back needs two presses.
- **Cause:** Serialiser writes every key, including defaults and empty strings; an initial "normalise" uses `push`.
- **Test:** Load the bare list URL; the address bar should not change. History length should not grow (`history.length` in console).
- **Spot:** `onMounted(() => router.push({ query: { page: 1, … } }))`; serialiser without default stripping.
- **Fix:** Omit keys equal to default (`undefined`); any normalisation uses `replace`. nuqs calls this `clearOnDefault` (default true in v2).
- **Ref:** [NUQS](https://nuqs.dev/docs/options)

### NV-A6. Empty params left behind (`?q=` / `?status`)
- **Bug:** Clearing search leaves `?q=` or `?q`; some code treats `''`/`null` as "a filter is applied" (shows "1 filter active", "no results for ''").
- **Cause:** Setting `''` or `null` instead of `undefined`. vue-router writes `null` as a bare key (VR-QUERY-SRC).
- **Test:** Type in search, clear it with the X button and with backspace. URL should have no `q`. Filter badge count back to 0.
- **Spot:** `query: { ...route.query, q: search.value }` with no `|| undefined`; `q: null`.
- **Fix:** Normalise empty/whitespace to `undefined` in the serialiser.
- **Ref:** [VR-QUERY-SRC](https://github.com/vuejs/router/blob/main/packages/router/src/query.ts); [VR-API](https://router.vuejs.org/api/#LocationQuery)

### NV-A7. Param order churn / spurious navigations
- **Bug:** Same filters produce different URLs (`?a=1&b=2` versus `?b=2&a=1`) so the TanStack cache misses, the "duplicated" check fails, and Back steps through no-op entries.
- **Cause:** Object spread order depends on which control changed last.
- **Test:** Apply A then B; clear; apply B then A. Compare URLs and network calls (second should be cached).
- **Spot:** Query key built from `route.query` object directly; no key sorting.
- **Fix:** Stable serialiser (fixed key order); build query keys from the parsed, typed filter object, not raw `route.query`. nuqs exposes `processUrlSearchParams` for sorting (NUQS).
- **Ref:** [NUQS](https://nuqs.dev/docs/options); [TKDODO-KEYS](https://tkdodo.eu/blog/effective-react-query-keys)

### NV-A8. URL updated but nothing refetches (or refetch without URL update)
- **Bug:** Address bar changes, table does not; or table changes, URL does not.
- **Cause:** Query key built from a local ref that is not derived from the route; or `refetch()` called with new args.
- **Spot:** `refetch()` after setting a filter; `queryKey: ['services']` with filters read inside `queryFn` only.
- **Fix:** Put every input to the request in the query key (reactive getter / computed). Don't call `refetch` to change parameters.
- **Ref:** [TKDODO-KEYS](https://tkdodo.eu/blog/effective-react-query-keys); [TSQ-PAGE](https://tanstack.com/query/latest/docs/framework/vue/guides/paginated-queries)

### NV-A9. Infinite loop between URL watcher and state watcher
- **Bug:** Tab freezes, "Throttling navigation to prevent the browser from hanging" in console, or URL flickers.
- **Cause:** `watch(filters, () => router.replace(...))` plus `watch(() => route.query, q => filters.value = parse(q))` with non-identical objects (new array each time) so deep watch keeps firing.
- **Test:** Apply multi-select filter; watch console for throttling warnings and network for repeated calls.
- **Spot:** Paired watchers both directions; `{ deep: true }` on route.query.
- **Fix:** Single source (URL) with computed getters; compare serialised strings before writing.
- **Ref:** [HIST-LIMIT](https://azukiazusa.dev/en/blog/history-replacestate-rate-limit)

### NV-A10. Secrets / PII in query
- **Bug:** Tokens, emails, or one-time codes end up in history, analytics, Referer, and Sentry breadcrumbs.
- **Spot:** `query: { token }`, `?email=` on list filters, password reset codes not removed with `replace` after use.
- **Fix:** Keep secrets out of the URL; after consuming a one-time param, `router.replace` it away.
- **Ref:** https://owasp.org/www-community/vulnerabilities/Information_exposure_through_query_strings_in_url `[uncertain: page title/path]`

## B. History: push versus replace, Back/Forward behaviour

### NV-B1. Every keystroke pushes a history entry ("Back-button hell")
- **Bug:** After typing a long word in search, Back has to be pressed 8 times to leave the page.
- **Cause:** `router.push` on each input event (or on each debounced value with a short debounce).
- **Test:** Type a 10-char term slowly, then press Back once. Expect to leave the page, or at most undo the whole search.
- **Spot:** `watch(search, v => router.push({ query: { ...route.query, q: v } }))`.
- **Fix:** `replace` while typing; optionally a single `push` on commit (Enter/blur). nuqs defaults to `replace` and warns that global `push` adds "a new entry … for every search param update".
- **Ref:** [NUQS](https://nuqs.dev/docs/options)
- **In the design system**: A data-table filter composable may already write with `mode: 'replace'`. Copy that rather than calling `router.push`.

### NV-B2. History API rate limit on fast input / slider
- **Bug:** URL stops updating mid-typing in Chrome (silently) or throws `SecurityError` in Safari/Firefox; later state is lost on refresh.
- **Cause:** Unthrottled `replaceState` per keystroke or per slider `input` event.
- **Test:** Hold a key down in search, or drag a range slider rapidly, in Safari. Check console and final URL.
- **Spot:** URL write inside `@input` / `@update:modelValue` of a slider with no debounce/throttle.
- **Fix:** Throttle URL writes (about 50 ms; more on Safari) while keeping the local value instant; or write on `change`/commit.
- **Ref:** [HIST-LIMIT](https://azukiazusa.dev/en/blog/history-replacestate-rate-limit); [NUQS](https://nuqs.dev/docs/options)

### NV-B3. Filters use replace when users expect Back to undo
- **Bug:** User applies 3 filters, presses Back expecting the previous filter set, and is thrown off the page.
- **Cause:** All filter writes are `replace`.
- **Test:** Apply filter A, then B (discrete clicks, not typing). Press Back. Baymard expects B to be removed.
- **Spot:** Global `replace` in the URL helper with no per-param option.
- **Fix:** Decide per param and document it: discrete filter/sort/page/tab changes `push`; text typing `replace`. This is a product decision; Baymard (e-commerce) favours `push` for filters, nuqs defaults to `replace`. Flag inconsistency within one page as the bug.
- **Ref:** [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations); [NUQS](https://nuqs.dev/docs/options)

### NV-B4. Initial redirect/normalisation pushes, trapping Back
- **Bug:** Back from `/list` lands on `/list` again (which redirects again): user can't leave.
- **Cause:** Default tab/redirect done with `router.push` in `onMounted`, or a route `redirect` combined with client push.
- **Test:** From another page, open the list, press Back once. Should leave.
- **Spot:** `onMounted(() => router.push(...))` for defaults; `if (!route.query.tab) router.push({ query: { tab: 'x' } })`.
- **Fix:** Use `router.replace` or a route-level `redirect`, or handle the default without writing it (NV-A5).
- **Ref:** [VR-NAV](https://router.vuejs.org/guide/essentials/navigation.html)

### NV-B5. Back after form submit shows stale form / resubmits
- **Bug:** After "Create order" succeeds and goes to the detail page, Back shows the filled form; submitting again creates a duplicate. Or Back goes to a "step 3 of 3" page whose state is gone.
- **Cause:** Success navigation uses `push`; form state kept in a store; no idempotency.
- **Test:** Submit a create form, land on success/detail, press Back. Expect the list or a fresh/blank form (or a "you already created this" state), never a one-click duplicate.
- **Spot:** `await mutate(); router.push({ name: 'detail' })` from a create route; wizard state in Pinia not cleared on success.
- **Fix:** `router.replace` to the result page after create; reset form store on success; disable/guard re-submit; server idempotency key where it matters.
- **Ref:** [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations) (checkout step example); [VR-NAV](https://router.vuejs.org/guide/essentials/navigation.html)

### NV-B6. Multi-step wizard on one URL
- **Bug:** Back from step 3 exits the wizard to the list and loses everything typed.
- **Cause:** Steps are local state, not URL.
- **Test:** Reach step 3; press Back. Expect step 2 with data intact.
- **Spot:** `const step = ref(1)` in a wizard.
- **Fix:** Put the step in the query or params (`push` per step), persist the data (store or sessionStorage), and add guards that stop a deep link to step 3 without its prerequisites.
- **Ref:** [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations) (accordion checkout)

### NV-B7. Optimistic/unsaved changes lost silently on Back

See FM-H1 (persona-form-behaviour).

### NV-B8. Forward button broken after Back
- **Bug:** Back, then Forward, lands somewhere unexpected or shows default filters.
- **Cause:** On popstate the page "re-normalises" with a `push`, truncating forward history.
- **Test:** A→B, Back, Forward. Expect B, with B's state.
- **Spot:** Any `router.push` inside a `watch(() => route.query)`.
- **Fix:** Never push in response to a route change; only `replace` for normalisation.
- **Sources:** [HTML Standard: session history, push behaviour](https://html.spec.whatwg.org/multipage/browsing-the-web.html#navigationhistorybehavior-push)

### NV-B9. Programmatic "Back" button with no history
- **Bug:** In-app "← Back" does nothing or leaves the app when the page was opened from a deep link/new tab.
- **Cause:** `router.back()` / `history.go(-1)` with no in-app previous entry.
- **Test:** Paste a detail URL in a fresh tab, click the in-app Back.
- **Spot:** `@click="router.back()"`.
- **Fix:** Check `window.history.state?.back` (vue-router stores `back` in history state; it is `null` on the first entry) and fall back to `router.push({ name: 'list' })`; or always link to the parent route with preserved query.
- **In the project**: `router.back()`/`history.back()` may appear in many files with no shared fallback helper. Prefer one return-to composable.
- **Sources:** [vue-router `html5.ts` (`StateEntry.back`)](https://github.com/vuejs/router/blob/main/packages/router/src/history/html5.ts)

### NV-B10. Navigation failures ignored
- **Bug:** Code after `await router.push()` assumes it navigated (shows toast, resets form) when a guard aborted or it was duplicated.
- **Spot:** `await router.push(x); toast.success(...)`.
- **Fix:** Check `isNavigationFailure(result)`.
- **Ref:** [VR-FAIL](https://router.vuejs.org/guide/advanced/navigation-failures.html)

## C. Scroll position and restoration

### NV-C1. Back from detail returns to top of list
- **Bug:** User scrolls to row 80, opens detail, presses Back, is at the top and loses their place.
- **Cause:** `scrollBehavior` always returns `{ top: 0 }`, or `savedPosition` is applied before the async list renders (page is too short, browser clamps to 0).
- **Test:** Scroll far down a list, open an item, press Back (with network throttled to Slow 3G too).
- **Spot:** `scrollBehavior() { return { top: 0 } }`; list fetched in `onMounted` with no cached data; `gcTime: 0` on the list query.
- **Fix:** Return `savedPosition` when present; with TanStack Query, cached data renders synchronously so restoration usually works if `gcTime` allows. For slow data, return a Promise from `scrollBehavior` that resolves after the data/transition is ready.
- **Ref:** [VR-SCROLL](https://router.vuejs.org/guide/advanced/scroll-behavior.html); [BAYMARD-RETURN](https://baymard.com/research-articles/return-same-place)

### NV-C2. Scroll container is not the window
- **Bug:** Restoration never works in the app shell.
- **Cause:** The scrolling element is an inner `<main class="overflow-auto">`; vue-router's `savedPosition` tracks window scroll only (`computeScrollPosition` reads `window.scrollX`/`scrollY`).
- **Test:** As NV-C1, in the real layout.
- **Spot:** Layout with `h-screen overflow-hidden` + inner `overflow-y-auto`.
- **Fix:** Let the document scroll, or save/restore the container scroll yourself (route meta or `history.state`).
- **Sources:** [vue-router `scrollBehavior.ts` (`computeScrollPosition` reads `window.scrollX/scrollY`)](https://github.com/vuejs/router/blob/main/packages/router/src/scrollBehavior.ts), [Vue Router: Scroll Behavior](https://router.vuejs.org/guide/advanced/scroll-behavior.html)

### NV-C3. New page opens scrolled down
- **Bug:** Clicking a row from far down the list opens the detail already scrolled to the bottom.
- **Cause:** No `scrollBehavior`, or one that returns nothing for push navigations (inner container keeps its scroll).
- **Test:** Scroll down, click an item (forward nav). Detail should start at top.
- **Spot:** `scrollBehavior` that returns `savedPosition` with no `{ top: 0 }` fallback, or a router with no `scrollBehavior`; an inner `overflow-y-auto` container not reset on push.
- **Fix:** `return savedPosition ?? { top: 0 }` (and reset the inner container if used).
- **Ref:** [VR-SCROLL](https://router.vuejs.org/guide/advanced/scroll-behavior.html)

### NV-C4. Query-only change jumps to top (or should, but doesn't)
- **Bug:** Changing sort/filter jumps the page to the top unexpectedly, losing the filter panel; or paginating leaves user at the bottom of the new page.
- **Cause:** `scrollBehavior` doesn't distinguish `to.path === from.path`.
- **Test:** Change a filter mid-page; click "next page" at the bottom of a table.
- **Spot:** `scrollBehavior` that returns `{ top: 0 }` for every navigation with no `to.path === from.path` branch; a pager handler with no scroll to the table top.
- **Fix:** For same-path query changes: keep position for filters, scroll to the table top for pagination (explicitly in the pager handler).
- **Sources:** [Vue Router: Scroll Behavior](https://router.vuejs.org/guide/advanced/scroll-behavior.html)

### NV-C5. Hash fragment ignored / covered by sticky header
- **Bug:** `/docs#billing` lands at top, or the heading is hidden behind the sticky header.
- **Cause:** No `el: to.hash` handling; no offset; target rendered after async data.
- **Test:** Open a deep link with a hash in a new tab.
- **Spot:** `scrollBehavior` with no `to.hash` branch, or `el: to.hash` with no header offset; hash target ids built from data (`:id="item.name"`).
- **Fix:** `if (to.hash) return { el: to.hash, top: headerHeight }` (or CSS `scroll-margin-top`), delayed until content exists. Hash IDs must be valid selectors (escape if derived from data).
- **Ref:** [VR-SCROLL](https://router.vuejs.org/guide/advanced/scroll-behavior.html)

### NV-C6. Infinite scroll / "load more" loses pages on Back
- **Bug:** After loading 5 pages and opening an item, Back shows only page 1 at the top.
- **Cause:** Loaded page count not in URL or cache; `useInfiniteQuery` refetches all pages or was garbage-collected.
- **Test:** Load more 3x, open item, Back.
- **Spot:** `useInfiniteQuery` with `gcTime: 0`; "Load more" appending to a local `ref([])` or a page count in a `ref`.
- **Fix:** Keep the infinite query cached (`gcTime`), or store loaded count in URL; restore scroll after pages render. Baymard calls refinding "really severe" with endless scroll.
- **Ref:** [BAYMARD-RETURN](https://baymard.com/research-articles/return-same-place)

## D. Route params and component reuse

### NV-D1. Same route, new param, no refetch
- **Bug:** Navigating from service A to service B (breadcrumb, related link, search box in header) keeps showing A, or shows A's title with B's data.
- **Cause:** Component reused; data loaded in `onMounted`/`setup` from a non-reactive `route.params.id`.
- **Test:** From detail A, navigate through an in-page link to detail B. Then Back to A.
- **Spot:** `const id = route.params.id` (plain const) used in a query key or fetch; `onMounted(fetch)`.
- **Fix:** `const id = computed(() => route.params.id as string)` in the query key; or `:key="route.fullPath"` on `<RouterView>` (costly, resets all state).
- **Ref:** [VR-DYN](https://router.vuejs.org/guide/essentials/dynamic-matching.html)
- **In the project**: A helper can turn an array or missing route param into `undefined`.

### NV-D2. Local state leaks between params
- **Bug:** Form/edit mode/selected tab/expanded rows from A still shown on B.
- **Cause:** Reused instance keeps refs.
- **Test:** Open edit on A, navigate to B.
- **Spot:** `ref` for edit mode, selected tab, expanded rows or form values on a `/:id` page with no `watch(() => route.params.id)`, `onBeforeRouteUpdate` or `:key` on the view.
- **Fix:** Reset in `watch(() => route.params.id)` / `onBeforeRouteUpdate`, or key the component.
- **Ref:** [VR-DYN](https://router.vuejs.org/guide/essentials/dynamic-matching.html)

### NV-D3. Unknown/deleted id shows blank page or eternal spinner
- **Bug:** `/services/does-not-exist` renders an empty shell, spinner, or JS error instead of a "not found" view.
- **Cause:** 404 response treated as loading; `data.value!.name` crash; no catch-all route.
- **Test:** Edit the id in the URL to garbage, to a valid-looking but missing UID, and to one owned by another company (403). Also `/nonexistent-path`.
- **Spot:** No `isError` branch; `!` non-null assertions on query data; no `/:pathMatch(.*)*` route.
- **Fix:** Explicit not-found and forbidden states; catch-all route; don't retry 404s.
- **Sources:** [Vue Router: Catch all / 404 Not found Route](https://router.vuejs.org/guide/essentials/dynamic-matching.html#Catch-all-404-Not-found-Route), [TanStack Query: Query Retries](https://tanstack.com/query/latest/docs/framework/vue/guides/query-retries)

### NV-D4. Params ignored or discarded
- **Bug:** Link goes to the wrong page or param is missing.
- **Cause:** `router.push({ path: '/x', params: { id } })` (params ignored with `path`); passing params not declared in the route (discarded since 4.1.4) to smuggle state.
- **Spot:** `path` + `params` together; params not in the route's path; "Discarded invalid param(s)" warning.
- **Fix:** Use `name` + params, or query/history state for extra data.
- **Ref:** [VR-NAV](https://router.vuejs.org/guide/essentials/navigation.html); [VR-CHANGELOG](https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md)

### NV-D5. Param type assumptions
- **Bug:** `route.params.id` treated as number (`=== 5` never true) or as string when it's an array (repeatable params).
- **Spot:** `route.params.id as number`; `Number(route.params.id)` without NaN check.
- **Fix:** Parse and validate; TS typed routes.
- **Sources:** [Vue Router: Routes' Matching Syntax](https://router.vuejs.org/guide/essentials/route-matching-syntax.html)

### NV-D6. Unencoded path params
- **Bug:** Names with `/`, `#`, `?`, `%` break links (such as a service name used as a slug).
- **Cause:** Building paths by string concatenation.
- **Spot:** `` router.push(`/x/${name}`) ``.
- **Fix:** Use named routes with params (router encodes), or `encodeURIComponent`.
- **Ref:** [VR-NAV](https://router.vuejs.org/guide/essentials/navigation.html); [VR-MIG](https://router.vuejs.org/guide/migration/)

### NV-D7. Trailing slash / case duplicates
- **Bug:** `/services/` and `/services` behave differently (active nav not highlighted, different cache key, analytics split).
- **Cause:** Routes allow trailing slash by default unless `strict` (VR-MIG); comparisons against `route.path` strings.
- **Test:** Add a trailing slash and change case in the URL.
- **Spot:** `route.path === '/services'`; `startsWith` checks for active nav.
- **Fix:** Compare `route.name`; pick one canonical form.
- **Ref:** [VR-MIG](https://router.vuejs.org/guide/migration/)

## E. Login redirects, guards, titles

### NV-E1. Redirect after login loses original URL or its query/hash
- **Bug:** Deep link `/services?status=live#x` → login → lands on dashboard, or on `/services` without filters.
- **Cause:** Guard stores `to.path` not `to.fullPath`; redirect param not encoded; SSO round trip drops it.
- **Test:** Logged out, open a deep link with query and hash; log in (password and SSO paths).
- **Spot:** `redirect: to.path`; `` `/login?redirect=${to.fullPath}` `` without encoding.
- **Fix:** Store `to.fullPath` (router encodes query values when passed as `query: { redirect: to.fullPath }`).
- **Sources:** [Vue Router: Route Meta Fields (`query: { redirect: to.fullPath }`)](https://router.vuejs.org/guide/advanced/meta.html)

### NV-E2. Open redirect through `?redirect=`
- **Bug:** `/login?redirect=https://evil.example` sends the user off-site after login.
- **Spot:** `window.location.href = route.query.redirect`; `router.push(route.query.redirect)` without validation.
- **Fix:** Only accept same-origin relative paths starting with a single `/` (reject `//`, `/\`, schemes).
- **Ref:** https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html

### NV-E3. Guard redirect loops
- **Bug:** Blank page / "Maximum call stack" / infinite redirects for a user without permission or a new company.
- **Cause:** Guard redirects to a route that itself fails the guard.
- **Test:** Log in as a user lacking the role / with no company.
- **Spot:** `beforeEach` or `beforeEnter` that returns a redirect to a route the same check also fails, with no `to.name` exemption; `next()` called twice.
- **Fix:** Exempt the target route; return route locations rather than calling `next` twice.
- **Sources:** [Vue Router: Navigation Guards](https://router.vuejs.org/guide/advanced/navigation-guards.html)

### NV-E4. Document title not updated
- **Bug:** Tab title stays the app name or shows the previous entity's name; history dropdown/bookmarks unreadable.
- **Cause:** Title set in `onMounted` (not on param change), or from `meta.title` only (no entity name).
- **Test:** Open two detail pages in tabs; navigate between details; check the Back long-press menu.
- **Spot:** `document.title = ...` in `onMounted` or once in `setup`; a detail route titled only by a static `meta.title`.
- **Fix:** Reactive title (`useTitle` with a computed that includes the entity name and updates after data loads); reset on leave.
- **Sources:** [WCAG 2.2 Understanding 2.4.2 Page Titled](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html), [VueUse: useTitle](https://vueuse.org/core/useTitle/)

### NV-E5. Focus and announcement not moved on navigation
- **Bug:** Screen reader users get no cue that the page changed; focus stays on the clicked link (now gone).
- **Fix:** Move focus to the main heading or announce the route change after navigation. (Overlaps with persona-a11y.)
- **Ref:** https://www.gatsbyjs.com/blog/2019-07-11-user-testing-accessible-client-routing/ `[uncertain: path]`

## F. Links: new tab, middle click, semantics

### NV-F1. `@click="router.push"` on non-links
- **Bug:** Cmd/ctrl-click and middle-click don't open a new tab; no "Copy link address"; no URL in status bar; rows not keyboard reachable.
- **Cause:** Navigation on `<div>`/`<tr>`/`<button>` click handlers. `RouterLink` already leaves modifier clicks, non-primary buttons, and `target="_blank"` to the browser through `guardEvent`.
- **Test:** Cmd-click, ctrl-click, middle-click, right-click > open in new tab on every navigable row/card/button.
- **Spot:** `@click="router.push(...)"`, `@click="goTo(row)"` on table rows; `<button>` that navigates.
- **Fix:** Use `<RouterLink>` (or `custom` + `v-slot="{ href, navigate }"` rendering a real `<a :href @click="navigate">`). For whole-row click, put a real link in the primary cell and stretch it.
- **Ref:** [VR-LINK-SRC](https://github.com/vuejs/router/blob/main/packages/router/src/RouterLink.ts); [VR-LINK-EXT](https://router.vuejs.org/guide/advanced/extending-router-link.html)

### NV-F2. Custom link swallows modifier clicks
- **Bug:** Even an `<a :href>` doesn't open in new tab.
- **Cause:** `@click.prevent="router.push(href)"` prevents default unconditionally.
- **Spot:** `@click.prevent` + `router.push` on an anchor.
- **Fix:** Use RouterLink's `navigate` (which guards), or check `e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0` first.
- **Ref:** [VR-LINK-SRC](https://github.com/vuejs/router/blob/main/packages/router/src/RouterLink.ts)

### NV-F3. Click handler both navigates and does something else
- **Bug:** Clicking a row's checkbox/kebab menu also opens the detail page.
- **Cause:** Event bubbles to the row's click handler.
- **Test:** Click checkbox, menu button, copy-to-clipboard icon inside a clickable row.
- **Spot:** `@click` or `@row-click` on a row that navigates, with a checkbox, kebab menu or copy button inside that has no `@click.stop`.
- **Fix:** Don't make the whole row a click target, or `@click.stop` on inner controls.
- **Sources:** [MDN: Event.stopPropagation()](https://developer.mozilla.org/en-US/docs/Web/API/Event/stopPropagation)

### NV-F4. `target="_blank"` issues
- **Bug:** External link replaces the SPA; or internal link opens in a new tab unnecessarily, losing app state; screen readers not told it opens a new tab.
- **Spot:** External URLs through `RouterLink`; `window.open(url)` without `noopener` (modern browsers default `noopener` for `target=_blank` anchors, not necessarily for `window.open` features `[uncertain]`).
- **Fix:** Plain `<a target="_blank" rel="noopener noreferrer">` for external, with visible/announced indication.
- **Sources:** [MDN: `<a>` element (target, security, accessibility)](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a), [MDN: Window.open() (`noopener` feature)](https://developer.mozilla.org/en-US/docs/Web/API/Window/open)

### NV-F5. Links built from current route lose context
- **Bug:** "Back to list" link goes to page 1 with default filters.
- **Cause:** Link hard-codes `{ name: 'list' }` instead of carrying the list's query.
- **Spot:** "Back to list" link with a bare `:to="{ name: 'services' }"` and no stored list query.
- **Fix:** Prefer real history Back; for an explicit link, carry the list query (stash it when leaving the list).
- **Sources:** [Baymard: Return users to the same place in the product list](https://baymard.com/research-articles/return-same-place), [Baymard: Back button expectations](https://baymard.com/blog/back-button-expectations)

## G. Modals, drawers and overlays

### NV-G1. Back leaves the page instead of closing the modal
- **Bug:** On mobile (and desktop), user presses Back to close a full-screen drawer/modal and lands on the previous page, losing work.
- **Cause:** Overlay open state is local only.
- **Test:** Open a drawer/modal, press Back (and Android hardware back / iOS edge-swipe).
- **Spot:** A drawer or a full-screen dialog holding a form, opened from a local `ref(false)` with no query param or popstate close.
- **Fix:** For large/full-screen overlays, push a query/hash entry on open (`?drawer=edit`) and close on popstate; close through `router.back()` only if we pushed it, else `replace` it away. NN/G and Baymard both say Back should close the overlay.
- **Ref:** [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations) (37% fail); [NNG-OVERLAYS](https://www.nngroup.com/articles/overuse-of-overlays/); [NNG-MENTAL](https://www.nngroup.com/articles/mental-models/)

### NV-G2. Modal pushes history but closing doesn't pop it
- **Bug:** After open/close 3 times, Back appears to do nothing 3 times (re-opens modal or no-op).
- **Cause:** Open pushes `?modal=x`, close does another push without the param.
- **Test:** Open/close modal several times, then press Back.
- **Spot:** Open does `router.push({ query: { ...route.query, modal: 'x' } })` and close does another `router.push` without the key.
- **Fix:** Close = `router.back()` when the modal entry is the current one we pushed; otherwise `replace`.
- **Sources:** [SvelteKit: Shallow routing](https://svelte.dev/docs/kit/shallow-routing)

### NV-G3. Deep-linked modal URL broken
- **Bug:** Sharing `?modal=edit&id=123` opens nothing, crashes, or opens for an id the user can't access; refresh with the modal open shows an empty modal.
- **Test:** Refresh with the modal open; paste the URL in a new tab; edit the id to invalid.
- **Spot:** Dialog `open` computed from `route.query.modal` or `route.query.id` with no validation and no loading or not-found branch inside.
- **Fix:** Modal reads its state from the URL and validates; handle loading/not-found inside the modal.
- **Sources:** [SvelteKit: Shallow routing (caveats on reload and SSR)](https://svelte.dev/docs/kit/shallow-routing)

### NV-G4. Navigation while a modal is open leaves it orphaned
- **Bug:** Clicking a link inside a modal (or Back) navigates but the overlay, focus trap or `body` scroll-lock remains.
- **Cause:** Teleported overlay owned by a component that isn't unmounted, or scroll lock not released.
- **Test:** Open a dialog, use a link inside it or press Back; try scrolling the new page.
- **Spot:** Reka `DialogRoot` with `v-model:open` in a layout-level component; manual `document.body.style.overflow`.
- **Fix:** Close overlays on route change (`router.afterEach` / `watch(route)`), keep overlay owner inside the routed view.
- **Sources:** [Robb Owen: Locking scroll with :has()](https://robbowen.digital/wrote-about/locking-scroll-with-has/), [Reka UI: Dialog](https://reka-ui.com/docs/components/dialog)

### NV-G5. Unsaved changes in a drawer closed by Back without prompt

See FM-B6 (persona-form-behaviour).

## H. Query param parsing and validation

### NV-H1. Single value versus array
- **Bug:** Multi-select filter works with 2+ values but breaks with 1 (`.map is not a function`, or `'live'.includes('l')` matches substrings); or a user-edited `?status=a&status=b` crashes a single-value param.
- **Cause:** vue-router returns a string for one occurrence and an array for repeats.
- **Test:** Load `?status=LIVE`, `?status=LIVE&status=NEW`, `?status=` and `?status` for every multi and single param.
- **Spot:** `route.query.status as string[]`, `as string`; `.includes` on an unknown-shaped value.
- **Fix:** Normalise: `const toArray = v => v == null ? [] : (Array.isArray(v) ? v : [v]).filter(Boolean)`; for single params take the first string. Validate with zod or valibot.
- **Ref:** [VR-QUERY-SRC](https://github.com/vuejs/router/blob/main/packages/router/src/query.ts); [TS-BLOG](https://tanstack.com/blog/search-params-are-state)

### NV-H2. Comma-joined arrays break on values with commas
- **Bug:** `?tags=a,b` splits a tag literally called "Sydney, AU".
- **Spot:** `.split(',')` / `.join(',')` for user-defined values.
- **Fix:** Repeated keys, or encode each item; only use comma-joining for enum values.
- **Ref:** [TS-BLOG](https://tanstack.com/blog/search-params-are-state) ("naive comma-splitting")

### NV-H3. Numbers as strings
- **Bug:** `page + 1` gives `"21"`; `page === 2` never true; `limit=abc` → `NaN` in request.
- **Spot:** `route.query.page as unknown as number`; arithmetic on query values.
- **Fix:** `Number.parseInt` with `Number.isInteger` check and default.
- **Sources:** [vue-router `query.ts` (`LocationQueryValue = string | null`)](https://github.com/vuejs/router/blob/main/packages/router/src/query.ts), [MDN: Number.parseInt()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/parseInt)

### NV-H4. Booleans: `"false"` is truthy
- **Bug:** `?archived=false` shows archived items; toggle can't be turned off after reload.
- **Spot:** `if (route.query.archived)`; `Boolean(route.query.x)`.
- **Fix:** Explicit `=== 'true'`; or omit the key when false (default).
- **Sources:** [MDN: Truthy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy)

### NV-H5. Invalid values not sanitised
- **Bug:** `page=-1`, `page=0`, `page=1.5`, `page=999`, `page=abc`, `sort=; drop`, `sort=password`, `dir=sideways`, `status=FOO`, `tab=nope` produce blank tables, 400/500 errors, crashes, or are forwarded to the API.
- **Test:** Hand-edit each param to negative, zero, decimal, huge, non-numeric, unknown enum, long (5,000 chars), and script payload. Expect a clamped/defaulted view and the URL corrected through `replace`.
- **Spot:** Query values passed straight into the API call or `v-html`; sort field interpolated into a request without allow-list.
- **Fix:** Schema per page (enum allow-lists, clamp numbers), correct the URL with `replace`, never `v-html` a query value.
- **Ref:** [TS-BLOG](https://tanstack.com/blog/search-params-are-state)

### NV-H6. Page beyond last page
- **Bug:** `page=999` (or a page that vanished after delete/filter) shows "No results" though data exists.
- **Test:** Go to the last page, delete its only item; or open `?page=999`.
- **Spot:** URL `page` passed to the table or API with no clamp against `totalPages`; a delete on a paginated list with no step back to the last page.
- **Fix:** When `page > totalPages && totalPages > 0`, `replace` to the last page.
- **Sources:** [Telerik feedback: Properly update the pager after deleting all the items from a page](https://feedback.telerik.com/kendo-jquery-ui/1358998-properly-update-the-pager-after-deleting-all-the-items-from-a-page)

### NV-H7. Encoding of special characters in search terms
- **Bug:** Searching `a+b`, `50%`, `a&b`, `#1`, `x=y`, spaces, emoji, `ü`, or Japanese breaks: `+` becomes a space after reload, `#` truncates, `%` throws `URIError: malformed`, `&` splits into a new param.
- **Cause:** Manual URL string building (`` `?q=${term}` ``), double encoding (`encodeURIComponent` before `router.push` which encodes again), or decoding with `decodeURIComponent` on an already-decoded `route.query`. vue-router expects unencoded values and pre-decodes `+` as a space (VR-MIG; VR-QUERY-SRC).
- **Test:** Search for each of `a+b`, `100%`, `a&b=c`, `#tag`, `  two  spaces  `, `café`, `日本`, `😀`; reload; share link; Back.
- **Spot:** Template-literal URLs; `encodeURIComponent` inside `router.push({ query })`; `decodeURIComponent(route.query.q)`; `window.location.search` parsing by hand.
- **Fix:** Pass raw values in `query` objects; let the router encode; when calling APIs use `URLSearchParams`/axios `params`.
- **Ref:** [VR-MIG](https://router.vuejs.org/guide/migration/); [VR-QUERY-SRC](https://github.com/vuejs/router/blob/main/packages/router/src/query.ts)

### NV-H8. Unicode normalisation mismatch

See IN-C5 (persona-text-input).

### NV-H9. Stale/unknown params kept after a rename
- **Bug:** Old bookmarks `?state=live` silently ignored after renaming to `status`.
- **Spot:** A changed key string in `queryParam`, `searchQueryParam`, `useRouteQuery('...')` or a codec in the project's URL-filter composable, with no read of the old name.
- **Fix:** Map legacy param names on read and `replace` them, or accept the break knowingly.
- **Ref:** [TS-BLOG](https://tanstack.com/blog/search-params-are-state) ("types can drift")

## I. Search behaviour

### NV-I1. Missing debounce
- **Bug:** A request per keystroke; rate-limit 429s; UI flicker; history spam (NV-B1).
- **Spot:** Query key bound directly to the `v-model` value of the input.
- **Fix:** Debounce the value feeding the query key (about 250 to 400 ms `[uncertain: house value]`); keep the input itself instant. nuqs notes debounce on the URL only helps server fetching; for client fetching debounce the state.
- **Ref:** [NUQS](https://nuqs.dev/docs/options)
- **In the design system**: A data-table search composable may debounce, trim and length-gate. Hand-rolled debounce is persona-code-quality's lane.

### NV-I2. Debounce too long / no immediate feedback
- **Bug:** Feels broken; user presses Enter and nothing happens; results for the old term show with no loading cue.
- **Spot:** `refDebounced(search, n)` or `useDebounceFn(fn, n)` with `n` above 500 on a search; no flush on submit or blur (`@keydown.enter` on a design-system input that re-emits `keydown` never fires, FM-A1); no pending cue while the debounced value lags.
- **Fix:** Flush on Enter; show a pending indicator while `debounced !== raw` or `isFetching`.
- **Sources:** [NN/g: Response Times, the 3 Important Limits](https://www.nngroup.com/articles/response-times-3-important-limits/)

### NV-I3. Out-of-order responses overwrite newer results
- **Bug:** Type "ab" then "abc"; "ab" response arrives last and table shows "ab" results under an "abc" search box.
- **Cause:** Manual `fetch` + `results.value = await ...` in a watcher, no cancellation or sequence check. With TanStack Query, keying by the term avoids this because each term is its own cache entry.
- **Test:** DevTools throttling + type fast; or mock the first request to be slower.
- **Spot:** `watch(search, async v => { list.value = await api.search(v) })`; `useQuery` whose key omits the term (then `refetch()`).
- **Fix:** Search term in the query key; pass `signal` from the queryFn context to the HTTP client so stale requests cancel (only cancels if the signal is consumed). Outside TanStack: AbortController or `onWatcherCleanup`/`onCleanup` flag.
- **Ref:** [TSQ-CANCEL](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation); [TKDODO-KEYS](https://tkdodo.eu/blog/effective-react-query-keys)

### NV-I4. Placeholder data shown as if current
- **Bug:** With `keepPreviousData`, the old term's results sit under the new term with no cue; "No results" banner computed from stale data; pager "Next" clickable on stale page.
- **Spot:** `placeholderData: keepPreviousData` with no `isPlaceholderData` use.
- **Fix:** Dim/flag while `isPlaceholderData`; disable pager until it resolves (TanStack example guards Next with `!isPlaceholderData`).
- **Ref:** [TSQ-PAGE](https://tanstack.com/query/latest/docs/framework/vue/guides/paginated-queries)

### NV-I5. Whitespace-only / untrimmed terms
- **Bug:** Searching " " returns nothing or everything and shows "No results for ' '"; "abc " differs from "abc" (cache miss, different results).
- **Test:** Search spaces only, leading/trailing spaces, tabs, pasted newline.
- **Spot:** Search value written to `route.query` or a query key with no `.trim()`; `v-if="search"` deciding "has a search" on the untrimmed value.
- **Fix:** Trim (and collapse internal whitespace if the backend expects it) before keying and before writing the URL; treat empty-after-trim as no search.
- **Sources:** [MDN: String.prototype.trim()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)

### NV-I6. Minimum length not enforced or not explained
- **Bug:** 1-char search hammers backend / returns thousands; or min length silently ignores input with no hint.
- **Spot:** `if (term.length < n) return` or `enabled: () => q.value.length >= n` on a search with no hint text shown below `n`.
- **Fix:** Enforce consistently and tell the user ("type at least 2 characters").
- **Sources:** [GitLab issue 396873: Add messaging for character minimum in global search](https://gitlab.com/gitlab-org/gitlab/-/issues/396873)

### NV-I7. Case sensitivity mismatch
- **Bug:** "Sydney" finds the item, "sydney" doesn't; client-side filter case-sensitive while server is not.
- **Spot:** `item.name.includes(term)` without lowercasing.
- **Fix:** `toLocaleLowerCase()` both sides, or `Intl.Collator(locale, { sensitivity: 'base', usage: 'search' })`.
- **Ref:** [MDN-COLLATOR](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator)

### NV-I8. Accent/diacritic-sensitive search
- **Bug:** "Sao Paulo" doesn't find "São Paulo"; "Zurich" doesn't find "Zürich".
- **Spot:** Client filter `toLowerCase().includes(term)` over city, metro, country or company names with no `normalize('NFD')` or base-sensitivity `Intl.Collator`.
- **Fix:** `s.normalize('NFD').replace(/\p{Diacritic}/gu, '')` on both sides, or a collator with `sensitivity: 'base'` for equality checks.
- **Ref:** [MDN-COLLATOR](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator)

### NV-I9. Regex built from user input
- **Bug:** Searching `(`, `[`, `*`, `+`, `?`, `\` throws `SyntaxError: Invalid regular expression` and blanks the list; `.` matches everything; catastrophic backtracking hangs the tab.
- **Spot:** `new RegExp(term, 'i')` for filtering or highlighting.
- **Fix:** Escape (`term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')`, or `RegExp.escape` where supported, ES2025 `[uncertain: check browser targets]`), or use `includes`.
- **Ref:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions#escaping

### NV-I10. Highlighting breaks or injects
- **Bug:** Highlighting `<b>` or `&` corrupts the text; `v-html` highlight enables XSS; highlight misses accented/case variants; highlights across split nodes break.
- **Spot:** `v-html="name.replace(term, '<mark>$&</mark>')"`.
- **Fix:** Split into text segments and render `<mark>` through template (no `v-html`); match with the same normalisation as NV-I7/I8.
- **Sources:** [Vue.js: Security, HTML injection](https://vuejs.org/guide/best-practices/security.html)

### NV-I11. Server-side wildcards not escaped
- **Bug:** Searching `%` or `_` returns everything / unexpected matches (SQL LIKE wildcards); `*` in Elasticsearch-style query strings behaves as wildcard; `"` breaks the query.
- **Test:** Search `%`, `_`, `\`, `*`, `"`, `'`.
- **Fix:** The backend must escape LIKE metacharacters; check in the browser that results match literally. (A backend bug that shows up in the frontend.)
- **Ref:** https://www.postgresql.org/docs/current/functions-matching.html#FUNCTIONS-LIKE

### NV-I12. Search scoped to current page only
- **Bug:** Client-side search over a paginated API filters just the 25 loaded rows; "No results" while matches exist on page 4.
- **Spot:** `computed(() => data.value.items.filter(...))` on server-paginated data.
- **Fix:** Send the term to the server, or fetch all when the dataset is known-small.
- **Sources:** [TanStack Table: Column Filtering (client-side versus server-side)](https://tanstack.com/table/v8/docs/guide/column-filtering), [TanStack Table: Sorting (client-side versus server-side)](https://tanstack.com/table/v8/docs/guide/sorting)

### NV-I13. Search box value and URL out of sync after Back / clear
- **Bug:** Back restores old results but input still shows the new text (or vice versa); X button clears input but not the URL/query.
- **Cause:** Input `v-model` on local ref that is only initialised once (NV-A2).
- **Test:** Search "a", search "b" (committed), Back; clear with X; Escape.
- **Spot:** Search input `v-model` on `ref(route.query.q)` with no route watch; a clear (X) or Escape handler that sets the ref to `''` and never writes the URL.
- **Fix:** Input mirrors the URL value when the route changes; clearing writes `undefined`.
- **Sources:** [VueUse: useRouteQuery](https://vueuse.org/router/useRouteQuery/), [VueUse `useRouteQuery` source (watches `route.query[name]`)](https://github.com/vueuse/vueuse/blob/main/packages/router/useRouteQuery/index.ts)

### NV-I14. Searching does not reset page / selection

See NV-J1.

## J. Pagination and counts

### NV-J1. Filter/search/sort change doesn't reset page to 1
- **Bug:** On page 5, filter to something with 2 pages; table shows "No results" or page 5 of 2.
- **Test:** Go to page 3+, then change each filter, the search, page size, and sort.
- **Spot:** Filter setters that don't touch `page`.
- **Fix:** Reset `page` (to `undefined`) in the same atomic write as the filter (NV-A4).
- **Sources:** [TanStack Table: Pagination (`autoResetPageIndex`)](https://tanstack.com/table/v8/docs/guide/pagination)

### NV-J2. Total count off-by-one / range text wrong
- **Bug:** "Showing 1-25 of 24", "Showing 26-50 of 30", "0-0 of 0" versus "1-0 of 0", "Page 1 of 0".
- **Cause:** Range computed as `page * size` without `min(total)`; 0- versus 1-based page index mismatch between UI and API.
- **Test:** Totals of 0, 1, exactly page size, page size + 1; last page.
- **Spot:** `(page - 1) * size + 1` without empty-case guard; `Math.ceil(total / size)` giving 0; API `page` 0-based while URL 1-based.
- **Fix:** One helper; test the boundaries above.
- **Sources:** [Telerik feedback: Properly update the pager after deleting all the items from a page](https://feedback.telerik.com/kendo-jquery-ui/1358998-properly-update-the-pager-after-deleting-all-the-items-from-a-page), [Elastic UI: Table selection ("Showing {x}-{pageCount} of {totalCount}")](https://eui.elastic.co/docs/patterns/tables/table-selection/)

### NV-J3. Count disagrees with rows after mutation
- **Bug:** Delete an item: rows update (optimistic), count/pager doesn't (or the other way).
- **Spot:** Mutation `onSuccess` invalidating only the exact list key (with page and filters) or only the detail key; a total count from a separate query left out.
- **Fix:** Invalidate the list queries (all pages/filters through a shared key prefix) after mutation.
- **Ref:** [TKDODO-KEYS](https://tkdodo.eu/blog/effective-react-query-keys) (hierarchical keys for invalidation)

### NV-J4. Unstable server ordering duplicates/skips rows across pages
- **Bug:** The same item appears on page 1 and 2, or some never appear.
- **Cause:** Server sorts on a non-unique column without a tiebreaker; or new rows inserted while paging (offset pagination).
- **Test:** Sort by a column with many equal values (status), step through pages, collect IDs, check for duplicates.
- **Fix:** Tiebreaker (`ORDER BY status, id`); cursor pagination for live data.
- **Ref:** [MDN-SORT](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) (client sort is stable since ES2019, so this is a server issue)

### NV-J5. Page size not persisted / not validated
- **Bug:** Page size resets on refresh; `?size=100000` hangs the browser or 500s.
- **Spot:** `Number(route.query.size)` or `pageSize` from the URL passed to the API with no allow-list.
- **Fix:** In URL (or user preference) with an allow-list.
- **Sources:** [TanStack blog: Search params are state](https://tanstack.com/blog/search-params-are-state)

### NV-J6. Pagination flicker / layout jump
- **Bug:** Table collapses to a spinner between pages; pager jumps under the cursor.
- **Spot:** Paginated `useQuery` with `page` in the key and no `placeholderData: keepPreviousData`; `v-if="isPending"` spinner replacing the whole table.
- **Fix:** `placeholderData: keepPreviousData` + stable min-height.
- **Ref:** [TSQ-PAGE](https://tanstack.com/query/latest/docs/framework/vue/guides/paginated-queries)

### NV-J7. Prefetch / Next clickable on last page
- **Bug:** "Next" enabled on the last page, fetches an empty page.
- **Spot:** `hasNext = items.length === pageSize` or `:disabled="items.length < pageSize"` on a Next button.
- **Fix:** Disable using `hasMore`/`totalPages`, not "returned a full page".
- **Ref:** [TSQ-PAGE](https://tanstack.com/query/latest/docs/framework/vue/guides/paginated-queries)

## K. Empty, no-results and error states

### NV-K1. One "empty" state for three different situations
- **Bug:** "You have no services. Create one!" shown when a filter matches nothing, or when the API errored.
- **Test:** (a) truly empty account, (b) filter with no matches, (c) API 500/offline, (d) loading.
- **Spot:** `v-if="!items.length"` without checking `isError`, `isPending`, or active filters.
- **Fix:** Distinct states: loading, error with retry, no data (with a call to action), and no results for filters (show active filters + "Clear filters").
- **Sources:** [NN/g: Designing Empty States in Complex Applications](https://www.nngroup.com/articles/empty-state-interface-design/)

### NV-K2. "Clear filters" doesn't clear the URL (or everything)
- **Bug:** Clear button resets chips but URL keeps params so refresh brings them back; or clears search but not sort/page; or clears tab too.
- **Test:** Apply filter+search+sort+page; clear; check URL, input box, chips, and request.
- **Spot:** Clear handler that resets local refs or chips (`filters.value = {}`) with no URL write, or `router.replace({ query: {} })` that also drops the tab.
- **Fix:** Clear writes `undefined` for each filter key in one `replace`/`push`; decide whether sort/tab are filters.
- **Sources:** [Baymard: How to design applied filters](https://baymard.com/research-articles/how-to-design-applied-filters)

### NV-K3. Applied filters invisible
- **Bug:** Results look wrong because a filter applied from a deep link or a collapsed panel isn't shown.
- **Spot:** Filter controls inside a collapsed `Collapsible`, `Popover` or drawer, with no active-filter count or chips on the trigger or above the list.
- **Fix:** Show active-filter chips/count always; Baymard notes Back-removed filters must be visible.
- **Ref:** [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations)

### NV-K4. Filter option list depends on loaded data
- **Bug:** Filter dropdown options built from the current page's rows, so options vanish when filtered.
- **Spot:** `options = unique(items.map(i => i.status))`.
- **Fix:** Options from enum/metadata endpoint.
- **Sources:** [TanStack Table: Column Faceting (custom server-side faceting)](https://tanstack.com/table/v8/docs/guide/column-faceting)

### NV-K5. Error state not cleared when filters change
- **Bug:** One failed request leaves an error banner after successful later queries (or hides results).
- **Spot:** `const error = ref(...)` set in a `catch` or `onError` on a list and never cleared on the next success or filter change.
- **Fix:** Derive from the current query's `isError`, not a sticky local ref.
- **Sources:** [TanStack Query: Queries (status and `isError`)](https://tanstack.com/query/latest/docs/framework/vue/guides/queries)

## L. Selection and bulk actions

### NV-L1. Selection persists invisibly across pages/filters
- **Bug:** User selects 3 rows, filters, selects 2 more, clicks "Delete 5"; deletes items no longer visible.
- **Test:** Select on page 1, go to page 2 or change filter, inspect the bulk-action count and the request payload.
- **Spot:** Row selection (`rowSelection`, a `Set` of ids) with no reset in the filter, search or page watcher, and a bulk action reading the full selection.
- **Fix:** Either clear selection on filter/page change, or show "5 selected (3 not shown)" explicitly with a review step.
- **Sources:** [Shopify Polaris: Migrate unstable bulk actions](https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/unstable-bulk-actions)

### NV-L2. "Select all" ambiguity
- **Bug:** Header checkbox selects only visible page while the action says "all"; or selects all N matching including hidden ones without saying so.
- **Spot:** `toggleAllRowsSelected(true)` on a paginated or filtered table, or a header that calls `toggleAllPageRowsSelected` beside a bulk label that says "all".
- **Fix:** Gmail pattern: select page, then offer "Select all 213 matching"; bulk API takes filter criteria for the all case.
- **Sources:** [Shopify Polaris: Migrate unstable bulk actions](https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/unstable-bulk-actions), [PatternFly: Bulk selection](https://v5-archive.patternfly.org/patterns/bulk-selection)

### NV-L3. Selection keyed by index
- **Bug:** After sort/refetch, a different row is selected.
- **Spot:** `selected = Set<number>` of row indices.
- **Fix:** Key by stable id.
- **Sources:** [TanStack Table: Row Selection (`getRowId`)](https://tanstack.com/table/v8/docs/guide/row-selection), [Shopify Polaris: Migrate unstable bulk actions](https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/unstable-bulk-actions)

### NV-L4. Header checkbox indeterminate/state wrong
- **Bug:** Header shows checked when only some selected; or stays checked after a row is deselected or rows change.
- **Spot:** Header checkbox `:checked="selected.size > 0"` or `=== rows.length` with no `indeterminate` state.
- **Fix:** Compute from visible ids; `indeterminate` state.
- **Sources:** [WAI-ARIA APG: Checkbox pattern (mixed state)](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/), [TanStack Table: Row Selection](https://tanstack.com/table/v8/docs/guide/row-selection)

### NV-L5. Bulk action leaves stale selection
- **Bug:** After bulk delete, selection still contains deleted ids; next action fails.
- **Spot:** Bulk mutation `onSuccess` with no `selected.value.clear()`, `resetRowSelection()` or prune of the affected ids.
- **Fix:** Clear/prune selection on success.
- **Sources:** [TanStack Table: Row Selection](https://tanstack.com/table/v8/docs/guide/row-selection)

## M. Sorting

### NV-M1. Numbers sorted as strings
- **Bug:** Speeds `10000, 1000, 500` or VLANs `10, 100, 2, 20`.
- **Spot:** `.sort()` with no compareFn; `a.speed.localeCompare(b.speed)`; values typed as string from API.
- **Fix:** Numeric compare, or `Intl.Collator(locale, { numeric: true })` for mixed strings ("Port 2" < "Port 10").
- **Ref:** [MDN-SORT](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort); [MDN-COLLATOR](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator)

### NV-M2. Case-sensitive / non-locale sort
- **Bug:** "Zebra" before "apple"; "Ångström" after "Z".
- **Spot:** `a < b ? -1 : 1`; `.sort()` on strings.
- **Fix:** Shared `Intl.Collator` (reuse one instance for performance).
- **Ref:** [MDN-COLLATOR](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator)

### NV-M3. Null/undefined placement and crashes
- **Bug:** `null.localeCompare` throws; nulls float to the top on ascending and the bottom on descending (inconsistent); `a - b` treats `null` as 0.
- **Test:** Sort a column with missing values both directions.
- **Spot:** Comparator `a.x.localeCompare(b.x)` on an optional field, or `a.x - b.x` where `x` can be `null` or `undefined`.
- **Fix:** Explicit nulls-last in both directions (or per product decision).
- **Ref:** [MDN-SORT](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) (undefined sorted last without compareFn; null is passed to compareFn)

### NV-M4. Sorting by formatted string
- **Bug:** Dates sorted "01 Feb" < "02 Jan"; prices "$1,000" < "$200"; "1.5 Gbps" versus "500 Mbps".
- **Spot:** Sort key is the displayed/formatted value.
- **Fix:** Sort on raw value (ISO date/epoch, number in base unit).
- **Sources:** [TanStack Table: Sorting (sorting functions)](https://tanstack.com/table/v8/docs/guide/sorting)

### NV-M5. Sort compares comparator returning boolean
- **Bug:** Inconsistent ordering across browsers.
- **Spot:** `.sort((a, b) => a > b)`.
- **Fix:** Return negative/zero/positive.
- **Sources:** [MDN: Array.prototype.sort() (comparator requirements)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)

### NV-M6. Mutating sort on reactive/query data
- **Bug:** `.sort()` mutates TanStack cached array or props; other views reorder; Vue warnings on props.
- **Spot:** `data.value.sort(...)` in a computed.
- **Fix:** `toSorted()` or `[...arr].sort()`.
- **Sources:** [MDN: Array.prototype.sort() (sorts in place)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort), [MDN: Array.prototype.toSorted()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted)

### NV-M7. Client sort on server-paginated data
- **Bug:** Sorting only reorders the current page.
- **Spot:** `.sort(`, `.toSorted(` or client `sorting` on `data.items` from an endpoint that takes `page` or `size`.
- **Fix:** Send sort to the server.
- **Sources:** [TanStack Table: Sorting (client-side versus server-side)](https://tanstack.com/table/v8/docs/guide/sorting)

### NV-M8. Sort indicator and URL out of sync
- **Bug:** Arrow shows ascending while data is descending after Back/refresh; `aria-sort` wrong.
- **Spot:** Sort arrow or `aria-sort` bound to a local `ref` while the data's sort comes from `route.query`.
- **Fix:** Indicator derived from the parsed URL value.
- **Ref:** [BAYMARD-BACK](https://baymard.com/blog/back-button-expectations) ("sort direction shown in the UI should match")

## N. Tabs

### NV-N1. Tab not in URL
- **Bug:** Refresh or share returns to first tab; Back leaves the page instead of the previous tab (or vice versa if tabs push).
- **Test:** Select tab 3, refresh, copy link, Back.
- **Spot:** `TabsRoot` `v-model` on a local `ref('...')` on a routed page, with no query param or child route.
- **Fix:** Tab in query or child route; Reka `TabsRoot` `v-model` bound to a URL-backed computed; decide push versus replace (child routes push).
- **Sources:** [TanStack blog: Search params are state](https://tanstack.com/blog/search-params-are-state), [Reka UI `TabsRoot.vue` (`modelValue`)](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/Tabs/TabsRoot.vue)

### NV-N2. Invalid tab value
- **Bug:** `?tab=foo` renders no tab panel (blank); tab hidden by permission/feature flag still reachable by URL.
- **Spot:** `TabsRoot :model-value="route.query.tab"` with no check against the visible tab list, or a tab hidden by `v-if` (permission, flag) still selectable from the URL.
- **Fix:** Validate against the visible tabs list; `replace` to default.
- **Sources:** [TanStack blog: Search params are state](https://tanstack.com/blog/search-params-are-state)

### NV-N3. Per-tab state collisions
- **Bug:** Tabs each with their own list share `?page=` / `?q=`, so page 4 of tab A applies to tab B.
- **Spot:** Two tab panels whose lists use the same `queryParam`, `searchQueryParam` or `page` key, with no reset on tab change.
- **Fix:** Reset or namespace params on tab change.
- **Sources:** [TanStack blog: Search params are state ("colliding formats")](https://tanstack.com/blog/search-params-are-state)

### NV-N4. Tab content not lazy / refetching
- **Bug:** All tabs fetch on load (slow), or switching tabs refetches and loses scroll.
- **Spot:** `TabsContent` with `force-mount`, or every tab's `useQuery` called in the parent page.
- **Fix:** Lazy mount + query cache; Reka `TabsContent` unmounts inactive panels by default (`unmountOnHide: true`) unless `forceMount`.
- **Sources:** [Reka UI `TabsRoot.vue` (`unmountOnHide` defaults to `true`)](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/Tabs/TabsRoot.vue), [Reka UI `TabsContent.vue` (`forceMount`)](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/Tabs/TabsContent.vue)

## O. Cache and data freshness across navigation

### NV-O1. Stale data after Back
- **Bug:** Edit an item, Back to list: list still shows old name/status until a manual refresh.
- **Cause:** Mutation doesn't invalidate list queries; long `staleTime`.
- **Test:** Edit/delete/create, then Back and also navigate through menu.
- **Spot:** Mutation with no `invalidateQueries` or `setQueryData` for the list key prefix; `staleTime: Infinity` on a list that edits change.
- **Fix:** `invalidateQueries({ queryKey: ['services'] })` (prefix covers all filtered lists) or `setQueryData` on detail and list.
- **Ref:** [TKDODO-KEYS](https://tkdodo.eu/blog/effective-react-query-keys)

### NV-O2. Optimistic update reverted or duplicated on Back
- **Bug:** Toggle shows on, Back+Forward shows off (the refetch after navigation beat the mutation), or item appears twice.
- **Cause:** No `cancelQueries` before optimistic set; no rollback on error; no invalidation `onSettled`.
- **Test:** Throttle network, toggle, immediately navigate away and back.
- **Spot:** `onMutate` with `setQueryData` and no `cancelQueries`, no `onError` rollback, or no `onSettled` invalidation.
- **Fix:** Standard pattern: `cancelQueries`, snapshot, `setQueryData`, roll back in `onError`, and `invalidateQueries` in `onSettled`.
- **Ref:** https://tanstack.com/query/latest/docs/framework/vue/guides/optimistic-updates

### NV-O3. Detail shows list-derived partial data
- **Bug:** Detail seeded from list cache (`initialData`) shows stale or missing fields with no refetch.
- **Spot:** Detail `useQuery` with `initialData` taken from a list cache (`getQueryData(listKey)?.find(...)`) and no `initialDataUpdatedAt`.
- **Fix:** Use `placeholderData` (not `initialData`) for list-seeded detail, or set `initialDataUpdatedAt`.
- **Ref:** https://tanstack.com/query/latest/docs/framework/vue/guides/initial-query-data

### NV-O4. bfcache / tab restore
- **Bug:** Page restored from browser bfcache (after leaving the SPA to an external page/SSO and pressing Back) shows stale data or a stuck spinner.
- **Test:** Leave to an external site, press Back.
- **Fix:** Listen to `pageshow` with `event.persisted` and refetch; TanStack refetches on window focus by default.
- **Ref:** https://web.dev/articles/bfcache

### NV-O5. Previous company/account data shown after switching context
- **Bug:** After switching company, Back shows the previous company's list from cache.
- **Cause:** Company id not in query keys.
- **Spot:** Query key for company-scoped data without the company id, on a path where a company switch doesn't call `queryClient.clear()`.
- **Fix:** Include tenant in keys or `queryClient.clear()` on switch.
- **Sources:** [TanStack Query: Query Keys](https://tanstack.com/query/latest/docs/framework/vue/guides/query-keys)

## P. Misc navigation details

### NV-P1. Breadcrumbs lose list state
- **Bug:** Breadcrumb "Services" goes to an unfiltered list.
- **Spot:** Breadcrumb item `to: { name: 'services' }` (or a bare path) with no stored list query.
- **Fix:** As NV-F5.
- **Sources:** [Baymard: Return users to the same place in the product list](https://baymard.com/research-articles/return-same-place), [NN/g: Breadcrumbs](https://www.nngroup.com/articles/breadcrumbs/)

### NV-P2. Active nav highlighting wrong
- **Bug:** Parent menu not active on child routes, or two items active.
- **Spot:** `route.path === item.path`; `exact-active-class` misuse.
- **Fix:** Use `RouterLink` `isActive` (matches parent records) or route `meta`.
- **Sources:** [Vue Router: Active links](https://router.vuejs.org/guide/essentials/active-links.html)

### NV-P3. Duplicate navigation warnings / no-op clicks
- **Bug:** Clicking the current nav item does nothing when the user expects a reset to the default list.
- **Cause:** "duplicated" navigation failure.
- **Fix:** Decide behaviour; if reset is wanted, navigate to the location without the query.
- **Ref:** [VR-FAIL](https://router.vuejs.org/guide/advanced/navigation-failures.html)

### NV-P4. Feature-flagged or permission-gated routes reachable by URL
- **Bug:** Hidden menu item, but `/admin-only` loads (or crashes) when typed.
- **Spot:** Nav item hidden with `v-if` on a permission check or a feature flag, while its route record has no matching `meta` check or `beforeEnter`.
- **Fix:** Guard in the router (meta), not only in the nav.
- **Sources:** [Vue Router: Route Meta Fields](https://router.vuejs.org/guide/advanced/meta.html), [OWASP Top 10 A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

### NV-P5. Navigating while a request or mutation is in flight
- **Bug:** Toast/error from the previous page appears on the new page; mutation `onSuccess` pushes to a route after the user already left.
- **Spot:** Mutation `onSuccess: () => router.push(...)` or a toast after `await` with no check that the route is still the one the call started on.
- **Fix:** Guard post-mutation navigation with a check that the user is still on the origin route.
- **Sources:** [TanStack Query: Mutations (callbacks on `mutate` skip after unmount)](https://tanstack.com/query/latest/docs/framework/vue/guides/mutations)

---

## Q. Permission and role gated UI

### NV-Q1. Hidden or disabled chosen without a reason
- **Bug:** A missing "Change plan" button makes users think the feature doesn't exist. A disabled button gives no reason, and keyboard users can't reach it to read one.
- **Cause:** Permission checks map straight to `v-if` or `disabled`, with no thought about whether the user needs to know the option exists.
- **Test:** Sign in with each role (admin, technical, finance, read-only) and compare the actions on the same screen. Tab to each disabled control and check whether a reason is announced.
- **Spot:** `v-if="can('order')"` on actions users expect to see; `:disabled` with no tooltip or helper text; native `disabled` on a control that should explain itself.
- **Fix:** Show unavailable options instead of hiding them when users need to know they exist. Use `aria-disabled` (focusable and announced) with a reason, and block the click in JS. See DS-N3 (persona-value-display) for tooltips on disabled buttons.
- **Sources:** [Smashing Magazine: Frustrating design patterns, disabled buttons](https://www.smashingmagazine.com/2021/08/frustrating-design-patterns-disabled-buttons/), [CSS-Tricks: Making disabled buttons more inclusive](https://css-tricks.com/making-disabled-buttons-more-inclusive/)

### NV-Q2. Deep link to a forbidden action shows a blank page or a misleading "not found"
- **Bug:** A link to `/services/123/edit` opened by a viewer shows an empty form, or a 404 that suggests the service was deleted. NV-P4 covers whether the route is reachable; this item covers the message.
- **Cause:** The guard or the page treats "no permission" the same as "no data", or the 403 falls through to a generic not-found route.
- **Test:** As a read-only user, open edit, order, and admin URLs directly. Also open a link to a resource in a company the user can't access.
- **Spot:** A guard that redirects every failure to `/404`; a page that renders the form whatever the permission state.
- **Fix:** A clear access page that says what the user can't do, links to view the item, and says who to ask. Don't blame the user, and don't show codes.
- **Sources:** [GOV.UK Design System: Page not found pages](https://design-system.service.gov.uk/patterns/page-not-found-pages/)

### NV-Q3. Permission checks inconsistent across screens
- **Bug:** The list hides "Delete", but the detail page shows it. A bulk action includes items the user can't change.
- **Cause:** Each screen writes its own role check.
- **Test:** For each action, compare the list row menu, the detail page, the bulk toolbar, and the keyboard shortcut for every role.
- **Spot:** Inline `user.role === 'admin'` in templates; the same rule written differently in two components.
- **Fix:** One central `can(action, subject)` helper (CASL style) used by every screen, and bulk actions that filter or flag items the user can't act on.
- **Sources:** [CASL: guide introduction](http://casl.js.org/v6/en/guide/intro/)

### NV-Q4. Permission-loading flash
- **Bug:** Admin buttons flash on, then off, while the profile loads. A click during the flash fires.
- **Cause:** A dependent query that is disabled or still loading is treated as "allowed".
- **Test:** Throttle the network, load a page as a read-only user, and watch the actions during the first second. Try clicking one during the flash.
- **Spot:** `const canEdit = computed(() => !profile.value || profile.value.canEdit)`; checks that default to `true`.
- **Fix:** Treat `pending` as not allowed, and render gated controls only after the permissions query succeeds.
- **Sources:** [TanStack Query: Dependent queries](https://tanstack.com/query/latest/docs/framework/vue/guides/dependent-queries)

---

## R. Actions, exports and downloads

### NV-R1. Actions offered when they can't be taken (nothing to act on)
- **Bug:** "Export CSV" is enabled on an empty table and downloads a header-only file. "Delete selected" is enabled with 0 selected. "Download invoice" appears before the invoice exists and leads to a 404. A "Next" step link is active before the current step is valid.
- **Cause:** Toolbar actions are rendered without reference to the data state. This differs from FM-C4 (persona-form-behaviour) (a disabled submit that gives no reason): here the action should be disabled, or explained, but isn't.
- **Test:** For every toolbar and row action: an empty list, a list filtered to zero, 0 selected, and a resource in a pending state.
- **Spot:** Action buttons with no `:disabled` tied to `rows.length`, `selected.size`, or status.
- **Fix:** Disable with a reason (tooltip or inline text), or hide the action when it does not apply to the state.
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### NV-R2. A list or export is silently capped at the first API page or a row limit
- **Bug:** A company's services list is missing entries, filters give wrong results on later pages, or a downloaded inventory stops at 2000 rows. Nothing says data is missing.
- **Cause:** The client fetches one page and presents it as the full set, ignores the `next` link or total count, or the export endpoint has a row limit the UI doesn't mention.
- **Test:** Use an account with more items than one API page (and more than any export limit). Compare the list count, the total from the API, and the number of rows in the export. Filter, then go to page 2.
- **Spot:** A fetch with no loop over `next` or `page` when the UI shows "all"; a hard-coded `limit` or `size` on a list call; an export with no row count shown.
- **Fix:** Follow pagination to the end (or page in the UI), show the total, and when a cap applies say so ("Showing the first 2000 of 5,312 rows").
- **Sources:** [RFC 8288: Web Linking (`next` relation for paged collections)](https://www.rfc-editor.org/rfc/rfc8288)

### NV-R3. A side-channel download (anchor href or `window.open`) skips the API client's context headers
- **Bug:** In a managed-account or company context, a CSV or PDF download comes from the wrong account, or fails, while the page itself shows the right data. This is related to NV-O5.
- **Cause:** The download URL is opened directly with `<a href>` or `window.open`, so the context header that the API client adds to every request is missing. An anchor can't send custom headers.
- **Test:** Switch into a managed account, then download every CSV, PDF, and statement on the page. Compare the contents with the on-screen data, and check the request headers in DevTools.
- **Spot:** `window.open(apiUrl)` or `<a :href="`${baseUrl}/…/csv`" download>` for API endpoints; a download path that bypasses the shared API client.
- **Fix:** Fetch the file through the API client (so it carries the same headers), then save it from a Blob URL. Or have the server issue a short-lived signed URL that already carries the context.
- **Sources:** [MDN: `<a download>` (no custom headers; use fetch plus a Blob URL)](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#download)

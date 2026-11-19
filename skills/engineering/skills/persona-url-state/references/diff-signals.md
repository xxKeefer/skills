# persona-url-state diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. A line marked `(rule N)` adds a case to that rule, and the numbered rules hold the other cases. The full case (cause, inputs, fix) is in the linked catalogue under the same ID.

## [persona-url-state catalogue](catalogue.md)

- NV-A9: Paired watchers in both directions: `watch(filters, () => router.replace(...))` plus `watch(() => route.query, ...)`, or `{ deep: true }` on `route.query` → One source (the URL); compare serialised strings before writing [default: change-requested]
- NV-B2: URL write inside `@input` or `@update:modelValue` of a slider or text field with no throttle or debounce → Throttle URL writes, or write on `change` [default: nit]
- NV-B3: A URL helper that uses `replace` for every param, or one page mixing `push` and `replace` for the same kind of filter → Choose `push` or `replace` per param, consistently [default: nit]
- NV-B5: `await mutate(); router.push({ name: 'detail' })` from a create route, or wizard state in Pinia not cleared on success → `router.replace` to the result page; reset the form store [default: change-requested]
- NV-B6: `const step = ref(1)` driving a multi-step wizard, with the step absent from the route → Step in the query or params, `push` per step [default: nit]
- NV-C3: `scrollBehavior` returning `savedPosition` with no `{ top: 0 }` fallback, or `createRouter` with no `scrollBehavior` → `return savedPosition ?? { top: 0 }`; reset inner scrollers on push [default: nit] (rule 8)
- NV-C4: `scrollBehavior` returning `{ top: 0 }` with no `to.path === from.path` branch for query-only changes → Keep scroll on same-path query changes; scroll in the pager [default: nit] (rule 8)
- NV-C5: `scrollBehavior` with no `to.hash` branch, `el: to.hash` with no offset, or `:id` built from data used as a hash target → `{ el: to.hash, top: headerHeight }` or `scroll-margin-top`; wait for the target [default: nit]
- NV-C6: `useInfiniteQuery` with `gcTime: 0`, or a "Load more" handler appending pages to a local `ref([])` → Keep the infinite query cached, or the loaded count in the URL [default: nit] (rule 8)
- NV-D4: `router.push({ path: '/x', params: { id } })`, or params not declared in the route's path used to pass state → Use `name` with params, or query or history state [default: nit]
- NV-D5: `route.params.id as number`, or `Number(route.params.id)` with no `NaN` check → Parse and validate the param [default: nit] (rule 4)
- NV-D7: `route.path === '/services'`, or `startsWith` on `route.path` for active nav or logic → Compare `route.name`; pick one canonical path [default: nit]
- NV-E1: `redirect: to.path` in an auth guard, or `` `/login?redirect=${to.fullPath}` `` built without encoding → Store `to.fullPath` through `query: { redirect }` [default: nit] (rule 9)
- NV-E3: Guard returning a redirect to a route that the same guard also rejects, with no `to.name` exemption, or `next()` called twice → Exempt the target route; return a location instead of calling `next` [default: change-requested]
- NV-E4: `document.title =` set in `onMounted` or once in setup, or a detail route with only a static `meta.title` → `useTitle` with a computed that includes the entity name [default: nit]
- NV-F3: Row `@click`/`@row-click` that navigates, with an inner checkbox, menu or copy button lacking `@click.stop` → `@click.stop` on inner controls, or link only the primary cell [default: nit]
- NV-G3: Dialog `open` computed from `route.query.modal`/`id` with no validation and no loading or not-found branch → Validate the URL value; handle loading and not-found in the dialog [default: nit] (rule 4)
- NV-G4: Reka `DialogRoot` with `v-model:open` in a layout-level component, or a manual `document.body.style.overflow` lock → Close overlays on route change; own them in the routed view [default: change-requested]
- NV-H2: `.split(',')` or `.join(',')` on query values holding user-defined names or tags → Repeated keys or per-item encoding; comma only for enums [default: nit]
- NV-H6: URL `page` used with no clamp against `totalPages`, or a delete on a paginated list with no step back → `replace` to the last page when `page > totalPages > 0` [default: nit] (rule 10)
- NV-H9: Changed key string in `queryParam`, `searchQueryParam`, `useRouteQuery` or a codec in the project's URL-filter composable, with no legacy read → Map the old name on read and `replace` it [default: nit]
- NV-I1: A query key bound straight to the `v-model` value of a search input, with no debounced value between them → Debounce the value feeding the query key [default: nit]
- NV-I2: `refDebounced`/`useDebounceFn` above 500 ms on a search, with no submit or blur flush → Flush on Enter; show pending while `debounced !== raw` or `isFetching` [default: nit]
- NV-I6: `term.length < n` guard or `enabled` length check on a search with no hint shown → Tell the user the minimum ("type at least 2 characters") [default: nit]
- NV-I12: `computed(() => data.value.items.filter(...))` over a server-paginated response → Send the term to the server [default: nit]
- NV-J2: `(page - 1) * size + 1` with no empty-case guard, `Math.ceil(total / size)` giving 0, or a 0-based API page beside a 1-based URL → One range helper covering the empty and last-page cases [default: nit]
- NV-J7: `hasNext = items.length === pageSize`, or Next `:disabled` from the returned row count → Disable from `hasMore` or `totalPages` [default: nit] (rule 10)
- NV-K1: `v-if="!items.length"` empty state with no check of `isError`, `isPending`, or active filters → Separate loading, error, no data and no-match states [default: nit] (rule 12)
- NV-K3: Filters inside a collapsed `Collapsible`, `Popover` or drawer with no active count or chips outside it → Always show active-filter chips or a count [default: nit] (rule 12)
- NV-K4: Filter options built from loaded rows: `unique(items.map(i => i.status))` → Take options from the enum or a metadata endpoint [default: nit]
- NV-L2: `toggleAllRowsSelected(true)` on a paginated or filtered table, or page-only select beside an "all" label → Select the page, then offer "Select all N matching" [default: change-requested]
- NV-L3: Row selection held as `Set<number>` of row indices → Key selection by stable id [default: nit]
- NV-L4: Header checkbox `:checked` from `selected.size > 0` or `=== rows.length` with no `indeterminate` → Compute from visible ids; set `indeterminate` [default: nit]
- NV-L5: Bulk mutation `onSuccess` with no `clear()`, `resetRowSelection()` or prune of the ids → Clear or prune the selection on success [default: nit]
- NV-M2: String sort with `a < b ? -1 : 1` or a bare `.sort()` on names → One shared `Intl.Collator` [default: nit]
- NV-M3: `a.x.localeCompare(b.x)` on an optional field, or `a.x - b.x` on a nullable number → Explicit nulls-last in both directions [default: change-requested] (rule 11)
- NV-M8: Sort arrow or `aria-sort` bound to a local `ref` while the data sort reads `route.query` → Derive the indicator from the parsed URL value [default: nit]
- NV-N3: Lists in two tabs sharing a `queryParam`, `searchQueryParam` or `page` key, with no reset on tab change → Namespace the keys per tab, or reset on tab change [default: nit]
- NV-N4: `TabsContent` with `force-mount`, or every tab's query called in the parent → Lazy mount panels; let the query cache keep data [default: nit]
- NV-P2: `route.path === item.path` for active nav, or misused `exact-active-class` → RouterLink `isActive`, or route `meta` [default: nit]
- NV-P4: Nav item behind `v-if` permission or flag while its route has no `meta` check or `beforeEnter` → Guard the route, not only the menu [default: change-requested]
- NV-Q1: `v-if="can('order')"` on an action users expect to see, or `:disabled` with no tooltip or helper text → Show it with `aria-disabled` and a stated reason [default: nit]
- NV-Q3: Inline `user.role === 'admin'` in a template, or the same permission rule written differently in two components → One central `can(action, subject)` helper [default: nit]
- NV-R1: Toolbar or bulk action button with no `:disabled` tied to `rows.length`, `selected.size`, or status → Disable with a reason, or hide when it doesn't apply [default: nit]

---
name: persona-url-state
description: "Staff URL-state and navigation reviewer. Reviews a diff for what refresh, a shared link, Back, and Forward do to a screen: filters, search, and tabs held in refs instead of the URL, query params read once so Back changes the URL but not the screen, router.push per keystroke or on a redirect/cancel (Back traps), query writes that drop other params, query values used unparsed (arrays, 'false', page=abc), filter changes that keep the old page or a hidden selection, tables that silently hide rows, router.back() with no fallback, overlays and scroll on Back, list sorting by display string, and empty states that can't tell 'no data' from 'no matches'. Every finding names the exact steps that break it. Use when the user asks for a URL / query-param / back-button / filter / pagination review, or invoke through mob-review. Does not cover link-vs-button and new-tab clicks (persona-a11y), races and route reads after an await (persona-async-state), query keys (persona-tanstack), open redirects (persona-security), or unescaped search text (persona-text-input)."
disable-model-invocation: true
---

Read [`PERSONA-CONTRACT.md`](../../PERSONA-CONTRACT.md) before you start, and follow every rule in it.

# persona-url-state: staff URL-state and navigation reviewer

You review a list or a flow by doing what users do: filter, open a row, press Back; refresh on page 3; paste the URL into a new tab; edit the query string by hand; press Back after a redirect. If the screen then shows something other than what the URL says, that's your finding.

This lane exists because Back and URL bugs keep shipping, and Baymard found 59% of sites get Back wrong somewhere ([Baymard](https://baymard.com/blog/back-button-expectations)). Examples: Back trapped by a redirect that pushes, Back going nowhere after a reload, Forward returning to a cancelled form, list rows past 10 silently hidden, filters lost between tabs.

The catalogue in [references/catalogue.md](references/catalogue.md) has the full list of `NV-` items; [references/fixtures.md](references/fixtures.md) has the per-list smoke script;

## Guard

Run only if the **changed lines** of non-test `.vue`/`.ts` under `apps/**` or `libs/**` touch the URL, history or a list control: `route.query`/`route.params`, `useRoute`, `useRouteQuery`, the project's URL-filter composable, `router.push`/`router.replace`/`router.back`/`router.go`, `history.`, `scrollBehavior`, a `queryParam`/`searchQueryParam` prop, list filter/search/sort/pagination/selection state, a tab's active value, a `.sort(`/`.toSorted(` on list data, a list fetch's page size or limit, an export or download (`window.open`, `<a :href … download>`), or a permission check on a control or route guard (`beforeEach`/`beforeEnter`). Otherwise return zero findings and stop. Judge the hunks, not the file. A hunk that only declares a route in `definePage({...})`/route `meta` doesn't count.

## Scope

Lane paths: `'*.ts' '*.vue' ':!*.spec.ts' ':!*.test.ts'`.

Read enough of the page to know which state is meant to survive a refresh and which isn't, and whether vue-router reuses the component across params.

When a fix needs the design system's data table props, a URL-filter composable, `useRouteQuery`, or the vue-router query parser, read [references/stack-facts.md](references/stack-facts.md).

## What you review

Each finding names the steps: "filter Status = Live, open a service, press Back: the filter is gone".

**State in the URL**

1. **List or tab state not in the URL (Nit; Change Requested when the diff moves state that was in the URL into a ref or store).** A new list page's filters, search, or active tab held in a `ref` or Pinia, so refresh, a shared link, and Back lose them. Use the data table's `queryParam`/`searchQueryParam` props, the project's URL-filter composable, or `useRouteQuery`. A missing sort or page param is Future at most. (NV-A1, NV-N1)
2. **Query or param read once (Change Requested).** `const status = ref(route.query.status)`, or a param read in `setup` with no watch. vue-router reuses the component, so Back, a same-route link, or a new id changes the URL but not the screen, or keeps the previous record's local state. Read through `computed`/`useRouteQuery`, or watch it, and reset local state when the id changes. (NV-A2, NV-D1, NV-D2)
3. **Query write drops other params (Change Requested).** `router.replace({ query: { search } })` without `...route.query`, so setting search wipes the status filter and tab. Two params written in two calls can also lose one. (NV-A3, NV-A4)
4. **Query value used unparsed (Change Requested).** `route.query.x` cast `as string` or `as string[]` when it can be either (or `null`); `"false"` treated as truthy; `Number(route.query.page)` with no check, so `?page=abc` gives `NaN` and `?page=-1` or `?page=999` reach the API; an enum or sort param not checked against the allowed values. Use a codec and fall back to the default. (NV-H1, NV-H3, NV-H4, NV-H5, NV-H6)
5. **URL noise (Nit).** Default values written to the URL, `?q=` left after clearing, or params reordered on every write so each change triggers a navigation. (NV-A5, NV-A6, NV-A7)

**History**

6. **Wrong history mode (Change Requested).** `router.push` on every keystroke or every filter change (each Back undoes one letter); a redirect, normalisation step, or "Cancel" that pushes, so Back lands on the page that redirected and sends the user forward again. Use `replace` for both. (NV-B1, NV-B4)
7. **`router.back()` with no fallback (Change Requested).** A Back or Cancel button calling `router.back()`/`history.back()` on a page that can be opened from a link, a new tab, or a reload: Back then leaves the app or does nothing. Check `window.history.state?.back` and fall back to a named route. (NV-B9)
When the diff touches a modal or drawer history entry, `scrollBehavior`, a post-login redirect, or a breadcrumb link, read [references/overlays-scroll-and-context.md](references/overlays-scroll-and-context.md). It holds rules 8 and 9.

**Lists**

10. **Filter change keeps the old page or a hidden selection, or rows go missing (Change Requested).** Changing a filter, search, or sort leaves the table on page 5 of 2 ("No results"); a bulk selection survives a filter or page change, so a bulk action hits rows the user can't see; pagination turned off on a table that can exceed one page, so rows past 10 vanish. Reset to the first page, and clear or scope the selection. (NV-J1, NV-L1, NV-H6, NV-J7)
When the diff sorts list data or changes a list's empty state, read [references/sorting-and-empty-states.md](references/sorting-and-empty-states.md). It holds rules 11 and 12.

When the diff touches a list fetch's page size or limit, an export or download, a permission check, or a route guard, read [references/fetching-exports-and-permissions.md](references/fetching-exports-and-permissions.md). It holds rules 13 to 16.

**Catalogue sweep.** After the numbered rules, check the changed hunks against [references/diff-signals.md](references/diff-signals.md). Report a match at its default severity (a numbered rule's severity wins when both apply), with the case ID in `detail`. Drop a match you can't tie to a changed line and a concrete input.

## Out of lane: do NOT report

- **A logout or company switch in another tab that this tab never hears about** → `persona-resilience`.
- **`@click="router.push"` on a row or button, so cmd-click and middle-click don't open a new tab** → `persona-a11y` #2.
- **Out-of-order search responses, a route param read after `await`, loading and error states** → `persona-async-state`.
- **A filter or page missing from the query key, `placeholderData` between pages** → `persona-tanstack`.
- **User text in a URL or regex unescaped, search not trimmed or accent-folded** → `persona-text-input`.
- **An unchecked `?redirect=`** → `persona-security` #6.
- **A blank page or endless spinner for an unknown id** → `persona-error-handling`.
- **Empty-state copy** → `persona-i18n` / `persona-decisions-log`. **Which empty-state component** → `persona-design-system`.
- **Whether a Back or refresh test exists** → `persona-test-design`.
- Anything on an unchanged line.

## Severity

- **Change Requested:** URL state moved into a ref or store (1), query read once (2), query write drops params (3), unparsed query value (4), wrong history mode (6), `router.back()` with no fallback (7), page or selection not reset, or rows hidden (10), sort by string (11), a list or export silently capped (13), an API download that skips the client's headers (14), a permission check that allows while loading (15).
- **Nit:** new list page with state not in the URL (1), URL noise (5), Back with overlays or scroll (8), context lost on the way back (9), shared empty state (12), a forbidden deep link that shows the page or "not found" (16).
- **Future:** sort and page in the URL for the design system's data table; a shared URL-filter composable. Suggest, never block.
- **Never:** "should be in the URL" for a transient UI toggle (an expanded row, a hover, an open tooltip); anything on an unchanged line.
- Catalogue sweep matches: the line's default severity.

## Output

- `category`: `url-state`.
- `detail`: the steps (filter, open, Back, refresh), and what the user then sees.
- `suggestion`: the fix.
- Example `summary`: `search pushes a history entry per keystroke — use replace`.
- Each finding names the steps and the wrong screen.

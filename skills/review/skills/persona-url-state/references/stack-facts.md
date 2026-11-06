# Stack facts

Stack facts to use in fixes:
- If the design system's data table syncs column filters and search through URL query params (a `queryParam` / `searchQueryParam` prop using `useRouteQuery` in `replace` mode), use those props.
- If the project has a URL-filter composable with typed codecs and defaults, use it. Otherwise `useRouteQuery` from `@vueuse/router` with `mode: 'replace'` is the default.
- If the project has a helper that turns an array or missing route param into `undefined`, use it.
- Sort and pagination may be plain refs in the design system's data table by design, and a table may keep its filters in a Pinia store. Don't flag code the diff leaves alone.
- vue-router's `parseQuery` gives a string for `?a=1`, an array for `?a=1&a=2`, `null` for `?a`, and decodes `+` as a space ([query.ts](https://github.com/vuejs/router/blob/main/packages/router/src/query.ts)).

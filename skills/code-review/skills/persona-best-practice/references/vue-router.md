# Vue Router: modern-API reference (written against 5.2.0)

This file was written against `vue-router` **5.2.0**; **5.4.0** was the latest published (same major, no rule
difference: 5.3 shipped fixes and perf only; 5.4 added `useScrollRestoration`/`onRouteRendered`, restores hash/top scroll by default, and moved more under `experimental`, nothing promoted out of
experimental). File-based routing is supplied by the **core package** (`vue-router/vite`). There is no separate `unplugin-vue-router` dependency; it was
merged into the router in v5.

## File-based routes for new pages

New pages live in `src/pages/` and are picked up by the `vue-router/vite` plugin (`[param].vue`
for dynamic segments, `[[param]].vue` for optional). Hand-registering a new page in a route
array → **Change Requested**; that route silently sits outside the generated `RouteNamedMap`
and loses typed navigation.

Routes are consumed from the virtual module, never rebuilt by hand:

```ts
import { routes, handleHotUpdate } from 'vue-router/auto-routes'   // ✅
```

A changed router entry that imports from `unplugin-vue-router/...` or `vue-router/auto` →
**Change Requested**; those specifiers are gone in v5.

## Per-page route config: `definePage()`

Route metadata for a page (name, meta, alias, path override) goes in a `definePage({...})` call
inside the page's `<script setup>`, not in a separate route array or an `<route>` block. A new
page that pushes its `meta` into a central array → **Nit**.

## Typed navigation over stringly-typed paths

Prefer the typed helpers (`router.push({ name: 'route-name', params })`, typed `RouteLocation`)
over `router.push('/some/path')` where the generated `RouteNamedMap` covers the route → **Nit**.

Route meta read through an untyped cast is a **typing** finding, not this persona's. See the
lane split with `persona-typing` in `SKILL.md`.

## Generated types must stay wired up

The plugin writes `src/route-map.d.ts` (configured through the plugin's `dts:` option). It is generated, 
a changed line inside it is a regeneration artefact, never a hand edit. A hand-modified
`route-map.d.ts` in a diff → **Change Requested**.

Volar needs the router plugins registered in the *app's own* `tsconfig.app.json` (Volar resolves
plugin specifiers relative to the declaring config). An app adopting file-based routing without
`vue-router/volar/sfc-route-blocks` in `vueCompilerOptions.plugins` → **Nit**.

## Experimental in 5.x: do not require

Param parsers (`experimental.paramParsers` + `definePage({ params: { path: { id: 'number' } } })`)
and data loaders are shipped but documented as **experimental**. Check whether the project uses them. You
may mention one as a **Future** if a diff hand-rolls the same thing (a `Number(route.params.id)`
cast repeated across a page tree); never raise not-using-them as a finding.

## Not your lane

Navigation-guard correctness, redirect loops, and auth gating → `persona-architecture` /
`persona-security`. You only flag "a newer router API exists".

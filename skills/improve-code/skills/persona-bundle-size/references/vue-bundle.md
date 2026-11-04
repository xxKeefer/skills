# Bundle-size reference: Vue 3.5 / Vue Router 5 / Vite 8 (Rolldown)

Grounded in the upstream docs (fetched 2026-09-25).
Re-verify with `update-personas` after a Vite/Vue major.

## What the docs say

**Vue: Performance guide** (<https://vuejs.org/guide/best-practices/performance.html>)
- "Be cautious of size when introducing new dependencies! In real-world applications, bloated bundles are most often a result of introducing heavy dependencies without realizing it."
- Prefer ES-module, tree-shaking-friendly deps (`lodash-es` over `lodash`). Size-check with <https://bundlejs.com/>, but "measure with your actual build setup for most accuracy".
- "Lazy loading is best used on features that are not immediately needed after initial page load."
- "For applications using Vue Router, it is strongly recommended to use lazy loading for route components."
- Unused built-ins (`<Transition>`, `<KeepAlive>`…) tree-shake away. Pre-compiled templates keep the ~14 kB runtime compiler out of the bundle, so a runtime-template build (`vue/dist/vue.esm-bundler.js` alias, a string `template:` option) brings it back.

**Vue: Async components** (<https://vuejs.org/guide/components/async.html>)
- `defineAsyncComponent(() => import('./X.vue'))` "only calls the loader function when it is actually rendered on the page" and passes props/slots through, so it drops in for the static import.
- Options: `loadingComponent`, `delay` (default **200 ms**, so fast networks don't flicker), `errorComponent`, `timeout` (default **Infinity**). With no `errorComponent`, a failed chunk load renders nothing.
- The `hydrate: hydrateOnVisible()/hydrateOnIdle()/…` strategies are SSR-only. Check whether the app uses SSR. If it does not, they don't apply.

**Vue: Suspense** (<https://vuejs.org/guide/built-ins/suspense.html>)
- `<Suspense>` is **experimental**. Async components are suspensible by default: inside a `<Suspense>`, their own `loading`/`error`/`delay`/`timeout` options are **ignored** unless `suspensible: false`.

**Vue: Compile-time flags** (<https://vuejs.org/api/compile-time-flags.html>)
- `__VUE_OPTIONS_API__` (default `true`). Disabling it gives smaller bundles but may break Options-API third-party libraries.
- `__VUE_PROD_DEVTOOLS__` and `__VUE_PROD_HYDRATION_MISMATCH_DETAILS__` (default `false`). Turning either on adds code. "Only enable this for debugging purposes."

**Vue Router: Lazy loading** (<https://router.vuejs.org/guide/advanced/lazy-loading.html>)
- Route `component: () => import('./views/X.vue')`. The router fetches it the first time the route is entered, then caches it.
- "**Do not use async components as route components.**" (`defineAsyncComponent` belongs inside a route component, not as the route component.)

**Vite 8** (<https://vite.dev/guide/features.html>, <https://vite.dev/guide/build.html>)
- `import.meta.glob` is lazy by default: each match gets its own chunk. `{ eager: true }` inlines every match, so there's no split.
- Named imports from JSON (`import { field } from './x.json'`) tree-shake. A default import pulls in the whole file.
- CSS used by an async chunk is extracted into its own file, so a lazy component also defers its CSS.
- Dynamic imports get an automatic parallel preload of their dependencies. Stale-deploy chunk failures fire `vite:preloadError` (`event.preventDefault()` suppresses the throw).
- Vite 8 bundles with **Rolldown**. Chunk control is `build.rolldownOptions.output.codeSplitting` (`groups: [{ name, test, priority, minSize, maxSize }]`), which supersedes `manualChunks`. Rolldown warns that manual splitting "can change the behavior of the application if side effects are triggered before the corresponding modules are actually used."

## What to look up in the project

Read the repo before flagging. These facts change what a finding can promise.

- **Routing:** are routes file-based (auto-lazy) or arrays of `() => import(...)`? Any static route import is a regression where the rest are lazy.
- **Async components:** how the repo wraps `defineAsyncComponent` today (bare, or with loading/error/timeout), and whether `<Suspense>` appears anywhere.
- **Known heavy deps:** map libraries, PDF generators, terminal/WASM bundles, chart and editor libraries. Check where each is imported (top level or inside a handler).
- **Chunking:** read the app's `vite.config.*`. A rule that buckets all of `node_modules` into one `vendor` chunk means a dependency used only behind a lazy boundary still ships eagerly, so lazy-importing a new dependency defers nothing unless the chunk config changes too. A lib built one chunk per source module externalises `dependencies` and `peerDependencies`.
- **Libs:** are they consumed as built `dist/` output through `exports`? Which declare `sideEffects` (`["**/*.css"]` or `false`) and which declare none, so bundlers assume every module has side effects? Does a UI lib barrel exist?
- **i18n:** does a build plugin split locales into tiers (base / core / lazy) with a namespace loader? Do other languages load through an async loader, or are all bundled?
- **Compile flags:** does an app disable the Options API through `vue({ features: { optionsAPI: false } })`? Does any app set `__VUE_PROD_DEVTOOLS__`?
- **Measurement:** is a bundle-analysis plugin (such as `@codecov/vite-plugin` with `enableBundleAnalysis`) wired up? Is there a size-limit gate, a visualizer, or a `chunkSizeWarningLimit`? Does a lint rule catch namespace or heavy-dependency imports?

## Quick checks (cheap, no build)

```bash
# Is the "lazy" module still statically imported somewhere eager? (If yes, splitting gains nothing.)
rg -n "from ['\"].*<ModuleName>(\.vue)?['\"]" apps libs -g '!*.spec.ts' -g '!*.stories.ts'
# Does this app handle stale-chunk failures?
rg -n "vite:preloadError" apps/<app>/src
# Size of a new dependency (published, minified + gzip)
#   https://bundlejs.com/?q=<pkg>   or   https://pkg-size.dev/<pkg>
# ESM / tree-shake signals of a new dependency
pnpm view <pkg> module exports sideEffects type --json
```

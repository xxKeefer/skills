# persona-best-practice: Vue Router 5 rules

**Vue Router 5**
- New pages should be file-based (`vue-router/vite`, `src/pages/`, `[param].vue`). Flag manual route registration for a new page. Prefer typed route helpers over stringly-typed `push('/path')` where typed navigation exists.
- Router 5 merged `unplugin-vue-router` into core: a changed import from `unplugin-vue-router/...` or `vue-router/auto` is a dead specifier. Change Requested. Routes come from `vue-router/auto-routes`.
- Per-page route config belongs in `definePage({...})` in the page's `<script setup>`, not a central route array (Nit). **Exception:** a `<route lang="json">` SFC block is the house convention in apps that already use it on every page. Do not flag a new page for matching its siblings. Count the app's pages first (`rg -l '^<route' apps/<app>/src/pages`).
- The generated route-types file (`route-map.d.ts`) is regenerated output; a hand edit to it in a diff is Change Requested.

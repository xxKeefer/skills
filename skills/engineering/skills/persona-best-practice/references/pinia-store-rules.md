# persona-best-practice: Pinia 4 rules

**Pinia 4**
- Setup stores `defineStore('id', () => {...})` for new stores over options stores. New state must be Pinia, not a legacy store such as Vuex (touch the legacy store only to modify existing state). (Reactivity loss from store destructuring / `storeToRefs` is `persona-vue-reactivity`'s call, not yours.)
- **Pinia 4 is ESM-only**: `require('pinia')` in a changed `*.cjs`/CJS config or script no longer resolves. Change Requested.
- **`@vue/devtools-api` is a peer dependency**: a changed `package.json` adding `pinia` without it is an incomplete install. Change Requested.
- `piniaSymbol` is a public export: flag a hand-rolled injection key or a cast at the internal symbol.

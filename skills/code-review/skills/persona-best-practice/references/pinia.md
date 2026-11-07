# Pinia: modern-API reference (written against 4.0.2)

This file was written against Pinia **4.0.2**; 4.1.0 later added `getStores()` and a dev warning when disposing a replaced store; no rule difference). New client state is
Pinia, never Vuex (touch Vuex only to modify existing legacy state). Peer requirements Pinia 4
imposes: Vue `^3.5.11`, TypeScript `>=5.6`, `@vue/devtools-api` `^8.1.5`. Check the project's installed
versions before you flag.

## Setup stores over options stores

New stores use the setup form `defineStore('id', () => {...})` (refs for state, computed for
getters, functions for actions) over the options object form. → **Nit** when a new store uses
the options form.

```ts
export const useThingStore = defineStore('thing', () => {
  const items = ref<Thing[]>([])
  const count = computed(() => items.value.length)
  const add = (t: Thing) => { items.value = [...items.value, t] }
  return { items, count, add }
})
```

## Pinia 4 is ESM only

Pinia 4 dropped the CJS build. `require('pinia')` no longer resolves, so a changed `*.cjs`
file, CJS config, or script that requires pinia breaks the build → **Change Requested**. App
code is already ESM; this only bites tooling and leftover config.

## `@vue/devtools-api` is a peer dependency in Pinia 4

It is no longer bundled: every package that depends on pinia declares it explicitly (smaller
install, less supply-chain surface). A changed `package.json` that adds `pinia` without
`@vue/devtools-api` → **Change Requested**.

## Consuming a store

- `storeToRefs(store)` to pull reactive state/getters out without losing reactivity. Pinia 4
  skips nullish values gracefully and emits a diagnostic for invalid properties. Don't
  hand-roll a guard around it.
- Actions can be destructured directly (they're bound).
- `piniaSymbol` is a public export in 4: flag a hand-rolled injection key or a cast at the
  internal symbol for reading the pinia instance → **Nit**.

Note: whether a given destructure *loses* reactivity is a **correctness** call owned by
`persona-vue-reactivity`, not this persona. You only flag "the options-store form was used
where a setup store is the modern default".

## Not your lane

Store reactivity correctness → `persona-vue-reactivity`. Server state that should be TanStack
Query rather than a store → `persona-tanstack`.

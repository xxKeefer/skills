# persona-code-quality: hand-rolled smell table

| Hand-rolled smell | Replace with | Lib |
|---|---|---|
| `setTimeout`-based debounce | `useDebounceFn`/`refDebounced` (reactive) or `debounce` | vueuse / es-toolkit |
| timestamp-guard throttle | `useThrottleFn`/`refThrottled` or `throttle` | vueuse / es-toolkit |
| `JSON.parse(JSON.stringify(x))` clone | `cloneDeep` | es-toolkit |
| manual `document.addEventListener('click')` outside-click | `onClickOutside` | vueuse |
| `addEventListener`/`removeEventListener` in mount/unmount | `useEventListener` | vueuse |
| `new ResizeObserver` by hand | `useResizeObserver`/`useElementSize` | vueuse |
| `localStorage` get/set + reactive sync | `useLocalStorage`/`useStorage` | vueuse |
| `window.matchMedia` reactive breakpoint | `useMediaQuery` | vueuse |
| `reduce` into `{key:[...]}` | `groupBy`/`keyBy` | es-toolkit |
| `[...new Set(arr)]` / manual dedupe | `uniq`/`uniqBy` | es-toolkit |
| manual deep/JSON equality | `isEqual` | es-toolkit |
| `Object.assign({}, a, b)` deep-merge intent | `merge`/`toMerged` (immutable) | es-toolkit |
| delete-keys-into-new-object | `omit`/`pick` (or `reactiveOmit`/`reactivePick` for reactive sources) | es-toolkit / vueuse |
| regex case conversion | `kebabCase`/`camelCase`/`snakeCase`/`startCase`/`capitalize` | es-toolkit |
| `x != null && x !== undefined` | `isNotNil`/`isNil` | es-toolkit |
| `Math.min(Math.max(...))` | `clamp` | es-toolkit |
| manual `Date`/`getTime()` deltas, add/subtract days, timezone math | `@internationalized/date` (`now`, `CalendarDate`, `add`, comparators) | @internationalized/date |

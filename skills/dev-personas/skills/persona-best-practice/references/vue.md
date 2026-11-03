# Vue: modern-API reference (written against 3.5.40)

This file was written against Vue **3.5.40**; later 3.5 patches have no API difference for these rules.
Every API below is stable on this version. The job: use the modern first-class API, not the
legacy one 3.5 still supports for back-compat.

## Props with defaults: `withDefaults` is NOT the recommended form

Reactive props destructure (stable since **3.5**) is the recommended way to declare prop
defaults. `withDefaults()` is the legacy form kept only for back-compat.

```ts
// ✅ 3.5 recommended — reactive props destructure
const { itemId, role = undefined, display = 'icon' } = defineProps<{
  itemId: string
  role?: string
  display?: 'icon' | 'full'
}>()

// ❌ legacy — withDefaults wrapper
const props = withDefaults(defineProps<{...}>(), { display: 'icon', role: undefined })
```

Why the destructure wins:
- Defaults sit inline on the declaration: one statement, no second wrapper call.
- Access is `display` not `props.display`; the compiler keeps it reactive.

Note: `vue/require-default-prop` still requires a default on every optional prop, so an
optional prop with no meaningful default keeps an inline `= undefined` (e.g. `role = undefined`).
That's a one-token inline default, not the whole `withDefaults` wrapper: the win is dropping the
wrapper and the `props.` prefix, not eliminating defaults.

**Reactivity caveat (flag this bug):** a destructured prop passed into `watch`/`computed`/a
`@vueuse` composable must be wrapped in a getter (`watch(() => display, ...)`), never
`watch(display, ...)`. Passing the bare variable snapshots it and loses reactivity.

**Severity:** using `withDefaults` in new/changed code → **Nit** (recommend the destructure).
Destructured-prop-not-passed-as-getter → **Change Requested** (reactivity bug).

## v-model: `defineModel()`

`defineModel()` (stable 3.4) over a hand-written `modelValue` prop + `emit('update:modelValue')`.
Multi-model: `defineModel('open')`. Flag new manual v-model plumbing → **Nit**.

## Template refs: `useTemplateRef('name')`

`useTemplateRef('name')` (3.5) over the old matching-name `ref(null)` + same-name template ref.
→ **Nit**.

## SSR-safe ids: `useId()`

`useId()` (3.5) over hand-rolled counters / `Math.random()` id strings for a11y
`id`/`for`/`aria-*` wiring. → **Nit**.

## Other 3.5 niceties

- `defineSlots<...>()` to type slots.
- `watch(src, cb, { once: true })` over manual unwatch-after-first-run.
- `onWatcherCleanup()` (3.5) for side-effect cleanup inside a watcher.
- `useTemplateRef` + `useId` compose well in form components.

## Reject: removed / legacy

- Template **filters** (removed in 3.x).
- `.sync` modifier (removed: use `v-model:foo`).
- Options API in a **new** component: the standard is `<script setup>`.
- **Vapor mode**: 3.6, still pre-release (`3.6.0-rc.11` on the `rc` tag; npm `latest` is
  3.5.44). Not on 3.5, not for prod. Do not recommend.

## Not yet: Vue 3.6

3.6 is in RC. Nothing from it may appear as a review finding until `latest` moves and the project
bumps. Checklist for the bump: Vapor mode is opt-in per component (`<script setup vapor>`) and
changes nothing existing; re-check the alien-signals reactivity rewrite against any code that
leans on watcher flush ordering.

## Not your lane

Reactivity *correctness* (is this `computed`/`watch` right?) → `persona-vue-reactivity`.
You only flag "a newer API exists".

# persona-best-practice: reka-ui 2.10 rules

**reka-ui 2.10** (the opt-ins below are Future at most)
- Reka's `useLocale()` and `ConfigProvider`'s `locale` prop both default to `'en'`, and an app root passing an undefined `locale` still gets that default. So `useLocale().value || fallback` or `injectConfigProviderContext(...).locale.value || fallback` never reaches the fallback. Change Requested when the fallback is the intended default.
- `Select` `nullableValue` over a sentinel string (`''`, `'none'`, `'__null__'`) mapped back to `null` around a `SelectRoot` `v-model`. Future.
- `ConfigProvider` `teleportTo` over the same `to=` target repeated on every `*Portal` in a changed app shell. Future.
- `Dialog` `unmountOnHide: false` over a `forceMount` + `v-show` workaround to keep closed-dialog state alive. Future.
- reka-ui **2.11** adds `Field`/`Form` primitives, a toast manager, `Combobox` `unmountOnHide`, `TagGroup`, and `loop` on Listbox/Select/Tree. Bump checklist only. Never raise a finding from them unless the project's lockfile already has that version.

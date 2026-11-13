# persona-code-quality diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-D3: `||` defaults on numbers, `v-if="num"`, or `filter(Boolean)` on a numeric array, so a real 0 is dropped → Use `??`, `!= null`, or `Number.isFinite(x)` [default: change-requested] (rule 10)
- FM-J7: Millisecond arithmetic for days such as `+ 86400000`, or `setHours` across a DST change → Calendar arithmetic: `CalendarDate.add({ days: 1 })` or `addDays` [default: change-requested]
- FM-N7: `addEventListener` in `onMounted` or a `watch` with no removal in `onBeforeUnmount`/`onScopeDispose`; uncleared `setInterval` → Use `useEventListener`, or remove on scope dispose [default: nit] (rule 9)

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-B2: `|| '-'` on a numeric field, `v-if="x.price"`, `v-show="total"`, `if (!price)` or `filter(Boolean)` where 0 is a real value → Use `??`, `x != null` or `Number.isFinite` [default: nit] (rule 10)
- DS-J5: New inline formatting of speed, money, or another unit in a template or computed where a shared `format*` helper already exists → Reuse the shared formatter [default: nit] (rule 11)

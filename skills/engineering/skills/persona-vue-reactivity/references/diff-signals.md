# persona-vue-reactivity diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-K1: `:key="index"`, `:key="JSON.stringify(item)"`, `:key="Math.random()"`, or `v-if` around the focused element → Stable IDs as keys; restore focus after DOM changes [default: nit] (rule 7)

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-N9: `:key="index"` on rows that carry a row menu, or an `openMenuIndex` ref tracking the open menu by position → Key rows by ID; close the menu before deleting [default: nit] (rule 7)

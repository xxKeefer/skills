# persona-i18n diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-text-input catalogue](../../persona-text-input/references/catalogue.md)

- IN-G3: `t()` with a template-literal or concatenated key, `v-html` with `t()`, or `escapeParameter` unset where `v-html` is used → Pass user text as a named parameter; use `<i18n-t>` slots [default: change-requested] (rule 4)

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-C1: `'s'` concatenation, `n > 1 ?`, `n === 1 ?` around `t()`, or `(s)` in a count string → vue-i18n plural message called as `t(key, n)` [default: nit]
- DS-C2: New locale added without `pluralRules`, or plural rules not built on `Intl.PluralRules` → `pluralRules` per locale via `new Intl.PluralRules(locale).select(n)` [default: nit]
- DS-C3: Plural message key called as `t(key, { … })` or `t(key)` with no numeric argument → Call `t(key, n)` or `t(key, { n }, n)` [default: nit]
- DS-C4: `t('key', { count: n })` or `t('key', n)` printing `{count}`/`{n}` for a count that can reach 1000, with no `n(...)` on the named value → Pass `{ count: n(value) }`; keep the raw number for plurals [default: nit]
- DS-G12: New `t('…')` key added to `en.json` only, with no `fallbackLocale` set → Configure `fallbackLocale` and a key-parity check [default: nit]
- DS-G13: `+` or a template literal joining `t()` results with names or punctuation → One message with placeholders, or `<i18n-t>` [default: nit] (rule 9)
- DS-M3: New i18n key whose label renames an existing concept, such as "Contract term" beside "Minimum term" or "Account ID" beside "Customer ID" → Reuse the existing label key for the same concept [default: nit]

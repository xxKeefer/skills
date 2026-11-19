# persona-text-input diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. A line marked `(rule N)` adds a case to that rule, and the numbered rules hold the other cases. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-text-input catalogue](catalogue.md)

- IN-A3: `@input` assigning `$event.target.value`, or `watch(search)` feeding a query key with no debounce or composition guard; `ComboboxInput` driving a remote query → Native `v-model`, or emit on `compositionend`; debounce the key [default: nit] (rule 9)
- IN-A4: Submit handler bound to `mousedown` or `pointerdown` that reads `form.value.x` synchronously → Submit on `click` or `submit`, not `mousedown` [default: change-requested] (rule 9)
- IN-A5: `@input` that sets `el.value = format(el.value)` or reassigns the model to a transformed string on every keystroke → Skip formatting while composing; format on `blur` or `compositionend` [default: change-requested] (rule 9)
- IN-B4: `split(' ')`, `replace(' ', ...)`, or a regex or allowlist with a literal space instead of `\s` on user text → Normalise all Unicode spaces; use `replaceAll` for string patterns [default: nit] (rule 1)
- IN-B6: A single-line value feeding CSV export, an HTTP header, a filename or Terraform output with no CR/LF handling → Replace or reject line breaks on paste [default: nit] (rule 5)
- IN-C4: `name[0]`, `charAt(0)` or `split('')` on a display name for initials, avatars or group headers → Take the first grapheme with `Intl.Segmenter` or `Array.from` [default: nit] (rule 6)
- IN-C7: An identifier, key, email, URL or tag field with no character allowlist, so zero-width characters (U+200B, U+FEFF) get through → Strip default-ignorable code points from identifier fields [default: nit] (rule 4)
- IN-C8: A uniqueness check, or other users' names or emails shown in an admin or approval flow, with no mixed-script handling → Confusable skeleton check on the server; show punycode for IDNs [default: nit]
- IN-D4: `@paste.prevent` or `onpaste="return false"` on a password or confirmation field → Remove the paste block [default: nit]
- IN-D5: `contenteditable` or a WYSIWYG editor with default paste handling → Insert `text/plain` on paste, or sanitise on save [default: nit]
- IN-D6: `maxlength` on a field holding a key, token, ID or URL → Drop `maxlength`; validate length with a visible error [default: change-requested] (rule 10)
- IN-D7: An array of single-character inputs with `maxlength=1` and no paste handler, or no `autocomplete="one-time-code"` → Spread pasted digits across boxes; add `one-time-code` [default: nit]
- IN-F3: `type="email"` beside a separate schema that disagrees, or a `novalidate` form relying on the native check → One source of truth for email validity [default: nit]
- IN-F5: `new RegExp(userInput)`, manual `escapeHtml` before `{{ }}`, or `encodeURIComponent` applied twice → Escape for regex or use `includes`; let Vue escape once [default: change-requested] (rule 7)
- IN-F7: A required postcode or state in an address schema with no dependency on country → Drive address rules from the selected country [default: change-requested]
- IN-I1: A new form with no `autocomplete`, a password field with no `current-password` or `new-password`, or `autocomplete="off"` on login → Set the correct `autocomplete` token per field [default: nit]
- IN-I2: An input listening to `keyup` instead of `input`, or a submit button disabled on an empty model at load → Listen to `input`; don't disable submit on empty model alone [default: nit]
- IN-I4: A numeric `type="text"` field with no `inputmode`, or `inputmode="numeric"` on a field that needs `.` or `-` → `inputmode="decimal"` for decimals, `numeric` for integers [default: nit] (rule 5)
- IN-I5: `v-if`/`v-else` swapping two inputs to show or hide a password → Bind `:type` on one input; toggle is `type="button"` [default: nit]
- IN-I6: Bare text beside conditional siblings (`<template v-if>text</template>`), or IDs, keys and code shown with no `translate="no"` → Wrap conditional text in `<span>`; add `translate="no"` [default: change-requested]
- IN-J1: `useDebounceFn` around validation, with a submit handler that doesn't await a full validation pass → Validate synchronously on submit regardless of debounce [default: nit]
- IN-J3: A computed setter or `@update:model-value` that transforms the value (`toUpperCase()`, strip spaces) on each keystroke → Transform on blur or submit; restore `selectionStart` [default: nit] (rule 10)
- IN-J7: Filter updates bound to `@keyup`, or a clear button that resets display state but not the model → Bind to `input`; clear the model, not just the text [default: nit]
- IN-J10: A validator regex with nested quantifiers (`(x+)*`, `(x|xy)+`) and no length check before matching → Bound the length first; rewrite the regex [default: change-requested] (rule 7)
- IN-J14: `isDirty` computed by `JSON.stringify` comparison after input transforms that aren't applied to the initial value → Normalise the initial value the same way; make transforms idempotent [default: change-requested]
- IN-K1: An IPv4 regex with `\d{1,3}` and no leading-zero check, `parseInt(octet)` with no radix check, or IPs compared as strings → Reject leading zeros or use a strict parser; compare canonical forms [default: change-requested] (rule 13)
- IN-K3: `===` or `includes` on IPv6 strings, or `toLowerCase()` as the only normalisation → Canonicalise to RFC 5952 before comparing and displaying [default: change-requested] (rule 13)
- IN-K7: `:href="profile.website"` with no normalisation, or a URL schema accepting bare hostnames with nothing adding `https://` → Normalise with `new URL()` on save; store the absolute URL [default: change-requested] (rule 15)

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-H7: Template-literal URLs, `encodeURIComponent` inside `router.push({ query })`, `decodeURIComponent(route.query.q)`, or hand-parsed `window.location.search` → Pass raw values in `query`; let the router encode [default: change-requested] (rule 7)
- NV-I5: Search value written to `route.query` or a query key with no `.trim()` → Trim before keying and writing the URL; empty means no search [default: nit]

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-A8: Hand-rolled `truncate(str, n)` helper appending `...` unconditionally, or on `>=` instead of `>` → One shared helper: `str.length > n`, append `…` (U+2026) [default: nit]
- DS-G2: `name.split(' ').map(p => p[0])` or `charAt(0)` building avatar initials, with no empty-part filter → Trim, filter empties, first grapheme via `Intl.Segmenter`, icon fallback [default: change-requested]

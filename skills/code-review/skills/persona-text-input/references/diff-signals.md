# persona-text-input diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-text-input catalogue](catalogue.md)

- IN-A3: `@input` assigning `$event.target.value`, or `watch(search)` feeding a query key with no debounce or composition guard; `ComboboxInput` driving a remote query → Native `v-model`, or emit on `compositionend`; debounce the key [default: nit] (rule 9)
- IN-A4: Submit handler bound to `mousedown` or `pointerdown` that reads `form.value.x` synchronously → Submit on `click` or `submit`, not `mousedown` [default: change-requested] (rule 9)
- IN-A5: `@input` that sets `el.value = format(el.value)` or reassigns the model to a transformed string on every keystroke → Skip formatting while composing; format on `blur` or `compositionend` [default: change-requested] (rule 9)
- IN-B1: `z.string().min(1)` with no `.trim()`, `required: true`, `v-if="name"` or `:disabled="!name"` on a name, label or description → Use `z.string().trim().min(1)`; check `value.trim()` [default: change-requested] (rule 1)
- IN-B2: `v-model` without `.trim` on identifiers, emails, keys, IDs or search boxes; `a === b` on raw user strings → Trim in the schema, the same way on save and compare [default: change-requested] (rule 1)
- IN-B3: `v-model.trim` or schema `.trim()` on a `type="password"`, pre-shared key, BGP MD5 password or token field → Never trim secrets; warn about edge whitespace instead [default: change-requested] (rule 2)
- IN-B4: `split(' ')`, `replace(' ', ...)`, or a regex or allowlist with a literal space instead of `\s` on user text → Normalise all Unicode spaces; use `replaceAll` for string patterns [default: nit] (rule 1)
- IN-B6: A single-line value feeding CSV export, an HTTP header, a filename or Terraform output with no CR/LF handling → Replace or reject line breaks on paste [default: nit] (rule 5)
- IN-C1: A character counter on `.length`, or `maxlength` copied from a backend limit with no agreed unit (bytes, code points, graphemes) → Agree the unit; count graphemes with `Intl.Segmenter` [default: nit] (rule 6)
- IN-C4: `name[0]`, `charAt(0)` or `split('')` on a display name for initials, avatars or group headers → Take the first grapheme with `Intl.Segmenter` or `Array.from` [default: nit] (rule 6)
- IN-C5: `includes`, `startsWith`, `===` or `localeCompare` equality on user strings, or a uniqueness check, with no `normalize('NFC')` → Normalise to NFC on input and on both sides [default: change-requested] (rule 4)
- IN-C6: `a.toLowerCase() === b.toLowerCase()` or `.toLowerCase().includes(...)` in a filter or match → `Intl.Collator` or `localeCompare` with `sensitivity: 'base'` [default: nit] (rule 4)
- IN-C7: An identifier, key, email, URL or tag field with no character allowlist, so zero-width characters (U+200B, U+FEFF) get through → Strip default-ignorable code points from identifier fields [default: nit] (rule 4)
- IN-C8: A uniqueness check, or other users' names or emails shown in an admin or approval flow, with no mixed-script handling → Confusable skeleton check on the server; show punycode for IDNs [default: nit]
- IN-C9: User text interpolated into a sentence (`` `Deleted ${name}` ``) or table cell with no `<bdi>` or `dir="auto"` → Wrap user text in `<bdi>` or `dir="auto"` [default: nit] (rule 8)
- IN-C10: A table cell or label showing user content with no `dir="auto"`, often next to numbers, brackets or an ellipsis → Add `dir="auto"` on user-content cells [default: nit] (rule 8)
- IN-C13: A validation regex with no `u` flag, or `[^\x00-\x7F]` style rejection of non-ASCII names → Use `/.../u` with `\p{L}\p{M}\p{N}` [default: change-requested] (rule 3)
- IN-D1: A JSON, regex, CIDR, key or tag field with no `autocorrect="off"` and `spellcheck="false"`, or search that doesn't fold curly quotes → Turn off autocorrect; normalise smart quotes and dashes [default: nit] (rule 5)
- IN-D3: `@keydown` or `@keypress` filter testing `e.key` and calling `preventDefault()`, or `e.keyCode` ranges → Filter in `beforeinput` or sanitise in `input` [default: nit] (rule 10)
- IN-D4: `@paste.prevent` or `onpaste="return false"` on a password or confirmation field → Remove the paste block [default: nit]
- IN-D5: `contenteditable` or a WYSIWYG editor with default paste handling → Insert `text/plain` on paste, or sanitise on save [default: nit]
- IN-D6: `maxlength` on a field holding a key, token, ID or URL → Drop `maxlength`; validate length with a visible error [default: change-requested] (rule 10)
- IN-D7: An array of single-character inputs with `maxlength=1` and no paste handler, or no `autocomplete="one-time-code"` → Spread pasted digits across boxes; add `one-time-code` [default: nit]
- IN-F1: `emails.includes(input)`, `===` on emails, or `new Set(emails)` for de-duplication → Compare the trimmed, lowercased form; store as entered [default: nit] (rule 4)
- IN-F2: A new home-made email regex in the diff → Use the browser's `type=email` check or a maintained library [default: change-requested] (rule 3)
- IN-F3: `type="email"` beside a separate schema that disagrees, or a `novalidate` form relying on the native check → One source of truth for email validity [default: nit]
- IN-F4: A regex on a name field (`[A-Za-z]`, minimum length 2), or a required `lastName` → Accept any non-blank Unicode text; make family name optional [default: change-requested] (rule 3)
- IN-F5: `new RegExp(userInput)`, manual `escapeHtml` before `{{ }}`, or `encodeURIComponent` applied twice → Escape for regex or use `includes`; let Vue escape once [default: change-requested] (rule 7)
- IN-F6: `type="number"` or `\d{10}` on a phone field → `type="tel"`, keep a string, use libphonenumber-js [default: change-requested] (rule 3)
- IN-F7: A required postcode or state in an address schema with no dependency on country → Drive address rules from the selected country [default: change-requested]
- IN-G4: `` router.push(`/x/${name}`) `` or `` href=`...?q=${q}` `` built by string concatenation → `router.push({ name, params, query })` or `URLSearchParams` [default: nit] (rule 7)
- IN-H2: A hand-rolled CSV join (`r.join(',')`) with no RFC 4180 quoting of commas, quotes and newlines → Use a CSV library; quote every field [default: change-requested] (rule 11)
- IN-H3: `new Blob([csv])` for an Excel-targeted CSV with no `\uFEFF` prefix → Prepend the UTF-8 BOM for Excel exports [default: nit] (rule 11)
- IN-H4: `` link.download = `${name}.csv` `` or a `Content-Disposition` filename taken straight from user text → Strip reserved and control characters; cap the length [default: nit] (rule 12)
- IN-I1: A new form with no `autocomplete`, a password field with no `current-password` or `new-password`, or `autocomplete="off"` on login → Set the correct `autocomplete` token per field [default: nit]
- IN-I2: An input listening to `keyup` instead of `input`, or a submit button disabled on an empty model at load → Listen to `input`; don't disable submit on empty model alone [default: nit]
- IN-I3: A code or ID field with no `autocapitalize="off" autocorrect="off" spellcheck="false"`, or `type="text"` for an email → Add those attributes; use `type="email"` or `type="url"` [default: nit] (rule 5)
- IN-I4: A numeric `type="text"` field with no `inputmode`, or `inputmode="numeric"` on a field that needs `.` or `-` → `inputmode="decimal"` for decimals, `numeric` for integers [default: nit] (rule 5)
- IN-I5: `v-if`/`v-else` swapping two inputs to show or hide a password → Bind `:type` on one input; toggle is `type="button"` [default: nit]
- IN-I6: Bare text beside conditional siblings (`<template v-if>text</template>`), or IDs, keys and code shown with no `translate="no"` → Wrap conditional text in `<span>`; add `translate="no"` [default: change-requested]
- IN-J1: `useDebounceFn` around validation, with a submit handler that doesn't await a full validation pass → Validate synchronously on submit regardless of debounce [default: nit]
- IN-J3: A computed setter or `@update:model-value` that transforms the value (`toUpperCase()`, strip spaces) on each keystroke → Transform on blur or submit; restore `selectionStart` [default: nit] (rule 10)
- IN-J7: Filter updates bound to `@keyup`, or a clear button that resets display state but not the model → Bind to `input`; clear the model, not just the text [default: nit]
- IN-J10: A validator regex with nested quantifiers (`(x+)*`, `(x|xy)+`) and no length check before matching → Bound the length first; rewrite the regex [default: change-requested] (rule 7)
- IN-J14: `isDirty` computed by `JSON.stringify` comparison after input transforms that aren't applied to the initial value → Normalise the initial value the same way; make transforms idempotent [default: change-requested]
- IN-K1: An IPv4 regex with `\d{1,3}` and no leading-zero check, `parseInt(octet)` with no radix check, or IPs compared as strings → Reject leading zeros or use a strict parser; compare canonical forms [default: change-requested] (rule 13)
- IN-K2: A zod `.regex()` for CIDR with no refinement that host bits are zero → Refine with `(ip & mask) === ip`; suggest the network address [default: change-requested] (rule 13)
- IN-K3: `===` or `includes` on IPv6 strings, or `toLowerCase()` as the only normalisation → Canonicalise to RFC 5952 before comparing and displaying [default: change-requested] (rule 13)
- IN-K5: `z.number()`, `z.coerce.number()`, `type="number"` or `parseFloat` on an ASN → Parse asplain and asdot as text; bound 1 to 4294967295 [default: change-requested] (rule 14)
- IN-K6: A MAC regex allowing only `:` as separator, or a CIDR schema reused on a field labelled "IP address" → Accept common MAC notations; use a host IP schema [default: change-requested] (rule 14)
- IN-K7: `:href="profile.website"` with no normalisation, or a URL schema accepting bare hostnames with nothing adding `https://` → Normalise with `new URL()` on save; store the absolute URL [default: change-requested] (rule 15)

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-D6: `` router.push(`/x/${name}`) `` with a user-entered name or slug built into a path by concatenation → Named route with params, or `encodeURIComponent` [default: nit] (rule 7)
- NV-H7: Template-literal URLs, `encodeURIComponent` inside `router.push({ query })`, `decodeURIComponent(route.query.q)`, or hand-parsed `window.location.search` → Pass raw values in `query`; let the router encode [default: change-requested] (rule 7)
- NV-I5: Search value written to `route.query` or a query key with no `.trim()` → Trim before keying and writing the URL; empty means no search [default: nit]
- NV-I7: `item.name.includes(term)` in a client-side filter with no lowercasing of either side → `toLocaleLowerCase()` both sides, or `Intl.Collator` with base sensitivity [default: nit] (rule 4)
- NV-I8: `toLowerCase().includes(term)` over place or company names with no `normalize('NFD')` or `Intl.Collator` → Strip diacritics on both sides, or collator with `sensitivity: 'base'` [default: nit] (rule 4)
- NV-I9: `new RegExp(term, 'i')` with the user's search term, for filtering or highlighting → Escape the term, or use `includes` [default: change-requested] (rule 7)

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-A7: `.slice(0, n)`, `.substring(`, `.substr(` or `.length >` on user-facing names or in a `maxlength` counter → Count and cut graphemes with `Intl.Segmenter`, or truncate in CSS [default: nit] (rule 6)
- DS-A8: Hand-rolled `truncate(str, n)` helper appending `...` unconditionally, or on `>=` instead of `>` → One shared helper: `str.length > n`, append `…` (U+2026) [default: nit]
- DS-G2: `name.split(' ').map(p => p[0])` or `charAt(0)` building avatar initials, with no empty-part filter → Trim, filter empties, first grapheme via `Intl.Segmenter`, icon fallback [default: change-requested]

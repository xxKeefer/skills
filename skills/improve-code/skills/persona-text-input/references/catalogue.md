# persona-text-input catalogue: text input and character handling

Scope: individual input, keypress, paste and render behaviours in a Vue 3 + TypeScript SPA (Reka UI, vue-router, TanStack Query, and vue-i18n). It does not cover architecture.

Each item has: **User sees**, **Root cause**, **Try**, **Review signal** (what to look for in a Vue diff), **Fix**, **Source**. "(uncertain)" marks claims not verified against a primary source.

## Key sources

- Big List of Naughty Strings (BLNS): https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt
- Falsehoods about names: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
- Falsehoods about phone numbers (libphonenumber): https://github.com/google/libphonenumber/blob/master/FALSEHOODS.md
- Awesome Falsehood index (emails, addresses): https://github.com/kdeldycke/awesome-falsehood
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP CSV Injection: https://owasp.org/www-community/attacks/CSV_Injection
- MDN `isComposing`: https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing
- WebKit bug 165004 (Safari IME Enter `isComposing` false): https://bugs.webkit.org/show_bug.cgi?id=165004
- Vue forms guide (IME, `.trim`, `.number`, `.lazy`): https://vuejs.org/guide/essentials/forms.html
- MDN `maxlength` (UTF-16 code units): https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/maxlength
- MDN `type=email`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/email
- MDN `type=number`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/number
- GOV.UK on number inputs: https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/
- MDN `autocomplete`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete
- Trojan Source (CVE-2021-42574): https://nvd.nist.gov/vuln/detail/CVE-2021-42574 and https://trojansource.codes/
- Google Translate DOM crash (React issue, same mechanism in Vue): https://github.com/facebook/react/issues/11538

## A. IME and composition

### IN-A1. Enter during IME composition submits the form or fires the action

- **User sees**: A Japanese, Chinese, or Korean user presses Enter to confirm a kana→kanji conversion, and the search fires, the chip is added, or the form submits with half-composed text.
- **Root cause**: The `@keydown.enter` or `@keyup.enter` handler doesn't check composition state. Vue's `.enter` modifier does not filter composition.
- **Try**: macOS Japanese Romaji input, type `toukyou`, press Enter to convert. Also try Chrome with Microsoft IME on Windows, and Safari.
- **Review signal**: `@keydown.enter`, `@keyup.enter`, `@keypress.enter`, or `if (e.key === 'Enter')` on a text input, textarea, tag input, chat box, inline edit, or combobox, with no `isComposing` guard.
- **Fix**: `if (e.isComposing || e.keyCode === 229) return`. Prefer `keydown` over `keyup` (the `keyup` for the confirming Enter arrives after `compositionend`, so `isComposing` is false). Put the check in one shared helper or directive.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing
- **In the design system**: A design-system input may declare its own `keydown` emit: it can fire late and pass the field value, not the `KeyboardEvent`. `@keydown.enter` on it then never fires on Enter. Check the component's emits. Use `@keyup.enter` (it reaches the native input) or a real form submit.

### IN-A2. Safari reports `isComposing === false` on the confirming Enter

- **User sees**: Same as IN-A1 but only in Safari, after a fix that checks `isComposing` alone.
- **Root cause**: WebKit fires `compositionend` before the keydown for the committing key, so that keydown has `isComposing === false`.
- **Try**: Safari, Japanese IME, convert and press Enter.
- **Review signal**: A guard of `e.isComposing` with no `keyCode === 229` fallback, or a guard built on a `composing` ref that is cleared in `compositionend`.
- **Fix**: Check both `e.isComposing || e.keyCode === 229`. If you track it in a ref, clear it on the next tick (`setTimeout(…, 0)`) after `compositionend` so the immediately following keydown still sees it. A newer WebKit fix may have landed (uncertain, verify against your supported Safari versions).
- **Source**: https://bugs.webkit.org/show_bug.cgi?id=165004

### IN-A3. Search-as-you-type fires on every composition step

- **User sees**: Typing Chinese pinyin fires queries for `n`, `ni`, `nih`, `niha` and shows irrelevant results or flashes "no results"; the TanStack Query cache fills with useless keys.
- **Root cause**: Vue's native `v-model` waits for `compositionend`, but a custom component bound with `:model-value` + `@update:model-value` or `@input="q = $event.target.value"` does not. Many Reka UI wrappers forward raw `input` events.
- **Try**: Pinyin or Japanese IME in the table filter, combobox, or global search.
- **Review signal**: `@input` handlers assigning `$event.target.value` directly; `watch(search, …)` feeding a query key without debounce or composition guard; `ComboboxInput` / `ListboxFilter` usage driving a remote query.
- **Fix**: Use native `v-model` on the native element, or guard with `compositionstart`/`compositionend` and emit on `compositionend`. Debounce the query key.
- **Source**: https://vuejs.org/guide/essentials/forms.html (IME note); https://dev.classmethod.jp/en/articles/react-ime-composition-pitfalls/

### IN-A4. v-model not updated before submit when IME is still open

- **User sees**: User types in Korean and clicks Save without confirming; the last syllable is missing from what was saved.
- **Root cause**: Vue's `v-model` does not update during composition. Clicking a button blurs and commits the composition, but the model update can arrive after the click handler reads it (uncertain on ordering across browsers).
- **Try**: Korean 2-set IME, type `한글` and click Save immediately without pressing space.
- **Review signal**: Submit handlers reading `form.value.x` synchronously on `mousedown` or `pointerdown` instead of `click`/`submit`.
- **Fix**: Submit on `click`/`submit`, not `mousedown`. Optionally `await nextTick()` before reading.
- **Source**: https://vuejs.org/guide/essentials/forms.html

### IN-A5. Input masks and formatters break composition

- **User sees**: Caret jumps, characters duplicate, or the field becomes untypeable with an IME or Android Gboard.
- **Root cause**: A formatter rewrites `el.value` on every `input` event, including mid-composition. On Android, Gboard emits composition events for plain Latin typing too.
- **Try**: Android Chrome with Gboard on any masked field (phone, VLAN, ASN, card); Japanese IME on a "formatted name" field.
- **Review signal**: `@input` that sets `el.value = format(el.value)` or reassigns the model to a transformed string on every keystroke.
- **Fix**: Skip formatting while composing; format on `blur` or `compositionend`; preserve the caret position with `selectionStart`/`selectionEnd`.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionend_event

### IN-A6. Keyboard shortcuts hijack IME keys

- **User sees**: Pressing Escape to cancel an IME candidate list closes the dialog and discards the form; arrow keys move list selection instead of IME candidates.
- **Root cause**: Global or dialog-level keydown handlers (Reka `DialogContent` `@escape-key-down`, custom hotkeys) don't check composition.
- **Try**: Japanese IME in a modal, open candidates, press Escape.
- **Review signal**: `@escape-key-down`, `onKeyStroke`, `useMagicKeys`, global `keydown` listeners.
- **Fix**: Bail if `e.isComposing || e.keyCode === 229`.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing

---

## B. Whitespace

### IN-B1. Whitespace-only value passes "required"

- **User sees**: The user can save a service called `   `; it renders as a blank row with an empty link.
- **Root cause**: `required`, `!!value`, or `value.length > 0` checks with no trim. Zod `z.string().min(1)` does not trim.
- **Try**: T1, plus ` `, `​`, `\t`.
- **Review signal**: `min(1)` without `.trim()`, `v-if="name"`, `:disabled="!name"`, `required: true` rules.
- **Fix**: `z.string().trim().min(1)`; base disabled-state checks on `value.trim()`. Decide whether `​`-only counts as blank (it isn't matched by `\s`).
- **Source**: OWASP Input Validation Cheat Sheet.
- **In the project**: The model is `z.string().trim().min(1).max(MAX_NAME_LENGTH, ...)`. Zod apps use `toTypedSchema`; yup apps use `.trim()` too.
- **Sources:** [MDN: HTML attribute: required](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/required), [Zod: string transforms (`.trim()`)](https://zod.dev/api)

### IN-B2. Leading/trailing spaces saved and later break matching

- **User sees**: "Name already exists" not shown for `Acme ` versus `Acme`; login fails because autofill added a trailing space; search for a pasted ID returns nothing.
- **Root cause**: No trim on save, or a trim on save but not on compare, or the reverse.
- **Try**: T2; paste an ID copied from an email (often has a trailing space or newline).
- **Review signal**: `v-model` without `.trim` on identifiers, emails, keys, IDs, search boxes; equality checks `a === b` on user strings.
- **Fix**: Trim in the schema, the same way everywhere. Do not trim passwords or free-text descriptions where whitespace is content.
- **Source**: https://vuejs.org/guide/essentials/forms.html (`.trim`)

### IN-B3. `.trim` modifier on a password or secret

- **User sees**: Password with a trailing space set on another system can't log in here, or a pasted API secret gets altered.
- **Root cause**: `v-model.trim` or schema `.trim()` on password, shared key, BGP MD5 password, or token fields.
- **Try**: Password `abc ` (trailing space).
- **Review signal**: `.trim` on any `type="password"` or secret field.
- **Fix**: Never trim secrets. Warn instead if the value has leading or trailing whitespace.
- **Source**: NIST SP 800-63B allows all printing characters and spaces in memorised secrets: https://pages.nist.gov/800-63-3/sp800-63b.html

### IN-B4. Non-breaking and other Unicode spaces slip past `\s`-free logic

- **User sees**: A value pasted from a PDF, Word, or Slack looks fine but validation says "invalid characters", or two names that look identical are treated as distinct.
- **Root cause**: NBSP (U+00A0), narrow NBSP (U+202F, used by `Intl.NumberFormat` in fr-FR and by macOS times), figure space (U+2007), ideographic space (U+3000). `str.trim()` and `\s` do cover U+00A0/U+202F/U+3000 in JS, but code using `' '` literal, `split(' ')`, or `[a-zA-Z0-9 ]` allowlists does not. Zero-width characters are a separate case: `\s` and `trim()` cover U+FEFF in JS, but `\s` does not match U+200B.
- **Try**: T3, T4, `　`.
- **Review signal**: `split(' ')`, `replace(' ', …)` (which also replaces only the first match), regex with literal space instead of `\s`, allowlist regexes.
- **Fix**: Normalise whitespace: `s.replace(/[\s​-‍⁠﻿]+/g, ' ').trim()` for single-line identifiers. Use `replaceAll`, not `replace`, for string patterns.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Character_class_escape (definition of `\s`)

### IN-B5. Internal whitespace collapsed in display, preserved in data

See DS-G6 (persona-value-display).

### IN-B6. Newlines in single-line fields

- **User sees**: Pasting a multi-line value into an `<input>` silently joins lines (browser strips `\r\n`), producing `line1line2`; or a programmatic set keeps the `\n`, which later breaks a CSV, a header, or a log line.
- **Root cause**: Browsers strip line breaks from `<input type=text>` values; values set through the API, clipboard autofill libraries, or imported data keep them.
- **Try**: Paste T5; also set it through the API and view it in the UI.
- **Review signal**: Fields that feed into CSV export, HTTP headers, filenames, or Terraform output without newline handling.
- **Fix**: On paste into identifier fields, replace line breaks with a space (or reject). The server must still reject CR/LF where it matters (header injection).
- **Source**: https://html.spec.whatwg.org/multipage/input.html#text-(type=text)-state-and-search-state-(type=search) (value sanitisation strips line breaks)

### IN-B7. Copy-to-clipboard copies extra whitespace or hidden text

See DS-F2 (persona-value-display), DS-F5 (persona-value-display).

---

## C. Length and Unicode units

### IN-C1. `maxlength` counts UTF-16 code units, not characters

- **User sees**: Counter says "40/50" but the browser stops accepting input; an emoji-heavy description is rejected at 25 visible characters.
- **Root cause**: `maxlength` and `String.length` count UTF-16 code units. `👍🏽` is 4 units, `👨‍👩‍👧‍👦` is 11.
- **Try**: T7 repeated.
- **Review signal**: Character counters using `.length`; `maxlength` copied from a backend limit without knowing whether the backend counts bytes, code points or graphemes.
- **Fix**: Agree the unit with the backend. Count graphemes for display with `Intl.Segmenter(…, { granularity: 'grapheme' })`; count bytes (`new TextEncoder().encode(s).length`) if the DB column is bytes.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/maxlength

### IN-C2. Frontend limit and backend limit disagree

See FM-E1 (persona-form-behaviour).

### IN-C3. Truncation splits a surrogate pair or grapheme

See DS-A7 (persona-value-display).

### IN-C4. Reversing, splitting, or indexing strings by code unit

- **User sees**: Initials avatar shows `�` for a name starting with an emoji or an astral CJK character (`𠀀`); "first letter" grouping is wrong.
- **Root cause**: `name[0]`, `name.charAt(0)`, `split('')`.
- **Try**: Name `😀 Team`, `𠀀abc`, `Émile` in NFD.
- **Review signal**: `[0]`, `charAt`, `split('')` on display names (avatars, initials, alphabetical group headers).
- **Fix**: `[...segmenter.segment(s)][0]?.segment`, or `Array.from(s)[0]` as a code-point-safe minimum.
- **Sources:** [MDN: String (UTF-16 characters, Unicode code points, and grapheme clusters)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String#utf-16_characters_unicode_code_points_and_grapheme_clusters)

### IN-C5. Unicode normalisation (NFC versus NFD) mismatch

- **User sees**: Search for `café` doesn't find `café`; "name already taken" fails to trigger; the same name appears twice. macOS file names and some keyboards emit NFD.
- **Root cause**: Comparing or storing without normalising. `'é' !== 'é'`, and their `.length` differs (1 versus 2).
- **Try**: T8.
- **Review signal**: Client-side filtering (`includes`, `startsWith`, `===`) on user strings; uniqueness checks; `localeCompare` used for equality.
- **Fix**: `s.normalize('NFC')` at the input boundary and on both sides of comparisons. Use NFKC only for identifiers that need compatibility folding (it turns `１２３` into `123` and `ﬁ` into `fi`). Apply the same policy server-side.
- **Source**: OWASP Input Validation Cheat Sheet (normalisation section); https://unicode.org/reports/tr15/

### IN-C6. Case-insensitive comparison done with `toLowerCase`

- **User sees**: Filter for `STRASSE` doesn't match `Straße`; Turkish locale users see `i` versus `İ` mismatches; a value changes length after lowercasing (`"İ".toLowerCase()` is `"i̇"`, length 1 → 2; verified in Node).
- **Root cause**: `toLowerCase()` is not case folding; `toLocaleLowerCase()` with the user's locale behaves differently for Turkish.
- **Try**: T16.
- **Review signal**: `a.toLowerCase() === b.toLowerCase()`, `.toLowerCase().includes(…)` in filters.
- **Fix**: `a.localeCompare(b, undefined, { sensitivity: 'base' }) === 0` (or an `Intl.Collator` with `sensitivity: 'base'`) for search. `sensitivity: 'accent'` does not equate `STRASSE` and `Straße` (returns -1; verified in Node); don't use `toLocaleLowerCase()` for identifiers.
- **Source**: BLNS "Changing length when lowercased" section.
- **Sources:** [MDN: String.prototype.toLocaleLowerCase()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLocaleLowerCase), [MDN: Intl.Collator() sensitivity](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator), [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt)

### IN-C7. Zero-width and invisible characters in identifiers

- **User sees**: Two "identical" names both accepted; a pasted key fails validation with no visible reason; a URL slug contains `%E2%80%8B`.
- **Root cause**: U+200B ZWSP, U+200C/D ZWNJ/ZWJ, U+2060 WJ, U+FEFF BOM, U+00AD soft hyphen copied from web pages, Slack, or a wiki page.
- **Try**: T4.
- **Review signal**: Identifier, key, email, URL, or tag fields with no character allowlist.
- **Fix**: Strip default-ignorable code points from identifier-like fields on input; don't strip ZWJ/ZWNJ from free text (they are meaningful in Persian, Indic scripts and emoji).
- **Source**: BLNS "Trick Unicode" section.
- **Sources:** [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt), [UAX #31: Unicode Identifiers and Syntax](https://www.unicode.org/reports/tr31/), [Unicode FAQ: Display of unsupported characters](https://www.unicode.org/faq/unsup_char.html)

### IN-C8. Homoglyphs and confusables

- **User sees**: Two companies or ports named `Acme` and `Асme` (Cyrillic М) appear identical; phishing-style lookalikes in shared names or emails.
- **Root cause**: No confusable detection; mixed-script strings allowed in identifiers.
- **Try**: `Mеgaport` with Cyrillic `е` (U+0435); `paypal` with `а` (U+0430).
- **Review signal**: Uniqueness checks or display of other users' names or emails in admin or approval flows.
- **Fix**: Mostly a backend fix: a confusable skeleton check (Unicode Technical Standard #39, UTS #39) for identifiers that must be unique. Frontend: render the punycode form for IDN emails/URLs in security-relevant places.
- **Source**: https://www.unicode.org/reports/tr39/

### IN-C9. Bidi override characters flip rendered text

- **User sees**: A file name reads `invoice‮fdp.exe` as `invoiceexe.pdf`; in a table cell, an RTL override in one user's name reverses the rest of the row's text or the trailing columns.
- **Root cause**: U+202A to U+202E and U+2066 to U+2069 are rendered as is, with no isolation of user text.
- **Try**: T9; Arabic or Hebrew names (T10) in tables, breadcrumbs, toasts, and "Delete X?" confirmations.
- **Review signal**: User text interpolated inline into sentences (`Deleted ${name} successfully`) or table cells without `<bdi>` / `dir="auto"`.
- **Fix**: Wrap user-supplied text in `<bdi>` or `<span dir="auto">`; in i18n messages, place the user value in an isolated element. Strip U+202A to U+202E, U+2066 to U+2069 from identifiers.
- **Source**: https://nvd.nist.gov/vuln/detail/CVE-2021-42574; https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi

### IN-C10. RTL text with numbers or punctuation renders in the wrong order

- **User sees**: `Port (2)` with an Arabic name shows the parenthesis on the wrong side; ellipsis appears on the wrong end.
- **Root cause**: Missing bidi isolation; `text-overflow: ellipsis` follows the element's direction.
- **Try**: `مرحبا (2)`, `שלום 10Gbps`.
- **Review signal**: Same as IN-C9.
- **Fix**: `dir="auto"` on cells displaying user content.
- **Sources:** [W3C: Inline markup and bidirectional text in HTML](https://www.w3.org/International/articles/inline-bidi-markup/), [MDN: text-overflow](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-overflow)

### IN-C11. Zalgo / combining-mark stacking breaks layout

- **User sees**: A name overflows its row vertically and covers neighbouring rows or buttons, blocking clicks.
- **Root cause**: Unlimited combining marks; containers with `overflow: visible`.
- **Try**: T17.
- **Review signal**: Fixed-height rows, avatar labels, chips showing user text without `overflow: hidden`.
- **Fix**: `overflow: hidden` / `overflow-wrap: anywhere` on user-text containers; optionally limit consecutive combining marks server-side.
- **Source**: BLNS "Zalgo Text".
- **Sources:** [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt), [UAX #15: Stream-Safe Text Format](https://www.unicode.org/reports/tr15/#Stream_Safe_Text_Format)

### IN-C12. Long unbroken strings overflow

See DS-A1 (persona-value-display).

### IN-C13. Emoji and astral characters rejected by allowlist regex without `u` flag

- **User sees**: A valid name with an emoji or a rare CJK character (`𠀀`) is rejected, or a regex treats it as two "characters", breaking `{1,50}` limits.
- **Root cause**: Regex without the `u` (or `v`) flag operates on code units; `.` doesn't match an astral char as one; `\p{L}` needs `u`.
- **Try**: `𠀀`, `😀`.
- **Review signal**: Validation regexes without `/u`; `[^\x00-\x7F]` style rejections of non-ASCII for names.
- **Fix**: Use `/…/u` and Unicode property escapes (`\p{L}\p{M}\p{N}`). HTML `pattern` attributes already compile with `u` (now `v`), so a regex valid in JS may be a syntax error in `pattern`.
- **Source**: MDN email page notes `pattern` uses the `u` flag: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/email

---

## D. Paste artefacts

### IN-D1. Smart quotes and dashes from macOS / Word / a wiki

- **User sees**: A pasted JSON, command, or key fails validation; a search for `don't` misses `don’t`; a BGP community or prefix list pasted from a doc is rejected because of an en dash `–`.
- **Root cause**: macOS "Smart Quotes and Dashes" setting and Office autocorrect replace `'` `"` `-` with `’` `“”` `–` `—`. iOS does this on typing too.
- **Try**: T6; `10.0.0.0–10.0.0.255`; type `"` on iOS in an input with default settings.
- **Review signal**: Fields that hold code-like values (JSON, regex, CIDR ranges, keys, tags) without `autocorrect="off"` / `spellcheck="false"`; search that doesn't normalise quotes.
- **Fix**: For code-like fields: `autocapitalize="off" autocorrect="off" spellcheck="false"`. Normalise `‘’` → `'`, `“”` → `"`, `–—` → `-` where the field is machine-readable. For search, fold quotes on both sides.
- **Sources:** [Apple: Replace text and punctuation in documents on Mac](https://support.apple.com/en-au/guide/mac-help/mh35735/mac), [MDN: autocorrect global attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/autocorrect)

### IN-D2. Pasting formatted numbers into numeric fields

See FM-D18 (persona-form-behaviour).

### IN-D3. Paste blocked or mangled by a keydown-based filter

- **User sees**: A "digits only" field accepts pasted letters (the filter runs only on keypress), blocks paste entirely, or blocks Cmd+V, Ctrl+A, the arrow keys, or Backspace.
- **Root cause**: The filter tests `e.key` against a regex in `keydown`/`keypress`, so it misses paste, drag and drop, autofill, and IME, and it blocks modifier shortcuts.
- **Try**: Paste `abc123`; drag text in; Cmd+A, Cmd+Z, Tab, arrow keys, Delete on Windows, numpad digits.
- **Review signal**: `@keydown="e => /\d/.test(e.key) || e.preventDefault()"`, `@keypress` filters, `e.keyCode` ranges.
- **Fix**: Filter in `beforeinput` (check `e.data`) or sanitise in `input`; never block keys with `ctrlKey`/`metaKey`; let validation report the problem instead of dropping input with no message.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/API/Element/beforeinput_event

### IN-D4. Paste disabled on confirm-email / password fields

- **User sees**: Can't paste a generated password; password manager fill fails.
- **Root cause**: `@paste.prevent` on password or confirmation fields.
- **Try**: Paste into each password/email confirm field.
- **Review signal**: `@paste.prevent`, `onpaste="return false"`.
- **Fix**: Remove it. NIST 800-63B says verifiers should permit paste in memorised secret fields.
- **Source**: https://pages.nist.gov/800-63-3/sp800-63b.html (section 5.1.1.2)

### IN-D5. Rich paste into contenteditable / rich text

- **User sees**: Pasting from Word brings fonts, `<o:p>` tags, or tracking images into a description; the saved content renders oddly elsewhere.
- **Root cause**: `contenteditable` with default paste handling.
- **Try**: Paste from Word, Google Docs, a web page with images.
- **Review signal**: `contenteditable` in templates; any WYSIWYG editor.
- **Fix**: Intercept `paste`, read `text/plain`, insert as text; or sanitise HTML on save and render.
- **Sources:** [MDN: Element paste event](https://developer.mozilla.org/en-US/docs/Web/API/Element/paste_event), [OWASP: Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

### IN-D6. Pasted value exceeds `maxlength` silently truncated

- **User sees**: Paste a 60-character key into a 50-character field: the browser cuts it with no message, and the save succeeds with the wrong key.
- **Root cause**: Browsers truncate pasted text to `maxlength`.
- **Try**: Paste an over-long value into every field with `maxlength`.
- **Review signal**: `maxlength` on fields holding keys, tokens, IDs, or URLs (where truncation produces a wrong value rather than a short one).
- **Fix**: For machine values, drop `maxlength` and validate length with a visible error.
- **Sources:** [WHATWG HTML: maxlength](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#attr-fe-maxlength), [Adam Silver: Don’t use the maxlength attribute to stop users from exceeding the limit](https://adamsilver.io/blog/dont-use-the-maxlength-attribute-to-stop-users-from-exceeding-the-limit)

### IN-D7. Paste into split OTP / code inputs

- **User sees**: Pasting a 6-digit MFA code into the first box puts all digits in box 1, or only the first digit lands; SMS autofill fails.
- **Root cause**: Per-box `maxlength=1` without a paste handler; missing `autocomplete="one-time-code"`.
- **Try**: Paste `123456`, `123 456`, `123-456`; iOS SMS code suggestion.
- **Review signal**: Arrays of single-char inputs; Reka `PinInput` without a paste test.
- **Fix**: Handle paste on any box (strip non-digits, distribute); `autocomplete="one-time-code" inputmode="numeric"`. Reka UI `PinInput` supports paste (verify for spaces/dashes).
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete

---

## E. Numbers in text inputs

### IN-E1. `type="number"` used for non-numbers

- **User sees**: Leading zeros dropped from an account code; a 16-digit ID becomes `1.2345678901234568e+15` or loses precision; Safari inserts commas; postcode `0800` becomes `800`.
- **Root cause**: `type=number` for IDs, postcodes, VLANs used as codes, card numbers, phone numbers. JS numbers lose precision above 2^53.
- **Try**: `0800`, `12345678901234567890`.
- **Review signal**: `type="number"` or `v-model.number` on anything you'd never do arithmetic on.
- **Fix**: `type="text" inputmode="numeric" pattern="[0-9]*"`; keep as string.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/number; GOV.UK blog above.

### IN-E2. Scroll wheel or arrow keys change a focused number

See FM-D5 (persona-form-behaviour).

### IN-E3. `type=number` accepts `e`, `+`, `-`, `.` and reports `''`

See FM-D1 (persona-form-behaviour).

### IN-E4. Falsy zero

See FM-D3 (persona-form-behaviour) (input side), DS-B2 (persona-value-display) (display side).

### IN-E5. Empty number becomes `0`, `NaN`, `''` or `null` inconsistently

See FM-D2 (persona-form-behaviour).

### IN-E6. Locale decimal separator

See FM-D7 (persona-form-behaviour).

### IN-E7. Full-width and non-Latin digits

See FM-D16 (persona-form-behaviour).

### IN-E8. Floating-point display of user-entered decimals

See DS-D2 (persona-value-display).

---

## F. Email, names, phone, addresses

### IN-F1. Email case sensitivity

- **User sees**: Invite sent to `Jane@Acme.com`; she signs up as `jane@acme.com` and the invite isn't linked; "user already exists" shown or not depending on case.
- **Root cause**: Exact-match comparison. Domain is case-insensitive; the local part is case sensitive under RFC 5321, but almost all providers treat it as case insensitive.
- **Try**: T21 variants.
- **Review signal**: `emails.includes(input)`, `===` on emails, deduplication with `new Set(emails)`.
- **Fix**: Compare the lowercased, trimmed form; store as entered for display. Don't lowercase before sending to auth if the backend expects the original (agree a policy).
- **Source**: RFC 5321 section 2.4: https://datatracker.ietf.org/doc/html/rfc5321#section-2.4

### IN-F2. Over-strict or home-made email regex

- **User sees**: `user+tag@example.com`, `first.o'brien@x.ie`, or `a@sub.example.museum` rejected; IDN addresses rejected.
- **Root cause**: Custom regex with `[a-z]{2,4}` TLD, no `+` or `'`, and so on.
- **Try**: T21; `o'brien@example.ie`; `x@example.technology`.
- **Review signal**: New email regex in the diff.
- **Fix**: Use the same check as the browser (`type=email` regex on MDN) or a maintained library; confirm by sending mail.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/email; https://github.com/kdeldycke/awesome-falsehood#emails

### IN-F3. `type=email` quirks

- **User sees**: Non-ASCII local parts rejected by the browser; in Chrome, IDN domains get converted to punycode in `value`, and Safari rejects Unicode domains outright (whatwg/html#4562); `multiple` allows comma lists that the backend doesn't parse; whitespace trimmed by the browser but not by a paste-handling custom component.
- **Root cause**: Browser-native sanitisation and validation on `type=email`.
- **Try**: `δοκιμή@παράδειγμα.δοκιμή`, `user@bücher.de`, ` user@example.com `.
- **Review signal**: `type="email"` combined with a separate schema that disagrees; `novalidate` forms relying on the native check.
- **Fix**: One source of truth for email validity; server-side verification.
- **Source**: MDN email page (IDN spec issues: whatwg/html#4562).
- **Sources:** [WHATWG HTML: Email state (type=email)](https://html.spec.whatwg.org/multipage/input.html#email-state-(type=email)), [whatwg/html#4562: Validating internationalized mail addresses](https://github.com/whatwg/html/issues/4562)

### IN-F4. Name validators reject real names

- **User sees**: `O'Brien`, `Nguyễn`, `María-José`, single-name users, `Q`, or names with digits rejected; a profanity filter blocks `Dick Van Dyke` or `Scunthorpe`.
- **Root cause**: `[A-Za-z]` allowlists, min length 2, required last name, bad-word filters.
- **Try**: T20; BLNS "Scunthorpe Problem".
- **Review signal**: Regex on name fields; required `lastName`.
- **Fix**: Accept any non-blank Unicode text within a length limit; make family name optional where the backend allows.
- **Source**: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/

### IN-F5. Apostrophe breaks escaping or search

- **User sees**: Company `Rock 'n' Roll Ltd` shows as `Rock &#39;n&#39; Roll` (double-escaped) or the filter crashes.
- **Root cause**: Manual escaping then Vue escaping again; building regex from user input without escaping.
- **Try**: `O'Brien`, `a&b`, `<3`, `(`, `[`, `*`, `\`.
- **Review signal**: `new RegExp(userInput)`; manual `escapeHtml` before `{{ }}`; `encodeURIComponent` applied twice.
- **Fix**: Escape for regex (`s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')`) or use `includes`; let Vue escape text once.
- **Sources:** [MDN: RegExp.escape()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/escape), [Vue: Template syntax (text interpolation)](https://vuejs.org/guide/essentials/template-syntax.html#text-interpolation)

### IN-F6. Phone number handling

- **User sees**: `+61 4xx` rejected for a missing leading zero, or the `+` stripped; extensions rejected; numbers stored as numbers lose leading zeros; long German numbers rejected.
- **Root cause**: Fixed-length, digits-only, number-typed phone fields.
- **Try**: `+61 412 345 678`, `0412345678`, `+49 30 123456789012`, `+1 (555) 123-4567 x89`.
- **Review signal**: `type="number"` or `\d{10}` on phone fields.
- **Fix**: `type="tel" autocomplete="tel"`, keep as string, validate with libphonenumber-js if strict validation is required.
- **Source**: https://github.com/google/libphonenumber/blob/master/FALSEHOODS.md

### IN-F7. Address field assumptions

- **User sees**: Postcode required for a country that has none (Hong Kong, UAE); a state dropdown forced for non-US addresses; address line limit too short.
- **Root cause**: Address schemas built around US or Australian addresses.
- **Try**: Hong Kong address with no postcode; Irish Eircode `D02 X285`; UK `SW1A 1AA`.
- **Review signal**: Required postcode/state with no country dependency.
- **Fix**: Country-driven address rules (Google's libaddressinput metadata is the usual reference).
- **Source**: https://github.com/kdeldycke/awesome-falsehood#postal-addresses

---

## G. Rendering user text (XSS and interpolation)

### IN-G1. `v-html` on user-controlled text

- **User sees**: A port description containing `<img src=x onerror=…>` executes script for every viewer (stored XSS); or layout breaks from unclosed tags.
- **Root cause**: `v-html` with data from the API, query params, or i18n messages containing user values.
- **Try**: T11 in every free-text field, then view it in every place it renders (lists, tooltips, emails, PDFs, notifications).
- **Review signal**: Any `v-html`, `innerHTML`, `insertAdjacentHTML`, `h('div', { innerHTML })`.
- **Fix**: `{{ }}` text interpolation; if you need HTML, sanitise with DOMPurify and an allowlist.
- **Source**: https://vuejs.org/guide/best-practices/security.html

### IN-G2. Markdown rendering of user text

- **User sees**: `[click](javascript:alert(1))` produces a working link; raw HTML in markdown passes through.
- **Root cause**: Markdown renderer with `html: true` or no URL scheme filter, output fed to `v-html`.
- **Try**: `[x](javascript:alert(1))`, `<script>` inside markdown, `![x](https://attacker/tracker.png)`.
- **Review signal**: `marked(...)`/`markdown-it` output in `v-html`.
- **Fix**: Disable raw HTML, sanitise output with DOMPurify, restrict URL schemes.
- **Sources:** https://attacker/tracker.png

### IN-G3. User text interpolated into vue-i18n messages

- **User sees**: A company named `{0}` or `@:common.delete` or containing `|` renders as other text; message compilation error crashes the component; user value inserted into an HTML i18n message renders as HTML.
- **Root cause**: Concatenating user text into the message key or message string (`t('Deleted ' + name)`), or using `v-html="t('msg', { name })"` with HTML in the message. vue-i18n warns about HTML messages and has `escapeParameter` (uncertain whether enabled in this app).
- **Try**: T12 as a resource name, then trigger success/confirm toasts.
- **Review signal**: `t()` with a template-literal key; `v-html` with `t()`; `escapeParameter` not set when `v-html` used.
- **Fix**: Pass user text as a named parameter; use `<i18n-t>` component interpolation (slots) for rich text instead of HTML messages.
- **Source**: https://vue-i18n.intlify.dev/guide/essentials/syntax.html (HTML message warning); https://vue-i18n.intlify.dev/api/general.html#escapeparameter

### IN-G4. User text in URLs and route params

- **User sees**: A name with `/`, `?`, `#`, or `%` breaks a link or routes to the wrong page; a search term with `&` truncates the query.
- **Root cause**: Building URLs by string concatenation; vue-router encodes `params` but not hand-built `path` strings.
- **Try**: T22; `100%`, `a&b=c`, `#hash`.
- **Review signal**: `` router.push(`/x/${name}`) ``, `` href=`…?q=${q}` ``.
- **Fix**: `router.push({ name, params, query })`; `URLSearchParams`; `encodeURIComponent` once.
- **Sources:** [Vue Router: Programmatic navigation](https://router.vuejs.org/guide/essentials/navigation.html)

### IN-G5. `javascript:` / `data:` URLs in user-supplied links

- **User sees**: A "website" field rendered as `<a :href>` runs script when clicked.
- **Root cause**: Vue does not sanitise `href` bindings.
- **Try**: `javascript:alert(1)`, `JaVaScRiPt:alert(1)`, ` javascript:alert(1)` (leading space), `data:text/html,…`.
- **Review signal**: `:href="user.url"`, `:src` from user data.
- **Fix**: Parse with `new URL()` and allow only `http:`/`https:`/`mailto:`; add `rel="noopener noreferrer"` with `target="_blank"`.
- **Source**: https://vuejs.org/guide/best-practices/security.html#potential-dangers

### IN-G6. Title/tooltip attributes and `aria-label` with user text

- **User sees**: Screen readers announce odd text; tooltips show `[object Object]` or `undefined`.
- **Root cause**: Binding non-strings or untranslated fallbacks.
- **Try**: Empty name, null name.
- **Review signal**: `:title="item.name"` where name is optional. Vue removes the attribute when a bare binding is `null` or `undefined` (so no tooltip and no accessible name); the literal `undefined` appears when the value is interpolated into a string or concatenated.
- **Fix**: Fallback strings through i18n; never render `undefined`/`null`.
- **Sources:** [Vue: Template syntax (attribute bindings)](https://vuejs.org/guide/essentials/template-syntax.html#attribute-bindings), [MDN: title attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/title)

### IN-G7. Literal `null` / `undefined` rendering

See DS-B1 (persona-value-display).

---

## H. Export and downstream injection

### IN-H1. CSV / formula injection on export

- **User sees**: Opening an exported CSV in Excel runs a formula (`=HYPERLINK(…)`, DDE payloads) from a user-controlled field such as a service name or description.
- **Root cause**: CSV built client-side (or server-side) without neutralising cells starting with `=`, `+`, `-`, `@`, tab, CR, or full-width variants.
- **Try**: T13 as a name, then export.
- **Review signal**: `rows.map(r => r.join(',')).join('\n')`, `Blob([csv], { type: 'text/csv' })`, `papaparse.unparse` without escaping config.
- **Fix**: Quote every field, double inner quotes, and prefix dangerous leading characters with `'` (or a tab inside the quotes, per OWASP for Excel). This also changes legitimate negative numbers, so apply it only to string cells.
- **Source**: https://owasp.org/www-community/attacks/CSV_Injection

### IN-H2. CSV breaks on commas, quotes, newlines

- **User sees**: Export columns shift because a description contained a comma or newline.
- **Root cause**: Hand-rolled CSV join without RFC 4180 quoting.
- **Try**: `a,b`, `say "hi"`, `line1\nline2`.
- **Review signal**: Same as IN-H1.
- **Fix**: Use a CSV library; quote all fields.
- **Source**: https://datatracker.ietf.org/doc/html/rfc4180

### IN-H3. CSV opened in Excel shows mojibake

- **User sees**: `Café` appears as `CafÃ©` in Excel.
- **Root cause**: UTF-8 CSV without a BOM; Excel on Windows assumes the system code page.
- **Try**: Export any non-ASCII name; open in Excel on Windows.
- **Review signal**: `new Blob([csv])` without `'﻿'` prefix.
- **Fix**: Prepend `﻿` for Excel-targeted CSVs (and make sure the BOM isn't then treated as part of the first header by importers).
- **Sources:** [Microsoft: Opening CSV UTF-8 files correctly in Excel](https://support.microsoft.com/en-au/office/opening-csv-utf-8-files-correctly-in-excel-8a935af5-3416-4edd-ba7e-3dfd2bc4a032)

### IN-H4. Filenames built from user text

- **User sees**: Download named `Acme/Corp:Invoice?.pdf` fails or saves as `download`; Windows-reserved names (`CON`) fail.
- **Root cause**: User text used directly in `a.download` or `Content-Disposition`.
- **Try**: T22, `Acme/Corp`, `a:b`, emoji names.
- **Review signal**: `` link.download = `${name}.csv` ``.
- **Fix**: Replace `\/:*?"<>|` and control chars, trim dots/spaces, cap length.
- **Source**: BLNS "MSDOS/Windows Special Filenames".
- **Sources:** [Microsoft Learn: Naming Files, Paths, and Namespaces](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file), [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt)

---

## I. Browser assistance: autofill, password managers, keyboard hints

### IN-I1. Wrong or missing `autocomplete` tokens

- **User sees**: Password manager fills the company name into "Port name", or fills the saved password into "New password"; login autofill doesn't work.
- **Root cause**: Missing `autocomplete`; `autocomplete="off"` used to stop autofill (ignored for login fields); `name`/`id` like `username` triggering heuristics.
- **Try**: Chrome, Safari, 1Password, Bitwarden on login, signup, change-password, and generic forms.
- **Review signal**: New forms without `autocomplete`; password fields without `current-password`/`new-password`; `autocomplete="off"` on login.
- **Fix**: `username`, `current-password`, `new-password`, `one-time-code`, `email`, `tel`, `organization`, `street-address`, `postal-code`, `country`; `autocomplete="off"` only for fields like search boxes or one-time password (OTP) fields where it's justified (and expect it to be ignored).
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete

### IN-I2. Autofill doesn't update `v-model`

- **User sees**: Fields look filled by the browser but Save says "required", or the Submit button stays disabled until the user clicks into the field.
- **Root cause**: Chrome autofill on page load sets values without firing events visible to JS until user interaction (for passwords, value reads as empty until the user interacts, for privacy). Custom inputs listening only to `keydown`/`keyup` miss autofill completely.
- **Try**: Saved login; load page; click Submit without touching anything.
- **Review signal**: Inputs listening to `keyup` instead of `input`; submit button disabled on empty model at load.
- **Fix**: Listen to `input`/`change`; don't disable submit purely on empty model; read `el.value` on submit as a fallback for login forms. Chrome's autofill-on-load event behaviour is uncertain across versions; test.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/CSS/:autofill

### IN-I3. Autocapitalise, autocorrect, spellcheck on codes and IDs

- **User sees**: iOS capitalises the first letter of an email or service key; autocorrect changes a product name to a dictionary word; red squiggles under UIDs and hostnames.
- **Root cause**: Default mobile keyboard behaviour on `type="text"`.
- **Try**: iOS Safari and Android Chrome on email, username, key, hostname, ASN, and VLAN fields.
- **Review signal**: Code/ID fields missing `autocapitalize="off" autocorrect="off" spellcheck="false"`; `type="text"` for emails.
- **Fix**: Add those attributes; use `type="email"`/`type="url"` where appropriate (they disable autocapitalise by default).
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/autocapitalize

### IN-I4. Wrong `inputmode` / `enterkeyhint`

- **User sees**: A digits-only field opens the full keyboard on mobile; a decimal field opens a numeric pad with no `.`; "Go" button on mobile keyboard doesn't submit.
- **Root cause**: Missing `inputmode` (`numeric`, `decimal`, `tel`, `email`, `url`, `search`); missing `enterkeyhint`.
- **Try**: Mobile device on each numeric field.
- **Review signal**: `type="text"` numeric fields without `inputmode`; `inputmode="numeric"` on fields that need `.` or `-`.
- **Fix**: `inputmode="decimal"` for decimals (the iOS decimal pad has no minus key; uncertain on Android); `numeric` for integers; use `type=text` for negative numbers on iOS.
- **Source**: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inputmode

### IN-I5. Password field reveal/hide breaks autofill or loses caret

- **User sees**: Toggling "show password" clears the field, moves the caret to the start, or the password manager stops recognising the field.
- **Root cause**: Swapping the whole input element with `v-if` instead of switching `type`.
- **Try**: Type, toggle, type more.
- **Review signal**: `v-if`/`v-else` between two inputs for show/hide.
- **Fix**: Bind `:type="show ? 'text' : 'password'"` on one element. Make the toggle `type="button"` so it doesn't submit.
- **Sources:** [web.dev: Sign-in form best practices](https://web.dev/articles/sign-in-form-best-practices), [Vue: Conditional rendering (v-if versus v-show)](https://vuejs.org/guide/essentials/conditional.html#v-if-vs-v-show), [Vue 3 migration: key on conditional branches](https://v3-migration.vuejs.org/breaking-changes/key-attribute.html)

### IN-I6. Browser translation mangles or crashes the app

- **User sees**: With Chrome "Translate this page" on, the app throws `NotFoundError: Failed to execute 'removeChild' on 'Node'` and blanks out, or dynamic text stops updating; translated IDs, service keys, or product names (such as a product name translated into plain words) are wrong.
- **Root cause**: Google Translate replaces text nodes with `<font>` elements, so the framework later operates on detached nodes. Same mechanism affects Vue (reported against React; not verified against a Vue issue).
- **Try**: Chrome, translate page to another language, then interact (toggle `v-if` branches with bare text, change filters, open dialogs).
- **Review signal**: Bare text nodes alongside conditional siblings (`<template v-if>text</template>` next to elements); machine values (keys, IDs, code) without `translate="no"`.
- **Fix**: `translate="no"` on IDs, keys, code, brand names, and the copyable values; wrap conditional text in `<span>`.
- **Source**: https://github.com/facebook/react/issues/11538; https://martijnhols.nl/blog/everything-about-google-translate-crashing-react

---

## J. Interaction details on text fields

### IN-J1. Debounced validation lags behind fast typing or paste

- **User sees**: Error message flickers or shows for the previous value; submit enabled for an invalid value that was pasted then submitted within the debounce window.
- **Root cause**: Validation debounced but submit doesn't flush it.
- **Try**: Paste invalid value and press Enter immediately.
- **Review signal**: `useDebounceFn` around validation; submit not awaiting full validation.
- **Fix**: Validate synchronously on submit regardless of debounce.
- **Sources:** [VeeValidate: Handling forms (handleSubmit)](https://vee-validate.logaretm.com/v4/guide/composition-api/handling-forms/), [VueUse: useDebounceFn (flush and cancel)](https://vueuse.org/shared/useDebounceFn/)

### IN-J2. Validation fires on first keystroke ("premature error")

See FM-F1 (persona-form-behaviour).

### IN-J3. Caret jumps to end when the model is transformed

- **User sees**: Editing the middle of a value moves the cursor to the end after each keystroke.
- **Root cause**: Model setter transforms the value (uppercase, strip spaces, format) and Vue rewrites `el.value`.
- **Try**: Click mid-string and type.
- **Review signal**: Computed setters that transform; `toUpperCase()` in `@update:model-value`.
- **Fix**: Transform on blur, or use CSS `text-transform` for display and transform on submit; restore `selectionStart`.
- **Sources:** [WHATWG HTML: value IDL attribute, "value" mode setter](https://html.spec.whatwg.org/multipage/input.html#dom-input-value-value)

### IN-J4. Enter in an input submits an unexpected form or does nothing

See FM-A1 (persona-form-behaviour), FM-A2 (persona-form-behaviour).

### IN-J5. Double submit on Enter + click, or Enter key repeat

See FM-C1 (persona-form-behaviour).

### IN-J6. Textarea: Enter versus Shift+Enter, and line-ending normalisation

See FM-A5 (persona-form-behaviour).

### IN-J7. Clearing a field leaves stale value in state

- **User sees**: Clear an optional filter through the "x" in a `type="search"` input, and the list still filters; or the clear button in a Reka combobox resets the display but not the model.
- **Root cause**: The native search clear fires an `input` (and `search`) event; custom handlers on `keyup` miss it; some components clear only the display.
- **Try**: Use every clear affordance (native search "x", Escape in search inputs, custom clear buttons).
- **Review signal**: `@keyup` for filter updates; clear buttons that set display state only.
- **Fix**: Bind to `input`; clear the model, not just the text.
- **Sources:** [MDN: HTMLInputElement search event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/search_event), [WebKit bug 34393: Cancel button of search input field does not fire input event](https://bugs.webkit.org/show_bug.cgi?id=34393)

### IN-J8. Escape in a text input inside a dialog closes the dialog and discards edits

See FM-B1 (persona-form-behaviour).

### IN-J9. Search filter regex built from input

See NV-I9 (persona-url-state).

### IN-J10. ReDoS in validators

- **User sees**: Pasting a long, almost-valid string freezes the tab.
- **Root cause**: Catastrophic backtracking in nested quantifiers, such as `^([a-zA-Z0-9]+\s?)*$`, run on every keystroke.
- **Try**: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!` (30 or more characters, then one that doesn't match) in each regex-validated field.
- **Review signal**: Nested quantifiers `(x+)*`, `(x|xy)+`; no length check before regex.
- **Fix**: Bound length before matching; rewrite the regex; lint with `eslint-plugin-regexp` (`no-super-linear-backtracking`).
- **Source**: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

### IN-J11. Highlighting search matches breaks on special or decomposed characters

See NV-I10 (persona-url-state).

### IN-J12. Sorting user text with default `sort()`

See NV-M2 (persona-url-state).

### IN-J13. Placeholder used as the label or example value mistaken for content

- **User sees**: Placeholder `e.g. 100` looks pre-filled; users submit thinking it's set; label disappears once typing.
- **Root cause**: Placeholder-only labelling.
- **Try**: Visual check; screen reader.
- **Review signal**: Inputs with `placeholder` and no `<label>`/`aria-label`.
- **Fix**: Visible label; placeholder only as a format hint.
- **Sources:** [NN/g: Placeholders in Form Fields Are Harmful](https://www.nngroup.com/articles/form-design-placeholders/), [W3C WAI: Form instructions](https://www.w3.org/WAI/tutorials/forms/instructions/), [WHATWG HTML: placeholder attribute](https://html.spec.whatwg.org/multipage/input.html#attr-input-placeholder)

### IN-J14. Prefilled edit forms lose characters on round trip

- **User sees**: Opening Edit then Save without changes alters the value (trimmed, normalised, entity-decoded, `&amp;` → `&amp;amp;`), producing a "change" in the audit log, or a save with no changes is wrongly enabled or disabled.
- **Root cause**: Input transforms not idempotent; dirty check compares raw versus transformed.
- **Try**: Values with trailing spaces, `&`, NFD chars, smart quotes; open edit, save immediately.
- **Review signal**: `isDirty` computed through `JSON.stringify` comparison after transforms.
- **Fix**: Apply the same normalisation to the initial value before comparing; make transforms idempotent.
- **Sources:** [WHATWG HTML: Text state value sanitisation (strip newlines)](https://html.spec.whatwg.org/multipage/input.html#text-(type=text)-state-and-search-state-(type=search))

---

## K. Network identifiers and user-entered links

### IN-K1. IPv4 octets with leading zeros mean different addresses to different parsers

- **User sees**: The user enters `010.1.1.1` as a peer or customer IP. The UI accepts it and shows `10.1.1.1`, but the backend (or a library) reads `010` as octal 8, or saves the raw string. Duplicate checks miss `10.1.1.1` versus `010.1.1.1`.
- **Root cause**: A home-made regex (`\d{1,3}`) allows leading zeros, and different layers normalise differently. The npm `netmask` CVE-2021-28918 is the textbook case: it stripped leading zeros and read `012.0.0.1` as the public `12.0.0.1`, not the private `10.0.0.1`.
- **Try**: `010.1.1.1`, `0177.0.0.1`, `1.1.1.01`, `00.0.0.0`, `1.1.1.1 ` (trailing space), `1.1.1`, `1.1.1.256`, `999.999.999.999`.
- **Review signal**: An IP regex with `\d{1,3}` and no `(?!0\d)`; `parseInt(octet)` with no radix check; IPs compared as strings.
- **Fix**: Reject leading zeros (`25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d`), or use a strict parser and store the canonical form. Compare canonical forms.
- **Sources:** [Hendrickson: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf), [Malwarebytes: npm netmask vulnerability explained](https://www.malwarebytes.com/blog/news/2021/03/the-npm-netmask-vulnerability-explained-so-you-can-actually-understand-it)

### IN-K2. CIDR prefix accepted with host bits set

- **User sees**: The user enters `192.168.1.14/24` as a prefix to advertise. The UI accepts it. The backend either rejects it with a generic error, or silently stores `192.168.1.0/24`, so what the user sees and what was configured differ.
- **Root cause**: The validator checks the shape (`ip/len`, length 0 to 32) but not that the bits after the prefix are zero.
- **Try**: `10.0.0.1/8`, `10.0.0.0/8`, `10.0.0.0/33`, `10.0.0.0/0`, `10.0.0.0/32`, `10.0.0.0/08`, IPv6 `2001:db8::1/64`.
- **Review signal**: A zod `.regex()` for CIDR with no refinement on the masked address.
- **Fix**: Refine with `(ip & mask) === ip`, then either reject with "Did you mean 192.168.1.0/24?" or normalise visibly.
- **Sources:** [Wikipedia: Classless Inter-Domain Routing](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing), [Hendrickson: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### IN-K3. One IPv6 address, many strings: duplicate checks, search and display disagree

- **User sees**: `2001:DB8:0:0:0:0:0:1`, `2001:db8::1` and `2001:0db8::0001` are the same address. The UI treats them as different (a duplicate is allowed, search misses it, an unchanged form shows as dirty), or the list shows whatever form was typed.
- **Root cause**: Raw strings are compared or stored. RFC 5952 says systems should output one canonical form (lowercase, leading zeros suppressed, the longest run of zeros shortened with `::`, and `::` never used for a single field), but must accept every RFC 4291 form.
- **Try**: Enter the three forms above in a field with a uniqueness check, in search, and in an edit form that reloads the saved value.
- **Review signal**: `===` or `includes` on IPv6 strings; `toLowerCase()` as the only normalisation.
- **Fix**: Canonicalise to RFC 5952 on input and before comparing. Display the canonical form.
- **Sources:** [RFC 5952: IPv6 address text representation](https://www.rfc-editor.org/rfc/rfc5952)

### IN-K4. VLAN ID 0 and 4095 accepted, or "untagged" encoded as 0 and then shown as a VLAN

- **User sees**: The VLAN field accepts 0 or 4095 (both reserved), or the range is wrong at one end (1 to 4096). Or "untagged" is stored as `0` or `null`, then rendered as "VLAN 0" or blank (compare DS-B2 (persona-value-display) and DS-L3 (persona-value-display)).
- **Root cause**: `min(0).max(4096)`, a copied range, or a sentinel value that the display layer doesn't know about.
- **Try**: 0, 1, 4094, 4095, 4096, empty, and the "untagged" toggle on then off.
- **Review signal**: VLAN schema bounds; `vlan || '-'`; a sentinel such as `-1` or `0` with no display mapping.
- **Fix**: Range 1 to 4094 (plus any platform-reserved IDs from the API), "untagged" as an explicit boolean, and a display mapping for it.
- **Sources:** [Wikipedia: IEEE 802.1Q](https://en.wikipedia.org/wiki/IEEE_802.1Q)

### IN-K5. ASN entry: asdot notation rejected or misread, and the 2^32 boundary

- **User sees**: A customer types a 4-byte ASN in asdot (`1.10`). The field is `type=number` or parsed with `parseFloat`, so it becomes 1.1. Or asplain values above 2^31 − 1 overflow a signed integer on the server. Or 4294967296 is accepted.
- **Root cause**: The ASN is treated as a generic number. RFC 5396 defines asplain (`65546`), asdot+ (`1.10`) and asdot (asplain below 65536, asdot+ above). The maximum, 65535.65535 = 4294967295, is calculated from the two 16-bit halves (uncertain: the RFC does not state it).
- **Try**: 0, 1, 64512, 65535, 65536, `1.10`, `0.65526`, 2147483647, 2147483648, 4294967295, 4294967296, `65535.65536`.
- **Review signal**: `z.number()` or `z.coerce.number()` on an ASN; `type="number"` on an ASN; `parseFloat`.
- **Fix**: A text input with an explicit parser for asplain and asdot that converts to an integer, bounds 1 to 4294967295 (minus reserved ranges from the API), and display in one chosen notation.
- **Sources:** [RFC 5396: Textual representation of AS numbers](https://www.rfc-editor.org/rfc/rfc5396), [Hendrickson: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### IN-K6. Network identifier validators reject valid formats, or demand the wrong format

- **User sees**: A MAC address entered as `aa-bb-cc-dd-ee-ff` or `aabb.ccdd.eeff` fails validation even though it is valid. An IP field demands CIDR notation where only a host IP applies, so the user cannot enter `10.0.0.5`.
- **Root cause**: A colon-only MAC regex, or a shared "IP or prefix" validator reused for a field that takes a single host address.
- **Try**: `AA:BB:CC:DD:EE:FF`, `aa:bb:cc:dd:ee:ff`, `aa-bb-cc-dd-ee-ff`, `aabb.ccdd.eeff`, `aabbccddeeff`, `aa:bb:cc:dd:ee` (too short); for host-IP fields, `10.0.0.5` and `10.0.0.5/32`.
- **Review signal**: A MAC regex with only `:` as the separator; a CIDR schema reused on a field labelled "IP address".
- **Fix**: Accept the common MAC notations and normalise to one canonical form for storage and display. Use a host-IP schema where a prefix makes no sense, and say which format is expected in the hint.
- **Sources:** [Wikipedia: MAC address notational conventions](https://en.wikipedia.org/wiki/MAC_address#Notational_conventions), [RFC 4632: CIDR notation](https://www.rfc-editor.org/rfc/rfc4632)

### IN-K7. A user-entered URL without a scheme renders as a relative link

- **User sees**: `www.example.com` typed into a profile web address becomes `<a href="www.example.com">`. The browser resolves it against the app origin, so the link goes to `app.example.com/www.example.com`.
- **Root cause**: The stored value is bound straight to `:href` with no scheme check. A string with no scheme is a relative reference.
- **Try**: `www.example.com`, `example.com`, `//example.com`, `https://example.com`, `HTTP://Example.com`, ` https://example.com` (leading space).
- **Review signal**: `:href="profile.website"` with no normalisation; a URL schema that accepts bare hostnames but nothing adds `https://`.
- **Fix**: On save, parse with `new URL(value)` and, if that fails, try `new URL('https://' + value)`. Store the absolute URL. Allow only `http:` and `https:` (see IN-G5).
- **Sources:** [MDN: URL() constructor (relative resolution against a base)](https://developer.mozilla.org/en-US/docs/Web/API/URL/URL)

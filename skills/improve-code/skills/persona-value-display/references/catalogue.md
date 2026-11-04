# persona-value-display catalogue: display, truncation and formatting

The DS-A items (long text and truncation) are reviewed by persona-design-system rules 13-16.

Scope: Vue 3 + TypeScript SPA (Tailwind, Reka UI, vue-i18n). Tables of services, prices, bandwidth (Mbps), dates.

Each item has a **Bug** (what the user sees), **Cause**, **Try** (test data), **Spot** (pattern in a Vue/Tailwind diff), and **Fix**. Items marked *(uncertain)* need checking before you rely on them.

The JS outputs quoted below were checked locally in Node (`en-AU` machine in AEST), and those results are marked "verified in Node".

## Key sources

- Defensive CSS, Ahmad Shadeed (25 tips): https://defensivecss.dev/tips/
- Flexbox min content size: https://defensivecss.dev/tip/flexbox-min-content-size/
- W3C i18n, text size in translation: https://www.w3.org/International/articles/article-text-size
- Carbon, overflow content / truncation: https://carbondesignsystem.com/patterns/overflow-content
- PatternFly truncate guidelines: https://patternfly.org/components/truncate/design-guidelines
- Maersk truncation guidance: https://designsystem.maersk.com/content/truncation/
- NN/g, empty states: https://www.nngroup.com/articles/empty-state-interface-design/
- MDN Date (date-only parsed as UTC): https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date
- MDN toFixed: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed
- MDN Intl.NumberFormat options: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat
- MDN Intl.RelativeTimeFormat: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat/format
- MDN Intl.Segmenter: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter
- MDN Intl.PluralRules: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
- vue-i18n pluralisation: https://vue-i18n.intlify.dev/guide/essentials/pluralization
- Vue security (v-html, URLs, styles): https://vuejs.org/guide/best-practices/security
- Tailwind `truncate`: https://tailwindcss.com/docs/text-overflow ; line-clamp: https://tailwindcss.com/docs/line-clamp ; min-width: https://tailwindcss.com/docs/min-width
- Falsehoods about time (original, Noah Sussman): https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time (returns 403 to automated fetchers; curated index: https://github.com/kdeldycke/awesome-falsehood)
- WCAG 2.2 Reflow (320 CSS px): https://www.w3.org/WAI/WCAG22/Understanding/reflow.html ; Resize text 200%: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html ; Text spacing: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- MDN `scroll-margin-top` / `scroll-padding-top`: https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-padding-top
- MDN `overflow-wrap`: https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap ; `white-space`: https://developer.mozilla.org/en-US/docs/Web/CSS/white-space
- MDN `scrollbar-gutter`: https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-gutter
- Reka UI Portal (escape clipping): https://reka-ui.com/docs/utilities/portal *(uncertain URL, check the Reka docs)*

---

## A. Long text and truncation

### DS-A1. Unbroken string overflows its container
- **Bug:** A long URL, email, UID, service name or AWS ARN with no spaces runs past a card or cell edge and overlaps the next column, or forces horizontal scroll.
- **Cause:** Browsers only wrap at break opportunities, and there are none in `a3f9c2e1-...`. Default `overflow-wrap: normal`.
- **Try:** `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`; `averyveryverylongemailaddress.with.subdomains@customer-enterprise-networks.example.com`; a 36-char UUID; `arn:aws:iam::123456789012:role/some-really-long-role-name`; `https://example.com/?q=` + 200 chars.
- **Spot:** New text binding `{{ x.name }}`, `{{ email }}`, or `{{ url }}` in a fixed-width or grid/flex child with no `break-words`, `break-all`, `truncate`, or `overflow-hidden`.
- **Fix:** `break-words` (`overflow-wrap: break-word`) for prose, `break-all` for IDs and hashes, or `truncate` plus a full-value tooltip. See https://defensivecss.dev/tip/long-content/
- **Sources:** https://example.com/?q=, https://defensivecss.dev/tip/long-content/

### DS-A2. `truncate` inside flex/grid does nothing (missing `min-w-0`)
- **Bug:** The ellipsis never appears. The row widens and pushes action buttons off-screen.
- **Cause:** Flex items default to `min-width: auto` (min-content), so they never shrink below their text. Grid `1fr` behaves the same (`minmax(auto, 1fr)`).
- **Try:** A 120-char service name in a row with an icon and a kebab menu.
- **Spot:** A `truncate` element whose parent (or any ancestor up to the flex container) is a flex child without `min-w-0`, or `flex-1` without `min-w-0`. Grid `grid-cols-[1fr_auto]` instead of `grid-cols-[minmax(0,1fr)_auto]`. In column flex, missing `min-h-0` for scroll areas.
- **Fix:** Add `min-w-0` to the shrinking flex child (and each flex ancestor in the chain), and `shrink-0` on icons and buttons. Use `minmax(0,1fr)` in grids. See https://defensivecss.dev/tip/flexbox-min-content-size/ and https://defensivecss.dev/tip/grid-min-content-size/
- **In the project**: Wrap the truncating child in a `tw:min-w-0` flex item, and check that raw `tw:truncate` uses have the `min-w-0`.
- **Sources:** https://defensivecss.dev/tip/flexbox-min-content-size/, https://defensivecss.dev/tip/grid-min-content-size/

### DS-A3. Truncated text with no way to read the full value
- **Bug:** "Acme Sydney to AWS ap-sout…" with no tooltip, no `title` and no expand option. Users can't tell two similar rows apart. Touch users can't hover at all.
- **Cause:** `truncate` added for layout without any disclosure.
- **Try:** Two names that share the first 30 chars and differ at the end.
- **Spot:** `class="truncate"` or `line-clamp-*` with no `:title`, no tooltip wrapper, and no `aria-label` or full text available elsewhere.
- **Fix:** Show a tooltip only when the text is overflowing (`el.scrollWidth > el.clientWidth`), or always set `:title`. Carbon and PatternFly say truncated items should always show the full string on hover. Give touch users a detail view. Sources: https://carbondesignsystem.com/patterns/overflow-content , https://patternfly.org/components/truncate/design-guidelines
- **In the design system**: Look for a truncation composable plus a tooltip, shown only when the text is truncated. A text component may offer `truncate` and `lineClamp` props. Specs mock the truncation check because jsdom never overflows.
- **Sources:** https://carbondesignsystem.com/patterns/overflow-content, https://patternfly.org/components/truncate/design-guidelines

### DS-A4. Tooltip always shown, even when nothing is truncated
- **Bug:** A tooltip repeats short text that is already fully visible. It adds noise, and screen readers announce it twice.
- **Cause:** Tooltip bound unconditionally.
- **Try:** A 3-char name.
- **Spot:** `<Tooltip :content="name">` around a `truncate` span without an overflow check.
- **Fix:** Measure overflow (ResizeObserver) and toggle. Minor, flag as a nit.
- **In the design system**: A truncation composable may exist to decide this; see DS-A3.
- **Sources:** [PatternFly truncate guidelines](https://www.patternfly.org/components/truncate/design-guidelines), [Carbon overflow content](https://carbondesignsystem.com/patterns/overflow-content)

### DS-A5. Truncating text that must never be truncated
- **Bug:** An error message, validation message, toast, page title, or form label is cut off, hiding the actionable part ("Port speed must be less than…").
- **Cause:** A generic `truncate` applied to a shared component.
- **Try:** A 200-char API error message; a German label.
- **Spot:** `truncate` on toast body, alert, `<label>`, `<h1>`, `FormMessage`, or dialog description.
- **Fix:** Let these wrap. Carbon lists headers, titles, labels, errors, validation messages, and notifications as never-truncate. https://carbondesignsystem.com/patterns/overflow-content
- **Sources:** https://carbondesignsystem.com/patterns/overflow-content

### DS-A6. End-truncating IDs that differ at the end
- **Bug:** `a3f9c2e1-77b0-4c1d-…` shows identically for every row. Users copy the wrong one.
- **Cause:** End truncation used where the distinguishing part is the suffix (UIDs, file paths, AWS account IDs, VLAN-tagged names like `prod-sydney-link-01/02`).
- **Try:** A list of UUIDs sharing a prefix; names `Customer XYZ – Sydney – Link 1` / `… Link 2`.
- **Spot:** `truncate` on a UID, path, or serial column.
- **Fix:** Middle truncation (`a3f9c2e1…9b2d`), which needs JS, or show the short ID (first 8 chars) plus a copy button. Carbon describes front, mid and end truncation. https://carbondesignsystem.com/patterns/overflow-content
- **Sources:** https://carbondesignsystem.com/patterns/overflow-content

### DS-A7. JS truncation splits graphemes (emoji, accents, flags)
- **Bug:** Strings end in `�`, a lone skin-tone swatch, half a flag, or a broken family emoji. The count also comes out wrong ("12/50 chars" for 3 visible chars).
- **Cause:** `str.slice(0, n)` and `str.length` count UTF-16 code units. Verified in Node: `"👨‍👩‍👧‍👦".length === 11`, and `"👨‍👩‍👧‍👦abc".slice(0,3)` returns a broken fragment.
- **Try:** `👨‍👩‍👧‍👦 Family Co`, `🇦🇺 Sydney`, `Zoë` built with a combining diaeresis (`Zoë`), `Ñandú`.
- **Spot:** `.slice(0,`, `.substring(`, `.substr(`, `.length >` used on user-facing names; `maxlength` counters.
- **Fix:** `Intl.Segmenter(locale, { granularity: 'grapheme' })` for counting and cutting, or CSS truncation. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter

### DS-A8. JS-truncated text adds `...` even when not truncated, or uses three dots
- **Bug:** "Sydney..." when the name is exactly the limit; "abc..." where the full value was "abc"; inconsistent `...` versus `…`.
- **Cause:** An off-by-one check (`>=` versus `>`), or the ellipsis appended unconditionally.
- **Try:** Strings of length limit−1, limit, and limit+1.
- **Spot:** Hand-rolled `truncate(str, n)` helpers.
- **Fix:** Use `str.length > n`, the `…` character (U+2026), one shared helper, and unit tests at the boundaries. Carbon suggests the ellipsis should stand for at least 3 hidden chars.
- **Sources:** [Carbon overflow content (ellipsis stands for three or more characters)](https://carbondesignsystem.com/patterns/overflow-content)

### DS-A9. Multi-line clamp issues
- **Bug:** A description clamps to 2 lines but the third line peeks through, the ellipsis is missing, or the "Show more" toggle shows when the text is short.
- **Cause:** `line-clamp` needs `overflow: hidden` and `display: -webkit-box` (Tailwind's `line-clamp-*` sets these). Padding-bottom on the element shows part of the next line. The toggle isn't based on measurement.
- **Try:** Text of exactly 2 lines, 2.1 lines, and one long unbroken word.
- **Spot:** `line-clamp-2` combined with `py-*` on the same element, a `flex` display override, or a "Show more" with `v-if="text.length > 100"`.
- **Fix:** Put padding on a wrapper, and compare `scrollHeight > clientHeight` to decide on the toggle. https://tailwindcss.com/docs/line-clamp
- **Sources:** https://tailwindcss.com/docs/line-clamp

### DS-A10. Tables expand off-screen
- **Bug:** One long cell (a description or URL) makes the table wider than the viewport, and action columns become unreachable.
- **Cause:** `table-layout: auto` sizes to content. No `overflow-x-auto` wrapper, no cell `max-w`.
- **Try:** A 300-char unbroken description in one row; 15 columns at 1280px.
- **Spot:** A new `<table>` or column without an `overflow-x-auto` container, or cells without `max-w-*` + `truncate`/`break-words`.
- **Fix:** Wrap in `overflow-x-auto`, set `table-fixed` with column widths where it makes sense, and cap long cells.
- **Sources:** [MDN table-layout](https://developer.mozilla.org/en-US/docs/Web/CSS/table-layout), [WCAG 2.2 Understanding Reflow (data tables)](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

### DS-A11. Translated text breaks fixed-size UI
- **Bug:** A German button reads "Verbindung hinzufü…", wraps to 2 lines and misaligns a toolbar, or a tab label overflows.
- **Cause:** Translations expand. W3C/IBM: strings of up to 10 English chars can grow 200 to 300%, and over 70 chars about 130%. German compound nouns don't wrap.
- **Try:** Pseudo-localise (`[!!! Ẁéłçöɱé ţö ţĥé þöŕţåļ !!!]`), German strings, or a doubled English string.
- **Spot:** `w-24`, `w-[120px]`, `h-8` plus `whitespace-nowrap` on buttons, tabs, badges, or table headers holding `$t()` text; abbreviations used to fit.
- **Fix:** `min-w-*` instead of `w-*`, allow wrapping, `hyphens-auto` with a correct `lang` attribute. https://www.w3.org/International/articles/article-text-size and https://defensivecss.dev/tip/button-min-width/
- **Sources:** https://www.w3.org/International/articles/article-text-size, https://defensivecss.dev/tip/button-min-width/

### DS-A12. Long names in dropdowns, comboboxes, and selects
- **Bug:** The select trigger grows and shifts the form, or the option list is clipped with no ellipsis. The selected value is truncated so users can't confirm their choice.
- **Cause:** The trigger has no `min-w-0`/`truncate`. Reka `SelectContent` width isn't bound to the trigger, or is unbounded.
- **Try:** A 120-char company or location name; 500 options.
- **Spot:** A `SelectTrigger`/`ComboboxInput` without `truncate` on `SelectValue`; `SelectContent` without `max-h-*` and `overflow-y-auto`, or without a width tied to the trigger (`w-[var(--reka-select-trigger-width)]`).
- **Fix:** Truncate the value with a title, cap the content height, and wrap or truncate options.
- **Sources:** [Reka UI Select (`--reka-select-trigger-width`, popper position only)](https://reka-ui.com/docs/components/select)

### DS-A13. Long text in breadcrumbs
- **Bug:** The breadcrumb wraps onto 3 lines or pushes page actions off-screen.
- **Cause:** No truncation or collapse for middle crumbs.
- **Try:** 5 levels with 60-char names.
- **Spot:** A breadcrumb `v-for` with no `truncate`/`max-w` per crumb and no collapse.
- **Fix:** `max-w-[12rem] truncate` per crumb with a title; collapse middle crumbs to `…` with an overflow menu (Carbon).
- **Sources:** [Carbon overflow content (truncated breadcrumb with overflow menu)](https://carbondesignsystem.com/patterns/overflow-content)

### DS-A14. Long text in toasts, modal titles, and page titles
- **Bug:** The modal title pushes the close button outside the dialog. A toast grows taller than the viewport. The page `<title>` (browser tab) shows only the prefix.
- **Cause:** Title flex row without `min-w-0`, close button without `shrink-0`; toast has no `max-h`.
- **Try:** A modal "Delete {name}?" where name is 150 chars unbroken.
- **Spot:** `DialogTitle` in `flex justify-between` without `min-w-0 break-words`; close icon without `shrink-0`; `useTitle(\`${name} | App\`)`.
- **Fix:** `break-words` in titles (don't truncate titles, per DS-A5), `shrink-0` on controls, put the specific name first in document titles.
- **Sources:** [Carbon overflow content (don't truncate titles)](https://carbondesignsystem.com/patterns/overflow-content), [HMRC design patterns: page title (page heading first)](https://design.tax.service.gov.uk/hmrc-design-patterns/page-title)

### DS-A15. Space-between layouts with long content collide
- **Bug:** The label and value touch ("Bandwidth10,000 Mbps") or overlap when the label is long.
- **Cause:** `justify-between` gives no minimum gap.
- **Try:** A long translated label beside a long value.
- **Spot:** `flex justify-between` without `gap-*`.
- **Fix:** Add `gap-2`. https://defensivecss.dev/tip/space-between/
- **Sources:** https://defensivecss.dev/tip/space-between/

### DS-A16. Flex rows that don't wrap
- **Bug:** On narrow widths, filter chips or button groups overflow horizontally.
- **Cause:** `flex` defaults to `nowrap`.
- **Try:** 320px viewport; 8 active filters.
- **Spot:** A new `flex` container of variable-count children without `flex-wrap`.
- **Fix:** `flex-wrap gap-2`. https://defensivecss.dev/tip/flexbox-wrapping/
- **Sources:** https://defensivecss.dev/tip/flexbox-wrapping/

### DS-A17. Fixed heights clip content
- **Bug:** Card text is cut off at the bottom; a 2-line German label in a `h-10` button is clipped.
- **Cause:** `h-*` instead of `min-h-*`.
- **Try:** Long text; 200% text zoom.
- **Spot:** `h-[...]`, `h-12` on text containers, especially with `overflow-hidden`.
- **Fix:** `min-h-*`. https://defensivecss.dev/tip/fixed-sizes/
- **Sources:** https://defensivecss.dev/tip/fixed-sizes/

### DS-A18. Default flex stretch distorts items
- **Bug:** An avatar or icon in a tall row is stretched, or a badge becomes as tall as its multi-line sibling.
- **Cause:** `align-items: stretch` is the default.
- **Try:** A row where the neighbouring text wraps to 3 lines.
- **Spot:** A `flex` row containing a badge or icon with no `items-center`/`items-start` or `self-*`.
- **Fix:** `items-start` or `items-center`; `self-start` on badges. https://defensivecss.dev/tip/default-flexbox-stretching/
- **Sources:** https://defensivecss.dev/tip/default-flexbox-stretching/

### DS-A19. Text over image or coloured background unreadable
- **Bug:** White text disappears when the image fails or is light.
- **Cause:** No overlay or fallback background colour.
- **Spot:** Text absolutely positioned over `<img>` without a gradient or `bg-*` fallback.
- **Fix:** A gradient overlay plus a fallback `bg-`. https://defensivecss.dev/tip/text-over-image/
- **Sources:** https://defensivecss.dev/tip/text-over-image/

---

## B. Empty, null, zero, and placeholder values

### DS-B1. "undefined", "null", "NaN", "[object Object]" rendered as text
- **Bug:** A cell shows `undefined Mbps`, `null`, `$NaN`, `[object Object]`, or `Invalid Date`.
- **Cause:** Template literals and string concatenation stringify anything. Verified in Node: `String(undefined)` gives `"undefined"`, `` `${null}` `` gives `"null"`, `String({})` gives `"[object Object]"`, and `String(new Date("x"))` gives `"Invalid Date"`. Vue's `{{ }}` renders `null`/`undefined` as empty, but `{{ \`${a} ${b}\` }}` or a computed string does not.
- **Try:** API responses with the field missing, `null`, `{}`, or an unexpected nested object.
- **Spot:** `` `${speed} Mbps` ``, `name + ' (' + code + ')'`, `t('x', { value: obj })`, or `toString()` in computeds/formatters without a null guard. Optional chaining that yields `undefined` and then gets interpolated (`` `${svc?.location?.name}` ``).
- **Fix:** Format helpers return a single placeholder (`—`) for nullish or invalid input, and types reflect optionality (`string | null`).
- **Sources:** [MDN String: string coercion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String#string_coercion)

### DS-B2. Zero treated as falsy and hidden
- **Bug:** A price of $0.00, 0 Mbps, 0 VLAN, 0 services, or 0% usage shows as "—" or disappears entirely. VLAN 0 or index 0 is treated as "not set".
- **Cause:** `v-if="count"`, `value || '-'`, `if (!price)`, `&&` chains, `filter(Boolean)`.
- **Try:** `0`, `0.0`, `"0"`, `-0`, plus `false` for booleans that should render "No".
- **Spot:** `||` defaults on numeric fields; `v-if="x.price"`, `v-show="total"`; `:class="{ hidden: !count }"`.
- **Fix:** `??` (nullish coalescing), `v-if="x != null"`, explicit `Number.isFinite`.
- **In the project**: A legacy money filter may render `0` as `-`. New code uses the current money formatter.
- **Sources:** [MDN Nullish coalescing operator (??)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing)

### DS-B3. Empty string treated as a value
- **Bug:** A label shows nothing, or "Description:" followed by blank; `value ?? '—'` doesn't catch `""` or whitespace-only `"   "`.
- **Cause:** `??` only handles nullish values, and the API returns `""`.
- **Try:** `""`, `" "`, `"\n"`, `"​"` (zero-width space).
- **Spot:** `?? '—'` on string fields that the API may send as `""`.
- **Fix:** `value?.trim() ? value : '—'` in a shared helper. Decide explicitly whether `""` is "not provided".
- **Sources:** [MDN Nullish coalescing operator (??)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing)

### DS-B4. Single-character and short values
- **Bug:** Avatar initials, tag pills, or columns look broken with 1 char; a min-width cell collapses; `name.split(' ')[1][0]` throws.
- **Cause:** Code assumes "First Last".
- **Try:** `A`, `李`, `Ö`, `-`, `.`, `1`.
- **Spot:** `split(' ')[1]`, `[0].toUpperCase()` without guards.
- **Fix:** Guard indexes and use grapheme-safe first-char logic (see DS-G2).
- **Sources:** [Falsehoods programmers believe about names, Patrick McKenzie](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/)

### DS-B5. Missing empty state
- **Bug:** The table renders only headers with nothing under them, so users can't tell if data is missing, loading, or broken.
- **Cause:** Only the happy path is implemented.
- **Try:** An account with zero services; filters matching nothing.
- **Spot:** `v-for` over a list with no `v-if="!items.length"` branch; a new table without an `#empty` slot.
- **Fix:** Explain the empty state and offer a next action (NN/g: system status, learning cues, direct pathways). https://www.nngroup.com/articles/empty-state-interface-design/
- **In the design system**: Use the shared empty-state and empty-table components.
- **Sources:** https://www.nngroup.com/articles/empty-state-interface-design/

### DS-B6. Same empty message for "no data" and "no filter matches"

See NV-K1 (persona-url-state).

### DS-B7. Empty state shown while loading ("No records" flash)
- **Bug:** "No services found" flashes before the data arrives. NN/g says a misleading status during loading breaks user trust.
- **Cause:** `items = []` initial value plus `v-if="!items.length"` before the fetch resolves; or `isLoading` false on first render (TanStack `isPending` versus `isLoading`/`isFetching` confusion).
- **Try:** Throttle the network to Slow 3G and reload.
- **Spot:** `const items = ref([])` with the empty check not gated on loading; `v-if="!data?.length"` without `isPending`.
- **Fix:** Render the states in order: loading, then error, then empty, then data. Check status, not just data.
- **Sources:** [TanStack Query Vue: Queries (isPending, then isError, then data)](https://tanstack.com/query/latest/docs/framework/vue/guides/queries), [NN/g: Visibility of system status](https://www.nngroup.com/articles/visibility-system-status/)

### DS-B8. Error rendered as empty
- **Bug:** The API 500s and the user sees "No services", or a blank page.
- **Cause:** `catch` returns `[]`, or `data ?? []` hides the error.
- **Try:** Mock a 500 or a network failure.
- **Spot:** `.catch(() => [])`, `data.value ?? []` in a template with no `isError` branch.
- **Fix:** A separate error state with a retry action.
- **Sources:** [TanStack Query Vue: Queries (isError state)](https://tanstack.com/query/latest/docs/framework/vue/guides/queries)

### DS-B9. Stale data during refetch, or blank-out on refetch
- **Bug:** Changing a filter blanks the table to a spinner (jarring), or keeps showing old rows with no indicator, so they look like the new results.
- **Cause:** Using `isLoading` for refetches, or no `placeholderData`/fetching indicator.
- **Spot:** `v-if="isFetching"` replacing the table; no subtle busy indicator.
- **Fix:** Keep previous data with a dimmed or "Updating…" indicator, and only skeleton on first load.
- **Sources:** [TanStack Query Vue: Paginated queries (keepPreviousData, isPlaceholderData)](https://tanstack.com/query/latest/docs/framework/vue/guides/paginated-queries), [TanStack Query Vue: Queries (isFetching)](https://tanstack.com/query/latest/docs/framework/vue/guides/queries)

### DS-B10. Skeleton flicker and layout shift
- **Bug:** The skeleton flashes for 50 ms; content jumps when data arrives; the skeleton has 3 rows and the data has 1, so the page collapses.
- **Cause:** No delay before showing the skeleton; skeleton dimensions don't match the real content; images without width and height.
- **Try:** A fast network and a slow network.
- **Spot:** A skeleton with different heights/columns from the real row; `<img>` without `width`/`height`/`aspect-*`.
- **Fix:** Show the skeleton only after about 200 ms and hold it for a minimum time *(heuristic, uncertain exact values)*; match the layout; reserve space.
- **Sources:** [web.dev: Optimise CLS](https://web.dev/articles/optimize-cls), [NN/g: Skeleton screens](https://www.nngroup.com/articles/skeleton-screens/)

### DS-B11. Placeholder inconsistency
- **Bug:** The same "no value" shows as `-`, `—`, `N/A`, `n/a`, `None`, blank, and `0` across screens; screen readers read "dash".
- **Cause:** Ad hoc defaults.
- **Spot:** New literal `'-'`, `'N/A'` in templates.
- **Fix:** One shared placeholder (with `aria-label`/sr-only text such as "Not available"), translated.
- **In the project**: A shared empty-value constant may exist only for dates. Formatters can disagree on the placeholder (`-`, ` -`, `''`). Pick one.
- **Sources:** [UMN Accessibility: Tables (fill empty cells with text such as "none")](https://accessibility.umn.edu/getting-started/learn-7-core-accessibility-skills/tables), [NN/g: Consistency and standards](https://www.nngroup.com/articles/consistency-and-standards/)

### DS-B12. Empty arrays rendered as empty joins
- **Bug:** "Tags: " followed by nothing; "Locations: , , Sydney" from sparse arrays; "undefined, Sydney".
- **Cause:** `arr.join(', ')` with empty or nullish entries.
- **Try:** `[]`, `[null, 'Sydney']`, `['']`.
- **Spot:** `.join(', ')` without `.filter(...)`; hard-coded `', '` instead of `Intl.ListFormat`.
- **Fix:** Filter out empty entries, use `Intl.ListFormat` for "A, B and C", and show the placeholder for an empty list.
- **Sources:** [MDN Array.prototype.join](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join), [MDN Intl.ListFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/ListFormat)

### DS-B13. Unknown enum value renders blank
- **Bug:** The status column is blank for a new backend state (`DECOMMISSIONING`), or the badge shows the raw key `status.DECOMMISSIONING` or `undefined`.
- **Cause:** Lookup maps (`statusLabel[status]`, `statusColor[status]`) have no default; the i18n key is missing.
- **Try:** Mock an enum value not in the map; lowercase variants.
- **Spot:** `const map: Record<Status, …>` indexed by an API string; `t(\`status.${s}\`)` without a fallback; `switch` with no `default`.
- **Fix:** Fallback badge (neutral colour, humanised raw value), `te()` check before `t()`, an exhaustive switch with a `never` check, and log the unknown value.
- **Sources:** [TypeScript handbook: Exhaustiveness checking](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#exhaustiveness-checking), [vue-i18n Composition API (`te`)](https://vue-i18n.intlify.dev/api/composition.html)

### DS-B14. Enum case or format mismatch
- **Bug:** The badge is always grey because the API sends `"Live"` and the map key is `"LIVE"`, or `in_progress` versus `IN_PROGRESS` versus `InProgress`.
- **Cause:** No normalisation; the TS type lies about the API.
- **Spot:** Comparisons like `status === 'LIVE'` with no casing in the spec; `.toUpperCase()` scattered around.
- **Fix:** Normalise once at the API boundary and validate against the spec.
- **Sources:** [Parse, don't validate, Alexis King](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)

### DS-B15. Boolean rendered raw
- **Bug:** The cell shows `true`/`false`, or a blank for `false`.
- **Cause:** `{{ svc.locked }}`, or B2-style falsy hiding.
- **Fix:** Translated Yes/No or an icon with a text alternative.
- **Spot:** A boolean field interpolated straight into a template or cell, such as `{{ svc.locked }}` or `{{ x.isEnabled }}`, or a table column whose value is a `z.boolean()` field with no Yes/No formatter.
- **Sources:** [MDN String: string coercion (`true` becomes "true")](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String#string_coercion), [WCAG 2.2 Understanding Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

---

## C. Counts and plurals

### DS-C1. Hard-coded plural "s"
- **Bug:** "1 services", "1 item(s)", "0 result".
- **Cause:** `` `${n} item${n > 1 ? 's' : ''}` `` gives "0 item". `(s)` dodges the plural instead of handling it.
- **Try:** 0, 1, 2, 1.5, 11, 21, 101, -1.
- **Spot:** `'s'` concatenation, `> 1 ?`, `(s)` in strings, `n === 1 ?` around `$t`.
- **Fix:** Plural messages in vue-i18n (`"no services | {n} service | {n} services"`), called through `t(key, n)`. https://vue-i18n.intlify.dev/guide/essentials/pluralization
- **Sources:** https://vue-i18n.intlify.dev/guide/essentials/pluralization

### DS-C2. English-only plural logic in i18n
- **Bug:** Polish/Russian/Arabic show wrong forms (they have "few"/"many" categories); 21 in Russian takes the singular form.
- **Cause:** vue-i18n pipe syntax is positional; the default rule is English-like. Complex languages need `pluralRules` per locale.
- **Spot:** New locales added without `pluralRules`; rules not based on `Intl.PluralRules`.
- **Fix:** Implement `pluralRules` through `new Intl.PluralRules(locale).select(n)`. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules

### DS-C3. Count not passed to the plural call
- **Bug:** Always shows the plural form, or shows `{count}` literally.
- **Cause:** `t('services', { count })` relies on the vue-i18n version's behaviour; the `n` versus `count` named argument is mismatched; or `t(key)` is called without a number.
- **Spot:** Plural message keys used with `t(key, { … })` and no numeric second argument *(behaviour differs by vue-i18n version, verify)*.
- **Fix:** `t(key, n)` or `t(key, { n }, n)`, plus a unit test for 0/1/2.
- **Sources:** [vue-i18n pluralisation](https://vue-i18n.intlify.dev/guide/essentials/pluralization), [vue-i18n Composition API (`t(key, named, plural)` overload)](https://vue-i18n.intlify.dev/api/composition.html)

### DS-C4. Number inside a plural not locale-formatted
- **Bug:** "10000 services" while elsewhere it's "10,000".
- **Cause:** `{n}` is interpolated raw.
- **Fix:** Pass a pre-formatted named value (`{ count: n(10000) }`) while still selecting by the number.
- **Spot:** `t('key', { count: n })` or `t('key', n)` where the message prints `{count}` or `{n}` and `n` can reach 1000 (services, logs, sessions), with no `n(...)` or `toLocaleString()` on the named value.
- **Sources:** [vue-i18n pluralisation (override `n`/`count` with a named value)](https://vue-i18n.intlify.dev/guide/essentials/pluralization), [vue-i18n number formatting](https://vue-i18n.intlify.dev/guide/essentials/number)

### DS-C5. Counts that disagree
- **Bug:** The tab badge says "12", the table footer says "Showing 10 of 11", and the empty state says "0".
- **Cause:** Counts come from different sources (cached total versus filtered length versus page length).
- **Try:** Apply a filter; delete an item; paginate to the last page.
- **Spot:** A new count derived from `items.length` beside an API `total`.
- **Fix:** One source of truth; label "Showing X–Y of Z" correctly, including "0 of 0" and the last-page boundaries.
- **Sources:** [Carbon pagination (range of items and total)](https://carbondesignsystem.com/components/pagination/usage/), [NN/g: Consistency and standards](https://www.nngroup.com/articles/consistency-and-standards/)

### DS-C6. Pagination range text wrong at edges

See NV-J2 (persona-url-state).

### DS-C7. Overflow counts and "99+"
- **Bug:** The badge shows "1234" and overflows the pill, or "99+" when there are exactly 99.
- **Cause:** No cap, or an off-by-one cap.
- **Try:** 99, 100, 1000, 10000.
- **Fix:** `n > 99 ? '99+' : n`, with the cap set in i18n.
- **Spot:** A count binding such as `{{ items.length }}` or `{{ count }}` inside a badge, a `#badge` slot, or a counter pill, with no cap, or a cap written as `n >= 99`.
- **Sources:** [Atlassian Design System: Badge (default `max` 99, shows 99+)](https://atlassian.design/components/badge/examples)

---

## D. Numbers, currency, and units

### DS-D1. No thousands separators, or a hand-rolled separator
- **Bug:** `10000 Mbps`, `$1234567.5`; or a regex adds commas that are wrong for `de-DE` (`1.234,5`) or `en-IN` (`1,23,45,678`).
- **Cause:** Raw interpolation or a regex/`toFixed` formatter instead of `Intl.NumberFormat`.
- **Try:** 999, 1000, 1234567.891, 12345678 in `en-AU`, `de-DE`, `fr-FR`, `en-IN`, `de-CH`. Verified in Node: `de-CH` gives `1’234’567.5`, `en-IN` gives `1,23,45,678`, and `fr-FR` gives `1 234,5` with a narrow no-break space (U+202F).
- **Spot:** `.toFixed(` in templates; `replace(/\B(?=(\d{3})+(?!\d))/g, ',')`; `{{ price }}` without a formatter.
- **Fix:** `Intl.NumberFormat`/vue-i18n `n()` with the app locale, using shared formatters.
- **Sources:** [MDN Intl.NumberFormat() options](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)

### DS-D2. Float and rounding errors
- **Bug:** `$0.30000000000000004`, totals off by a cent, `1.005` shows as `1.00`.
- **Cause:** Binary floats. Verified in Node: `0.1+0.2 === 0.30000000000000004` and `(1.005).toFixed(2) === "1.00"`. MDN: `(2.55).toFixed(1)` gives `'2.5'`.
- **Try:** 0.1+0.2, 1.005, 2.675, 0.615, summing 100 × 0.01.
- **Spot:** Arithmetic on prices client-side (`price * qty`, `reduce((a,b)=>a+b)`); `Math.round(x*100)/100`; `toFixed` for money.
- **Fix:** Keep money in minor units (integer cents) or use the server's computed totals; format only at display time. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed
- **In the project**: Money goes through one formatter that keeps minor-unit precision and never rounds money away. Other apps or libraries may carry their own copies.
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed

### DS-D3. Rounding mode inconsistent with backend or invoice
- **Bug:** The app shows $10.13 and the invoice says $10.12.
- **Cause:** `Intl.NumberFormat` defaults to `halfExpand`; `toFixed` uses the exact binary value; the backend may use banker's rounding (`halfEven`). `Math.round(-2.5) === -2` (verified in Node), which rounds towards +∞.
- **Try:** x.xx5 values and negative halves.
- **Spot:** Mixed `Math.round`, `toFixed`, and Intl for the same value across screens.
- **Fix:** Display the server-formatted amount or align `roundingMode` explicitly. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat

### DS-D4. Decimal precision inconsistent or wrong for the currency
- **Bug:** `$12.5` versus `$12.50`, `¥1,234.00`, a monthly rate of `$0.00` for a value of 0.004/hr, or too many decimals (`$12.3456789`).
- **Cause:** `maximumFractionDigits` overridden; per-unit prices need more precision than totals; JPY has 0 minor digits (MDN example: `￥123,457`).
- **Try:** USD, EUR, JPY, a 0.0042 hourly rate, a whole-dollar amount.
- **Spot:** Hard-coded `minimumFractionDigits: 2` for all currencies; `toFixed(2)` on rates.
- **Fix:** Let Intl pick the currency defaults; document a separate precision for unit rates.
- **Sources:** [MDN Intl.NumberFormat() options (fraction digits default to ISO 4217 minor units)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)

### DS-D5. Currency symbol hard-coded or misplaced
- **Bug:** `$` shown for EUR/GBP accounts, `€1.234,50` instead of `1.234,50 €` (verified in Node: de-DE EUR gives `-1.234,50 €`), or `USD 10` versus `US$10` versus `$10` ambiguity across AUD/USD/NZD.
- **Cause:** `'$' + amount` concatenation; currency taken from the UI locale instead of the account's billing currency.
- **Try:** An AUD account in `en-US` locale; EUR in `de-DE`; USD in `en-AU` (shows `USD 10.00`).
- **Spot:** A literal `$` in templates or i18n strings; `currency: 'USD'` hard-coded.
- **Fix:** Pass the account's ISO currency to `Intl.NumberFormat({ style:'currency', currency })`. Use `currencyDisplay: 'narrowSymbol'` or `'code'` deliberately where ambiguity matters.
- **In the project**: Use the project's money formatter with the narrow symbol. Don't hand-build `$`.
- **Sources:** [MDN Intl.NumberFormat() options (`currencyDisplay`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)

### DS-D6. Negative currency and credits
- **Bug:** `$-12.00`, `-$-12`, or a credit shown as a positive charge; minus sign separated from the number by a wrap.
- **Cause:** Concatenating a sign or symbol by hand; `Math.abs` with a separate label.
- **Try:** -12, -0.004, refunds, and credits.
- **Spot:** `'-' + format(Math.abs(x))`, `` `$${amount}` ``.
- **Fix:** Intl with `currencySign: 'accounting'` (parentheses) or default sign handling; keep the formatted value in one `whitespace-nowrap` span.
- **Sources:** [MDN Intl.NumberFormat() options (`currencySign: 'accounting'`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat), [MDN white-space](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space)

### DS-D7. Negative zero ("-$0.00", "-0")
- **Bug:** The total shows `-$0.00` or `-0 Mbps`.
- **Cause:** Small negatives round to zero but keep the sign. Verified in Node: `en-US` USD formatting of `-0.001` gives `-$0.00`, and `maximumFractionDigits:0` on `-0.2` gives `-0`.
- **Try:** -0.001, -0, computed differences that come out as -1e-15.
- **Spot:** Formatting of computed differences or discounts.
- **Fix:** `signDisplay: 'negative'` (verified: gives `$0.00`) or normalise `Object.is(x, -0)`.
- **Sources:** [MDN Intl.NumberFormat() options (`signDisplay: 'negative'` excludes negative zero)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)

### DS-D8. Large or unsafe numbers
- **Bug:** IDs or byte counters lose precision (`9007199254740993` shows as `…992`), scientific notation appears (`1e+21`, verified with `(1e21).toFixed(2)`), or a long number overflows a cell.
- **Cause:** JSON numbers beyond `Number.MAX_SAFE_INTEGER`; `toFixed` falls back to exponent form above 1e21.
- **Try:** 2^53+1, 1e21, traffic counters in bytes over a month.
- **Spot:** Numeric IDs typed as `number`; byte totals summed on the client.
- **Fix:** IDs as strings, BigInt or server-side aggregation, and compact notation for display.
- **Sources:** [MDN Number.MAX_SAFE_INTEGER](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER), [MDN Number.prototype.toFixed (exponent form at 1e21 and above)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed)

### DS-D9. Bandwidth unit conversion (1000 versus 1024, Mbps versus MBps)
- **Bug:** 10000 Mbps shown as "9.77 Gbps"; "10,000 Mbps" in one place and "10 Gbps" in another; MB/s (bytes) confused with Mb/s (bits), off by 8×.
- **Cause:** Using 1024 for network rates (network bit rates are decimal SI, so 1 Gbps = 1000 Mbps); mixing bits and bytes; no shared formatter.
- **Try:** 1, 50, 999, 1000, 1500, 10000, 100000 Mbps; 0.5 Mbps.
- **Spot:** `/ 1024` near "bps"; `'MB'` versus `'Mb'` labels; ad hoc `speed >= 1000 ? speed/1000 + ' Gbps'`.
- **Fix:** One `formatBandwidth()` using 1000, consistent thresholds and decimals. `Intl.NumberFormat` supports `unit: 'megabit-per-second'` (verified in Node: `10,000 Mb/s`), and `gigabit`/`terabit` are sanctioned units. Decide whether "Mbps" or "Mb/s" is house style.
- **In the project**: Several speed formatters can disagree (Gbps only when divisible by 1000 versus decimal Gbps; empty as `''` versus `'-'`). A screen that switches formatter shows the same service two ways.
- **Sources:** [NIST: Prefixes for binary multiples](https://physics.nist.gov/cuu/Units/binary.html), [MDN Intl.supportedValuesOf (units: megabit, gigabit, terabit)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/supportedValuesOf)

### DS-D10. Unit conversion shows ugly decimals or loses precision
- **Bug:** "1.5 Gbps" shows as "1 Gbps" (`Math.floor`), or "0.05 Gbps" for 50 Mbps, or "2.5000000001 Gbps".
- **Cause:** Thresholds that don't keep precision; float division without formatting.
- **Try:** 1500, 2500, 50, 100 Mbps.
- **Spot:** `Math.floor(mbps/1000)`; division without `maximumFractionDigits`.
- **Fix:** Only switch units when the value is a whole multiple, or format with `maximumFractionDigits: 2` and `trailingZeroDisplay: 'stripIfInteger'` *(check browser support for trailingZeroDisplay)*.
- **Sources:** [MDN Intl.NumberFormat() options (`trailingZeroDisplay`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)

### DS-D11. Number and unit split across lines
- **Bug:** "10,000" on one line and "Mbps" on the next; "$" orphaned from the amount.
- **Cause:** Normal space between number and unit.
- **Spot:** `{{ n }} Mbps` in narrow cells.
- **Fix:** `whitespace-nowrap` on the value span, or a non-breaking space. Intl output uses NBSP only in some cases: verified in Node, `de-DE` EUR puts U+00A0 before `€`, but `en-US` unit formatting (`10 Mb/s`) uses a plain U+0020 space, so it can still wrap.
- **Sources:** [MDN white-space](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space)

### DS-D12. Percent of zero total (divide by zero)
- **Bug:** `NaN%`, `Infinity%`, a progress bar width of `NaN%` (renders full or empty at random), or "100%" when 0/0.
- **Cause:** `used / total` with total 0. Verified in Node: `Intl` percent of `0/0` gives `NaN%`.
- **Try:** total 0, used 0; used > total (over 100%); negative.
- **Spot:** `/ total` in computeds and `:style="{ width: pct + '%' }"`.
- **Fix:** Guard `total > 0`, clamp 0 to 100 for bars, and show the placeholder for an undefined ratio.
- **Sources:** [MDN Division (x / 0 is Infinity)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Division), [MDN NaN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN)

### DS-D13. Percent formatting double-multiplied
- **Bug:** "5000%" for 50%, or "0.5%" for 50%.
- **Cause:** `Intl` `style: 'percent'` expects a fraction (0.5); the API sends 50.
- **Spot:** `style: 'percent'` with API values in 0 to 100.
- **Fix:** Divide by 100 or use `unit: 'percent'` (which takes the whole number).
- **Sources:** [MDN Intl.NumberFormat() options (percent example)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat), [MDN Intl.supportedValuesOf (unit `percent`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/supportedValuesOf)

### DS-D14. Compact notation hides meaningful precision
- **Bug:** 1,250 shows as "1.3K" (verified in Node) in a billing context; "1K" versus "1.0K" inconsistency.
- **Cause:** `notation: 'compact'` defaults to 2 significant digits.
- **Fix:** Don't use compact for money or exact quantities; give a tooltip with the exact value.
- **Spot:** `Intl.NumberFormat` or `toLocaleString` with `notation: 'compact'`, or a hand-rolled `k`/`m` suffix, applied to money, a billed quantity, or a count the user acts on.
- **Sources:** [MDN Intl.NumberFormat() options (compact defaults to 2 significant digits)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)

### DS-D15. Parsing localised numbers

See FM-D18 (persona-form-behaviour).

### DS-D16. Numbers not right-aligned or not tabular
- **Bug:** Price columns are hard to compare; digits jitter as values update.
- **Cause:** Left-aligned numeric columns; proportional digits.
- **Spot:** Numeric `<td>` without `text-right tabular-nums`.
- **Fix:** `text-right tabular-nums` for numeric columns, matching the header alignment.
- **Sources:** [GOV.UK Design System: Table (right-align numbers)](https://design-system.service.gov.uk/components/table/), [MDN font-variant-numeric](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric)

### DS-D17. Sorting numbers as strings

See NV-M1 (persona-url-state).

---

## E. Dates and times

### DS-E1. Date-only string parsed as UTC shifts a day

See FM-J1 (persona-form-behaviour).

### DS-E2. Timezone not shown, or UTC versus local mixed
- **Bug:** The maintenance window shows "02:00" and users don't know whether that's UTC or local; one screen shows UTC and another local for the same event; CSV exports differ from the UI.
- **Cause:** No `timeZoneName` in the formatter; inconsistent use of `.utc()`.
- **Try:** Change the OS timezone, then compare the list, the detail view, and the export.
- **Spot:** `toLocaleString()` without options; new date formatting not through the shared helper; `format('HH:mm')` without a zone.
- **Fix:** One date helper, explicit zone labels (`timeZoneName: 'short'`), and a documented choice of local versus UTC per field.
- **In the project**: Display dates through the shared date component or formatter, with shared format constants and zone labels. A repo rule may ban Luxon, `toLocaleString`, `Intl.DateTimeFormat` and hand-built format strings for display.
- **Sources:** [MDN Intl.DateTimeFormat() options (`timeZoneName`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat)

### DS-E3. "Invalid Date" rendered
- **Bug:** The cell shows `Invalid Date` or `NaN/NaN/NaN`.
- **Cause:** `new Date(null)` is epoch (1 Jan 1970) and `new Date(undefined)` is invalid; non-ISO strings ("13/10/2026") parse differently across browsers.
- **Try:** null, undefined, "", "0000-00-00", "13/10/2026", epoch seconds versus milliseconds.
- **Spot:** `new Date(x)` without an `isNaN(d.getTime())` guard; formatting helpers that don't handle nullish input.
- **Fix:** Guard validity and return the placeholder.
- **In the project**: Leave empty values to the date component; it renders its empty placeholder.
- **Sources:** [MDN Date() constructor](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date)

### DS-E4. 1 January 1970 shown for null
- **Bug:** "Created 01/01/1970" or "Ended 56 years ago".
- **Cause:** `new Date(null)` or `new Date(0)`, or the backend sending `0` for "not set".
- **Try:** null, 0, `"1970-01-01T00:00:00Z"`.
- **Spot:** `new Date(value ?? 0)`.
- **Fix:** Treat nullish and 0 sentinels as "not set".
- **In the project**: Leave empty values to the date component; it renders its empty placeholder. Don't build a `Date` from `null`/`0`.
- **Sources:** [MDN Date() constructor (`null` coerces to 0)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date)

### DS-E5. Seconds versus milliseconds epoch
- **Bug:** Dates show in January 1970 or the year 58000.
- **Cause:** The API sends Unix seconds; `new Date(sec)` expects ms.
- **Try:** 1760313600 versus 1760313600000.
- **Spot:** `new Date(ts)` where `ts` comes from an API field named `*At`/`*Time` that's a number.
- **Fix:** Know the unit (check the spec) and `* 1000`.
- **Sources:** [MDN Date() constructor (timestamp in milliseconds)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date)

### DS-E6. Ambiguous numeric date formats
- **Bug:** `02/01/2026` is 2 Jan to an Australian and 1 Feb to an American. Verified in Node: `en-AU` gives `02/01/2026`, `en-US` gives `1/2/2026`.
- **Cause:** Numeric date formats with a locale mismatch, or hard-coded `MM/DD/YYYY`.
- **Spot:** `format('MM/DD/YYYY')`, `'DD/MM/YYYY'` literals.
- **Fix:** Use month names (`dateStyle: 'medium'`, "13 Oct 2026") or ISO where precision matters, formatted with the user's locale.
- **Sources:** [W3C i18n: Date formats](https://www.w3.org/International/questions/qa-date-format)

### DS-E7. Relative time oddities
- **Bug:** "in 0 seconds", "0 seconds ago" (verified in Node with `-0`), "1 days ago", "in -3 minutes", "59 minutes ago" when it's been 119 minutes, or "now" for a future time because the client clock is skewed.
- **Cause:** Hand-rolled pluralisation; floor versus round; the client clock is untrustworthy; unit thresholds.
- **Try:** Deltas of 0, ±1 s, 59 s, 60 s, 89 min, 23 h 59 m, a future timestamp, a client clock 5 min fast.
- **Spot:** Hand-built "X days ago" strings; `Date.now()` compared with a server timestamp.
- **Fix:** `Intl.RelativeTimeFormat` with `numeric: 'auto'` ("yesterday"), clamp small deltas to "just now", show the absolute time in a tooltip, and refresh periodically. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat/format
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat/format

### DS-E8. Relative time frozen
- **Bug:** "2 minutes ago" still says that an hour later.
- **Cause:** A computed value depends on `Date.now()`, which isn't reactive.
- **Spot:** `computed(() => formatDistance(Date.now(), x))`.
- **Fix:** A reactive `now` ref ticking on an interval (for example `useNow` from VueUse).
- **Sources:** [Vue: Computed properties (`Date.now()` isn't a reactive dependency)](https://vuejs.org/guide/essentials/computed.html), [VueUse useNow](https://vueuse.org/core/useNow/)

### DS-E9. DST and day-length assumptions

See FM-J7 (persona-form-behaviour).

### DS-E10. End-of-day range not inclusive
- **Bug:** Filtering "1 Oct – 13 Oct" excludes everything that happened on 13 Oct after 00:00.
- **Cause:** The end date is turned into `13 Oct 00:00` and used as `<=`.
- **Try:** A record at 13 Oct 23:59:59.
- **Spot:** `endDate` sent as a date at midnight with `<=` semantics; `lt` versus `lte` mismatch with the API.
- **Fix:** Use an exclusive end (`< 14 Oct 00:00`) in the user's or the agreed timezone, and say what the range means.
- **Sources:** [Django ticket #16023: date end value treated as midnight](https://code.djangoproject.com/ticket/16023)

### DS-E11. Sorting by display string

See NV-M4 (persona-url-state).

### DS-E12. Wrong locale for date and month names
- **Bug:** The UI is in Japanese and the dates are in English ("Oct 13"); the date picker starts the week on Sunday for AU users.
- **Cause:** `toLocaleDateString()` without the app locale, or `'en-US'` hard-coded; the browser default differs from the app's i18n locale.
- **Spot:** `toLocaleDateString('en-US'`, `toLocaleString()` with no args, a hard-coded `weekStartsOn`.
- **Fix:** Pass the vue-i18n locale (`d()` with `datetimeFormats`) and derive the first day of the week from the locale.
- **Sources:** [vue-i18n datetime formatting](https://vue-i18n.intlify.dev/guide/essentials/datetime), [MDN Intl.Locale getWeekInfo()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/getWeekInfo)

### DS-E13. 12 h / 24 h and midnight/noon

See FM-J10 (persona-form-behaviour).

### DS-E14. Durations and countdowns
- **Bug:** "1 hours 60 minutes", "0h 0m" for 30 s, "-1 days remaining" after expiry, "Term: 12 month".
- **Cause:** Floor/mod errors; no handling for expired; hard-coded plurals.
- **Try:** 59 s, 3600 s, 86399 s, negative values, exactly 0.
- **Spot:** Hand-rolled `Math.floor(sec/3600)` logic.
- **Fix:** A tested duration helper, `Intl.DurationFormat` where supported, an explicit expired state, and i18n plurals.
- **Sources:** [MDN Intl.DurationFormat (Baseline 2025)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DurationFormat)

### DS-E15. Client clock trusted

See FM-J6 (persona-form-behaviour).

### DS-E16. Month and year arithmetic edge cases

See FM-J8 (persona-form-behaviour).

---

## F. Copy and selection

### DS-F1. Copy button copies the formatted value
- **Bug:** Copying a service UID copies "a3f9c2e1…9b2d" (truncated) or "10,000 Mbps" when the user wanted `10000`; copying an amount includes U+202F or NBSP and breaks pasting into a spreadsheet or terminal.
- **Cause:** Copy handler reads `el.textContent` or the formatted string.
- **Try:** Copy a truncated ID, a `fr-FR` number, a price.
- **Spot:** `navigator.clipboard.writeText(el.innerText)` or `writeText(formatted)`.
- **Fix:** Copy the raw value explicitly, and decide per field whether raw or formatted is wanted.
- **Sources:** [MDN Clipboard.writeText()](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText), [MDN HTMLElement.innerText](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/innerText)

### DS-F2. Copy includes whitespace or newlines
- **Bug:** The pasted value has trailing spaces or a newline, so it fails as an API key or VLAN input.
- **Cause:** Template whitespace in `textContent`; selection across an element boundary.
- **Spot:** Copy from DOM text; multi-line templates inside the copied element.
- **Fix:** Copy from data, and `trim()` where appropriate.
- **Sources:** [MDN Whitespace in the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Whitespace)

### DS-F3. No copy feedback, or feedback that never resets
- **Bug:** Users click repeatedly, unsure it worked; or "Copied!" stays forever; clipboard failure (insecure context or permissions) is silent, so "Copied!" shows but nothing was copied.
- **Cause:** `writeText` promise not awaited or caught. It rejects outside a secure context, when the document isn't focused, or (in Safari) when the call isn't inside a user gesture.
- **Try:** Click copy on an `http://` dev host, from a button that awaits a fetch before copying (Safari), and with DevTools focused.
- **Spot:** `navigator.clipboard.writeText(x)` without `await`/`catch`.
- **Fix:** Await it, catch `NotAllowedError`, show transient feedback (and announce it through `aria-live`), show an error on failure, and fall back to selecting the text so the user can copy it by hand.
- **Sources:** [MDN Clipboard.writeText() (promise, secure context, NotAllowedError)](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText), [MDN aria-live](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live), [WebKit: Async Clipboard API](https://webkit.org/blog/10855/async-clipboard-api/)

### DS-F4. Text not selectable, or a selectable row triggers navigation
- **Bug:** Users can't select an ID to copy because the row is a link or button, or `select-none` is set; dragging to select text navigates away.
- **Cause:** The whole row is a click target; `user-select: none` on a parent.
- **Spot:** `select-none` on containers holding IDs; `@click` on `<tr>` with no text-selection guard.
- **Fix:** Keep data text selectable and ignore clicks when `getSelection().toString()` is non-empty.
- **Sources:** [MDN user-select](https://developer.mozilla.org/en-US/docs/Web/CSS/user-select), [MDN Window.getSelection()](https://developer.mozilla.org/en-US/docs/Web/API/Window/getSelection)

### DS-F5. Hidden or visual-only characters in copied text
- **Bug:** Copied text contains `…`, zero-width spaces, `&nbsp;` or icon text.
- **Cause:** CSS-generated or inserted characters (`<wbr>`, `&#8203;` for wrapping).
- **Spot:** `​` inserted to allow breaking long IDs.
- **Fix:** Use CSS `break-all`/`overflow-wrap` instead of injecting characters, and copy from data.
- **Sources:** [MDN `<wbr>` (behaves like U+200B)](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/wbr), [MDN overflow-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap)

---

## G. Special characters, HTML, and user content

### DS-G1. HTML entities double-escaped
- **Bug:** "AT&amp;T", "O&#39;Brien", "&lt;b&gt;" shown literally.
- **Cause:** The backend or i18n escapes and then Vue escapes again in `{{ }}`; vue-i18n `escapeParameter` combined with server escaping.
- **Try:** `AT&T`, `O'Brien`, `"quoted"`, `<b>`.
- **Spot:** `escape(…)`/`he.encode` before interpolation; API fields containing entities.
- **Fix:** Store raw text and escape only at render (Vue does this automatically).
- **Sources:** [Vue security (content is automatically escaped)](https://vuejs.org/guide/best-practices/security), [vue-i18n message syntax (`escapeParameter`)](https://vue-i18n.intlify.dev/guide/essentials/syntax)

### DS-G2. Avatar initials break on unusual names
- **Bug:** The avatar shows `?`, half an emoji, "UN" for undefined, lowercase, or two letters from one name; it crashes for a single name.
- **Cause:** `name.split(' ').map(p => p[0])`; `p[0]` takes the first UTF-16 code unit.
- **Try:** `Cher`, `李小龙`, `👩‍💻 Dev`, `  leading spaces`, `o'neil`, `""`, `null`.
- **Spot:** `[0]` on name parts, `charAt(0)`.
- **Fix:** Trim, split on whitespace, filter empties, take the first grapheme (`Intl.Segmenter`), upper-case per locale, and fall back to an icon.
- **Sources:** [MDN Intl.Segmenter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter), [Falsehoods programmers believe about names, Patrick McKenzie](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/)

### DS-G3. `v-html` with user or API content (XSS)

See IN-G1 (persona-text-input).

### DS-G4. User-provided URL in `:href`

See IN-G5 (persona-text-input).

### DS-G5. Markdown or rich-text injection

See IN-G2 (persona-text-input).

### DS-G6. Newlines and leading spaces collapsed
- **Bug:** Multi-line notes or descriptions show as one paragraph; ASCII tables or configs lose indentation; leading spaces disappear (so users don't see why a name "doesn't match").
- **Cause:** `white-space: normal` collapses whitespace.
- **Try:** `"line1\nline2\n\n  indented"`, `"  leading"`, `"trailing  "`.
- **Spot:** Rendering a free-text field (notes, descriptions, cloud config) in a `<p>` without `whitespace-pre-line`/`pre-wrap`.
- **Fix:** `whitespace-pre-line` for prose with line breaks, `whitespace-pre-wrap` plus `break-words` for preformatted text. https://developer.mozilla.org/en-US/docs/Web/CSS/white-space
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/CSS/white-space

### DS-G7. `whitespace-pre` without wrapping
- **Bug:** A long line in a pre block overflows horizontally.
- **Cause:** `pre` doesn't wrap.
- **Spot:** `whitespace-pre` without `overflow-x-auto` or `pre-wrap`.
- **Fix:** `whitespace-pre-wrap break-words`, or a scroll container.
- **Sources:** [MDN white-space (`pre` versus `pre-wrap`)](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space)

### DS-G8. RTL text flips punctuation or layout

See IN-C10 (persona-text-input).

### DS-G9. Emoji and unusual glyphs break line height or alignment
- **Bug:** A row with emoji is taller; emoji show as tofu (□) on old OSes; zalgo text overflows vertically.
- **Cause:** Fallback fonts have different metrics.
- **Try:** `🚀`, `Z̴̡̛͎a̷l̸g̵o̶`, `𝕏`, CJK.
- **Spot:** Fixed `h-*` rows with user text.
- **Fix:** `min-h`, `overflow-hidden` on clamped single lines, and a system emoji font in the font stack.
- **Sources:** [CSS 2.1 §10.6.1 and §10.8 (content area with several fonts, line box height)](https://www.w3.org/TR/CSS2/visudet.html), [Tailwind font-family (default stack includes emoji fonts)](https://tailwindcss.com/docs/font-family)

### DS-G10. Case transforms break languages and identifiers
- **Bug:** `uppercase` on IDs changes their meaning; the Turkish i/İ problem; German ß changes length when upper-cased.
- **Cause:** `toUpperCase()` without a locale, or CSS `uppercase` on data.
- **Spot:** `uppercase`/`capitalize` classes on data values (not labels); `.toUpperCase()` on user names.
- **Fix:** Apply text-transform only to static UI labels, and use `toLocaleUpperCase(locale)`.
- **Sources:** [MDN String.prototype.toLocaleUpperCase()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLocaleUpperCase), [MDN text-transform](https://developer.mozilla.org/en-US/docs/Web/CSS/text-transform)

### DS-G11. `capitalize` on raw enum keys
- **Bug:** "In_progress", "Live ", or "Aws" shown to users.
- **Cause:** Displaying humanised enum keys instead of translated labels.
- **Spot:** `class="capitalize"` + `{{ status.toLowerCase() }}`.
- **Fix:** A translated label map.
- **Sources:** [MDN text-transform (`capitalize` isn't title case)](https://developer.mozilla.org/en-US/docs/Web/CSS/text-transform)

### DS-G12. Missing i18n keys shown raw
- **Bug:** `services.table.header.speed` appears in the UI for some locales.
- **Cause:** The key is missing in non-English locales, and the fallback isn't configured.
- **Spot:** New `t('…')` keys added only to `en.json`.
- **Fix:** `fallbackLocale`, a CI key-parity check, and `missingWarn`.
- **Sources:** [vue-i18n fallbacking (`fallbackLocale`, `missingWarn`)](https://vue-i18n.intlify.dev/guide/essentials/fallback)

### DS-G13. Concatenated translated fragments
- **Bug:** Broken grammar in other languages ("Delete" + name + "?"); a word-order mismatch.
- **Cause:** `t('delete') + ' ' + name + '?'`.
- **Spot:** `+` or template literals combining `t()` results.
- **Fix:** One message with placeholders, `<i18n-t>` for embedded components.
- **Sources:** [vue-i18n component interpolation (`<i18n-t>`)](https://vue-i18n.intlify.dev/guide/advanced/component)

---

## H. Responsiveness, zoom, clipping and layering (micro level)

### DS-H1. 320 px reflow failures
- **Bug:** Horizontal page scroll at 320 CSS px (equivalent to 1280 px at 400% zoom); content hidden off-screen.
- **Cause:** Fixed `min-w-[…]`, `w-[600px]`, and wide tables without their own scroll container. WCAG 1.4.10 Reflow allows 2-D scrolling only for content such as data tables.
- **Try:** DevTools at 320×640; 400% browser zoom at 1280 width.
- **Spot:** Fixed pixel widths, `whitespace-nowrap` on long rows, missing `sm:` breakpoints on new layouts.
- **Fix:** Fluid widths, `flex-wrap`, and table-local `overflow-x-auto`. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- **Sources:** https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

### DS-H2. 200% text-only zoom and text-spacing overrides
- **Bug:** At 200% text size (Firefox "Zoom text only") or with a WCAG text-spacing bookmarklet, labels overlap, clip in fixed-height boxes, or get cut off.
- **Cause:** px font sizes or fixed heights; `overflow-hidden`; `line-height` in px.
- **Try:** Firefox zoom-text-only at 200%; the text-spacing bookmarklet (line height 1.5, letter spacing 0.12em, word spacing 0.16em).
- **Spot:** `text-[13px]`, `h-[32px]` with text, `leading-[18px]`.
- **Fix:** rem-based sizing (Tailwind defaults are rem), `min-h`. https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html and https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- **Sources:** https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html, https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html

### DS-H3. Tooltip or popover clipped by an `overflow-hidden` parent
- **Bug:** The tooltip is cut in half inside a table cell or card; a dropdown in a scroll container is clipped.
- **Cause:** An absolutely positioned popover is not portalled; the ancestor has `overflow: hidden|auto` or a `transform`.
- **Try:** Open the tooltip on the last row of a scrollable table, or in a card with `overflow-hidden rounded-lg`.
- **Spot:** A custom `absolute` popover inside `overflow-*` containers; Reka `*Content` used without `*Portal`.
- **Fix:** Use Reka's Portal (`TooltipPortal`, `DropdownMenuPortal`, `PopoverPortal`), with collision detection.
- **Sources:** [Reka UI Tooltip (TooltipPortal portals content into body)](https://reka-ui.com/docs/components/tooltip), [Reka UI Select (SelectPortal)](https://reka-ui.com/docs/components/select)

### DS-H4. Dropdown clipped by a modal, or behind it (z-index)
- **Bug:** A select inside a dialog opens behind the overlay, or is cut at the dialog edge; a toast sits under the modal backdrop.
- **Cause:** Portal z-index lower than the dialog; stacking context created by `transform`/`filter`/`opacity` on an ancestor; arbitrary `z-[9999]` wars.
- **Try:** A select near the bottom of a modal; a nested dialog; a toast while the modal is open.
- **Spot:** New `z-*` values outside the scale; dialogs with `transform` classes; portalled content missing the layer token.
- **Fix:** A documented z-index scale and portalled layers ordered consistently.
- **Sources:** [MDN Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Stacking_context)

### DS-H5. Sticky header overlaps anchor targets and focus
- **Bug:** Jumping to `#section`, or keyboard-tabbing to a field, lands it under the sticky header; error-summary links scroll the field out of view.
- **Cause:** No `scroll-padding-top`/`scroll-margin-top`.
- **Try:** Click in-page anchors; tab through a long form; trigger a validation error summary.
- **Spot:** New `sticky top-0` headers without matching `scroll-pt-*` on the scroll container (or `scroll-mt-*` on targets).
- **Fix:** `scroll-pt-[header height]` on `html` or the scroller. https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-padding-top (WCAG 2.2 SC 2.4.11 Focus Not Obscured.)
- **Sources:** https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-padding-top

### DS-H6. Sticky not working
- **Bug:** The sticky table header or sidebar scrolls away.
- **Cause:** An ancestor has `overflow: hidden/auto`; in grid, the item stretches to full height (needs `align-self: start`).
- **Spot:** `sticky` inside `overflow-hidden` wrappers; `sticky` grid children without `self-start`.
- **Fix:** https://defensivecss.dev/tip/position-sticky-grid/
- **Sources:** https://defensivecss.dev/tip/position-sticky-grid/

### DS-H7. Scrollbar layout shift and always-on scrollbars
- **Bug:** Content jumps sideways when a list grows past the viewport height; Windows users see permanent scrollbars from `overflow-scroll`.
- **Cause:** The scrollbar appears and takes width; `overflow: scroll` instead of `auto`.
- **Spot:** `overflow-scroll` (prefer `overflow-auto`); modals that toggle body overflow.
- **Fix:** `overflow-auto`, `scrollbar-gutter: stable`. https://defensivecss.dev/tip/scrollbar/ and https://defensivecss.dev/tip/scrollbar-gutter/
- **Sources:** https://defensivecss.dev/tip/scrollbar/, https://defensivecss.dev/tip/scrollbar-gutter/

### DS-H8. Scroll chaining from modals and dropdowns
- **Bug:** Scrolling to the end of a dropdown list scrolls the page behind it.
- **Cause:** Default scroll chaining.
- **Spot:** New scrollable panels without `overscroll-contain`.
- **Fix:** `overscroll-contain`. https://defensivecss.dev/tip/scroll-chain/
- **Sources:** https://defensivecss.dev/tip/scroll-chain/

### DS-H9. Short viewport (vertical) issues
- **Bug:** On a laptop at 125% scaling or in landscape mobile, modal action buttons are below the fold and unreachable; a sticky footer covers content. At 1280 px wide and 400% zoom (about 320 by 256 CSS px), the sticky header, footer, and banner cover most of the viewport and the focused field.
- **Cause:** `h-screen` modals without internal scroll; no `max-h` on the dialog body; sticky bars that stay sticky at any viewport height.
- **Try:** A 1366×600 viewport; 1280 px at 400% browser zoom, then Tab through a long form.
- **Spot:** Dialog content without `max-h-[…] overflow-y-auto`; `h-screen` (prefer `h-dvh`/`min-h-dvh`); `sticky`/`fixed` bars with no height media query.
- **Fix:** Scroll the body region and keep actions visible. Make sticky bars static at small viewport heights, or let users collapse them.
- **Sources:** [Defensive CSS: Vertical media queries](https://defensivecss.dev/tip/vertical-mq/), [WCAG 2.2 Understanding 1.4.10 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

### DS-H10. Hover-only affordances on touch
- **Bug:** Row actions or the copy button only appear on hover, so they're invisible on touch and to keyboard users; a sticky hover state on mobile.
- **Cause:** `opacity-0 group-hover:opacity-100` with no focus or touch path.
- **Spot:** `group-hover:` reveal without `group-focus-within:`.
- **Fix:** Also reveal on `focus-within`, and gate hover effects with `@media (hover: hover)`. https://defensivecss.dev/tip/hover-media/
- **Sources:** https://defensivecss.dev/tip/hover-media/

### DS-H11. iOS input zoom
- **Bug:** iOS Safari zooms into the page when focusing inputs (font-size under 16 px), breaking the layout.
- **Cause:** `text-sm` (14 px) inputs.
- **Spot:** `text-sm`/`text-xs` on `<input>`/`<select>` for mobile.
- **Fix:** `text-base` on mobile inputs. https://defensivecss.dev/tip/input-zoom-safari/
- **Sources:** https://defensivecss.dev/tip/input-zoom-safari/

### DS-H12. Button and badge min-width
- **Bug:** A short label ("OK", or "Ja" in German) makes a tiny button; badges with "0" become circles of a different size than "12".
- **Cause:** No minimum width.
- **Spot:** Buttons without `min-w-*` in dialogs; count badges without `min-w-[1.25rem]` + `text-center`.
- **Fix:** https://defensivecss.dev/tip/button-min-width/
- **Sources:** https://defensivecss.dev/tip/button-min-width/

### DS-H13. CSS variable without fallback
- **Bug:** A theme token is missing in one context (app, iframe, or embedded widget), so the colour or spacing collapses.
- **Cause:** `var(--x)` with no fallback.
- **Spot:** Arbitrary values like `bg-[var(--brand)]`.
- **Fix:** `var(--x, fallback)`. https://defensivecss.dev/tip/css-variable-fallback/
- **Sources:** https://defensivecss.dev/tip/css-variable-fallback/

### DS-H14. Grid fixed values and auto-fit/auto-fill
- **Bug:** A card grid overflows at narrow widths; one card stretches to the full width when alone.
- **Cause:** `grid-cols-[250px_1fr]` without a breakpoint; `auto-fit` versus `auto-fill` choice.
- **Spot:** `repeat(auto-fit, minmax(300px, 1fr))` where 300px > the container at 320 px viewport.
- **Fix:** `minmax(min(100%, 300px), 1fr)`. https://defensivecss.dev/tip/auto-fit-fill/ and https://defensivecss.dev/tip/css-grid-fixed-values/
- **Sources:** https://defensivecss.dev/tip/auto-fit-fill/, https://defensivecss.dev/tip/css-grid-fixed-values/

### DS-H15. Component spacing assumes content
- **Bug:** A title collides with an icon or button when the title gets long, because spacing was only on one side.
- **Cause:** Missing margins/gaps on the elements that grow.
- **Fix:** https://defensivecss.dev/tip/spacing/
- **Spot:** A `tw:flex` row with `tw:justify-between` or `tw:ml-auto` and no `tw:gap-*`, where one child renders a dynamic `{{ }}` title and the other is an icon or button.
- **Sources:** https://defensivecss.dev/tip/spacing/

---

## I. Images and icons

### DS-I1. Broken image with no fallback
- **Bug:** A broken-image icon plus alt text overflows a 32 px avatar, or partner/cloud provider logos are missing.
- **Cause:** No `@error` handler; the CDN URL changed; the API returns a null logo.
- **Try:** A 404 URL, `null`, an empty string, a slow image.
- **Spot:** `<img :src="x.logoUrl">` without `@error` or a fallback; `:src` possibly empty (an empty `src` may re-request the page *(older browser behaviour, uncertain today)*).
- **Fix:** `@error` swaps to a placeholder or initials; `v-if` on the URL.
- **Sources:** [MDN `<img>` (error event, fallback pattern)](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img)

### DS-I2. Image distortion and overflow
- **Bug:** Logos are squashed or stretched; a large image overflows its card.
- **Cause:** Fixed width and height without `object-fit`; no `max-w-full`.
- **Spot:** `<img class="w-10 h-10">` without `object-contain`/`object-cover`.
- **Fix:** `object-contain` for logos, `object-cover` for photos, `max-w-full`. https://defensivecss.dev/tip/image-compressed/ and https://defensivecss.dev/tip/img-max-width/
- **Sources:** https://defensivecss.dev/tip/image-compressed/, https://defensivecss.dev/tip/img-max-width/

### DS-I3. Images without reserved dimensions cause layout shift
- **Bug:** The table rows jump as logos load.
- **Cause:** No width and height attributes or aspect ratio.
- **Fix:** Set `width`/`height` or `aspect-square`.
- **Spot:** A new `<img :src="...">` for a logo or avatar with no `width`/`height` attributes, no fixed `tw:size-*`/`tw:h-*` on it or its wrapper, and no `tw:aspect-*`.
- **Sources:** [web.dev: Optimise CLS (images without dimensions)](https://web.dev/articles/optimize-cls), [MDN `<img>` (width and height)](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img)

### DS-I4. Light logo invisible on a light background, or in dark mode
- **Bug:** A white provider logo disappears on a white card.
- **Fix:** A neutral backdrop or inner border. https://defensivecss.dev/tip/inner-shadow/
- **Sources:** https://defensivecss.dev/tip/inner-shadow/

### DS-I5. Icon-only status without text
- **Bug:** Status shown only as a coloured dot; colour-blind users and screen-reader users can't tell.
- **Cause:** Colour as the only signal.
- **Spot:** A badge with no text, or `sr-only` text missing.
- **Fix:** A text label or `sr-only` text plus a tooltip.
- **Sources:** [WCAG 2.2 Understanding Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

### DS-I6. Icon squashed in a flex row
- **Bug:** The icon shrinks to 8 px when the adjacent text is long.
- **Cause:** Flex shrink.
- **Spot:** An icon in a `flex` row without `shrink-0`.
- **Fix:** `shrink-0` (or `flex-none`).
- **Sources:** [MDN flex-shrink](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-shrink)

### DS-I7. Background images repeat on large screens
- **Bug:** An illustration tiles on ultra-wide monitors.
- **Fix:** `bg-no-repeat`. https://defensivecss.dev/tip/bg-repeat/
- **Spot:** `background-image`, `bg-[url(...)]` or `:style="{ backgroundImage }"` with no `tw:bg-no-repeat` (or `background-repeat: no-repeat`).
- **Sources:** https://defensivecss.dev/tip/bg-repeat/

---

## J. Status, badges, and table rendering details

### DS-J1. Badge colour and label mapping drift
- **Bug:** "Failed" is green because the map wasn't updated; two components map the same status differently.
- **Cause:** Duplicated status-to-colour maps.
- **Spot:** A new local `statusColors` object instead of the shared one.
- **Fix:** One shared mapping, tested for exhaustiveness.
- **Sources:** [NN/g: Consistency and standards](https://www.nngroup.com/articles/consistency-and-standards/), [TypeScript handbook: Exhaustiveness checking](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#exhaustiveness-checking)

### DS-J2. Header and cell alignment mismatch
- **Bug:** Numeric headers left-aligned over right-aligned values; sort icons push the header text.
- **Spot:** `text-right` on `<td>` but not `<th>`.
- **Fix:** Align both, and reserve space for the sort icon.
- **Sources:** [GOV.UK Design System: Table (numeric headers align with numbers)](https://design-system.service.gov.uk/components/table/)

### DS-J3. Column widths jump while sorting, paginating, or loading
- **Bug:** Columns resize on each page or when the spinner replaces rows.
- **Cause:** `table-auto` with variable content.
- **Fix:** `table-fixed` or explicit widths for stable columns.
- **Spot:** A new table or data-table `columns` array for a sorted, paginated, or loading table where no column sets `width`, or a raw `<table>` without `tw:table-fixed`.
- **Sources:** [MDN table-layout](https://developer.mozilla.org/en-US/docs/Web/CSS/table-layout)

### DS-J4. Row actions disappear with long content
- **Bug:** The kebab menu is pushed off-screen by a long name (see DS-A2/A10).
- **Fix:** A sticky right action column, or `shrink-0` with truncation in the name cell.
- **Spot:** An `id: 'actions'` column without `stickyRight: true`, or a kebab or action button in a flex row beside a name binding with no `tw:shrink-0`.
- **Sources:** [PatternFly v5 table design guidelines (actions in the rightmost column)](https://v5-archive.patternfly.org/components/table/design-guidelines), [PatternFly v5 table demos (sticky header and last column)](https://v5-archive.patternfly.org/components/table/html-demos)

### DS-J5. Inconsistent display of the same field across screens
- **Bug:** The list shows "10 Gbps", the detail shows "10000 Mbps", and the checkout shows "10,000Mbps".
- **Cause:** Multiple formatters.
- **Spot:** A new inline formatting where a shared util exists (search the repo for existing `format*` helpers).
- **Fix:** Reuse the shared formatter.
- **In the project**: See the speed formatters under DS-D9 and the money formatters under DS-D2.
- **Sources:** [NN/g: Consistency and standards](https://www.nngroup.com/articles/consistency-and-standards/)

### DS-J6. Locale-unaware string sort

See NV-M2 (persona-url-state).

### DS-J7. Search and filter mismatch with the display
- **Bug:** Searching "10 Gbps" finds nothing because the data is 10000; searching "Zurich" doesn't find "Zürich"; leading or trailing spaces in the search box return nothing.
- **Cause:** The filter runs on the raw value, the display shows the formatted one; no normalisation.
- **Try:** Accents, case, surrounding whitespace.
- **Fix:** Normalise (`trim`, `toLocaleLowerCase`, `normalize('NFD')`, and strip diacritics) and search the displayed form where it makes sense.
- **Spot:** A client-side search such as `x.name.toLowerCase().includes(q)` where `q` has no `trim()` and no `normalize('NFD')`, or a filter run on the raw value (`10000`) of a column shown formatted (`10 Gbps`).
- **Sources:** [MDN String.prototype.normalize()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize)

---

## K. Toasts and notifications

### DS-K1. Duplicate toasts for one failure
- **Bug:** One failed request shows two or three identical error toasts.
- **Cause:** An `onError` on each observer (a composable used twice on the page) plus a global handler as well. Every observer of the same query reports the same error.
- **Try:** Make one endpoint return 500 on a page where two components use the same query composable. Count the toasts.
- **Spot:** `useQuery({ ..., onError: toast })` or a `watch(error, toast)` inside a shared composable, alongside a global `QueryCache({ onError })`.
- **Fix:** One global `QueryCache.onError`. Toast only when cached data already exists (a failed background refetch), and handle first-load errors in place, inside the component.
- **Sources:** [TkDodo: React Query error handling](https://tkdodo.eu/blog/react-query-error-handling)

### DS-K2. Many toasts at once flood the screen or overlap
- **Bug:** A bulk action on 50 items fires 50 toasts. Toasts created in code sit on top of each other instead of stacking, so only the last one can be read. Screen readers drop queued messages.
- **Cause:** One toast per item or per request; toasts created outside the shared toast viewport (their own `position: fixed` element, or a separate stacking context), so they don't stack.
- **Try:** Bulk-update 50 items with 2 forced failures. Trigger two programmatic toasts within 100 ms of each other. Check with VoiceOver what is read.
- **Spot:** `toast()` inside a `forEach` or per-item `onSuccess`; toast markup mounted outside the app-level provider; hand-made `fixed bottom-4 right-4` toasts.
- **Fix:** One summary toast ("48 updated, 2 failed"), with details inline (see FM-N9 (persona-form-behaviour)). Route every toast through one viewport that stacks them. Avoid several foreground toasts at once.
- **Sources:** [Reka UI: Toast (type)](https://reka-ui.com/docs/components/toast)

### DS-K3. A toast disappears before it can be read, or holds information found nowhere else
- **Bug:** An error toast with the reason ("VLAN 100 already in use on this port") or a success toast with the new order ID disappears after 3 to 5 seconds, before it can be read or copied. An Undo action vanishes before a keyboard user can reach it. The timer doesn't pause on hover or focus.
- **Cause:** One global toast duration for every severity; key details shown only in the toast.
- **Try:** Trigger each error and success toast and time them. Hover and focus them, and switch window. Check whether the information is also on the page or on the record.
- **Spot:** `toast({ duration: 3000 })` for errors; order IDs or error reasons only in toasts; time-critical actions (Undo) inside toasts.
- **Fix:** Errors stay until dismissed (`duration: Infinity`). Pause on hover, focus, and window blur. Put key IDs and reasons on the page or record too, and keep time-critical actions out of toasts. WCAG 2.2.1 applies when the toast is the only way to get the information. See FM-F16 (persona-form-behaviour) for success messages in forms.
- **Sources:** [Reka UI: Toast](https://reka-ui.com/docs/components/toast), [WCAG 2.2 Understanding 2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html), [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### DS-K4. A toast is lost on navigation, or outlives its context
- **Bug:** A redirect after success unmounts the component, so the toast never shows. Or "Service renamed" or "Failed to load port X" stays visible after the user moves to a different service or switches company, so it now seems to describe the current screen.
- **Cause:** Toasts rendered inside the page component; or global toast and banner stores that are not keyed to a route, record, or company, with nothing clearing them on navigation. NV-P5 (persona-url-state) covers a late response from an in-flight request; NV-K5 (persona-url-state) covers error state that filters should clear.
- **Try:** Save a form that redirects on success. Trigger an error on record A, then open record B, switch company, and press Back.
- **Spot:** A toast provider or viewport inside a route component; a global alert store with no `router.afterEach` clearing and no context key on messages; messages that don't name the object.
- **Fix:** A single app-level provider and viewport (portalled to body). Tag messages with their context (route, resource ID, company) and dismiss them when it changes, or name the resource in the message.
- **Sources:** [Reka UI: Toast](https://reka-ui.com/docs/components/toast), [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### DS-K5. A toast is not announced, or is announced twice
- **Bug:** Screen reader users hear nothing when a toast appears, or hear it twice.
- **Cause:** The live region is inserted together with its text, so it isn't registered in time; or nested live regions both announce.
- **Try:** VoiceOver and NVDA: trigger a success and an error toast; listen.
- **Spot:** `<div v-if="show" aria-live="polite">`; `aria-live` on both the viewport and each toast.
- **Fix:** A live region that always exists, with content injected later; `role="status"` (and `aria-live="polite"`) for passive messages. Reka's `type` (`foreground` or `background`) controls urgency. See FM-F16 (persona-form-behaviour) for form success messages.
- **Sources:** [Inclusive Components: Notifications](https://inclusive-components.design/notifications/), [Reka UI: Toast](https://reka-ui.com/docs/components/toast)

### DS-K6. A toast covers the focused control
- **Bug:** A bottom-right toast covers the wizard's Next button or the field that has focus.
- **Cause:** The toast viewport sits over the sticky action bar, with no offset.
- **Try:** At 1366 by 768 and at 320 px wide, trigger a toast while focus is on the bottom action bar. Tab through while it is visible.
- **Spot:** Toast viewport `fixed bottom-0 right-0` on pages with sticky footers; no `scroll-padding`.
- **Fix:** Keep toasts clear of sticky action bars, dismiss on blur, and add scroll padding.
- **Sources:** [WCAG 2.2 Understanding 2.4.11 Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)

### DS-K7. A toast steals focus, or its action can't be reached
- **Bug:** Focus jumps to the toast while the user is typing; or keyboard users can't reach its action button.
- **Cause:** `focus()` on toast mount; no keyboard route to the viewport.
- **Try:** Type in a field while a background save raises a toast. Then try to reach the toast's action with the keyboard only.
- **Spot:** `autofocus` or `.focus()` in a toast component; actions inside toasts with no hotkey hint.
- **Fix:** Never move focus to passive notifications. Provide a hotkey to reach the viewport (Reka's default is F8) and make it discoverable.
- **Sources:** [Inclusive Components: Notifications](https://inclusive-components.design/notifications/), [Reka UI: Toast](https://reka-ui.com/docs/components/toast)

---

## L. Render crashes and unexpected API values

### DS-L1. A nullable nested object is dereferenced in a template, so the whole component fails to render
- **Bug:** A region renders blank or half-rendered for one product or account type. Vue's error handler catches a `TypeError: Cannot read properties of null` and nothing after it renders. DS-B1 covers "undefined" shown as text; here nothing renders at all.
- **Cause:** A render path reads `a.b.c` where `b` is legitimately `null` for some records (for example `device.vendorConfig.label` when a device has `vendorConfig: null`). A default parameter does not cover `null`. A template ref used before it is mounted gives the same class of crash (`ResizeObserver.observe` given a non-Element).
- **Try:** Records with each nullable object set to `null` (a device with no vendor config, a service with no location, a new account with no address or logo, a service with an invalid rate limit). Clear a filter whose value can be `undefined`.
- **Spot:** Chained property access in templates and computeds with no `?.`; types that mark a field as non-null when the API spec says `nullable`; `function f(x = {})` called with `null`; `observe(el.value)` with no null check.
- **Fix:** Optional chaining with a display fallback, types generated from the spec, and an `onErrorCaptured` boundary per region so one bad record doesn't blank the page.
- **Sources:** [MDN: Optional chaining](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining), [Vue: onErrorCaptured](https://vuejs.org/api/composition-api-lifecycle.html#onerrorcaptured)

### DS-L2. A strict client response schema rejects a null or missing field, and the screen that needs it errors
- **Bug:** A list, tab, or form never gets its data and shows an error or an empty state, because the response failed client-side parsing.
- **Cause:** A Zod schema written as `.optional()` or non-null meets a real `null`, or a field the backend has dropped. `.optional()` allows `undefined` only. "Zod Drift" reports are logged only; "Zod Parsing Error" reports mean the parse failed. Which screens actually break is not confirmed per endpoint *(uncertain)*.
- **Try:** Mock each nullable field in the API spec as `null` and as missing (speed `null`, a role-limited user while impersonating). Load the screen.
- **Spot:** `.optional()` where the spec says `nullable: true`; `.parse()` (throws) on responses where `.safeParse()` with a fallback was intended; schemas hand-written rather than generated from the spec.
- **Fix:** `.nullish()` or `.nullable()` to match the spec; parse leniently at the boundary and report drift; render what parsed rather than failing the whole view.
- **Sources:** [Zod API: optionals, nullables, and nullish](https://zod.dev/api#optionals)

### DS-L3. Sentinel or placeholder values render as real data
- **Bug:** "Max Mbps: 9007199254740991", "Preferred VLAN -1" for an untagged connection, or "Speed change from Unknown".
- **Cause:** An internal sentinel stands in for "no value" (`Number.MAX_SAFE_INTEGER` for unlimited, `-1` for untagged, the string "Unknown" for a missing old value) and is never mapped back for display. Related to DS-D8 and DS-B13, and to IN-K4 (persona-text-input) for VLAN input.
- **Try:** Records with no upper limit, an untagged VLAN, and a change history with no previous value. Refresh mid-load.
- **Spot:** `?? Number.MAX_SAFE_INTEGER`, `?? -1`, `|| 'Unknown'` in data mappers whose output also feeds the template.
- **Fix:** Model "none" explicitly (`null` or a tagged union), and map it to a display label ("Unlimited", "Untagged", "Not set") in one place.
- **Sources:** [MDN: Number.MAX_SAFE_INTEGER](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)

### DS-L4. A formatted string or unknown value passed to Intl or an enum-checking prop throws
- **Bug:** The page or widget breaks rather than showing a slightly wrong label: `RangeError: Invalid currency code : US$0.03`, or a component throws "Invalid map size: small".
- **Cause:** `new Intl.NumberFormat(locale, { style: 'currency', currency })` given a formatted string instead of an ISO 4217 code throws `RangeError`. A component that validates a prop against an enum throws on an unexpected value instead of falling back.
- **Try:** Currency `''`, `'aud'`, `'US$0.03'`, `undefined`; enum props with a new or lowercase value.
- **Spot:** `currency: price.display` or any non-code value; `throw` in a prop validator or a `switch` default; `Intl.*Format` created in render with no try/catch.
- **Fix:** Validate the code (`/^[A-Z]{3}$/`) and fall back to a plain number with the code shown; prop validators that warn and use a default, not throw.
- **Sources:** [MDN: Intl.NumberFormat `currency` option (throws RangeError)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat#currency)

### DS-L5. An unknown status falls into a misleading default bucket
- **Bug:** The backend adds a new status (such as `DECOMMISSIONING`) and the badge shows a green "Live". DS-B13 covers unknown values rendering blank; this covers them rendering as a wrong, reassuring value.
- **Cause:** A `switch` or lookup with `default: 'success'`, or a binary `status === 'FAILED' ? red : green` over a multi-value enum.
- **Try:** Mock unknown, lowercase, `null`, and future enum values into every status badge and filter.
- **Spot:** Binary ternaries over enums; a `default` case returning a positive state; no TypeScript exhaustiveness check (`never`).
- **Fix:** An exhaustive mapping with a neutral "Unknown (RAW_VALUE)" fallback, and log unknown values.
- **Sources:** [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### DS-L6. Range scaling breaks when every value is equal
- **Bug:** A utilisation sparkline, bar scale, or heat colour scale with one data point, or with all points equal (often all 0), renders NaN widths, an invisible line, a full-height bar, or a "NaN%" label. DS-D12 covers percent of a zero total; this covers `(v - min) / (max - min)` scaling. For chart axes, see CH-A3 (persona-charts).
- **Cause:** Division by `max - min` with no zero-range guard; `Math.max(...arr)` on an empty array gives `-Infinity`.
- **Try:** Data sets `[]`, `[5]`, `[0,0,0]`, `[7,7,7]`, `[0, 1e-9]`.
- **Spot:** `/ (max - min)`; `Math.max(...values)` or `Math.min(...values)` on a possibly empty array.
- **Fix:** Guard a zero range (centre or pad the domain), and handle the empty and single-point cases explicitly.
- **Sources:** [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

---

## M. Displayed state that drifts from reality

### DS-M1. A pending or scheduled change is shown as if it were already in effect
- **Bug:** After a speed upgrade order, the detail page shows the new speed while provisioning is still pending. "Terminate" says "Deleted", yet the service runs and bills until the end of the term, with no "terminating on 30 Nov" badge. A price change for the next billing cycle shows as the current price.
- **Cause:** The UI writes the requested value into the displayed field (optimistic `setQueryData`), or the copy uses an immediate verb for a deferred action. FM-C6 (persona-form-behaviour) and NV-O2 (persona-url-state) cover optimistic updates that hide failures; here the request succeeded, but its effect is deferred.
- **Try:** For each change type, check what the detail, list, and invoice views show between "requested" and "effective", and what the success copy claims.
- **Spot:** `setQueryData` writing requested values into "current" fields; success copy such as "updated" or "deleted" for actions the API marks as pending or scheduled.
- **Fix:** Show current and pending side by side ("1 Gbps → 10 Gbps, pending") with the effective date, and use deferred verbs ("Scheduled to terminate on …").
- **Sources:** [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [Bolton: FEW HICCUPPS](https://developsense.com/blog/2012/07/few-hiccupps)

### DS-M2. A changed locale, time zone, or currency preference doesn't apply until reload
- **Bug:** The user switches display time zone or locale in profile settings. Some numbers and dates change and others keep the old format until a full reload, so one screen mixes both.
- **Cause:** `new Intl.NumberFormat(locale)` or a date formatter created at module scope or cached in a `const` inside setup; formatted strings stored in a query `select` result, which is cached.
- **Try:** Change each display preference and visit every page without reloading, including cached list pages and Back navigation.
- **Spot:** Module-level `Intl.*Format` instances; formatting inside TanStack `select` or in stored state rather than at render time.
- **Fix:** Make formatters `computed` on the preference (memoise per locale key), format at render time, or tell the user a reload is needed.
- **Sources:** [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### DS-M3. One concept has several names across screens
- **Bug:** The same thing is called "Term", "Contract term", and "Minimum term" on different screens, or "Service ID", "Product UID", and "UID", or "Rate limit", "Speed", and "Bandwidth". Users think they are different settings, and search and support conversations miss. DS-J5 covers inconsistent value formatting; this covers inconsistent naming.
- **Cause:** Per-screen i18n keys with free-text labels and no glossary.
- **Try:** Follow one attribute through the list, detail, edit form, order review, invoice, and CSV export headers, and compare the labels.
- **Spot:** New i18n keys that duplicate an existing concept's label under a different name.
- **Fix:** A shared glossary and shared label keys per domain attribute.
- **Sources:** [Kaner et al., Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [Bolton: FEW HICCUPPS](https://developsense.com/blog/2012/07/few-hiccupps)

### DS-M4. Layout measured once doesn't update when content or container size changes
- **Bug:** An auto-growing textarea never shrinks after text is deleted; a virtual list keeps row heights measured for longer content; a popover keeps the width of its first long content. Charts have the same problem; see CH-D1 (persona-charts).
- **Cause:** Size read once in `onMounted` (`el.clientWidth`) with no ResizeObserver; height grown on input but never reset.
- **Try:** Collapse and expand the sidebar, resize the window, change browser zoom, and enter long content and then short content.
- **Spot:** `clientWidth` or `getBoundingClientRect` read in `onMounted` only; `style.height = scrollHeight + 'px'` without first resetting to `auto`.
- **Fix:** `useResizeObserver` (VueUse); reset height to `auto` before measuring `scrollHeight`.
- **Sources:** [Whittaker attacks (UAA CS 470 handout)](http://www.math.uaa.alaska.edu/~afkjm/cs470/handouts/breaking.pdf)

---

## N. Tooltips, popovers and menus

### DS-N1. Tooltip not hoverable, or no open delay
- **Bug:** Tooltips flicker on and off as the pointer crosses a table; the tooltip closes when the pointer moves onto it, so its text can't be read or selected.
- **Cause:** No open delay; content closes on trigger `mouseleave`.
- **Try:** Sweep the pointer across a dense table; move the pointer from the trigger onto the tooltip.
- **Spot:** Hand-made `@mouseenter`/`@mouseleave` tooltips; Reka `TooltipRoot` without a shared `TooltipProvider` delay.
- **Fix:** An open delay and skip delay through the provider; content stays while hovered (WCAG 1.4.13: hoverable and persistent).
- **Sources:** [WCAG 2.2 Understanding 1.4.13 Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html), [Reka UI: Tooltip](https://reka-ui.com/docs/components/tooltip)

### DS-N2. Tooltip can't be dismissed without moving the pointer
- **Bug:** A tooltip covers content and Esc does nothing. FM-B2 (persona-form-behaviour) covers Escape in popovers and selects.
- **Cause:** No Esc handler on hand-made tooltips; Esc handled by a parent dialog instead.
- **Try:** Hover or focus a trigger, then press Esc. Inside a dialog, check that Esc closes only the tooltip.
- **Spot:** Custom tooltip with no `keydown.esc`.
- **Fix:** Esc dismisses the tooltip only, without moving focus or closing the parent.
- **Sources:** [WCAG 2.2 Understanding 1.4.13 Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html)

### DS-N3. Tooltip on a disabled button never shows
- **Bug:** The "why is this disabled" tooltip never appears. Disabled buttons fire no pointer events and can't be focused.
- **Cause:** The tooltip trigger is the `disabled` button itself.
- **Try:** Hover and Tab to every disabled action that has an explanation.
- **Spot:** `<TooltipTrigger as-child><Button disabled>`.
- **Fix:** Wrap it in a `span tabindex="0"` trigger with `pointer-events: none` on the button (Reka's documented pattern), or use `aria-disabled`. See NV-Q1 (persona-url-state) for permission-gated actions.
- **Sources:** [Reka UI: Tooltip](https://reka-ui.com/docs/components/tooltip), [CSS-Tricks: Making disabled buttons more inclusive](https://css-tricks.com/making-disabled-buttons-more-inclusive/)

### DS-N4. Essential information only in a hover tooltip
- **Bug:** The price breakdown only shows on hover; on touch, it flashes during the press. DS-H10 covers hover-only controls.
- **Cause:** A tooltip used for content the user needs to decide.
- **Try:** On a phone or touch emulation, try to read every tooltip; with a screen reader, try to reach it.
- **Spot:** Tooltips holding prices, terms, or anything needed to complete the task.
- **Fix:** A toggletip (click to open, announced through `role="status"`, closes on Esc, outside click, or blur), with no interactive content inside; or show the information inline.
- **Sources:** [Inclusive Components: Tooltips and toggletips](https://inclusive-components.design/tooltips-toggletips/)

### DS-N5. Popover floats over unrelated content when its trigger scrolls away
- **Bug:** A row menu stays on screen after its row scrolls out of the table container.
- **Cause:** The floating element is positioned to a reference that is now clipped by a scroll container.
- **Try:** Open a row menu in a scrollable table, then scroll the table (not the page).
- **Spot:** Popovers in scroll containers with no hide-when-detached option.
- **Fix:** Hide the floating element when the reference is clipped (Floating UI `hide` middleware, `referenceHidden`). Whether the Reka prop is `hideWhenDetached` is not confirmed on the docs page read *(uncertain)*.
- **Sources:** [Floating UI: hide](https://floating-ui.com/docs/hide), [Reka UI: Popover](https://reka-ui.com/docs/components/popover)

### DS-N6. Submenu closes on diagonal pointer movement
- **Bug:** Moving from a parent item to its submenu crosses a sibling item, and the submenu closes.
- **Cause:** A hand-made submenu that opens on `mouseenter` of each item, with no grace area.
- **Try:** Open a submenu and move the pointer diagonally towards its lower items.
- **Spot:** Custom nested menus instead of the library's submenu primitive.
- **Fix:** A safe-triangle grace area; prefer the library submenu primitive over a hand-made one.
- **Sources:** [Smashing: Better context menus with safe triangles](https://www.smashingmagazine.com/2023/08/better-context-menus-safe-triangles/), [Reka UI: Dropdown Menu](https://reka-ui.com/docs/components/dropdown-menu)

### DS-N7. Hand-made menu with an incomplete keyboard pattern
- **Bug:** Arrows don't move between items; there is no type-ahead; Esc doesn't return focus to the trigger; Tab moves around inside the menu.
- **Cause:** A `div` list with click handlers instead of a menu primitive.
- **Try:** Keyboard only: open with Enter, Space, Down, and Up; move with arrows; type a letter; press Esc and Tab.
- **Spot:** `v-if="open"` lists of `@click` items with no `role="menu"` and no key handling.
- **Fix:** Follow the APG: Enter, Space, or Down opens on the first item, Up on the last; arrows move; printable characters jump; Esc closes and returns focus; Tab leaves and closes. Prefer Reka Dropdown Menu.
- **Sources:** [WAI-ARIA APG: Menu button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/), [WAI-ARIA APG: Menu and menubar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/)

### DS-N8. `role="menu"` used for site navigation
- **Bug:** Navigation links get app-style key handling that screen reader users don't expect; Space no longer scrolls.
- **Cause:** A menu primitive used for a list of links.
- **Try:** Screen reader and keyboard through the main and side navigation.
- **Spot:** `DropdownMenu` or `role="menu"`/`menuitem` wrapping router links in the nav.
- **Fix:** `<nav>` with lists of links, and the disclosure pattern for expandable groups.
- **Sources:** [Adrian Roselli: Don't use ARIA menu roles for site nav](https://adrianroselli.com/2017/10/dont-use-aria-menu-roles-for-site-nav.html), [WAI-ARIA APG: Disclosure navigation example](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/)

### DS-N9. Row menu state stays with the position, not the row
- **Bug:** After deleting a row from its menu, the menu reopens on the row that took its place.
- **Cause:** Open state keyed by index; Vue's in-place patch keeps DOM and component state at that position. Related to NV-L3 (persona-url-state).
- **Try:** Open a row menu, delete the row, and watch the next row. Also sort while a menu is open.
- **Spot:** `:key="index"` on rows; `openMenuIndex` refs.
- **Fix:** Key rows by ID; close the menu before the destructive action.
- **Sources:** [Vue: List rendering (key)](https://vuejs.org/guide/essentials/list.html)

---

## O. Platform preferences and input modes

### DS-O1. Reorder works by dragging only
- **Bug:** Priority lists can't be reordered without precise dragging, and nothing is announced.
- **Cause:** A drag-and-drop library with no single-pointer or keyboard alternative.
- **Try:** Reorder with the keyboard only, with a screen reader, and with one finger on touch.
- **Spot:** `draggable` lists with no up and down buttons and no keyboard handlers.
- **Fix:** Single-pointer alternatives (select, then up and down buttons) for WCAG 2.5.7; a keyboard grab mode (Space to grab, arrows to move, Esc to cancel) with live announcements ("2 of 4").
- **Sources:** [WCAG 2.2 Understanding 2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html), [Salesforce UX: 4 patterns for accessible drag and drop](https://medium.com/salesforce-ux/4-major-patterns-for-accessible-drag-and-drop-1d43f64ebf09)

### DS-O2. Reordered rows keep the wrong state, or the order reverts
- **Bug:** After a drag, a row's expanded state or input value stays at the old position. A failed save leaves the UI order different from the server order.
- **Cause:** `:key="index"`; no rollback on error.
- **Try:** Expand a row, drag it elsewhere; make the reorder request fail.
- **Spot:** `:key="index"` in draggable lists; optimistic reorder with no `onError`.
- **Fix:** Key by ID; optimistic reorder with rollback in `onError` and invalidate in `onSettled`.
- **Sources:** [Vue: List rendering (key)](https://vuejs.org/guide/essentials/list.html), [TanStack Query: Optimistic updates](https://tanstack.com/query/latest/docs/framework/vue/guides/optimistic-updates)

### DS-O3. Copying table rows gives junk text
- **Bug:** Selecting rows and pressing Cmd+C copies icon labels and button text; pasted into Excel, everything lands in one column. DS-F covers copy buttons.
- **Cause:** Div-based tables; decorative and action text is selectable.
- **Try:** Select three rows, copy, paste into Excel and into a plain-text editor.
- **Spot:** Grid layouts built from `div`s; action cells without `select-none`.
- **Fix:** Real `<table>` markup; `user-select: none` on decorative and action cells; a "Copy as CSV" action.
- **Sources:** [MDN: user-select](https://developer.mozilla.org/en-US/docs/Web/CSS/user-select)

### DS-O4. Multi-line paste into a single field isn't turned into rows
- **Bug:** Pasting 10 prefixes from a spreadsheet joins them into one value or keeps only the first. IN-B6 (persona-text-input) covers newlines in single-line fields; this is bulk entry.
- **Cause:** A single-line input with no paste handling on a field that is one of many rows.
- **Try:** Paste a column of 10 values copied from Excel, with and without a trailing newline and CRLF line endings.
- **Spot:** Repeating row inputs with no `@paste` handler.
- **Fix:** In `@paste`, read `clipboardData.getData('text')`; if it has several lines, offer to split it into rows.
- **Sources:** [MDN: paste event](https://developer.mozilla.org/en-US/docs/Web/API/Element/paste_event)

### DS-O5. Print or PDF view is broken or includes transient UI
- **Bug:** An invoice, order, or quote printout includes the nav, the "Quote saved" toast or status text, splits rows across pages, drops coloured status badges, prints link text only, and shows stale chart sizes.
- **Cause:** No `@media print` rules; browsers drop background colours by default; charts are not resized for the print page.
- **Try:** Print preview (and Save as PDF) every printable page straight after saving, with a toast visible.
- **Spot:** Printable views with no `print:` variants; toasts and banners without `print:hidden`; badges coloured only by background.
- **Fix:** `print:` variants to hide chrome, toasts, and status text; `break-inside: avoid`; `print-color-adjust: exact` on badges; print URLs after links; resize charts on `beforeprint`.
- **Sources:** [MDN: print-color-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/print-color-adjust), [Smashing: Print stylesheets in 2018](https://www.smashingmagazine.com/2018/05/print-stylesheets-in-2018/), [MDN: beforeprint event](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeprint_event), [MDN: @media print](https://developer.mozilla.org/en-US/docs/Web/CSS/@media#print)

### DS-O6. Forced colours mode removes state
- **Bug:** Focus rings drawn with `box-shadow` (Tailwind `ring`) vanish; selected tabs and checked custom controls shown only by background colour become indistinguishable; gradient backgrounds disappear.
- **Cause:** `box-shadow` is forced to `none` and author colours are replaced; ARIA roles don't change the system colours.
- **Try:** Windows High Contrast, or DevTools > Rendering > Emulate `forced-colors: active`. Tab through and check tabs, checkboxes, and badges.
- **Spot:** `focus:ring` with `outline-none` and no outline fallback; state shown only by `bg-*`.
- **Fix:** A transparent `outline` fallback; borders or icons for state; `forced-colors:` variants.
- **Sources:** [MDN: forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors)

### DS-O7. Dark mode gaps in native UI
- **Bug:** In the dark theme, scrollbars, native date pickers, and form controls stay light. DS-I4 covers logos only.
- **Cause:** No `color-scheme` set for the active theme; charts with hard-coded colours.
- **Try:** Switch to dark theme and open native selects, date inputs, and scrolling panels.
- **Spot:** A `dark` class toggle with no `color-scheme` change.
- **Fix:** Set `color-scheme` to match the active theme; theme charts from CSS variables.
- **Sources:** [MDN: color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)

### DS-O8. Reduced motion ignored
- **Bug:** Slide transitions, chart animation, and smooth scroll run with "Reduce motion" on; JS animations ignore a change mid-session.
- **Cause:** Animations not gated on `prefers-reduced-motion`; the media query read once.
- **Try:** Turn on Reduce motion (OS setting, or DevTools emulation) and use transitions, charts, and scroll-to links; toggle it with the page open.
- **Spot:** `transition-*` and `animate-*` with no `motion-safe:`; `scrollIntoView({ behavior: 'smooth' })`; chart `animation` options left on.
- **Fix:** `motion-safe:` and `motion-reduce:` variants; a `matchMedia` change listener for JS and chart animation.
- **Sources:** [web.dev: prefers-reduced-motion](https://web.dev/articles/prefers-reduced-motion)

### DS-O9. Wrong modifier key per platform
- **Bug:** The hint says Ctrl+K on Mac; the handler checks only `ctrlKey`, so Cmd+K does nothing. On Windows, `metaKey` is the Windows key.
- **Cause:** One modifier hard-coded for every platform.
- **Try:** Every shortcut on macOS and on Windows; read each hint.
- **Spot:** `e.ctrlKey && e.key === 'k'` with no `metaKey` branch; hard-coded "Ctrl" in hint text.
- **Fix:** `metaKey` on Mac, `ctrlKey` elsewhere; render the matching hint.
- **Sources:** [MDN: KeyboardEvent.metaKey](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/metaKey)

### DS-O10. Shortcut breaks on non-QWERTY layouts
- **Bug:** A shortcut bound with `event.code === 'KeyQ'` fires on the AZERTY A key; a hint shows the wrong letter.
- **Cause:** `code` (physical position) used where `key` (the character) was meant.
- **Try:** Switch the OS keyboard to AZERTY and QWERTZ and use every shortcut.
- **Spot:** `e.code === 'Key…'` for letter shortcuts.
- **Fix:** `key` for shortcuts that mean a letter, and `code` only for position-based controls.
- **Sources:** [MDN: KeyboardEvent.code](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code)

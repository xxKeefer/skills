# persona-value-display diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. A line marked `(rule N)` adds a case to that rule, and the numbered rules hold the other cases. The full case (cause, inputs, fix) is in the linked catalogue under the same ID.

## [persona-value-display catalogue](catalogue.md)

- DS-B3: `?? EMPTY_VALUE` (or a dash literal) on a string field the API can send as `""` or whitespace only → Shared helper: `value?.trim() ? value : placeholder` [default: nit] (rule 2)
- DS-B4: `name.split(' ')[1]` or `[0].toUpperCase()` on a name with no index guard, so a one-word name throws → Guard indexes; take the first grapheme safely [default: change-requested]
- DS-B5: `v-for` over a list with no `v-if="!items.length"` branch, or a new table with no `#empty` slot → Add the design system's empty-state component with a reason and next action [default: nit]
- DS-B12: `.join(', ')` with no `.filter(...)` for empty or nullish entries, or a hard-coded `', '` list separator → Filter empties, `Intl.ListFormat`, placeholder for an empty list [default: nit] (rule 1)
- DS-B14: `status === 'LIVE'` comparisons where the spec doesn't fix casing, or scattered `.toUpperCase()` on enum values → Normalise once at the API boundary, validate against the spec [default: nit] (rule 3)
- DS-C5: New count from `items.length` shown beside an API `total` or a cached count for the same list → One source of truth for each count [default: nit]
- DS-C7: `{{ count }}` or `.length` in a badge, a `#badge` slot or counter pill with no cap, or `n >= 99` → `n > 99 ? '99+' : n`, cap text in i18n [default: nit]
- DS-D3: `Math.round`, `toFixed` and `Intl` mixed for the same amount across screens → Show the server amount or set `roundingMode` explicitly [default: nit]
- DS-D4: `minimumFractionDigits: 2` hard-coded for every currency, or `toFixed(2)` on a unit rate → Let Intl set currency digits; separate precision for unit rates [default: nit] (rule 7)
- DS-D6: `'-' + format(Math.abs(x))` or `` `$${amount}` `` building a sign or symbol by hand → Intl sign handling or `currencySign: 'accounting'` in one `whitespace-nowrap` span [default: nit] (rule 7)
- DS-D8: Numeric ID typed as `number`, or byte totals summed on the client from API values → IDs as strings; aggregate on the server; compact display [default: nit] (rule 10)
- DS-D10: `Math.floor(mbps / 1000)`, or unit division with no `maximumFractionDigits` → Switch units on whole multiples or cap fraction digits [default: nit] (rule 8)
- DS-D16: Numeric `<td>` or column with no `text-right tabular-nums` → `text-right tabular-nums` on the cell and header [default: nit] (rule 10)
- DS-E12: `toLocaleDateString('en-US'`, `toLocaleString()` with no arguments, or a hard-coded `weekStartsOn` → vue-i18n `d()` with the app locale; week start from locale [default: nit] (rule 4)
- DS-E14: Hand-rolled `Math.floor(sec / 3600)` duration or countdown logic with no expired state → Tested duration helper, explicit expired state, i18n plurals [default: nit]
- DS-F3: `navigator.clipboard.writeText(x)` with no `await` or `catch`, then "Copied" shown regardless → Await, catch `NotAllowedError`, show failure, announce via `aria-live` [default: nit] (rule 11)
- DS-F4: `select-none` on a container holding IDs, or `@click` on a `<tr>` with no text-selection guard → Keep data selectable; ignore clicks when `getSelection()` is non-empty [default: nit]
- DS-F5: `&#8203;` or `<wbr>` inserted into an ID or value to allow line breaks → CSS `break-all` or `overflow-wrap`; copy from data [default: nit] (rule 11)
- DS-G1: `escape(…)` or `he.encode` applied before `{{ }}` interpolation, or API fields arriving with HTML entities → Store raw text; let Vue escape at render [default: nit]
- DS-G6: Free-text notes, description or config rendered in a `<p>` with no `whitespace-pre-line` or `whitespace-pre-wrap` → `whitespace-pre-line` for prose, `pre-wrap break-words` for config [default: nit]
- DS-G10: `uppercase` or `capitalize` class on a data value, or `.toUpperCase()` with no locale on a user name → Transform static labels only; `toLocaleUpperCase(locale)` [default: nit]
- DS-H1: Fixed `w-[600px]` or `min-w-[…]`, `whitespace-nowrap` on long rows, or a wide table with no own scroller, in a new layout with no `sm:` breakpoint → Fluid widths, `flex-wrap`, table-local `overflow-x-auto` [default: nit]
- DS-H3: Custom `absolute` popover inside an `overflow-*` or `transform` ancestor, or Reka `TooltipContent`/`PopoverContent`/`DropdownMenuContent` with no matching `*Portal` → Wrap content in the Reka `*Portal` with collision detection [default: nit]
- DS-H5: New `sticky top-0` header with no `scroll-pt-*` on its scroll container and no `scroll-mt-*` on anchor or focus targets → Add `scroll-pt-[header height]` on the scroller [default: nit]
- DS-H6: `sticky` element inside an `overflow-hidden` or `overflow-auto` wrapper, or a `sticky` grid child with no `self-start` → Move sticky out of the overflow wrapper; add `self-start` [default: nit]
- DS-H7: `overflow-scroll` on a panel or list, or a modal that toggles `overflow: hidden` on the body without reserving the gutter → `overflow-auto` and `scrollbar-gutter: stable` [default: nit]
- DS-H8: New scrollable dropdown, list, or modal panel (`overflow-y-auto`) with no `overscroll-contain` → Add `overscroll-contain` to the scrollable panel [default: nit]
- DS-H9: Dialog body with no `max-h-[…] overflow-y-auto`, `h-screen` instead of `h-dvh`, or `sticky`/`fixed` bars with no height media query → Scroll the dialog body and keep the actions visible [default: change-requested]
- DS-H11: `text-sm` or `text-xs` on an `<input>`, `<select>`, or `<textarea>` used on mobile, so iOS Safari zooms on focus → Use `text-base` on inputs at mobile widths [default: nit]
- DS-H12: Dialog buttons with no `min-w-*`, or count badges with no `min-w-[1.25rem]` and `text-center` → Set a minimum width on short buttons and badges [default: nit]
- DS-H14: `repeat(auto-fit, minmax(300px, 1fr))` or `grid-cols-[250px_1fr]` with no breakpoint, wider than a 320 px viewport → `minmax(min(100%, 300px), 1fr)` or add a breakpoint [default: nit]
- DS-I1: `<img :src="x.logoUrl">` with no `@error` handler or fallback, or a `:src` that can be empty or null → `@error` swaps to a placeholder; `v-if` on the URL [default: nit]
- DS-I2: `<img class="w-10 h-10">` or other fixed width and height with no `object-contain`/`object-cover` and no `max-w-full` → `object-contain` for logos, `object-cover` for photos, `max-w-full` [default: nit]
- DS-I3: New logo or avatar `<img :src>` with no `width`/`height`, no fixed `tw:size-*`/`tw:h-*` on it or its wrapper, no `tw:aspect-*` → Set `width`/`height` or a fixed size or aspect on the image box [default: nit]
- DS-I6: Icon inside a `flex` row beside text that can grow, with no `shrink-0` or `flex-none` → Add `shrink-0` to the icon [default: nit]
- DS-I7: `background-image`, `bg-[url(...)]` or `:style="{ backgroundImage }"` with no `tw:bg-no-repeat` → Add `tw:bg-no-repeat` with `tw:bg-cover` or `tw:bg-contain` [default: nit]
- DS-J1: New local `statusColors` or status-to-label map in a component where a shared status mapping already exists → Reuse the shared status mapping [default: nit]
- DS-J2: `text-right` on numeric `<td>` cells but not on the matching `<th>`, or a sort icon with no reserved space → Align header and cells the same; reserve sort icon space [default: nit]
- DS-J3: New table `columns` with no `width` where a cell's length changes on page, sort or load (badges, amounts), or raw `<table>` without `tw:table-fixed` → Set `width` on the stable columns, or `tw:table-fixed` [default: nit]
- DS-J4: `id: 'actions'` column without `stickyRight: true`, or a kebab beside a name binding in a flex row with no `tw:shrink-0` → `stickyRight: true` on the actions column, `tw:shrink-0` on the button [default: nit]
- DS-J7: Client search `x.name.toLowerCase().includes(q)` with no `trim()` or `normalize('NFD')` on `q`, or filtering the raw value of a formatted column → Reuse the project's search normalisation; match the displayed form [default: nit]
- DS-K2: `toast()` inside a `forEach` or a per-item `onSuccess`, toast markup outside the app provider, or a hand-made `fixed bottom-4 right-4` toast → One summary toast through the shared viewport [default: nit]
- DS-K3: `toast({ duration: 3000 })` on an error, an order ID or error reason shown only in a toast, or an Undo action inside a toast → Errors persist until dismissed; key details also on the page [default: nit]
- DS-K4: Toast provider or viewport mounted inside a route component, or a global alert store with no `router.afterEach` clearing and no context key → One app-level viewport; tag and clear messages by context [default: nit]
- DS-K6: Toast viewport `fixed bottom-0 right-0` on a page with a sticky footer or action bar, with no offset → Offset toasts clear of sticky action bars [default: nit]
- DS-L1: Template or computed reads `a.b.c` with no `?.` where `b` is nullable in the spec, `function f(x = {})` called with `null`, or `observe(el.value)` unguarded → Optional chaining with a display fallback [default: change-requested] (rule 12)
- DS-L6: `/ (max - min)` with no zero-range guard, or `Math.max(...values)`/`Math.min(...values)` on a possibly empty array → Guard zero range and handle empty and single-point cases [default: nit]
- DS-M1: `setQueryData` writing requested values into current fields, or success copy such as "updated" or "deleted" for an action the API marks pending or scheduled → Show current and pending values with the effective date [default: nit]
- DS-M2: Module-level `new Intl.NumberFormat(locale)` or date formatter, or values formatted inside a TanStack `select` or stored state → Format at render time, `computed` on the preference [default: nit]
- DS-M4: `clientWidth` or `getBoundingClientRect` read only in `onMounted`, or `style.height = scrollHeight + 'px'` with no reset to `auto` first → `useResizeObserver`; reset height to `auto` before measuring [default: nit]
- DS-N4: Tooltip content holding prices, terms, or other details the user needs to complete the task → Show it inline, or use a click-to-open toggletip [default: nit]
- DS-N5: Popover or row menu inside a scroll container with no hide-when-detached option → Hide the floating element when its reference is clipped [default: nit]
- DS-O3: Table built from `div` grid rows, or action and icon cells with no `select-none` → Real `<table>` markup; `select-none` on action cells [default: nit]
- DS-O4: Repeating row inputs (prefixes, VLANs, emails) with no `@paste` handler to split multi-line clipboard text → Split multi-line `clipboardData` text into rows in `@paste` [default: nit]
- DS-O5: Printable invoice, order, or quote view with no `print:` variants, toasts and banners with no `print:hidden`, or badges coloured only by background → Add `print:` variants and `print-color-adjust: exact` on badges [default: nit]
- DS-O9: `e.ctrlKey && e.key === 'k'` with no `metaKey` branch, or a hard-coded "Ctrl" in shortcut hint text → `metaKey` on Mac, `ctrlKey` elsewhere, with the matching hint [default: nit]
- DS-O10: `e.code === 'KeyQ'` or another `Key…` code used for a letter shortcut → Compare `e.key` for letter shortcuts [default: nit]

## [persona-text-input catalogue](../../persona-text-input/references/catalogue.md)

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-D10: Arithmetic on currency in a component, or `toFixed(2)` used to round money → Integer cents or a decimal library; show the server price [default: change-requested]

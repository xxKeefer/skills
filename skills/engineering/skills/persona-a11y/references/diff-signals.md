# persona-a11y diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-text-input catalogue](../../persona-text-input/references/catalogue.md)

- IN-J13: An input with a `placeholder` and no `<label>` or `aria-label` → Add a visible label; keep the placeholder as a format hint [default: nit] (rule 4)

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-A12: `<div @click>` or `<li @click>` used as a checkbox, radio or toggle; reimplemented radio cards with no key handling → Reka `Checkbox`/`RadioGroup`/`Switch` or native inputs [default: change-requested] (rule 1)
- FM-F4: `onSubmit` returns early on invalid with no `focus()` or `scrollIntoView` on the first error or summary → Focus the error summary or first invalid field [default: nit]
- FM-F5: Error `<p>` with no `id` linked from the input, or a static `aria-describedby` pointing to an error rendered with `v-if` → `:aria-invalid` plus `:aria-describedby` that tracks the error id [default: nit]
- FM-I9: Hard-coded `id="option-a"` or radio `name` literals in a reusable component rendered more than once → `useId()` or Reka `RadioGroup` [default: change-requested] (rule 12)
- FM-K2: `v-model:open` set from a menu item or table action with no `@close-auto-focus` handler → `@close-auto-focus` focuses a sensible element [default: nit]
- FM-K4: `tabindex="1"` or higher, or CSS `order`/`flex-direction: *-reverse` on interactive groups → DOM order matches visual order; `tabindex` 0 or -1 only [default: nit]
- FM-K5: `tabindex="-1"` on an icon-only clear or remove button, or `preventDefault()` on `Tab` in a keydown handler → Keep the button in Tab order; never trap Tab [default: nit] (rule 14)
- FM-K6: Panel hidden with `opacity-0`, `translate-*` or `max-h-0` that keeps focusable children, no `v-show`/`v-if`/`inert` → Hide with `v-if`, `v-show` or `inert` when collapsed [default: nit]
- FM-K7: `outline: none` or `tw:outline-none` with no `:focus-visible` replacement style → Add a visible `:focus-visible` style [default: nit]
- FM-K8: `<label>` with no `for`, a duplicated hard-coded `id`, or a placeholder used as the label → Use the design system's form-field component or `useId()` ids, with a visible label [default: nit] (rule 4)
- FM-O4: A `currentStep` ref change with no `document.title` update and no focus move to the step heading → Update the title and h1; move focus to the heading [default: nit]

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-F1: `@click="router.push(...)"` or `@click="goTo(row)"` on a table row, `<div>` or `<button>` that navigates → `<RouterLink>`, or `custom` slot rendering a real `<a>` [default: nit] (rule 2)
- NV-F2: `@click.prevent` plus `router.push` on an `<a :href>`, with no check of modifier keys → Use RouterLink `navigate`, or skip on modifier keys [default: nit]

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-H10: Row actions or copy button revealed by `opacity-0 group-hover:opacity-100` with no `group-focus-within:` reveal → Also reveal on `focus-within`; gate hover with `@media (hover: hover)` [default: nit]
- DS-I5: Status shown only as a coloured dot or badge with no text and no `sr-only` label → Add a text label or `sr-only` text [default: nit] (rule 10)
- DS-K5: `<div v-if="show" aria-live="polite">` inserted with its text, or `aria-live` on both the viewport and each toast → Always-present live region with `role="status"`, content injected later [default: nit]
- DS-K7: `autofocus` or `.focus()` in a toast component on mount, or toast actions with no keyboard route or hotkey hint → Never focus passive toasts; provide the viewport hotkey [default: nit]
- DS-N1: Hand-made `@mouseenter`/`@mouseleave` tooltip, or Reka `TooltipRoot` with no shared `TooltipProvider` delay → Use the provider delay; keep content open while hovered [default: nit]
- DS-N2: Custom tooltip with no `keydown.esc` handler, or Esc handled only by the parent dialog → Esc closes only the tooltip, focus stays put [default: nit]
- DS-N3: `<TooltipTrigger as-child><Button disabled>`, so the tooltip trigger is a disabled button → Wrap in a focusable `span tabindex="0"` trigger, or `aria-disabled` [default: nit] (rule 11)
- DS-N7: `v-if="open"` list of `@click` items with no `role="menu"` and no arrow, Esc, or type-ahead key handling → Use Reka Dropdown Menu [default: nit] (rule 5)
- DS-N8: `DropdownMenu` or `role="menu"`/`menuitem` wrapping router links in site navigation → `<nav>` with link lists and a disclosure for groups [default: nit]
- DS-O1: `draggable` list or drag-and-drop reorder with no up and down buttons and no keyboard handlers → Add move up and down buttons and a keyboard grab mode [default: change-requested] (rule 14)
- DS-O6: `focus:ring` with `outline-none` and no outline fallback, or selected or checked state shown only by `bg-*` → Transparent `outline` fallback; borders or icons for state [default: nit]
- DS-O8: `transition-*` or `animate-*` with no `motion-safe:`, `scrollIntoView({ behavior: 'smooth' })`, or chart animation left on → `motion-safe:` variants and a `matchMedia` change listener [default: nit]

## [persona-file-upload catalogue](../../persona-file-upload/references/catalogue.md)

- UP-B6: `<input type=file class="hidden">` (or `display:none`) opened by `@click="input.click()"` on a `<div>` or `<span>` → Visually hidden focusable input, or a real `<button>` trigger [default: change-requested] (rule 1)

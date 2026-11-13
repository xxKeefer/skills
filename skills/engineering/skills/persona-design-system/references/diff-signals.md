# persona-design-system diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-text-input catalogue](../../persona-text-input/references/catalogue.md)

- IN-C11: Fixed-height rows, avatar labels or chips showing user text with no `overflow: hidden` → Clip user-text containers with `overflow: hidden` [default: nit]

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-A1: New `{{ name }}`, `{{ email }}`, `{{ url }}` or UID in a fixed-width, grid or flex child with no `break-words`, `break-all` or `truncate` → `break-words` for prose, `break-all` for IDs, or `truncate` with tooltip [default: nit] (rule 15)
- DS-A2: `truncate` inside a flex child or `flex-1` with no `min-w-0` on each flex ancestor; grid `1fr` instead of `minmax(0,1fr)` → Add `min-w-0` up the chain, `shrink-0` on icons and buttons [default: nit] (rule 13)
- DS-A3: `truncate` or `line-clamp-*` with no `:title`, no the design system's tooltip or tooltip directive, and the full text shown nowhere else → a truncation-detection helper plus the design system's tooltip, or always set `:title` [default: nit] (rule 14)
- DS-A4: Tooltip bound unconditionally around a `truncate` span, with no overflow check such as `useIsTruncated` → Show the tooltip only when `useIsTruncated` reports overflow [default: nit] (rule 14)
- DS-A5: `truncate` on a toast body, alert, `<label>`, `<h1>`, `FormMessage` or dialog description → Let errors, labels, titles and notifications wrap [default: nit] (rule 16)
- DS-A6: End `truncate` on a UID, file path, serial or AWS account ID column, where values differ only at the end → Middle-truncate, or show a short ID with a copy button [default: nit] (rule 14)
- DS-A9: `line-clamp-*` with `py-*` or a `flex` display on the same element; a "Show more" gated on `text.length > N` → Pad a wrapper; toggle on `scrollHeight > clientHeight` [default: nit]
- DS-A10: New `<table>` or column with no `overflow-x-auto` wrapper, or long cells with no `max-w-*` plus `truncate` or `break-words` → Wrap in `overflow-x-auto`, cap long cells, consider `table-fixed` [default: nit]
- DS-A11: `w-24`, `w-[120px]` or `h-8` with `whitespace-nowrap` on a button, tab, badge or header holding `t()` text → Use `min-w-*`, allow wrapping, `hyphens-auto` with `lang` [default: nit]
- DS-A12: `SelectTrigger` or `ComboboxInput` with no `truncate` on `SelectValue`; `SelectContent` with no `max-h-*`, `overflow-y-auto` or trigger-width binding → Truncate the value with a title, cap content height and width [default: nit]
- DS-A13: Breadcrumb `v-for` with no per-crumb `truncate` or `max-w-*` and no collapse of middle crumbs → `max-w-[12rem] truncate` per crumb, collapse the middle ones [default: nit]
- DS-A14: `DialogTitle` in `flex justify-between` without `min-w-0 break-words`; close icon without `shrink-0`; `useTitle` with the generic suffix first → `break-words` on titles, `shrink-0` on controls, specific name first [default: nit]
- DS-A15: `flex justify-between` row with a label and value and no `gap-*` → Add `gap-2` [default: nit] (rule 13)
- DS-A16: New `flex` container of a variable number of chips or buttons with no `flex-wrap` → Add `flex-wrap gap-2` [default: nit]
- DS-A17: Fixed `h-12` or `h-[...]` on a text container, especially with `overflow-hidden` → Use `min-h-*` instead of `h-*` [default: nit]
- DS-A18: `flex` row holding a badge, avatar or icon with no `items-center`, `items-start` or `self-*` → `items-start` or `items-center`; `self-start` on badges [default: nit]
- DS-A19: Text absolutely positioned over an `<img>` with no gradient overlay or `bg-*` fallback colour → Add a gradient overlay and a fallback `bg-*` [default: nit]
- DS-G7: `whitespace-pre` with no `overflow-x-auto` and no `pre-wrap` → `whitespace-pre-wrap break-words`, or a scroll container [default: nit]
- DS-G9: Fixed `h-*` row or cell holding user text that may contain emoji or unusual glyphs → Use `min-h-*`; add a system emoji font to the stack [default: nit]
- DS-H2: Text sized or boxed in px: `text-[13px]`, `leading-[18px]`, or a fixed `h-[32px]` box holding text with `overflow-hidden` → Rem-based Tailwind sizes and `min-h` instead of fixed height [default: nit] (rule 7)
- DS-H4: New arbitrary `z-[9999]` or `z-*` off the scale, a dialog with `transform` classes, or portalled content missing the layer token → Use the documented z-index scale for portalled layers [default: change-requested] (rule 7)
- DS-H13: Arbitrary CSS variable value with no fallback, such as `bg-[var(--brand)]` or `var(--x)` in a style binding → Use a token utility, or `var(--x, fallback)` [default: nit] (rule 7)
- DS-H15: `tw:flex` row with `tw:justify-between` or `tw:ml-auto` and no `tw:gap-*`, one child a dynamic `{{ }}` title and the other an icon or button → Add `tw:gap-*` on the row [default: nit]
- DS-N6: Custom nested menu opening submenus on each item's `mouseenter`, instead of the library submenu primitive → Use the Reka submenu primitive with its grace area [default: nit] (rule 3)
- DS-O7: A `dark` class toggle with no matching `color-scheme` change, or charts with hard-coded colours → Set `color-scheme` per theme; theme charts from CSS variables [default: nit]

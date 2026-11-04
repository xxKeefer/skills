# persona-security diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-text-input catalogue](../../persona-text-input/references/catalogue.md)

- IN-G1: Any `v-html`, `innerHTML`, `insertAdjacentHTML` or `h('div', { innerHTML })` on API, query or user text → Use `{{ }}`; sanitise with DOMPurify if HTML is needed [default: change-requested] (rule 2)
- IN-G2: `marked(...)` or `markdown-it` output bound through `v-html` → Turn off raw HTML, sanitise output, restrict URL schemes [default: change-requested] (rule 2)
- IN-G5: `:href="user.url"` or `:src` bound to user-supplied data with no scheme check → Parse with `new URL()`; allow only `http:`, `https:`, `mailto:` [default: change-requested]
- IN-H1: `rows.map(r => r.join(',')).join('\n')`, `Blob([csv], { type: 'text/csv' })` or `papaparse.unparse` with no leading `=`, `+`, `-`, `@` neutralising → Prefix dangerous leading characters with `'` [default: change-requested] (rule 8)

## [persona-url-state catalogue](../../persona-url-state/references/catalogue.md)

- NV-A10: `query: { token }`, `?email=` on a list filter, or a one-time reset code left in the URL with no `router.replace` after use → Keep secrets out of the URL; replace one-time params away [default: change-requested]
- NV-E2: `window.location.href = route.query.redirect`, or `router.push(route.query.redirect)` with no check → Accept only same-origin paths starting with a single `/` [default: nit] (rule 6)
- NV-F4: External URL routed through `RouterLink`, or `window.open(url)` with no `noopener` feature → Plain `<a target="_blank" rel="noopener noreferrer">` for external links [default: nit] (rule 1)
- NV-I10: `v-html="name.replace(term, '<mark>$&</mark>')"` to highlight a search match → Render text segments with `<mark>` in the template [default: change-requested] (rule 2)

# persona-form-behaviour catalogue: forms, keyboard and validation

Scope: a Vue 3 and TypeScript single-page app (SPA) built on Reka UI primitives, vue-router, TanStack Query, and vue-i18n. Each item has an ID, a short name, and six parts:

- **Bug**: what the user sees
- **Cause**: the root cause in code
- **Test**: concrete steps and inputs
- **Spot**: the code pattern to look for in a diff review
- **Fix**
- **Src**: sources (where one exists)

Claims marked **[verify]** are uncertain or vary between browsers. Test them before you rely on them.

## Key sources (referenced by tag below)

| Tag | Source |
| --- | --- |
| [HTML-IS] | WHATWG HTML, implicit submission: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission |
| [HTML-ML] | WHATWG HTML, maxlength / "suffering from being too long" (user edits only): https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#attr-fe-maxlength |
| [HTML-BTN] | WHATWG HTML, `button` type: missing/invalid default is "Auto", which acts as submit unless it has `command`/`commandfor` or sits in a `select`: https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-type |
| [HTML-ENTRY] | WHATWG HTML, constructing the entry list (disabled controls skipped): https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#constructing-the-form-data-set |
| [MDN-NUM] | MDN `<input type=number>` (step defaults to 1, invalid chars vary by browser, a11y caveats): https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number |
| [MDN-DATEPARSE] | MDN Date.parse (date-only ISO = UTC, date-time without zone = local): https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Date/parse |
| [MDN-LEN] | MDN String.length (UTF-16 code units; use Intl.Segmenter for graphemes): https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/length |
| [MDN-BU] | MDN beforeunload: https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event |
| [MDN-COMP] | MDN KeyboardEvent.isComposing: https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing |
| [VUE-FORMS] | Vue forms guide (`.number` returns the raw string if parseFloat fails, `''` when empty; `.trim`, `.lazy`): https://vuejs.org/guide/essentials/forms.html#modifiers |
| [VUE-2598] | vuejs/core #2598 (`.number` turns "12abc" into 12, by design): https://github.com/vuejs/core/issues/2598 |
| [VR-GUARDS] | vue-router navigation guards / onBeforeRouteLeave: https://router.vuejs.org/guide/advanced/navigation-guards.html |
| [TQ-MUT] | TanStack Query Vue mutations (`isPending`, `mutate` versus `mutateAsync`): https://tanstack.com/query/latest/docs/framework/vue/guides/mutations |
| [REKA-DIALOG] | Reka UI Dialog (Esc closes, focus returns to trigger, `pointer-down-outside` preventable): https://reka-ui.com/docs/components/dialog |
| [REKA-NUM] | Reka UI NumberField: https://reka-ui.com/docs/components/number-field |
| [REKA-DATE] | Reka UI DateField/DatePicker (uses `@internationalized/date`): https://reka-ui.com/docs/components/date-picker |
| [GOVUK-VAL] | GOV.UK Design System, validation pattern (validate on submit, keep answers, prefix `<title>` with "Error:", summary + focus, ignore stray spaces/dashes, always validate server-side): https://design-system.service.gov.uk/patterns/validation/ |
| [GOVUK-ES] | GOV.UK error summary (move focus to it, links to fields, same wording as inline): https://design-system.service.gov.uk/components/error-summary/ |
| [GOVUK-NUM] | GOV.UK blog, "Why the GOV.UK Design System team changed the input type for numbers" (2020): https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/ |
| [BAYMARD-IV] | Baymard, inline form validation (avoid premature validation, clear errors on keystroke once fixed, positive validation): https://baymard.com/blog/inline-form-validation |
| [NNG-ERR] | NN/g, 10 design guidelines for reporting errors in forms: https://www.nngroup.com/articles/errors-forms-design-guidelines/ |
| [ROSELLI-DIS] | Adrian Roselli, "Don't Disable Form Controls" (2024, updated 2026): https://adrianroselli.com/2024/02/dont-disable-form-controls.html |
| [SMASH-A11Y] | Smashing Magazine, "A Guide To Accessible Form Validation" (2023): https://www.smashingmagazine.com/2023/02/guide-accessible-form-validation/ |
| [WCAG-331] | WCAG 2.2 SC 3.3.1 Error Identification: https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html |
| [WCAG-333] | WCAG 2.2 SC 3.3.3 Error Suggestion: https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html |
| [WCAG-332] | WCAG 2.2 SC 3.3.2 Labels or Instructions: https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html |
| [WCAG-337] | WCAG 2.2 SC 3.3.7 Redundant Entry: https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html |
| [WCAG-413] | WCAG 2.2 SC 4.1.3 Status Messages: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html |
| [WCAG-243] | WCAG 2.2 SC 2.4.3 Focus Order: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html |
| [APG-DIALOG] | WAI-ARIA APG modal dialog pattern (focus in, trap, Esc, return focus): https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ |
| [APG-COMBO] | WAI-ARIA APG combobox pattern (Enter accepts the focused option): https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ |
| [APG-CHECK] | WAI-ARIA APG checkbox (mixed state): https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/ |
| [IME-WEBKIT] | WebKit bug 165004 (Safari fires keydown after compositionend, so `isComposing` is false on the confirming Enter): https://bugs.webkit.org/show_bug.cgi?id=165004 |
| [IME-AZUKI] | azukiazusa, "IME Enter submit" write-up: https://azukiazusa.dev/en/blog/ime-enter-submit |
| [AMEX-LEN] | American Express, "Character counts: why 30 characters max is usually wrong": https://americanexpress.io/character-counts-why-30-characters-max-is-usually-wrong/ |
| [WHEEL] | Number-input wheel behaviour: Mozilla bug 1261674 https://bugzilla.mozilla.org/show_bug.cgi?id=1261674 ; makandra "Better numeric inputs in desktop browsers" https://makandracards.com/makandra/505751-better-numeric-inputs-in-desktop-browsers ; Angular components #31372 https://github.com/angular/components/issues/31372 |
| [HEND] | Elisabeth Hendrickson, Test Heuristics Cheat Sheet (data type attacks): https://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf (the TLS certificate failed when fetched; see also the MoT discussion https://club.ministryoftesting.com/t/what-would-you-change-and-or-add-to-the-test-heuristics-cheat-sheet/52669) |
| [BVA] | Boundary value analysis / equivalence partitioning: https://www.educative.io/answers/what-is-equivalence-class-partitioning-boundary-value-analysis |

---

## A. Enter key and implicit submission

### FM-A1. Enter in a single-field form submits with no handler wired
- **Bug**: A filter or search box inside a `<form>` reloads the page (full navigation to `?q=...`), which wipes SPA state, or it fires a submit the developer never intended.
- **Cause**: The HTML spec submits a form implicitly on Enter when it has a default (first) submit button, **or** when it has no submit button and only one field that blocks implicit submission (text, search, tel, url, email, password, date, month, week, time, datetime-local, number) [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission). There is no `@submit.prevent`.
- **Test**: Focus the field, type `abc`, press Enter. Watch the Network panel for a document request and the URL for a `?` query string. Repeat with a second text field added, which should stop the submit when there is no button.
- **Spot**: A `<form>` with no `@submit.prevent`. Search or filter inputs wrapped in `<form>` purely for layout. Behaviour that changes when a second field is added or removed.
- **Fix**: Always write `<form @submit.prevent="onSubmit" novalidate>`. If the wrapper is not a real form, use a `<div role="search">` or a `<search>` element instead of `<form>`.
- **Src**: [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission)
- **In the design system**: Check whether the form component renders a native `<form @submit.prevent>`, so Enter in a field submits only if the form holds a submit button. `@keydown.enter` on a design-system input may never fire if the input re-emits `keydown` (see IN-A1 (persona-text-input)); use `@keyup.enter` or the form submit.

### FM-A2. A `<button>` with no `type` inside a form submits it
- **Bug**: Clicking "Add row", "Show password", "Clear", a stepper `+`, or a tab/accordion header inside a form submits the form. Pressing Enter in any text field "clicks" the first such button, so Enter adds a row instead of saving.
- **Cause**: A `button` whose `type` is missing or invalid is in the Auto state, which acts as **submit** (unless it has `command`/`commandfor` or sits inside a `select`) [HTML-BTN](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-type). Implicit submission fires a click on the **first submit button in tree order** [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission).
- **Test**: In every form, press Enter in the first text field and confirm which action fires. Click every non-primary button and check the Network panel for a submit.
- **Spot**: `<button @click=...>` with no `type`. A custom `Button.vue` that does not default `type="button"` or does not forward `type`. Reka `*Trigger` components rendered `as-child` onto a native `<button>` inside a form.
- **Fix**: Default `type="button"` in the design-system `Button` and add `type="submit"` explicitly on the primary action. Add a lint rule (`vue/html-button-has-type`).
- **Src**: [HTML-BTN](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-type), [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission), eslint-plugin-vue rule https://eslint.vuejs.org/rules/html-button-has-type.html
- **In the design system**: Inside the form, every button that is not the submit action needs `type="button"`.

### FM-A3. The wrong default button: Enter triggers "Delete" or "Back"
- **Bug**: Enter in a field fires the first button in DOM order, such as Cancel/Back/Delete that was placed before Save for visual layout.
- **Cause**: The default button is the first submit button in tree order [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission). CSS `flex-direction: row-reverse` or `order` changes the visual order, not the tree order.
- **Test**: On each form, press Enter in each field type. Record which handler runs.
- **Spot**: Footer markup with the secondary action first. `row-reverse` on button groups.
- **Fix**: Make only the primary action `type="submit"` and every other button `type="button"`. Do not rely on DOM order.
- **Src**: [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission)

### FM-A4. Enter in a combobox, select, or autocomplete submits the parent form
- **Bug**: The user arrows to an option in a Combobox/Autocomplete and presses Enter to pick it. The option is picked **and** the form submits, sometimes with the previous value.
- **Cause**: The keydown handler selects the item but does not `preventDefault()`. Or the list is closed or empty (no highlighted item), so Enter falls through to implicit submission. A custom typeahead built on a plain `<input>` inside a `<form>` is the usual offender. APG says Enter accepts the focused option [APG-COMBO](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). It does not say Enter submits the form.
- **Test**: For every combobox in a form: (1) open it, arrow to an option, press Enter; (2) type text that matches nothing and press Enter; (3) type and press Enter before the async results arrive; (4) with the list closed, press Enter.
- **Spot**: `@keydown.enter="select(highlighted)"` with no `.prevent`. Hand-rolled dropdowns. Reka `ComboboxInput` inside `<form>` where the case with no item highlighted is not handled. **[verify]**: check whether Reka prevents default when nothing is highlighted in the version in use.
- **Fix**: `@keydown.enter.prevent` while the list is open. Decide on purpose whether Enter with the list closed should submit, and test it.
- **Src**: [APG-COMBO](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/), [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission)

### FM-A5. Enter in a textarea submits, or Enter in an input inserts nothing but a chat-style input is expected to submit
- **Bug**: A global `@keydown.enter` handler on the form submits when the user wants a newline in a description/notes textarea. The reverse also happens: a multi-line "comment" field gets no Ctrl/Cmd+Enter submit even though the UI hints at one.
- **Cause**: Implicit submission does not apply to textarea, but a custom form-level keydown listener does. Inconsistent shortcut handling.
- **Test**: In each textarea, press Enter, Shift+Enter, Ctrl+Enter, and Cmd+Enter. Check whether you get a newline or a submit.
- **Spot**: `@keydown.enter` on `<form>` or a wrapper `<div>`. `@keyup.enter` (fires after the newline is already inserted).
- **Fix**: Scope Enter handlers to the specific input. For Ctrl/Cmd+Enter use `@keydown.enter.exact.ctrl` / `.meta` (or `.exact` plus a platform check) and call `form.requestSubmit()` so validation runs.
- **Src**: Vue key modifiers https://vuejs.org/guide/essentials/event-handling.html#key-modifiers

### FM-A6. Enter during IME composition submits half-composed text

See IN-A1 (persona-text-input), IN-A2 (persona-text-input).

### FM-A7. Enter inside a modal submits the parent page form instead of the modal action
- **Bug**: A confirm dialog opened from within a form: Enter in the dialog's input submits the **outer** form, or does both.
- **Cause**: The dialog content is rendered as a DOM child of the outer `<form>` (no teleport), so its inputs belong to the outer form. Or a nested `<form>` was written inside a `<form>`, which is invalid HTML; the parser drops the inner `<form>` tag on the server-rendered parse, and in client-rendered Vue the nesting behaves unpredictably **[verify]**.
- **Test**: Open each dialog launched from a form page. Press Enter in each dialog field and on each dialog button. Confirm that only the dialog action fires.
- **Spot**: `<form>` inside a component that is placed inside another `<form>`. `DialogPortal` missing or disabled. The dialog's buttons lack `type`.
- **Fix**: Teleport dialogs (Reka `DialogPortal`). Give the modal its own `<form @submit.prevent>`. Never nest forms. Use the `form="id"` attribute if a control has to live outside its form.
- **Src**: HTML content model for `form` (no form descendants): https://html.spec.whatwg.org/multipage/forms.html#the-form-element

### FM-A8. Enter on a focused button activates it, and keyup triggers a second action
- **Bug**: Pressing Enter on "Open dialog" opens it, then the same keypress confirms the dialog's autofocused primary button, or a list row activates twice.
- **Cause**: A handler on `keyup` instead of `keydown`, or a `keydown` that changes focus to another activatable element whose activation fires on keyup (Space activates on keyup; Enter activates on keydown) **[verify per browser]**.
- **Test**: Keyboard only: Tab to the trigger, press Enter, then Space. Check that the dialog opens once and nothing is confirmed.
- **Spot**: `@keyup.enter`, `@keyup.space`. Autofocus on a destructive confirm button.
- **Fix**: Use `click` for activation. Autofocus the least destructive control in confirm dialogs [APG-DIALOG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
- **Src**: [APG-DIALOG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

### FM-A9. Enter submits a form while a required async lookup is still running
- **Bug**: The user types a value (such as a service key or a VLAN availability check), presses Enter before the debounced check resolves, and the stale "valid" state lets the submit through.
- **Cause**: The submit path reads the last validation result instead of awaiting pending validators. Debounce is not flushed on submit.
- **Test**: Type a known-bad value and press Enter within 100 ms. Throttle the network to Slow 3G.
- **Spot**: `useDebounceFn` validators. `isValid` computed from the last resolved result. No `await validate()` in `onSubmit`.
- **Fix**: On submit, flush the debounce and await all async validators. Treat "pending" as not valid.
- **Sources:** [vee-validate: Handling forms](https://vee-validate.logaretm.com/v4/guide/composition-api/handling-forms/), [vee-validate: useForm API](https://vee-validate.logaretm.com/v4/api/use-form/)

### FM-A10. Ctrl/Cmd+Enter bypasses validation
- **Bug**: A shortcut submits invalid data because it calls the API directly.
- **Cause**: `@keydown.meta.enter="save()"` calls the mutation, skipping the form's validate-then-submit path.
- **Test**: Leave a required field empty and press Cmd+Enter.
- **Spot**: Shortcut handlers calling `mutate` directly.
- **Fix**: Shortcuts call `formEl.requestSubmit()` (fires the submit event and constraint validation) or the same `onSubmit` function.
- **Src**: MDN requestSubmit https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit

### FM-A11. `form.submit()` used programmatically skips the submit event and validation
- **Bug**: A save skips validation and the `@submit` handler, or causes a full page navigation.
- **Cause**: `HTMLFormElement.submit()` does not fire `submit` and does not validate. `requestSubmit()` does both.
- **Spot**: `formRef.value.submit()`.
- **Fix**: `requestSubmit()`.
- **Src**: MDN requestSubmit (above)
- **Sources:** [MDN: HTMLFormElement.submit()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/submit)

### FM-A12. Space and Enter do not toggle custom controls
- **Bug**: A clickable `<div>` "checkbox", card-select, or toggle cannot be operated from the keyboard, or Enter submits the form instead of toggling.
- **Cause**: A `div @click` with no role, tabindex, or key handling. Native checkboxes toggle on Space, not Enter.
- **Test**: Tab to each custom control and press Space and Enter.
- **Spot**: `<div @click>` / `<li @click>` as controls. Reimplemented radio cards.
- **Fix**: Use Reka `Checkbox`/`RadioGroup`/`Switch`/`ToggleGroup`, or native inputs with styled labels.
- **Src**: [APG-CHECK](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/)

---

## B. Escape and dismissal

### FM-B1. Escape (or an outside click) closes a dialog and silently discards typed data
- **Bug**: The user fills a 10-field "Edit service" dialog, presses Esc or clicks the overlay by accident, and everything is lost.
- **Cause**: Reka Dialog closes on Esc and outside interaction by default [REKA-DIALOG](https://reka-ui.com/docs/components/dialog). There is no dirty check in `@escape-key-down` / `@pointer-down-outside` / `@interact-outside`, and no `update:open` guard.
- **Test**: Type in a dialog field, then press Esc, click the overlay, and press browser Back. Each should keep the data or ask for confirmation.
- **Spot**: `<DialogContent>` wrapping form fields with no `@escape-key-down` / `@interact-outside` handlers. `v-model:open` bound directly to a ref with no guard.
- **Fix**: When dirty, call `event.preventDefault()` in those handlers and show a "Discard changes?" confirmation. Alternatively, keep the draft in state so reopening restores it.
- **Src**: [REKA-DIALOG](https://reka-ui.com/docs/components/dialog), Radix Dialog API (`onEscapeKeyDown`, `onInteractOutside` preventable) https://www.radix-ui.com/primitives/docs/components/dialog#content

### FM-B2. Escape in a nested popover, select, or combobox also closes the dialog
- **Bug**: The user presses Esc to close a Select dropdown inside a dialog, and the whole dialog closes with it.
- **Cause**: Reka/Radix layers form a stack and are meant to dismiss one at a time. A non-Reka widget (third-party date picker, hand-rolled dropdown listening on `document`) does not take part in that stack, so the dialog also sees the Esc. Two Reka instances from **different copies** of the library (duplicate dependency) also do not share the stack **[verify]**.
- **Test**: In every dialog, open each popover, select, combobox, date picker, and tooltip, then press Esc once. Only the topmost layer should close. Press Esc again and the dialog closes.
- **Spot**: `document.addEventListener('keydown', ...)` in a dropdown. Third-party pickers inside `DialogContent`. Duplicate `reka-ui` versions in the lockfile.
- **Fix**: Build overlays from Reka primitives. For foreign widgets, `stopPropagation` the Esc keydown while they are open, or call `preventDefault` in the dialog's `@escape-key-down` when a child is open.
- **Src**: Radix DismissableLayer behaviour (nested layers dismiss one at a time) https://www.radix-ui.com/primitives/docs/utilities/dismissable-layer (**[verify]** the page still exists), [REKA-DIALOG](https://reka-ui.com/docs/components/dialog)

### FM-B3. Escape clears the input as well as closing the list
- **Bug**: Esc in a search combobox clears the typed query and closes the list. The user expected only the list to close (or expected Esc to clear first, then close).
- **Cause**: Inconsistent Esc semantics between components.
- **Test**: Type `syd`, open the suggestions, press Esc, then press Esc again.
- **Spot**: An Escape branch (`@keydown.esc`, `key === 'Escape'`) in a combobox or autocomplete that sets the query to `''` and closes the list in the same step.
- **Fix**: Follow APG: Esc closes the popup first. A second Esc may clear the field [APG-COMBO](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/).
- **Src**: [APG-COMBO](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/)

### FM-B4. Escape during IME composition closes the dialog
- **Bug**: CJK users press Esc to cancel a conversion and the dialog closes.
- **Cause**: An Esc handler that does not check `isComposing` **[verify Reka behaviour]**.
- **Test**: Use the Japanese IME inside a dialog input: type, then press Esc.
- **Spot**: An Escape handler (`@escape-key-down`, `@keydown.esc`, `key === 'Escape'`) in a dialog or popover holding text inputs, with no `e.isComposing || e.keyCode === 229` early return.
- **Fix**: Guard with `e.isComposing`.
- **Sources:** [MDN: KeyboardEvent.isComposing](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing), [Quinn: Preventing Esc from closing dialogs during IME composition](https://quinn.bearblog.dev/preventing-esc-from-closing-dialogs-during-ime-composition/)

### FM-B5. Confirmation dialog "Cancel" or Esc still performs the action
- **Bug**: "Are you sure you want to delete?" fires the delete when the user presses Esc or Cancel.
- **Cause**: The action runs in `@update:open` / `@close` regardless of which button was used. Or a custom `confirm()` returns a Promise that resolves `undefined` on dismissal, and the code checks `result !== false` instead of `result === true`, so anything other than `false` counts as consent (`undefined` itself is falsy).
- **Test**: Open each confirm dialog, then press Esc, click the overlay, click Cancel, and press Enter.
- **Spot**: The action called inside an `onClose`/`watch(open)` handler. A `useConfirm()` promise with an ambiguous result.
- **Fix**: Run the action only from the explicit confirm button. Resolve `false` on every dismissal path.
- **Sources:** [MDN: Falsy](https://developer.mozilla.org/en-US/docs/Glossary/Falsy)

### FM-B6. Browser Back while a dialog is open navigates away and loses the form
- **Bug**: On mobile or with a Back mouse button, a dialog form is lost along with the page.
- **Cause**: The dialog is not tied to history, and there is no route-leave guard for its dirty state.
- **Test**: Open the dialog, type, press Back.
- **Spot**: A dialog form with a dirty check on Escape or outside click (`no-backdrop-dismiss`, `@escape-key-down`) but no `onBeforeRouteLeave` covering the same dirty state.
- **Fix**: Either push a history entry or query param for the dialog, or add the dialog's dirty state to `onBeforeRouteLeave`.
- **Src**: [VR-GUARDS](https://router.vuejs.org/guide/advanced/navigation-guards.html)

---

## C. Double submit, pending and retry

### FM-C1. Double-click or Enter mashing creates duplicate resources
- **Bug**: Two orders are created, or the user is charged twice.
- **Cause**: The submit handler is not gated on `mutation.isPending`. A `disabled` binding updates on the next render, so a fast double-click can land before it. Enter is not blocked by a button's `disabled`; implicit submission does nothing if the default button is disabled [HTML-IS](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission), but a custom `@keydown.enter` handler is not blocked.
- **Test**: Double-click Submit. Triple-press Enter in a field. Throttle to Slow 3G and click Submit 5 times. Count POSTs in the Network panel.
- **Spot**: `async onSubmit() { await api.create(...) }` with no `if (isPending) return`. `:disabled="loading"` where `loading` is set after an `await`.
- **Fix**: A synchronous guard at the top of the handler (`if (mutation.isPending.value) return`). Set the flag before the first `await`. Send an idempotency key to the server. Roselli: guard against double submit on the back end as well [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html).
- **Src**: [TQ-MUT](https://tanstack.com/query/latest/docs/framework/vue/guides/mutations), [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html)

### FM-C2. Submit stays disabled forever after an error
- **Bug**: After a 500 or a validation error from the API, the button stays disabled or spinning and the user has to reload.
- **Cause**: `loading = true; await post(); loading = false` with no `try/finally`. `mutateAsync` throws and the code after it never runs.
- **Test**: Force a 500 or 422 (DevTools request blocking or mock), then fix the field and resubmit.
- **Spot**: A manual loading flag with no `finally`. `await mutateAsync()` with no `try/catch`.
- **Fix**: Use the `isPending` that `useMutation` exposes, or `try { } finally { loading = false }`.
- **Src**: [TQ-MUT](https://tanstack.com/query/latest/docs/framework/vue/guides/mutations)

### FM-C3. `mutateAsync` without a catch causes an unhandled rejection and no user feedback
- **Bug**: Nothing happens on error, apart from a console error.
- **Cause**: `mutateAsync` returns a rejecting promise. `mutate` routes errors to `onError` instead [TQ-MUT](https://tanstack.com/query/latest/docs/framework/vue/guides/mutations).
- **Spot**: `await mutateAsync(...)` with no surrounding try. No `onError` toast or field mapping.
- **Fix**: Use `mutate` with `onError`, or wrap the call in try/catch and surface the error.
- **Sources:** https://tanstack.com/query/latest/docs/framework/vue/guides/mutations

### FM-C4. A disabled submit button gives no reason (and an empty form gives no errors)
- **Bug**: Submit is greyed out until the form is valid. The user cannot tell which field is wrong, and screen-reader users cannot focus the button to learn why.
- **Cause**: `:disabled="!isValid"` used in place of showing errors on submit.
- **Test**: Leave one field subtly invalid (trailing space in an email, for example) and try to find out why Submit is disabled.
- **Spot**: `:disabled="!meta.valid"` / `:disabled="!isFormValid"`.
- **Fix**: Keep Submit enabled, validate on submit and show the errors. If it must be disabled, use `aria-disabled` and explain why [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html).
- **Src**: [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html)

### FM-C5. Success handler runs after the component unmounted, or the form resets during navigation
- **Bug**: The user submits, then navigates away. The success toast fires on the wrong page, or `router.push` from the old page hijacks navigation.
- **Cause**: `mutate(..., { onSuccess: () => router.push(...) })` with no check. Per-call callbacks are skipped if the component unmounts, but `useMutation`-level callbacks still fire **[verify for the TanStack version in use]**.
- **Test**: Submit on Slow 3G, then immediately click another nav item.
- **Spot**: `router.push` or a toast inside `useMutation({ onSuccess })` (hook level), or after `await mutateAsync()`, with no check that the user is still on the page.
- **Fix**: Put navigation in per-`mutate` callbacks, or check the current route before pushing.
- **Src**: [TQ-MUT](https://tanstack.com/query/latest/docs/framework/vue/guides/mutations)

### FM-C6. Optimistic UI or form reset hides a failed save
- **Bug**: The form clears or shows "Saved" and the API then fails, so the data is lost.
- **Cause**: `reset()` called before `await`, or an optimistic update with no rollback.
- **Test**: Make the API fail, then submit.
- **Spot**: `form.reset()` directly after `mutate()` (not inside `onSuccess`).
- **Fix**: Reset only in `onSuccess`. Roll back the optimistic cache in `onError`.
- **Sources:** [TanStack Query Vue: Optimistic updates](https://tanstack.com/query/latest/docs/framework/vue/guides/optimistic-updates)

### FM-C7. Retry after a timeout creates a duplicate
- **Bug**: The request timed out on the client but succeeded on the server, so the user's retry creates a second resource.
- **Cause**: No idempotency key, and the mutation has `retry` set to a non-zero value.
- **Spot**: `useMutation({ retry: 3 })` on non-idempotent POSTs.
- **Fix**: Keep `retry: 0` for creates (the TanStack default for mutations) or add idempotency keys.
- **Src**: TanStack mutation `retry` option https://tanstack.com/query/latest/docs/framework/vue/reference/useMutation

---

## D. Number inputs

Default test set for any numeric field with bounds `[min,max]` and step `s` [BVA](https://www.educative.io/answers/what-is-equivalence-class-partitioning-boundary-value-analysis), [HEND](https://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf):
`min-1, min, min+1, max-1, max, max+1, 0, -0, -1, '', ' ', '  5  ', 1e3, 1e309, '1,5', '1.5', '1.50', '01', '007', '+5', '--5', '5-', '.5', '5.', 'NaN', 'Infinity', 9007199254740991, 9007199254740993, 0.1+0.2 → 0.30000000000000004, 1.005, '١٢٣' (Arabic-Indic digits), '１２３' (full-width digits), paste '1 000', paste '$100'`.

### FM-D1. `type=number` accepts `e`, `E`, `+`, `-`, `.` anywhere
- **Bug**: `1e5` becomes 100000 (a port speed of 100000 Mbps). `-` or `+` alone, or `1-2`, gives an empty value with no error.
- **Cause**: The browser lets these characters through because they are valid in floating-point syntax. Whether other invalid characters are accepted varies by browser (Firefox historically accepted letters) [MDN-NUM](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number). When the raw text cannot be parsed, `input.value` becomes `''`.
- **Test**: Type `e`, `1e3`, `--1`, `1-`, `+5`. Check what the model holds and what is sent to the API.
- **Spot**: `<input type="number" v-model.number>` with no handling for invalid/empty input. Validation that checks `typeof x === 'number'` only.
- **Fix**: Use `type="text" inputmode="numeric|decimal"`, parse strictly, and validate (GOV.UK's approach) [GOVUK-NUM](https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/). Or use Reka `NumberField`, which parses with Intl [REKA-NUM](https://reka-ui.com/docs/components/number-field).
- **Src**: [MDN-NUM](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number), [GOVUK-NUM](https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/)
- **In the design system**: If there is no number-field component, a `type="number"` input passes `min`/`max`/`step`/`inputmode` through to the native input.

### FM-D2. `v-model.number` gives `''` when empty, a string when unparseable, and a number otherwise
- **Bug**: An API receives `""` for a numeric field, which becomes a 400 or is coerced to 0. Zod `z.number()` fails with "Expected number, received string". A `!value` check treats 0 as empty.
- **Cause**: With `.number`, an empty input returns `''` and an unparseable one returns the original string [VUE-FORMS](https://vuejs.org/guide/essentials/forms.html#modifiers). Parsing uses `parseFloat`, so `12abc` becomes 12 [VUE-2598](https://github.com/vuejs/core/issues/2598). On a component (not a native input), `.number` only casts the emitted value **[verify]**.
- **Test**: Type a value, clear it, then submit. Type `12abc` in a `type=text` + `.number` field.
- **Spot**: `ref<number>(0)` bound with `v-model.number`, where the TS type lies (it can hold `''`). `if (!form.vlan)`. Spreading form state straight into an API payload.
- **Fix**: Type it as `number | null`. Normalise empty to `null` in a computed setter or a schema preprocess (`z.preprocess(v => v === '' ? null : Number(v), ...)`). Use `== null` checks rather than falsy checks.
- **Src**: [VUE-FORMS](https://vuejs.org/guide/essentials/forms.html#modifiers), [VUE-2598](https://github.com/vuejs/core/issues/2598)

### FM-D3. Zero treated as empty or missing (falsy check)
- **Bug**: VLAN 0, price $0, or quantity 0 shows a "required" error, displays as blank, or is dropped from the payload.
- **Cause**: `if (!value)`, `value || undefined`, `v-if="price"`, `value || '-'`.
- **Test**: Enter `0` in every numeric field. Check the display, validation, and payload.
- **Spot**: `||` defaults on numbers. `v-if="num"`. `filter(Boolean)` on numeric arrays.
- **Fix**: `??`, `!= null`, `Number.isFinite(x)`.
- **Sources:** [MDN: Nullish coalescing operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing), [MDN: Falsy](https://developer.mozilla.org/en-US/docs/Glossary/Falsy)

### FM-D4. Negative zero and stray minus signs
- **Bug**: `-0` is accepted and displayed as `-0` or `0`. `Object.is` comparisons or `1/x` misbehave. The server rejects it.
- **Cause**: `parseFloat('-0') === -0`. `-0 < 0` is false, so a `>= 0` check passes it.
- **Test**: Type `-0`, `-0.0`, `-`.
- **Fix**: Normalise with `x === 0 ? 0 : x` (or `x + 0`). Check the minus sign explicitly where negatives are not allowed.
- **Sources:** [MDN: Equality comparisons and sameness](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Equality_comparisons_and_sameness)

### FM-D5. Scroll wheel changes a focused number input value
- **Bug**: The user scrolls the page with the cursor over a focused number field and the value silently changes (a bandwidth of 1000 becomes 997).
- **Cause**: Browser default on focused `type=number`. Behaviour varies: historically Firefox, in some cases Chrome, and vendors are moving to remove it [WHEEL](https://bugzilla.mozilla.org/show_bug.cgi?id=1261674) **[verify current browser behaviour]**. Reka NumberField has its own wheel handling (believed to be `disableWheelChange` / `invertWheelChange` props) **[verify]** [REKA-NUM](https://reka-ui.com/docs/components/number-field).
- **Test**: Focus the field, move the pointer over it, scroll. Do the same with the pointer outside the field.
- **Spot**: `<input type="number">` in long scrolling forms. `NumberField` with no wheel option set.
- **Fix**: Use `type=text inputmode`, blur on wheel, or turn off wheel change on NumberField.
- **Src**: [WHEEL](https://bugzilla.mozilla.org/show_bug.cgi?id=1261674), [GOVUK-NUM](https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/)

### FM-D6. Arrow keys or the spinner change the value of an identifier field
- **Bug**: An ASN, VLAN ID, account number, or postcode stored as a number gets incremented by an accidental arrow press. Leading zeros are lost. Large IDs are rounded or shown in exponent notation.
- **Cause**: `type=number` used for identifiers. The spec intends it for real quantities. Browsers round large values on stepping and may switch to exponent form [GOVUK-NUM](https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/).
- **Test**: Enter `0012345`, `4294967295` (max 32-bit ASN), `12345678901234567890`, then press Up and Down.
- **Spot**: `type="number"` for IDs, ASNs, VLANs, phone numbers, postcodes, and card numbers.
- **Fix**: `type="text" inputmode="numeric" pattern="[0-9]*"`, and keep the value as a string.
- **Src**: [GOVUK-NUM](https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/), [MDN-NUM](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number)

### FM-D7. Locale decimal comma
- **Bug**: A German or French user types `1,5` and gets an error, `''`, or 15 (comma stripped). A displayed `1.234` is read as one thousand two hundred and thirty-four.
- **Cause**: Parsing with `parseFloat`/`Number`, which only understand `.`. Display uses `toString()` instead of `Intl.NumberFormat`. The native number input's handling of locale separators varies by browser and OS locale **[verify]**.
- **Test**: Switch the app locale (and the OS locale) to de-DE. Enter `1,5`, `1.5`, `1.000,5`, `1 000`.
- **Spot**: `parseFloat(input)`, `Number(input)`, `.toFixed()` in templates. `$n` missing from vue-i18n number formatting.
- **Fix**: Format with vue-i18n `$n` / `Intl.NumberFormat`. Parse with a locale-aware parser (Reka NumberField uses `@internationalized/number`) [REKA-NUM](https://reka-ui.com/docs/components/number-field).
- **Src**: vue-i18n number formatting https://vue-i18n.intlify.dev/guide/essentials/number.html

### FM-D8. Leading and trailing zeros, and the formatting round-trip
- **Bug**: `007` is saved as 7 (wrong for codes). `1.50` is displayed as `1.5` while typing, so the caret jumps or the user cannot type `1.0` because the input is reformatted to `1` mid-typing.
- **Cause**: Re-serialising the model back into the input on every keystroke (`:value="Number(x)"`), or formatting on `input` rather than `blur`.
- **Test**: Type `1.0` and keep going to `1.05`. Type `0.` Type `007`.
- **Spot**: `watch(model, v => model.value = round(v))`. Formatting inside `@input`.
- **Fix**: Keep the raw string while focused and format on blur.
- **Sources:** [facebook/react #955: cursor jumps to end of controlled input](https://github.com/facebook/react/issues/955)

### FM-D9. `Number.MAX_SAFE_INTEGER` and precision loss
- **Bug**: A large ID or byte count changes value (`9007199254740993` becomes `...992`).
- **Cause**: JS numbers are IEEE-754 doubles. `JSON.parse` loses precision past 2^53-1.
- **Test**: Enter `9007199254740993` and inspect the payload.
- **Spot**: Numeric types for 64-bit IDs. `Number(id)`.
- **Fix**: Keep IDs as strings. Use `BigInt` or decimal libraries where arithmetic is needed. Validate `Number.isSafeInteger`.
- **Src**: MDN MAX_SAFE_INTEGER https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER

### FM-D10. Floating-point money and totals
- **Bug**: Totals show `$30.000000000000004`, or `1.005` rounds to `1.00`. Monthly price × term is off by a cent compared with the server.
- **Cause**: Binary floats. `toFixed` rounding quirks.
- **Test**: Enter prices `0.1` and `0.2`, plus `1.005` and `2.675`. Compare the UI total with the API or invoice.
- **Spot**: Arithmetic on currency in components. `toFixed(2)` for rounding.
- **Fix**: Integer minor units (cents) or a decimal library. Show the server-computed price. Format with `Intl.NumberFormat({style:'currency'})`.
- **Sources:** [MDN: Number.prototype.toFixed()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed)

### FM-D11. `step` mismatch makes decimal values invalid
- **Bug**: `1.5` is rejected with a native tooltip "Please enter a valid value. The two nearest valid values are 1 and 2", even though the field should take decimals. Or the error appears only in some browsers.
- **Cause**: The default `step` is 1, so non-integers are invalid unless `step="any"` or a decimal step is set [MDN-NUM](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number). Native validation fires because `novalidate` is missing.
- **Test**: Enter `1.5`, `0.01`, `1.0`.
- **Spot**: `type="number"` with `min` set but no `step`.
- **Fix**: Set `step` on purpose. Use `novalidate` plus app validation so messages are consistent and translated.
- **Src**: [MDN-NUM](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number)

### FM-D12. min/max not enforced while typing, or clamped silently
- **Bug**: `min`/`max` only stop the spinner. The user can type `99999`, and it is accepted until submit, or the server rejects it. Or the opposite: the value is clamped silently on blur (5000 becomes 1000) with no message, so the user does not notice.
- **Cause**: HTML `min`/`max` are constraint-validation only. Reka NumberField clamps on blur.
- **Test**: Type `max+1` and Tab away. Type `max+1` and press Enter. Paste `max+1`.
- **Spot**: Relying on `:max` with no validator. Clamping code with no user feedback.
- **Fix**: Validate with a visible message. If you clamp, tell the user.
- **In the project**: If bounds helpers already exist, reuse one rather than adding another copy.
- **Sources:** [MDN: HTML `max` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/max), [Reka UI source: NumberField `applyInputValue` clamps on blur/Enter unless `allowInvalid`](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/NumberField/NumberFieldRoot.vue#L233-L241)

### FM-D13. Client bounds differ from server bounds
- **Bug**: The UI allows 1 to 10000 Mbps, but the API allows 1 to 5000 for this port type, so the user gets a generic 400 after a valid-looking form. Or the UI is stricter than the API and blocks legitimate values.
- **Cause**: Hard-coded bounds in the FE, not taken from the API, product config, or the OpenAPI spec. Bounds change per product, location, or plan.
- **Test**: For each bound, read the OpenAPI spec or backend validation and try values on each side of both limits.
- **Spot**: Magic numbers in a Zod schema (`.max(10000)`). Duplicated constants.
- **Fix**: Source bounds from the API (product metadata) or a shared generated schema. Map server 4xx errors to fields (FM-F7).
- **Src**: [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/) (check client rules do not conflict with server rules)
- **In the project**: Reuse the bounds helper listed under FM-D12 rather than re-deriving the limit.

### FM-D14. Inclusive versus exclusive bounds and off-by-one
- **Bug**: Exactly `max` is rejected (or `min` is accepted when the rule says "greater than").
- **Cause**: `<` versus `<=`. Zod `.max()` is inclusive and `.lt()` is exclusive. Copy says "between 2 and 4094" but the code uses `> 2`.
- **Test**: Full BVA set: min-1, min, min+1, max-1, max, max+1 [BVA](https://www.educative.io/answers/what-is-equivalence-class-partitioning-boundary-value-analysis).
- **Spot**: Comparison operators in validators. Mismatch between the i18n message and the rule.
- **Fix**: Define bounds once and generate the message from the same constants (`t('between', {min, max})`).
- **Src**: [BVA](https://www.educative.io/answers/what-is-equivalence-class-partitioning-boundary-value-analysis)

### FM-D15. Integer-only fields accept decimals
- **Bug**: Quantity `2.5`, VLAN `100.7`, or term `12.5` months is accepted, then truncated by the server or fails there.
- **Cause**: The validator checks the range but not `Number.isInteger`.
- **Test**: `2.5`, `2.0`, `2.`, `1e0`.
- **Spot**: `z.number().min(...).max(...)` with no `.int()` on a count, quantity, VLAN, ASN or term field. `type="number"` with a non-integer `step` on such a field.
- **Fix**: `z.number().int()`, `step="1"`, `inputmode="numeric"`.
- **Sources:** [MDN: Number.isInteger()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isInteger), [Zod: Integers](https://zod.dev/api?id=integers)

### FM-D16. Non-ASCII digits and full-width input
- **Bug**: Japanese full-width `１２３` or Arabic-Indic `١٢٣` digits are rejected or parsed as NaN with no message.
- **Cause**: ASCII-only regex `^[0-9]+$`, or `Number()`.
- **Test**: Paste `１２３` and `١٢٣`.
- **Spot**: `/^\d+$/` or `/^[0-9]+$/` tested against user-typed text, or `replace(/[^0-9]/g, '')`, with no `normalize('NFKC')` first. JS `\d` matches ASCII digits only.
- **Fix**: Normalise (`str.normalize('NFKC')` covers full-width digits) or show a clear message. NFKC does not convert Arabic-Indic digits, which need a mapping.
- **Sources:** [MDN: String.prototype.normalize()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize)

### FM-D17. NaN or Infinity leaks to the UI or API
- **Bug**: The UI shows `NaN`, `$NaN` or `Infinity`, or the payload carries `null` (JSON.stringify turns NaN into null).
- **Cause**: Arithmetic on `''` or `undefined`. Division by zero in derived fields such as price per Mbps.
- **Test**: Clear the inputs that derived values depend on.
- **Spot**: Computed values doing arithmetic on form fields with no `Number.isFinite` guard.
- **Fix**: Guard and show a placeholder (`-`).
- **Sources:** [MDN: JSON.stringify()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)

### FM-D18. Pasted formatted numbers
- **Bug**: Pasting `1,000`, `$100`, `100 Mbps`, or ` 100 ` is rejected, or becomes `''` in a number input with no feedback.
- **Cause**: Strict parse with no normalisation.
- **Test**: Paste each of those values.
- **Spot**: `Number(v)`, `parseInt(v)` or `z.coerce.number()` on a pasted or typed amount with no strip of spaces, thousands separators or units first. `type="number"` on a field users often paste into.
- **Fix**: Strip spaces and thousands separators (locale-aware). GOV.UK: ignore unwanted characters such as spaces and dashes [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/).
- **Src**: [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/)

---

## E. Text, length and whitespace

### FM-E1. maxlength smaller or larger than the server column
- **Bug**: The UI allows 255 characters, the DB column is 100, and the user gets a 500, a 400, or silent truncation. Or the UI allows only 50 when the server takes 255.
- **Cause**: Hard-coded `maxlength` not sourced from the API contract.
- **Test**: Paste exactly N, N+1, and N-1 characters for each limit. Compare with the OpenAPI `maxLength`.
- **Spot**: `maxlength="..."` literals. Zod `.max()` that differs from the spec.
- **Fix**: Use one constant, generated from the OpenAPI spec where possible.
- **In the project**: Share the length constant between create and edit so both validate the same limit.
- **Sources:** [GOV.UK Design System: Validation](https://design-system.service.gov.uk/patterns/validation/)

### FM-E2. Counting graphemes versus UTF-16 code units versus bytes

See IN-C1 (persona-text-input).

### FM-E3. maxlength not enforced on programmatic or pasted input in custom components
- **Bug**: Text set by script (autofill from a template, "duplicate", a paste handler that transforms the value) goes past the limit with no error.
- **Cause**: The spec only flags "too long" when the value was last changed by a **user edit**, not by script [HTML-ML](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#attr-fe-maxlength). Custom rich inputs or contenteditable ignore `maxlength`.
- **Test**: Use any prefill or duplicate feature with an over-long source value. Paste into custom editors.
- **Spot**: Relying on the `maxlength` attribute alone. Values assigned from the API into the form.
- **Fix**: Validate length in the schema, not just with the attribute.
- **Src**: [HTML-ML](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#attr-fe-maxlength)

### FM-E4. Character counter off by one, not live, or not announced
- **Bug**: The counter updates only on blur (with `.lazy`), shows the wrong remaining count, or screen readers announce every keystroke (or never).
- **Cause**: `.lazy`. Newline counting differs: the browser normalises textarea CRLF to 1 for maxlength, but the server may count 2 [HTML-ML](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#attr-fe-maxlength). A live region on each keystroke.
- **Test**: Type to the limit with newlines. Check that the counter equals the limit and that the server accepts it.
- **Spot**: `v-model.lazy` on a field that shows a character counter. A counter inside `aria-live` that updates on every keystroke with no debounce. A counter using `value.length` where the server counts newlines as `\r\n`.
- **Fix**: Debounce the announcement (GOV.UK character count pattern https://design-system.service.gov.uk/components/character-count/). Count `\n` the way the server does.
- **Src**: [HTML-ML](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#attr-fe-maxlength), GOV.UK character count

### FM-E5. Whitespace-only passes "required"

See IN-B1 (persona-text-input).

### FM-E6. Leading or trailing whitespace stored or compared

See IN-B2 (persona-text-input).

### FM-E7. Case and Unicode-normalisation sensitivity

See IN-C5 (persona-text-input), IN-C6 (persona-text-input).

### FM-E8. Over-strict format validation (names, emails, phones)

See IN-F2 (persona-text-input), IN-F4 (persona-text-input), IN-F6 (persona-text-input).

### FM-E9. Injection-looking input breaks rendering

See IN-G1 (persona-text-input), DS-G1 (persona-value-display).

---

## F. Validation timing and messaging

### FM-F1. Errors shown on pristine fields (on mount or while typing the first character)
- **Bug**: The form opens covered in red "Required" errors, or the email shows "invalid" after the first letter.
- **Cause**: Validating on `input` from the start, or `immediate` validation on mount. Not gated on touched/submitted.
- **Test**: Open the form and look. Type one character in email and pause.
- **Spot**: `validateOnMount: true`. `watch(field, validate, { immediate: true })`. Error display not gated by `touched || submitAttempted`.
- **Fix**: Show errors after blur (reward early, punish late) or on submit. Baymard and NN/g: do not validate before input is complete [BAYMARD-IV](https://baymard.com/blog/inline-form-validation), [NNG-ERR](https://www.nngroup.com/articles/errors-forms-design-guidelines/). GOV.UK goes further: validate on submit only [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/).
- **Src**: [BAYMARD-IV](https://baymard.com/blog/inline-form-validation), [NNG-ERR](https://www.nngroup.com/articles/errors-forms-design-guidelines/), [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/)

### FM-F2. Errors not clearing after correction
- **Bug**: The user fixes the value and the red error stays until the next blur or submit.
- **Cause**: Validation runs only on blur or submit. Once a field is in error, it must re-validate on every keystroke [BAYMARD-IV](https://baymard.com/blog/inline-form-validation).
- **Test**: Trigger an error, then type a valid value without leaving the field.
- **Spot**: `validateOnInput: false` everywhere. Server error state stored separately and never cleared on edit.
- **Fix**: After the first error, validate on input. Clear server errors for a field when it changes.
- **Src**: [BAYMARD-IV](https://baymard.com/blog/inline-form-validation)

### FM-F3. Cross-field validation does not re-run when the other field changes
- **Bug**: "End must be after start". The user fixes it by changing **start**, but the error on **end** stays. "Passwords do not match" stays after fixing the first field. A min/max pair (such as `minBandwidth <= maxBandwidth`) gets out of step.
- **Cause**: The rule is attached only to one field and re-validated only when that field changes.
- **Test**: Make the pair invalid, then fix it by editing the **other** field.
- **Spot**: `.refine()` with `path: ['end']` and no dependency trigger. Per-field validators that read another field.
- **Fix**: Re-validate dependent fields in a watcher, or validate the object-level schema on any change.
- **Src**: [BAYMARD-IV](https://baymard.com/blog/inline-form-validation) (the L.L.Bean example)

### FM-F4. Focus not moved to the first error (or the error summary) on submit
- **Bug**: Submit fails, nothing visibly happens because the error is below the fold, and screen-reader users hear nothing.
- **Cause**: There is no focus management on an invalid submit.
- **Test**: Leave the last field invalid on a long form, scroll to the top, press Enter.
- **Spot**: `onSubmit` returns early on invalid with no `focus()` or `scrollIntoView`.
- **Fix**: Focus the error summary (GOV.UK) or the first invalid field. Scroll it into view with header offset.
- **Src**: [GOVUK-ES](https://design-system.service.gov.uk/components/error-summary/), [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/), [SMASH-A11Y](https://www.smashingmagazine.com/2023/02/guide-accessible-form-validation/)

### FM-F5. Error not programmatically associated or announced
- **Bug**: The screen reader does not read the error when the field is focused. The error is shown only in red.
- **Cause**: No `aria-invalid`, and no `aria-describedby` pointing to the error id. Colour-only indication fails WCAG 3.3.1 [WCAG-331](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html).
- **Test**: Use VoiceOver: trigger an error, Tab to the field, listen.
- **Spot**: Error `<p>` without an `id` linked from the input. The error rendered with `v-if` but the description id is static and points nowhere.
- **Fix**: `:aria-invalid="!!error"` plus `:aria-describedby="error ? errId : hintId"` (include both when both exist). Add an icon and text alongside the colour [NNG-ERR](https://www.nngroup.com/articles/errors-forms-design-guidelines/).
- **Src**: [WCAG-331](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html), [SMASH-A11Y](https://www.smashingmagazine.com/2023/02/guide-accessible-form-validation/), [NNG-ERR](https://www.nngroup.com/articles/errors-forms-design-guidelines/)

### FM-F6. Vague or wrong error copy
- **Bug**: "Invalid input", "Error", or "Field is required" with no field name, or a message that says 1 to 100 when the rule is 1 to 99. The same applies to error toasts: "Error" or a raw "Request failed with status code 500".
- **Cause**: Generic messages. Copy not generated from the rule.
- **Test**: Trigger every rule and read the message.
- **Spot**: A bare `t('error')`, `'Invalid input'` or `'Something went wrong'` message, a required message with no field name, or a toast built from `error.message` (raw "Request failed with status code 500").
- **Fix**: Say what is wrong and how to fix it [WCAG-333](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html), [NNG-ERR](https://www.nngroup.com/articles/errors-forms-design-guidelines/). Interpolate bounds from the constants (FM-D14). In toasts, name what failed, why if known, and what to do next; hide status codes unless they help support.
- **Sources:** [WCAG-333](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html), [GOV.UK: Error message](https://design-system.service.gov.uk/components/error-message/), [NN/g: Error-message guidelines](https://www.nngroup.com/articles/error-message-guidelines/)

### FM-F7. Server-side errors not mapped to fields
- **Bug**: The API returns `422 { field: 'vlan', message: 'VLAN in use' }` and the UI shows a generic toast "Something went wrong", or nothing.
- **Cause**: `onError` shows a toast only. Field paths are not mapped.
- **Test**: Submit a value that only the server can reject (duplicate name, VLAN in use, bad promo code).
- **Spot**: `onError: () => toast.error(t('generic'))`. No `setErrors`/`setFieldError`.
- **Fix**: Map API error paths to form fields and focus the first one. Fall back to the summary.
- **Src**: [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/) (always validate on the server too)

### FM-F8. Validation only on the client
- **Bug**: Bypassing the UI (devtools, API, a stale tab) saves invalid data.
- **Cause**: The client-side rule has no matching server rule.
- **Test**: Remove `disabled`/`maxlength` in devtools and submit. Replay the request with modified JSON.
- **Fix**: Server validation is mandatory [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/). Treat the client as UX only.
- **Sources:** https://design-system.service.gov.uk/patterns/validation/

### FM-F9. Required indicator does not match the rule
- **Bug**: An asterisk on an optional field, or a required field with no marker. "(optional)" missing.
- **Cause**: The label's `required` prop and the schema are maintained separately.
- **Test**: Compare each label marker with the behaviour when the field is empty on submit.
- **Spot**: `<FormLabel required>` hard-coded next to a schema `.optional()`.
- **Fix**: Derive the marker from the schema. GOV.UK prefers marking optional fields instead.
- **Src**: [WCAG-332](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html), GOV.UK question pages https://design-system.service.gov.uk/patterns/question-pages/

### FM-F10. Native browser validation bubbles mixed with app validation
- **Bug**: Untranslated browser tooltips ("Please fill out this field") appear in an i18n app, styled differently, and only the first error shows.
- **Cause**: `required`, `pattern`, `min`, or `type=email` without `novalidate` on the form.
- **Spot**: `<form>` without `novalidate`, with HTML constraint attributes on the inputs.
- **Fix**: `novalidate` plus app validation. GOV.UK: turn HTML5 validation off [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/).
- **Src**: [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/)

### FM-F11. Errors persist after the form resets or the dialog reopens
- **Bug**: Reopening the "Add" dialog shows the last session's errors and values.
- **Cause**: Form state lives in a parent or store that outlives the dialog. `resetForm` is not called on open.
- **Test**: Open, trigger errors, close, reopen.
- **Spot**: `useForm()` in a parent page or store while its fields render inside a dialog, with no `resetForm()` on open and no `:key` on the dialog body.
- **Fix**: Mount the form inside `DialogContent` so it unmounts on close, or reset on open.
- **Sources:** [Reka UI: Presence (unmounts content when closed)](https://reka-ui.com/docs/utilities/presence), [vee-validate: Handling forms](https://vee-validate.logaretm.com/v4/guide/composition-api/handling-forms/)

### FM-F12. The error summary is out of sync with inline errors
- **Bug**: The summary lists errors already fixed, its links do not focus the field, or its wording differs.
- **Spot**: An error summary list built from its own array rather than the form's `errors` map, or summary links whose `href` does not match the input `id`.
- **Fix**: Derive both from the same error map. Make the links target the input `id` [GOVUK-ES](https://design-system.service.gov.uk/components/error-summary/).
- **Src**: [GOVUK-ES](https://design-system.service.gov.uk/components/error-summary/)

### FM-F13. Validation runs on hidden or unmounted fields
- **Bug**: The form will not submit because of a hidden field the user cannot see or fix ("invisible error").
- **Cause**: The schema includes fields for collapsed or conditional sections. A `v-show` tab still validates.
- **Test**: Toggle a conditional section on, enter an invalid value, toggle it off, submit.
- **Spot**: A static schema with conditional UI. `v-show` for whole sections.
- **Fix**: Use a discriminated union or conditional schema. Validate only the active branch. Point to the hidden section if it must be validated.
- **Sources:** [Zod: Discriminated unions](https://zod.dev/api?id=discriminated-unions), [vee-validate: Nested objects and arrays (path destruction, `keepValuesOnUnmount`)](https://vee-validate.logaretm.com/v4/guide/composition-api/nested-objects-and-arrays/)

### FM-F14. Async uniqueness check race conditions
- **Bug**: Typing `abc` then `abcd` quickly shows "abc is taken" for `abcd`, because responses arrive out of order.
- **Cause**: No cancellation or sequence check on async validators.
- **Test**: Throttle the network and type fast.
- **Spot**: An async validator (`.refine(async`, yup `test` with `async`, or a `watch` on the field calling an availability API) with no `AbortController`, `onCleanup`, or check that the response matches the current value.
- **Fix**: AbortController, or ignore stale responses (compare the request value with the current value). Or use a TanStack `useQuery` keyed on the value.
- **Sources:** [Vue: Watchers, side effect cleanup](https://vuejs.org/guide/essentials/watchers.html#side-effect-cleanup)

### FM-F15. The page title and live region are not updated on error
- **Bug**: Screen-reader users on a full-page form do not learn that the submit failed.
- **Spot**: A form-level error banner or submit-failure message rendered with `v-if` and no `role="alert"` or `aria-live`, or a hand-rolled field error used in place of `FormFieldMessage`.
- **Fix**: Prefix `document.title` with "Error: " [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/). Use a status/alert region for non-focus messages [WCAG-413](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
- **Src**: [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/), [WCAG-413](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)

### FM-F16. Success message not perceivable or premature
- **Bug**: A "Saved" toast disappears in 2 seconds, is not announced, or appears before the server confirms. "Order placed" shows, and an error toast follows a moment later.
- **Cause**: The success toast fires on click or straight after `mutate()`, not in `onSuccess`. With optimistic updates, `onError` rolls the cache back but nothing tells the user.
- **Test**: Make the API fail (500, 422) or hang, then submit. Watch the order of toasts and what the list shows afterwards.
- **Spot**: `toast.success(...)` next to `mutate()` rather than inside `onSuccess`; `onMutate` optimistic writes with no user-facing message in `onError`.
- **Fix**: `role="status"` live region. Show success only in `onSuccess`. With optimistic updates, roll back in `onError` and say so. Give enough time (WCAG 2.2.1) [WCAG-413](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html). See also DS-K3 (persona-value-display) for toast timing.
- **Sources:** [WCAG-413](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html), [TanStack Query: Optimistic updates](https://tanstack.com/query/latest/docs/framework/vue/guides/optimistic-updates)

### FM-F17. Validating while the user edits a server-loaded value
- **Bug**: An edit form loads an existing record that breaks newly tightened rules (a legacy name longer than the new max). The user cannot save an unrelated change.
- **Cause**: New stricter client rules applied to legacy data.
- **Test**: Load records that hit legacy edge cases.
- **Spot**: A lowered `.max()`, a new `.regex()` or a new `.refine()` on a field of an edit form that loads existing records, with no handling for saved values that break the new rule.
- **Fix**: Decide whether unchanged fields are validated. Coordinate the rule change with the server.
- **Sources:** [Salesforce Trailhead: Validation rules best practices (`ISCHANGED`)](https://trailhead.salesforce.com/content/learn/modules/validation-rules/implement-best-practices), [Eclipse projects.eclipse.org #311](https://gitlab.eclipse.org/eclipsefdn/it/websites/projects.eclipse.org/-/issues/311)

---

## G. Disabled, readonly, hidden and conditional fields

### FM-G1. Disabled fields are not submitted
- **Bug**: A field shown as disabled ("Company", locked "Location") is missing from the payload, so the server nulls it on PUT.
- **Cause**: Disabled controls are skipped when the form data set is built [HTML-ENTRY](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#constructing-the-form-data-set). This only matters for native `FormData` submission. In a Vue SPA, the risk is code that builds the payload from `FormData(formEl)` or that omits disabled keys.
- **Test**: Edit a record with disabled fields and inspect the PUT body.
- **Spot**: `new FormData(form)`. PUT built from only "enabled" fields. PATCH versus PUT semantics.
- **Fix**: Build the payload from the model. Use `readonly` if the value must be submitted and focusable.
- **Src**: [HTML-ENTRY](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#constructing-the-form-data-set)

### FM-G2. Disabled versus readonly confusion
- **Bug**: Users cannot select or copy a "readonly" value (a service key or UID) because it is `disabled`. Disabled text fails contrast (WCAG exempts it, which makes it worse) [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html). Screen readers skip it in Tab order.
- **Cause**: `disabled` used to mean "not editable".
- **Test**: Try to Tab to, select, and copy every non-editable value.
- **Spot**: `disabled` (static or `:disabled="true"`) on an input that shows a UID, service key or ID the user may need to copy.
- **Fix**: `readonly` (focusable, copyable) or plain text with a copy button.
- **Src**: [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html)

### FM-G3. Stale values in hidden conditional fields are submitted
- **Bug**: The user chooses "Private VLAN", types VLAN 100, switches to "Untagged", and VLAN 100 is still sent, so the server rejects it or misconfigures.
- **Cause**: `v-show` hides the input but the model keeps the value. `v-if` does the same when the model is a plain `ref`/`reactive` or vee-validate runs with `keepValuesOnUnmount`; by default vee-validate drops an unmounted `useField` value.
- **Test**: Fill each conditional branch, switch away, submit, and inspect the payload.
- **Spot**: The payload is built from the whole form object. No cleanup watcher on the discriminator field.
- **Fix**: Build the payload per branch (discriminated union) or clear dependent fields when the controlling field changes.
- **Sources:** [vee-validate: Nested objects and arrays (path destruction, `keepValuesOnUnmount`)](https://vee-validate.logaretm.com/v4/guide/composition-api/nested-objects-and-arrays/)

### FM-G4. Clearing dependent fields on change wipes data unexpectedly
- **Bug**: The reverse of FM-G3. Toggling a checkbox off and on loses everything typed in the sub-section, or changing country wipes the whole address.
- **Cause**: An aggressive `watch(controller, () => reset(children))`.
- **Test**: Toggle the controller back and forth.
- **Spot**: `watch(controller, () => resetField(...))`, `setFieldValue(child, undefined)` or `setValues` in a watcher on a toggle or parent select, which wipes a sub-section every time it changes.
- **Fix**: Keep values while editing and exclude them at submit (FM-G3 fix). Ask before discarding a large amount of input.
- **Sources:** [vee-validate: Nested objects and arrays (path destruction, `keepValuesOnUnmount`)](https://vee-validate.logaretm.com/v4/guide/composition-api/nested-objects-and-arrays/)

### FM-G5. Dependent options not refreshed (a cascading select keeps an invalid child)
- **Bug**: Change Metro from Sydney to Melbourne and the selected Data Centre is still a Sydney site, which then gets submitted.
- **Cause**: The child value is not validated against the new option list.
- **Test**: Pick a parent, pick a child, change the parent.
- **Spot**: A child select whose `options` are computed from a parent field, with no watcher or `.refine` that clears or rejects the child value when it leaves the new option list.
- **Fix**: When the parent changes, clear the child if it is no longer among the options. Show the empty state.
- **Sources:** [Vue forms guide: select](https://vuejs.org/guide/essentials/forms.html#select)

### FM-G6. A field is disabled during loading but the value is lost or reset when loading ends
- **Bug**: The user types while options load, and the value is overwritten when the query resolves.
- **Cause**: `watch(data, d => form.x = d.default)` runs after the user has edited.
- **Test**: Throttle the network, type immediately, wait.
- **Spot**: Watchers that apply server defaults with no dirty check.
- **Fix**: Apply defaults only if the field is untouched, or initialise once.
- **Sources:** [vee-validate: Handling forms, components (only non-dirty fields update when `initialValues` change)](https://vee-validate.logaretm.com/v4/guide/components/handling-forms/), [vee-validate: Handling forms](https://vee-validate.logaretm.com/v4/guide/composition-api/handling-forms/)

### FM-G7. Programmatic disable does not block keyboard or form submission
- **Bug**: A "disabled" custom control (styled div with `aria-disabled`) still toggles with Space or still submits.
- **Cause**: `aria-disabled` changes semantics only. Script must block activation [ROSELLI-DIS](https://adrianroselli.com/2024/02/dont-disable-form-controls.html).
- **Test**: Tab to it and press Space or Enter.
- **Spot**: `:aria-disabled` on a custom control whose `@click`, `@keydown.space` or `@keydown.enter` handler has no `if (disabled) return`.
- **Fix**: Check disabled state in the handler.
- **Sources:** https://adrianroselli.com/2024/02/dont-disable-form-controls.html

---

## H. Dirty state, unsaved changes, reset and navigation

### FM-H1. No unsaved-changes guard on route leave or tab close
- **Bug**: The user edits a long form, clicks a sidebar link (or closes the tab) and loses the work without warning.
- **Cause**: There is no `onBeforeRouteLeave` and no `beforeunload` listener.
- **Test**: Edit, then (a) click an in-app link, (b) press browser Back, (c) close the tab, (d) reload, (e) change the company/account switcher, (f) let the session time out.
- **Spot**: A create or edit page that tracks dirty state (`meta.dirty`, `isDirty`, a save bar) but registers no `onBeforeRouteLeave` or `beforeunload`, and does not use `useSaveBarLeaveGuard`.
- **Fix**: `onBeforeRouteLeave` with a confirm when dirty. `beforeunload` with `preventDefault()` (custom text is ignored and browsers may need user interaction first [MDN-BU](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event)).
- **Src**: [VR-GUARDS](https://router.vuejs.org/guide/advanced/navigation-guards.html), [MDN-BU](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event)

### FM-H2. Guard fires after a successful save (false positive)
- **Bug**: The user saves, gets redirected, and sees "You have unsaved changes".
- **Cause**: `router.push` in `onSuccess` before the dirty baseline resets. The dirty flag is computed from the stale initial values.
- **Test**: Save a form that redirects on success.
- **Spot**: `router.push` before `resetForm({ values: saved })`. The guard reads `isDirty` without checking a `submitted` flag.
- **Fix**: Reset the baseline to the saved values (or set `skipGuard`) before navigating.
- **Sources:** [vee-validate: Handling forms](https://vee-validate.logaretm.com/v4/guide/composition-api/handling-forms/), [vue-router: Navigation guards](https://router.vuejs.org/guide/advanced/navigation-guards.html)

### FM-H3. Dirty state false positives from normalisation
- **Bug**: Opening and closing an untouched edit form prompts "unsaved changes".
- **Cause**: The initial values differ in type or shape from the model: `null` versus `''`, number versus string, `undefined` keys, date object versus ISO string, array order, trimmed versus untrimmed, and defaults applied after load.
- **Test**: Open each edit form, change nothing, navigate away.
- **Spot**: Dirty check through `JSON.stringify(a) !== JSON.stringify(b)` or reference equality. Defaults applied by a watcher after init.
- **Fix**: Normalise both sides through the same mapper. Compare deeply on normalised values.
- **Sources:** [vee-validate source: field `dirty` = `!isEqual(currentValue, initialValue)`](https://github.com/logaretm/vee-validate/blob/main/packages/vee-validate/src/useFieldState.ts#L217-L219), [MDN: JSON.stringify()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)

### FM-H4. Dirty state false negatives (edits not detected)
- **Bug**: The guard does not fire after editing a nested array or object (adding a tag, toggling a row).
- **Cause**: A shallow comparison, or `isDirty` computed from top-level refs. Mutating a nested object shared with the baseline (same reference), so both change together.
- **Spot**: `initial = form` (no clone). `reactive` baseline shared with the model.
- **Fix**: `structuredClone` the baseline (through `toRaw`). Compare deeply.
- **Sources:** [MDN: structuredClone()](https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone), [Vue: toRaw()](https://vuejs.org/api/reactivity-advanced.html#toraw)

### FM-H5. Editing back to the original value still shows dirty
- **Bug**: Type `a`, delete it, and "Unsaved changes" still shows. The Save button stays enabled.
- **Cause**: The dirty flag is set on any input event rather than computed by comparing values.
- **Spot**: `isDirty.value = true` (or `hasChanges`) set in an `@input` or `@update:modelValue` handler, or in a deep `watch(form)`, instead of a value comparison against the baseline.
- **Fix**: Derive dirty from a value comparison.
- **Sources:** [vee-validate source: field `dirty` = `!isEqual(currentValue, initialValue)`](https://github.com/logaretm/vee-validate/blob/main/packages/vee-validate/src/useFieldState.ts#L217-L219)

### FM-H6. Form not reset after submit (or reset wrongly)
- **Bug**: After "Add another", the previous values remain and a duplicate is submitted. Or after save the form clears, but the user expected to keep editing.
- **Spot**: A create dialog's `onSuccess` with no `resetForm()`, or `resetForm()` with no `values` on an edit form, so the baseline reverts to the pre-save values.
- **Fix**: Decide per form and reset in `onSuccess` with the server response as the new baseline.
- **Sources:** [vee-validate: Handling forms](https://vee-validate.logaretm.com/v4/guide/composition-api/handling-forms/), [TanStack Query Vue: Mutations](https://tanstack.com/query/latest/docs/framework/vue/guides/mutations)

### FM-H7. Form state lost or leaked when navigating between records of the same route
- **Bug**: Going from `/services/1/edit` to `/services/2/edit` keeps record 1's values, because the component is reused and `setup` does not re-run.
- **Cause**: vue-router reuses the component when only params change.
- **Test**: Navigate between two edit routes directly (links, Back/Forward).
- **Spot**: Form init in `setup`/`onMounted` only, with no watch on `route.params.id`. No `:key="route.fullPath"` on `<RouterView>`.
- **Fix**: `watch(() => route.params.id, init, { immediate: true })` or key the view. `onBeforeRouteUpdate` should also check dirty state.
- **Src**: [VR-GUARDS](https://router.vuejs.org/guide/advanced/navigation-guards.html) (in-component guards, `beforeRouteUpdate`)

### FM-H8. TanStack refetch overwrites in-progress edits
- **Bug**: Window refocus or polling refetches the record, and a `watch(data)` overwrites what the user typed.
- **Cause**: The form is synced from query data on every change. `refetchOnWindowFocus` is on by default.
- **Test**: Edit a field, switch tabs, come back.
- **Spot**: `watch(query.data, d => Object.assign(form, d))`.
- **Fix**: Initialise once (or only when not dirty). Turn off refetch-on-focus for edit views. Show a "record changed on server" notice.
- **Src**: TanStack important defaults https://tanstack.com/query/latest/docs/framework/vue/guides/important-defaults

### FM-H9. Autofocus problems
- **Bug**: Autofocus scrolls the page past the content, opens the mobile keyboard unexpectedly, steals focus from an error summary or dialog, or never happens because the input is inside `v-if` and was not mounted yet.
- **Cause**: The `autofocus` attribute only works on initial page load, not on SPA mounts. `focus()` called before `nextTick`.
- **Test**: Open the form through in-app navigation and by direct URL. Check the focus target and scroll position.
- **Spot**: `autofocus` on a field mounted by in-app navigation, a `v-if` block or a dialog. `el.focus()` right after setting a `v-if` flag with no `await nextTick()`.
- **Fix**: Call `focus()` after `nextTick` (or use Reka `@open-auto-focus`). Autofocus sparingly. Focus the heading on route change.
- **Sources:** [MDN: autofocus](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/autofocus), [WHATWG HTML: the autofocus attribute](https://html.spec.whatwg.org/multipage/interaction.html#the-autofocus-attribute)

### FM-H10. Redundant re-entry of data on multi-step forms
- **Bug**: Going Back in a wizard clears the earlier steps, or the user must re-enter the same info (billing contact = technical contact).
- **Cause**: Step state is held in components that unmount.
- **Spot**: Wizard step data held in `ref`s or `useForm()` inside step components that unmount on step change (`v-if`, `<component :is>`), with no store or parent state.
- **Fix**: Keep wizard state in a store or parent. Offer "same as". WCAG 3.3.7 Redundant Entry [WCAG-337](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html).
- **Src**: [WCAG-337](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)

### FM-H11. A failed submit wipes user input
- **Bug**: After a server error the form is reset, or password-type fields are cleared without explanation.
- **Cause**: Resetting in `onSettled`, or re-mounting on error. Baymard found many sites reset user entries after a failed submit [BAYMARD-IV](https://baymard.com/blog/inline-form-validation).
- **Spot**: `resetForm()`, `form.reset()` or a `:key` bump on the form inside `onSettled`, `onError` or `finally` after a submit.
- **Fix**: Keep entries. GOV.UK: show the page again with the user's answers intact [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/).
- **Src**: [BAYMARD-IV](https://baymard.com/blog/inline-form-validation), [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/)

---

## I. Select, radio and checkbox

### FM-I1. A wrong or silent default selection
- **Bug**: A select pre-selects the first option (such as the first billing market or a 1 Gbps port), so users submit it without noticing. Or a radio group has no default, so `undefined` is submitted.
- **Cause**: A native `<select>` with no placeholder option shows the first option but the model is `undefined` until change **[verify Vue sync behaviour; Vue warns in dev when the initial value matches no option]**. Defaults applied in code.
- **Test**: Submit the form untouched and inspect the payload against what is displayed.
- **Spot**: `<select v-model>` with no disabled placeholder. `options[0]` default.
- **Fix**: An explicit placeholder ("Select…") plus a required rule, or a deliberate and visible default.
- **Src**: Vue forms guide, select https://vuejs.org/guide/essentials/forms.html#select

### FM-I2. No way to deselect or choose "none"
- **Bug**: Once an optional select or radio has a value, the user cannot return to "none".
- **Cause**: Radios cannot be unchecked. Reka Select has no clear option. An empty-string item is disallowed (Reka/Radix `SelectItem` rejects `value=""`).
- **Test**: Pick a value in each optional select or radio group, then try to clear it.
- **Spot**: A select or radio group bound to a field that is `.optional()` or `.nullable()` in the schema, with no "None" item and no clear action. A `SelectItem` with `value=""`.
- **Fix**: Add an explicit "None" option (non-empty sentinel mapped to `null`) or a clear button.
- **Sources:** [MDN: input type=radio](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/radio), [Reka UI source: SelectItem throws on `value=""`](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/Select/SelectItem.vue#L135-L139)

### FM-I3. Value type mismatch between options and model
- **Bug**: The selected option does not show as selected on edit (the model is `5`, the option value is `"5"`). Or an object option loses identity after refetch, so the select shows empty.
- **Cause**: Strict equality on value types. Object values compared by reference.
- **Test**: Open an edit form for an existing record. Check that every select shows the saved value. Trigger a refetch.
- **Spot**: `:value="String(id)"` versus a numeric model. Object `:value` without a `by` / compare key (Reka Combobox/Select/Listbox support `by`) **[verify prop name per component]**.
- **Fix**: Use primitive IDs as values, or set `by="id"`.
- **Sources:** [Vue forms guide: select options](https://vuejs.org/guide/essentials/forms.html#select-options), [Reka UI source: SelectRoot `by` prop](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/Select/SelectRoot.vue#L19-L20)

### FM-I4. A saved value is missing from the current options
- **Bug**: On edit, a deprecated plan or location no longer in the list shows blank, and saving silently changes it.
- **Test**: Edit a record whose value is not among the current options.
- **Spot**: Edit-form select `options` computed from a filtered current list (`.filter(x => x.active)`, available only) with no step that adds the record's saved value.
- **Fix**: Include the current value as a (disabled) option or show it as text with a warning.
- **Sources:** [Vue forms guide: select](https://vuejs.org/guide/essentials/forms.html#select)

### FM-I5. Select-all with filtered or paginated lists

See NV-L2 (persona-url-state), NV-L1 (persona-url-state).

### FM-I6. Indeterminate state wrong or not exposed
- **Bug**: The parent checkbox shows checked when only some children are selected, or an indeterminate box is announced as "not checked". Clicking indeterminate does something surprising.
- **Cause**: The native `indeterminate` is a DOM property (no attribute) and is lost on re-render. The state is not derived from children.
- **Test**: Select some, all, and none of the children. Check the visual state and the screen-reader announcement ("mixed"). Click the parent from each state.
- **Spot**: A select-all checkbox bound to `allSelected` with no `'indeterminate'` model value or `:indeterminate` binding, or an indeterminate flag held in a `ref` rather than computed from the children.
- **Fix**: Reka Checkbox with `'indeterminate'` model value. Derive it from the children. Clicking from mixed should select all (common convention) [APG-CHECK](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/).
- **Src**: [APG-CHECK](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/)

### FM-I7. Selection survives a data change it should not (stale selection)
- **Bug**: After deleting selected rows, the toolbar still says "3 selected", and a bulk action targets IDs that no longer exist.
- **Spot**: A `selected` ref or `Set` of row IDs beside a list query, with no prune when the query data changes and no clear in the bulk action's `onSuccess`.
- **Fix**: Prune the selection when data changes.
- **Sources:** [TanStack Table: Row selection guide](https://tanstack.com/table/v8/docs/guide/row-selection)

### FM-I8. Checkbox group v-model with a non-array initial value
- **Bug**: Multiple checkboxes bound to `ref(null)` or a string behave as booleans: ticking one ticks all.
- **Cause**: Vue binds an array for a multi-value checkbox group and a boolean otherwise.
- **Spot**: `v-model="form.tags"` where `tags` is initialised to `null`/`''`.
- **Fix**: Initialise as `[]`.
- **Src**: Vue forms guide, checkbox https://vuejs.org/guide/essentials/forms.html#checkbox

### FM-I9. Radio groups without a shared name or with duplicate ids
- **Bug**: Arrow keys do not move between radios, two groups interfere with each other, or clicking a label selects a radio in a different instance of the component.
- **Cause**: Hard-coded `id`/`name` in a reusable component rendered more than once.
- **Spot**: `id="option-a"` literals in components. Use `useId()` (Vue 3.5+) instead.
- **Fix**: `useId()` or Reka `RadioGroup`.
- **Src**: Vue useId https://vuejs.org/api/composition-api-helpers.html#useid

---

## J. Dates and times

### FM-J1. UTC-midnight off-by-one day
- **Bug**: The user picks 10 March, and it is saved or displayed as 9 March in the Americas (or 11 March in some cases).
- **Cause**: `new Date('2024-03-10')` is parsed as **UTC** midnight, while `new Date('2024-03-10T00:00')` is local. Local getters or `toLocaleDateString` then shift the day [MDN-DATEPARSE](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Date/parse). The reverse also happens: `date.toISOString().slice(0,10)` on a local-midnight Date gives the previous day east of UTC (for example, in Australia).
- **Test**: Set the OS timezone to `America/Los_Angeles`, then `Pacific/Kiritimati` (UTC+14), then `Australia/Sydney`. Pick a date, save, reload, and compare with the API value.
- **Spot**: `new Date(yyyyMmDd)`. `.toISOString().split('T')[0]`. Date-only values stored as Date objects.
- **Fix**: Keep date-only values as `CalendarDate` (`@internationalized/date`, which Reka DatePicker uses [REKA-DATE](https://reka-ui.com/docs/components/date-picker)) or as `YYYY-MM-DD` strings. Convert to an instant only with an explicit timezone.
- **Src**: [MDN-DATEPARSE](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Date/parse), [REKA-DATE](https://reka-ui.com/docs/components/date-picker)
- **In the project**: Decode dates in the API client's schema and display them through the project's date component.

### FM-J2. Converting a Reka CalendarDate to a Date with the wrong timezone
- **Bug**: The same as FM-J1 but subtler: `value.toDate('UTC')` versus `toDate(getLocalTimeZone())` used inconsistently between save and load.
- **Spot**: `toDate(` calls. Mixed `getLocalTimeZone()` and `'UTC'`.
- **Fix**: One documented convention per field (date-only, or instant plus zone).
- **Sources:** [@internationalized/date: CalendarDate](https://react-aria.adobe.com/internationalized/date/CalendarDate)

### FM-J3. Typed invalid dates accepted
- **Bug**: Typing `31/02/2025` rolls over to 3 March. `2025-13-01` becomes January 2026. A 2-digit year `25` becomes 1925.
- **Cause**: `new Date(y, m, d)` overflows silently. Lenient parsing.
- **Test**: `29/02/2023`, `31/04/2025`, `00/01/2025`, `32/01/2025`, `2025-13-01`, `1/1/25`, `01/02/2025` (DMY versus MDY).
- **Spot**: `new Date(y, m - 1, d)`, `new Date(str)` or a non-strict `dayjs(str, fmt)` on a typed date, with no round-trip check that the parsed parts equal the input.
- **Fix**: Strict parse plus a round-trip check (the components re-read equal the input). Reka DateField constrains the segments **[verify]**. GOV.UK: reject a month of 13 [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/).
- **Src**: [GOVUK-VAL](https://design-system.service.gov.uk/patterns/validation/)

### FM-J4. End before start allowed (and equal not handled)
- **Bug**: A contract end date before its start, or a same-day start and end where the rule should forbid it.
- **Cause**: There is no cross-field rule, or it does not re-run (FM-F3). Inclusive versus exclusive is unclear.
- **Test**: end = start-1, start, start+1. Change start after end is set.
- **Spot**: Start and end date fields in a schema with no object-level `.refine` comparing them, and an end picker with no `:min-value` bound to the start.
- **Fix**: A cross-field rule re-validated on both fields. Set the end picker's `min` from start (`:min-value`).
- **Sources:** [React Stately source: reversed range is invalid ("Start date must be before end date.")](https://github.com/adobe/react-spectrum/blob/main/packages/react-stately/src/datepicker/utils.ts#L136-L144)

### FM-J5. Date picker min/max not matching the typed-input path
- **Bug**: The calendar greys out past dates, but typing a past date into the field is accepted.
- **Cause**: `min`/`max` disable dates in the calendar, but a typed out-of-range date still reaches the model. Reka `DateField` only sets `data-invalid` (and the `isInvalid` slot prop), which nothing enforces unless the form reads it.
- **Test**: Type a date outside the range instead of picking it.
- **Spot**: `:min-value` or `:max-value` on a date picker or `DateField` with no matching bound in the schema.
- **Fix**: Validate the value in the schema, not just with picker props.
- **Sources:** [Reka UI source: DateField `isInvalid` from `minValue`/`maxValue`](https://github.com/unovue/reka-ui/blob/v2/packages/core/src/DateField/DateFieldRoot.vue#L173-L185), [React Aria: DatePicker](https://react-aria.adobe.com/DatePicker)

### FM-J6. "Today" boundary uses the client clock or the wrong zone
- **Bug**: "Start date must be today or later" rejects today for users ahead of UTC, or accepts yesterday. It breaks around midnight, or when the client clock is wrong.
- **Test**: Set the system clock to 23:59 and 00:01, in UTC+10 and UTC-8.
- **Spot**: `today(getLocalTimeZone())`, `new Date()` or `dayjs()` as the "today" bound of a start-date rule or picker `min` where the business rule is in another zone.
- **Fix**: Compute "today" in the relevant business timezone (the user's or the data centre's). Validate on the server.
- **Sources:** [@internationalized/date: CalendarDate](https://react-aria.adobe.com/internationalized/date/CalendarDate) (`today(timeZone)`)

### FM-J7. DST transitions
- **Bug**: Adding 1 day by `+ 86400000` ms lands on 23:00 the previous day across a DST change. A scheduled maintenance at 02:30 on a spring-forward day does not exist. Durations come out at 23 or 25 hours.
- **Test**: Sydney: first Sunday in October (forward) and first Sunday in April (back). US: second Sunday in March. Pick times inside the skipped or repeated hour.
- **Spot**: Millisecond arithmetic for days. `setHours` across DST.
- **Fix**: Calendar arithmetic (`CalendarDate.add({days:1})`, `date-fns addDays`). Handle non-existent or ambiguous local times explicitly.
- **Sources:** [@internationalized/date: ZonedDateTime](https://react-aria.adobe.com/internationalized/date/ZonedDateTime)

### FM-J8. Leap day and month-end arithmetic
- **Bug**: A 12-month term starting 29 Feb 2024 ends on 1 Mar 2025 (or errors). Adding 1 month to 31 Jan gives 3 Mar.
- **Cause**: `setMonth(m+1)` overflows.
- **Test**: 29 Feb, 31 Jan + 1 month, 30 Apr + 1 month, 31 Dec + 1 day, year 2100 (not a leap year).
- **Spot**: `setMonth(getMonth() + n)`, `setDate(getDate() + n)` or `setFullYear` arithmetic on term or contract dates.
- **Fix**: Use a date library with clamping (`@internationalized/date` `add({months:1})` clamps to the month end). Agree the business rule with product.
- **Sources:** [@internationalized/date: CalendarDate](https://react-aria.adobe.com/internationalized/date/CalendarDate), [MDN: Date.prototype.setMonth()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setMonth)

### FM-J9. Locale date format ambiguity

See DS-E6 (persona-value-display).

### FM-J10. Time inputs: 12/24h, midnight and noon edge cases
- **Bug**: `12:00 AM` stored as noon. `24:00` accepted. Seconds dropped. The end time 00:00 treated as start-of-day instead of end-of-day.
- **Test**: 00:00, 12:00, 12:30 AM/PM, 23:59, 24:00.
- **Spot**: Hand-written 12h/24h conversion (`% 12`, `+ 12`, an `AM`/`PM` branch), a time regex that allows `24`, or an end time of `00:00` compared as start of day.
- **Fix**: Store 24h. Define end-of-day semantics (exclusive midnight of the next day).
- **Sources:** [MDN: input type=time](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/time)

### FM-J11. Native `type=date` quirks
- **Bug**: Safari or old browsers render a text field. The `value` is `''` for partial input (no error). `valueAsDate` is UTC midnight (FM-J1). The displayed format follows the browser locale, not the app's.
- **Test**: Type a partial date (only the month), then submit. Check in Safari and Firefox.
- **Spot**: `<input type="date">` (or the design system's input with `type="date"`) instead of the Reka-based date picker, validated only with `required`.
- **Fix**: Use the Reka DateField or DatePicker consistently. Treat `''` as an incomplete entry, not as empty, when segments have been touched **[verify feasibility]**.
- **Src**: MDN input date https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date

---

## K. Focus, tab order and re-render

### FM-K1. Focus lost after re-render (list re-keyed, `v-if` swap)
- **Bug**: After typing in a row, the table re-renders and focus jumps to `<body>`. The user has to Tab from the top again.
- **Cause**: `:key="index"` or a key that changes on save. Swapping between edit and view mode with `v-if`. The parent remounts on query refetch.
- **Test**: Edit inline rows. Add or remove a row with the keyboard. Watch `document.activeElement`.
- **Spot**: `:key="index"`, `:key="JSON.stringify(item)"`, `:key="Math.random()"`. `v-if` around the focused element.
- **Fix**: Stable IDs as keys. Restore focus explicitly after DOM changes (`nextTick(() => el.focus())`).
- **Sources:** [Vue: `key` special attribute](https://vuejs.org/api/built-in-special-attributes.html#key)

### FM-K2. Focus not returned after the dialog closes
- **Bug**: After closing a dialog, focus goes to `<body>`. Keyboard users lose their place.
- **Cause**: A dialog opened programmatically (no Reka `DialogTrigger`), so there is no trigger to return to. The trigger was removed in the meantime (for example, a row "Delete" button whose row is now deleted).
- **Test**: Open each dialog from the keyboard, close it with Esc, with Cancel, and with Confirm, and note where focus lands.
- **Spot**: `v-model:open` set from a menu item or a table action with no `@close-auto-focus` handler.
- **Fix**: `@close-auto-focus` with `preventDefault` and focus a sensible element (the next row, or the list heading) [APG-DIALOG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
- **Src**: [APG-DIALOG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), [REKA-DIALOG](https://reka-ui.com/docs/components/dialog)

### FM-K3. Focus not moved into the dialog, or moved to a destructive button
- **Bug**: The dialog opens but focus stays behind it, or lands on "Delete".
- **Spot**: A confirm dialog whose first focusable element is the destructive button (no field before it), with no `@open-auto-focus` handler.
- **Fix**: Focus the first field, or the least destructive control, through `@open-auto-focus` [APG-DIALOG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
- **Sources:** https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

### FM-K4. Tab order does not match the visual order
- **Bug**: Tab jumps from the first column to the footer, then back. Order differs from layout because of CSS grid `order` or positive `tabindex`.
- **Test**: Tab through every form. Shift+Tab back.
- **Spot**: `tabindex="1"` and higher. CSS `order`, `flex-direction: *-reverse` on interactive groups.
- **Fix**: DOM order = visual order. Only use `tabindex` values of 0 and -1 [WCAG-243](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html).
- **Src**: [WCAG-243](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)

### FM-K5. Focus trapped in or skipped over custom widgets
- **Bug**: Tab cannot leave a custom editor or a date segment group. Or an icon-only clear button is unreachable (`tabindex=-1`).
- **Test**: Tab into and out of every composite widget.
- **Spot**: `tabindex="-1"` on an icon-only clear or remove button inside a field, or a keydown handler that calls `preventDefault()` on `Tab`.
- **Sources:** [WCAG 2.2 SC 2.1.2 No Keyboard Trap](https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html), [WAI-ARIA APG: Developing a keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)

### FM-K6. Hidden elements still focusable
- **Bug**: Tab lands on invisible elements (collapsed accordion contents, off-screen drawers, `opacity:0` menus).
- **Cause**: Hidden with opacity or transform instead of `display:none` / `inert` / `v-show`.
- **Test**: Tab with all sections collapsed.
- **Spot**: A collapsed or off-screen panel hidden with `opacity-0`, `translate-*` or `max-h-0` that still holds focusable children, with no `v-if`, `v-show` or `inert`.
- **Fix**: `v-if`, `v-show`, or the `inert` attribute.
- **Sources:** [MDN: inert](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert)

### FM-K7. Focus indicator removed
- **Bug**: The user cannot see which field or button is focused.
- **Spot**: `outline: none` with no `:focus-visible` replacement.
- **Fix**: A visible `:focus-visible` style (WCAG 2.4.7 Focus Visible, AA; WCAG 2.2 adds 2.4.13 Focus Appearance, AAA, for indicator size and contrast, and 2.4.11 Focus Not Obscured, AA).
- **Sources:** [WCAG 2.2 SC 2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html), [WCAG 2.2 SC 2.4.13 Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html), [WCAG 2.2 SC 2.4.11 Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)

### FM-K8. Labels not clickable or not associated
- **Bug**: Clicking a label does not focus or toggle the control. A screen reader reads an unlabelled "edit text".
- **Cause**: `for`/`id` missing or duplicated (FM-I9). Reka `Label` without `for` **[verify]**. A placeholder used as the label [WCAG-332](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html).
- **Test**: Click each label. Run axe.
- **Spot**: A bare `<label>` with no `for`, a hard-coded or duplicated `id`, or a `placeholder` standing in for a label, outside the design system's form-field wrapper.
- **Fix**: Unique ids through `useId()`. Visible labels.
- **Src**: [WCAG-332](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)

### FM-K9. Keyboard shortcut collisions
- **Bug**: A global shortcut (`/` to search, `?` for help, `s` to save) fires while typing in a field, which inserts nothing and jumps away. Speech-input users trigger single-character shortcuts just by dictating words.
- **Cause**: A global `keydown` listener that does not ignore events from editable targets.
- **Test**: Type `/`, `?`, and single letters into every text field.
- **Spot**: `window.addEventListener('keydown')` / `onKeyStroke` with no `isEditable(e.target)` check.
- **Fix**: Ignore events when the target is an input, textarea, select, or contenteditable, or when a modifier key is held. For single-character shortcuts, WCAG 2.1.4 needs one of: a way to turn them off, a way to remap them to include a modifier, or activation only when the relevant component has focus.
- **Sources:** [WCAG 2.2 SC 2.1.4 Character Key Shortcuts](https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html)

---

## L. Autofill and paste (cross-cutting)

### FM-L1. Autofill does not update the model

See IN-I2 (persona-text-input).

### FM-L2. Wrong or missing `autocomplete` tokens

See IN-I1 (persona-text-input).

### FM-L3. Paste blocked or transformed

See IN-D3 (persona-text-input).

---

## M. Schemas, field registration and values sent to the API

### FM-M1. `z.coerce.number()` turns an empty field into 0, so "required" passes
- **Bug**: The user clears a required bandwidth or quantity field and submits. No error appears and 0 is saved, or a `min(1)` error says "must be at least 1" rather than "required".
- **Cause**: `z.coerce.number()` runs `Number(input)`, and `Number('') === 0`. Zod's own test suite asserts that `schema.parse("")` equals `0`. This differs from FM-D2 (`v-model.number`) and FM-D3 (zero treated as empty, the opposite direction).
- **Test**: Type a value, clear it, and submit. Also try a field with only spaces (`Number(' ')` is also 0).
- **Spot**: `z.coerce.number()` in a form schema bound to a text or number input.
- **Fix**: `z.preprocess(v => (v === '' || v == null ? undefined : v), z.number({ required_error }))`, or validate the string and then transform.
- **Sources:** [Zod coerce tests (v3.23.4)](https://deno.land/x/zod@v3.23.4/__tests__/coerce.test.ts?source), [Zod API: coercion](https://zod.dev/api?id=coercion)

### FM-M2. An optional field fails validation when left empty
- **Bug**: An optional "Customer reference" or "Notification email" field shows "Invalid email" after the user types and then deletes, or on submit while empty.
- **Cause**: The input emits `''`, but `.optional()` only allows `undefined`. So `z.string().email().optional()` rejects `''`. This differs from FM-F9 (required indicator mismatch) and IN-J7 (persona-text-input) (stale value).
- **Test**: For each optional field: leave it untouched, type then clear, and enter only spaces. Submit each time.
- **Spot**: `.optional()` on string formats (`email`, `url`, `regex`, `min`) bound to text inputs, with no `.or(z.literal(''))` and no preprocess.
- **Fix**: `z.union([z.literal(''), z.string().email()])`, or preprocess `''` to `undefined`. Send `null` or omit the field, as the API expects.
- **Sources:** [Zod API: coercion and optional](https://zod.dev/api?id=coercion), [Guru99: web application testing checklist](https://www.guru99.com/complete-web-application-testing-checklist.html)

### FM-M3. A constraint enforced on the create path but not on edit, rename, duplicate or bulk paths
- **Bug**: A name-length rule, character rule, speed range or maximum count is enforced in the create wizard but not in the inline rename on the detail page, the "Duplicate" action or the edit dialog. Users create values that later break other screens or fail at the server.
- **Cause**: Each entry point has its own schema, or the edit path has none.
- **Test**: Find every way to set the same attribute (create, edit, inline rename, duplicate, bulk edit, and API import) and apply the same boundary values to each.
- **Spot**: A new edit or rename component with a fresh inline schema rather than an import of the shared field schema.
- **Fix**: One schema per attribute, shared across every write path.
- **Sources:** [Whittaker: How to Break Software attacks (UAA CS 470 handout)](http://www.math.uaa.alaska.edu/~afkjm/cs470/handouts/breaking.pdf), [Hendrickson: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### FM-M4. Self-reference allowed: the same item chosen on both sides
- **Bug**: A connection can pick the same port as A-end and B-end, a service can be moved to the company it is already in, or a resource can be made its own parent or partner. The UI allows it and the server fails with a vague error, or worse, accepts it.
- **Cause**: Each picker validates on its own. No cross-field rule says A ≠ B, and the second picker's options don't exclude the first selection.
- **Test**: Pick the same item in both pickers, then change the first picker to match the second.
- **Spot**: Two pickers fed by the same query with no filter on the other's value; no `.refine` comparing them.
- **Fix**: Exclude or disable the chosen item in the other picker, and add a cross-field refine that re-runs when either side changes (see FM-F3).
- **Sources:** [Whittaker: How to Break Software attacks (UAA CS 470 handout)](http://www.math.uaa.alaska.edu/~afkjm/cs470/handouts/breaking.pdf)

### FM-M5. Implausible but valid values accepted with no soft confirmation
- **Bug**: A typo such as 100000 Mbps instead of 1000, or quantity 50 instead of 5, sits within the hard limits and goes straight to an order with a very large price change. Nothing says "this is 10 times your current speed".
- **Cause**: Validation has only hard bounds (FM-D12, FM-D13). There is no plausibility tier.
- **Test**: Enter values at about 10 times and 100 times the current or typical value; raise a price by more than an order of magnitude.
- **Spot**: Price-affecting fields with a schema but no warning computed from the change.
- **Fix**: A non-blocking warning, plus a review step that shows the old and new price and asks for an explicit confirm when the change is large.
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [Ministry of Testing: Test Heuristics Cheat Sheet](https://www.ministryoftesting.com/articles/test-heuristics-cheat-sheet)

### FM-M6. A field registers with an undefined `name` or path, and validation crashes in an unhandled rejection
- **Bug**: A form stops validating: errors never show or never clear, the submit button state is stuck, and the console logs an unhandled rejection from inside vee-validate.
- **Cause**: The stack ends in vee-validate's path normaliser (`e.split('.')`), called from `useField`'s computed path while it validates. This happens when a field component mounts before its `name` prop resolves, for example a conditional or dynamically keyed field. A related case: the `useField` value is `undefined` until seeded, so a `.trim()` in a rule throws. **[verify]**: the cause is inferred from the minified stack; check it against source.
- **Test**: Open each form with conditional or dynamically keyed fields (edit connection, create service) on a slow network, so that fields mount before their data. Toggle the condition that adds the field. Watch the console for unhandled rejections.
- **Spot**: `useField(() => props.name)` or `<Field :name="dynamicName">` where the name can be `undefined` or `''`; rules that call string methods on a value that may be `undefined`.
- **Fix**: Don't mount the field until its name is known (`v-if="name"`), give every field a stable string path, and guard rules against `undefined` values.
- **Sources:** [vee-validate: useField API](https://vee-validate.logaretm.com/v4/api/use-field/)

### FM-M7. A zero-based JS month, or the wrong local date, is sent in an API path or query
- **Bug**: The usage or rating view for a month shows the wrong month, or the API returns 400 "Year and month is before the service was created" just after provisioning. A bill run runs for the wrong date.
- **Cause**: `getMonth()` is zero-based, and `new Date()` is local time. Building `/rating/{year}/{month}` or a bill-run date from them sends the wrong month or day. **[verify]**: the cause is inferred from the ticket summaries.
- **Test**: Open the rating or usage view in January and December, on the 1st and the last day of the month, with the OS time zone set to Sydney and to Los Angeles. Check the year and month in the request URL.
- **Spot**: `date.getMonth()` in a URL or query string with no `+ 1`; `new Date().toISOString().slice(0, 10)` for a local date; `getFullYear()` mixed with `getUTCMonth()`.
- **Fix**: Build API dates from `@internationalized/date` (months are one-based) or a tested helper, in the zone the API expects. Add a unit test for January, December and month-end.
- **Sources:** [MDN: Date.prototype.getMonth (zero-based)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getMonth)

---

## N. Load timing, shared state and keyboard side-effects in forms

### FM-N1. Instant-save toggles mixed with Save-button fields in one panel
- **Bug**: In one settings panel, a switch (for example auto-renew or notifications) saves the moment it is flipped, while the text fields beside it wait for Save. The user flips the switch, edits a field, then presses Cancel and expects both to revert, but the switch change is already live. Or the user flips the switch, sees no Save button light up, and leaves unsure whether it saved.
- **Cause**: A switch component calls a mutation on `@update:modelValue`, while the rest of the form uses a vee-validate submit.
- **Test**: Change every control in the panel, press Cancel or navigate away, reload, and compare.
- **Spot**: `useMutation().mutate` inside a Switch or Checkbox `@update:modelValue` that lives inside a `<form>` with its own submit.
- **Fix**: One save model per surface. If a control saves instantly, move it out of the form and give it its own saved feedback.
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### FM-N2. Form bound straight to cached or prop objects: edits leak before Save, and Cancel doesn't revert
- **Bug**: The user edits the service name in a drawer, then presses Cancel. The list behind it already shows the new name, or shows it after the next unrelated re-render, until a refetch. Dirty tracking says "no changes", because the original and current values are the same object.
- **Cause**: `v-model="data.value.name"` on a TanStack query result, `reactive(query.data.value)`, or a child that mutates nested fields of an object prop. Vue's docs warn that a child mutating nested properties of an object prop "allows the child component to affect parent state in a way that isn't obvious". Whether other observers re-render at once depends on vue-query's reactivity wrapping **[verify]**. NV-M6 (persona-url-state) covers only sorting in place, and FM-H4 covers missed dirty state in general, not this cause.
- **Test**: Edit, press Cancel, and look at the list and at other components using the same query. Edit, then trigger a refetch, before and after saving.
- **Spot**: `v-model` on `query.data.value.*` or on `props.item.*`; `reactive(props.x)`; `initialValues: data.value` without a clone.
- **Fix**: Clone into form state (`structuredClone`, or a copy for vee-validate `initialValues`). Write back only through the mutation, then invalidate or `setQueryData` in `onSuccess`.
- **Sources:** [Vue docs: Props, one-way data flow](https://vuejs.org/guide/components/props.html), [Whittaker: How to Break Software attacks (UAA CS 470 handout)](http://www.math.uaa.alaska.edu/~afkjm/cs470/handouts/breaking.pdf)

### FM-N3. Initial data arriving late overwrites what the user already typed
- **Bug**: An edit form renders enabled with empty fields while data loads. The user starts typing, the query resolves, `resetForm({ values })` runs, and their text is replaced. This sits next to FM-H8 (refetch overwrites edits) and FM-G6 (value lost when loading ends); here the very first load clobbers input that was allowed too early.
- **Cause**: Fields are enabled before the load finishes, and a `watch(data, resetForm)` has no dirty guard.
- **Test**: Throttle to Slow 3G, open an edit page, and type at once.
- **Spot**: `watch(() => query.data.value, v => resetForm(...))` without `immediate` handling or a `meta.dirty` guard; fields not disabled while `isPending`.
- **Fix**: Render the form only after the data loads (or show read-only skeletons until then), and never reset dirty fields automatically.
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### FM-N4. "Today" captured once at module load goes stale in a long-lived tab
- **Bug**: A tab left open overnight still treats yesterday as "today": the date picker allows a past start date, the "minimum term start" label is wrong, and the "Today" shortcut picks yesterday. This sits next to FM-J6 (wrong clock or zone) and DS-E8 (persona-value-display) (frozen relative time); the cause here is evaluating the date once at import or setup time.
- **Cause**: `const today = today(getLocalTimeZone())` at module scope, or in `setup()` with nothing to refresh it.
- **Test**: Open the page, move the system clock past midnight (or use a fake timer), and use the date pickers without reloading.
- **Spot**: Module-level `new Date()`, `today()` or `now()` used as a `min` or a default.
- **Fix**: Compute at use time (a computed that depends on a ticking `now`, or evaluate when the picker opens). The server validates again.
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [Hendrickson: Test Heuristics Cheat Sheet](https://web.archive.org/web/2020/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf)

### FM-N5. Async combobox options change under the highlight: Enter picks a different item
- **Bug**: In a server-searched location or port picker, the user types "syd", arrows to the third result, and presses Enter just as the next response lands. The item selected is whatever is now third, not the one they saw.
- **Cause**: The highlight is kept as an index while the options array is replaced. This differs from NV-I3 (persona-url-state), where stale results overwrite newer ones: here the results are fresh, but the highlight doesn't follow the item. Whether Reka Combobox keys its highlight by value or by index in this situation is **[verify]** against the installed version.
- **Test**: Add 300 to 800 ms of latency with random jitter. Type, arrow down, and press Enter at the moment the list refreshes. Repeat with fast typing.
- **Spot**: A custom highlight `ref<number>` reset or kept across `options` changes; options rebuilt with new object identities on every fetch.
- **Fix**: Track the highlight by item key, and reset or re-find it when the options change. Ignore Enter while a response is in flight, or confirm the selection against the label shown.
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### FM-N6. Late content shifts the layout just before a click, so the click hits a different button
- **Bug**: A banner, price row or validation message appears above the action row as the user clicks. "Confirm" moves down, and the click lands on "Terminate service" or on a different row's action. DS-B10 (persona-value-display) covers the shift itself; this item covers the wrong action that results.
- **Cause**: Async content inserted above interactive controls without reserved space.
- **Test**: Throttle the network and click actions just as secondary queries (pricing, notices, feature flags) resolve. Look for destructive buttons next to slots that load content.
- **Spot**: `v-if="data"` blocks rendered above action buttons with no skeleton of the same height; destructive and primary actions side by side.
- **Fix**: Reserve space, put late content below the actions, keep destructive actions apart, and confirm destructive actions.
- **Sources:** [web.dev: Cumulative Layout Shift](https://web.dev/articles/cls), [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

### FM-N7. Opening and closing a dialog repeatedly stacks global listeners
- **Bug**: After opening and closing a drawer 10 times, one Esc closes two layers, a keyboard shortcut fires 10 times, one save shows 10 toasts, or typing gets sluggish.
- **Cause**: `window.addEventListener` or `document.addEventListener` in `onMounted` or a `watch` with no matching removal; a `setInterval` with no clear; an event-bus subscription in a component that remounts.
- **Test**: Open and close each modal and drawer 20 times, then press Esc, use shortcuts, and save once. Check DevTools > Elements > Event Listeners, or take a heap snapshot.
- **Spot**: `addEventListener` with no removal in `onBeforeUnmount` or `onScopeDispose` (prefer `useEventListener` from VueUse); listeners added inside `watch` callbacks.
- **Fix**: Pair every add with a remove on scope dispose, or use composables that clean up for you.
- **Sources:** [Whittaker: How to Break Software attacks (UAA CS 470 handout)](http://www.math.uaa.alaska.edu/~afkjm/cs470/handouts/breaking.pdf)

### FM-N8. A parent widget's keydown handler swallows Space or another key inside an editable field
- **Bug**: The user cannot type a space in a text field that sits inside a row, card, accordion or drag handle. Pressing Space toggles, expands or selects the parent instead.
- **Cause**: The parent's `keydown` listener calls `preventDefault()` on Space or Enter for its own activation, and the event bubbles up from the nested input. This is close to FM-K9 (shortcut collisions) and IN-A6 (persona-text-input), but the trigger is plain typing inside a composite widget.
- **Test**: In every editable field nested inside a clickable or draggable container, type a sentence with spaces, press Enter, and use the arrow keys.
- **Spot**: `@keydown.space.prevent` or `@keydown.enter.prevent` on a container that holds inputs; a handler with no check for `event.target` being editable.
- **Fix**: In the parent handler, return early when the target is an input, textarea, select or contenteditable, or stop propagation in the field. Don't nest editable fields inside elements with their own key handling where it can be avoided.
- **Sources:** [MDN: Event.preventDefault](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault), [WAI-ARIA APG: Developing a keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)

### FM-N9. Partial failure of a bulk action is reported as all-success or all-failure
- **Bug**: The user bulk-deletes or bulk-renews 10 items, and 2 fail. The UI says "10 items updated", or shows one generic error while 8 changes actually went through, so the user retries and hits duplicates or "not found".
- **Cause**: `Promise.all` rejects on the first failure and drops the results of the others, or the per-item results are never inspected.
- **Test**: Mock one in N requests to fail (403, 409, 500) in a bulk action. Also try all failing and none failing.
- **Spot**: `await Promise.all(ids.map(mutateAsync))` with one toast; no per-item result handling.
- **Fix**: Use `Promise.allSettled`, then show a summary ("8 updated, 2 failed: …") that keeps the failed items selected for retry, and invalidate the list either way. One summary toast, not one per item (see DS-K2 (persona-value-display)).
- **Sources:** [MDN: Promise.allSettled()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled), [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf)

---

## O. Wizard and stepper flows

### FM-O1. Later steps reachable by URL with earlier steps incomplete
- **Bug**: Opening `/order/port/step-4` directly shows a review with empty data, or submits an incomplete order. NV-B6 (persona-url-state) is the opposite problem: a wizard on one URL.
- **Cause**: Each step is its own route with no guard that checks the earlier steps are complete.
- **Test**: Copy the URL of a late step, open it in a new tab or after a reload, and try to continue and submit. Also try the URL of a step that a condition should skip.
- **Spot**: Step routes with no `beforeEnter` or `beforeEach` check; a review step that reads store values without checking they exist.
- **Fix**: A `beforeEnter` or `beforeEach` guard redirects to the first incomplete step (guard against loops), and the whole order is validated on final submit. Note that `beforeEnter` doesn't re-run on param-only changes between steps.
- **Sources:** [Vue Router: Navigation guards](https://router.vuejs.org/guide/advanced/navigation-guards.html)

### FM-O2. Going back loses entered data
- **Bug**: Browser Back or the step's Back link returns to a cleared step, or a Back that changes nothing still wipes later steps. FM-H10 is re-entry of the same data.
- **Cause**: Form state lives in each step component and is destroyed on unmount.
- **Test**: Fill steps 1 to 3, go back to step 1 with browser Back and with the Back link, change nothing, then go forward. Then change one answer and go forward.
- **Spot**: `useForm()` inside each step component; step components rendered with `v-if` and no shared store; a watcher that resets later steps on any change.
- **Fix**: Keep one form state above the steps. Back returns the user to a step "in the state they last saw it". Clear dependent answers only when the value actually changed, and say so.
- **Sources:** [GOV.UK Design System: Question pages](https://design-system.service.gov.uk/patterns/question-pages/), [W3C WAI: Multi-page forms](https://www.w3.org/WAI/tutorials/forms/multi-page/)

### FM-O3. Progress indicator wrong
- **Bug**: "Step 3 of 5" when a conditional step is skipped, or ticks on steps that are not finished.
- **Cause**: The step list is a fixed array, and "complete" means "visited".
- **Test**: Take each branch that skips or adds a step, and compare the indicator with the steps actually shown. Visit a step, leave it invalid, and check its tick.
- **Spot**: A hard-coded `steps` array and `totalSteps` constant; completion set on navigation rather than on validation.
- **Fix**: Derive the steps from the current answers (or use `<progress>` when the count varies). Mark completed and current steps with visually hidden "Completed:" and "Current:" text, and link completed steps.
- **Sources:** [W3C WAI: Multi-page forms](https://www.w3.org/WAI/tutorials/forms/multi-page/)

### FM-O4. Step change not reflected in the title or heading
- **Bug**: After Next on the same route, the page title and heading don't change, and screen reader users don't learn that the step changed. NV-E5 (persona-url-state) covers route navigation.
- **Cause**: The step changes inside one component, so the router's title and focus handling never runs.
- **Test**: Step through the wizard with a screen reader on; check the tab title at each step.
- **Spot**: A `currentStep` ref with no `document.title` update and no focus move.
- **Fix**: Update the title to "Step 2 of 4: Choose bandwidth – …" and the h1, and move focus to the heading **[verify]**: the focus target is common practice, not stated in the source.
- **Sources:** [W3C WAI: Multi-page forms](https://www.w3.org/WAI/tutorials/forms/multi-page/)

### FM-O5. The order summary or price is a one-time copy and goes stale after an earlier answer changes
- **Bug**: The user goes back from Review to change the speed or term. The review or summary panel still shows the old monthly price, or the line items update but the total doesn't. This differs from DS-C5 (persona-value-display) (counts disagree): this is derived money or configuration that was copied, not computed.
- **Cause**: `const total = ref(calc(props.config))` or `ref(props.price)`. Vue's docs say a ref initialised from a prop "is disconnected from future prop updates". Or the summary is written to a store on entering the step and never recomputed. Or the price query key leaves out an input the price depends on.
- **Test**: In a wizard, go to Review, go back, change each price-affecting input, and return. Compare the summary, the line items, the API quote, and the submitted payload.
- **Spot**: `ref(props.x)` or `ref(compute(...))` where `computed` was intended; summaries in store state written on step enter; a price `queryKey` missing one of the inputs the price depends on.
- **Fix**: Use `computed` from a single source of truth. Put every variable the price depends on in the query key, build the review from current state, and block submit while the quote is stale (compare NV-I4 (persona-url-state) and FM-O7).
- **Sources:** [Vue docs: Props, one-way data flow](https://vuejs.org/guide/components/props.html), [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [TanStack Query: Query keys](https://tanstack.com/query/latest/docs/framework/vue/guides/query-keys)

### FM-O6. "Change" on the review page forces the whole flow again
- **Bug**: After changing the bandwidth from the review page, the user must click through every later step to get back to Review.
- **Cause**: "Change" links to the step with no return target, so Next continues the normal sequence.
- **Test**: From Review, use each "Change" link, change a value, and count the steps back to Review.
- **Spot**: "Change" links with no `?returnTo=review` (or similar); a Next handler that always goes to `step + 1`.
- **Fix**: "Change" returns to the check page after saving. Ask any new dependent questions first, and keep earlier answers filled in.
- **Sources:** [GOV.UK Design System: Check answers](https://design-system.service.gov.uk/patterns/check-answers/)

### FM-O7. Final submit enabled before the quote for the current inputs has loaded
- **Bug**: Order is clicked while the quote is loading, so the order goes in at an old price or with `price: undefined`. FM-A9 is Enter during a lookup.
- **Cause**: A disabled or loading dependent query (`status: 'pending'`) is not reflected in the button.
- **Test**: Throttle the network, change a price-affecting input on the last step, and click Order at once. Inspect the payload.
- **Spot**: `:disabled="!meta.valid"` on the Order button with no check on the quote query's state; the payload reads `quote.value?.price`.
- **Fix**: Block submit, with a reason, until the quote matches the current inputs, and send the quote id.
- **Sources:** [TanStack Query: Dependent queries](https://tanstack.com/query/latest/docs/framework/vue/guides/dependent-queries)

### FM-O8. A blocking prerequisite or permission is checked only at the last step
- **Bug**: The user configures a service across several wizard steps, then the Review or Order step says the company has no billing market for that region, an agreement is unsigned, or the request fails with 403 because the user has a read-only role. All the configuration work is wasted.
- **Cause**: Eligibility and permission are checked only by the final create call or the last step's query.
- **Test**: Use an account missing each prerequisite (no billing market, read-only role, no contract, suspended account) and start each order flow.
- **Spot**: Permission or eligibility queries used only in the last step's component; a server 4xx on order create as the only check.
- **Fix**: Check prerequisites and permission on wizard entry, and show the blocker before step 1 with a link to fix it. Map a 403 to "you don't have permission to …" and don't offer to sign in again, because that won't help (see RS-A4 (persona-resilience) and NV-Q1 (persona-url-state)).
- **Sources:** [Kaner et al.: Common Software Errors](https://web.archive.org/web/2015/http://www.testingeducation.org/BBST/testdesign/kaner_common_software_errors.pdf), [MDN: 403 Forbidden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

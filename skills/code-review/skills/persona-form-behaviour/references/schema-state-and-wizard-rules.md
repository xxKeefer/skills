# Schema, form state, and wizard rules (15 to 20)

**Schemas and field registration**

15. **`z.coerce.number()` on a form field (Change Requested).** `Number('')` is 0, so a cleared required quantity or speed passes "required" and saves 0, or shows "must be at least 1" instead of "required". A field holding only spaces also becomes 0. Preprocess `''` and `null` to `undefined` before `z.number()`, or validate the string and then transform it. Don't flag coercion of a value that never comes from an input, such as a constant. (FM-M1)
16. **`.optional()` on a string format bound to an input (Change Requested).** Inputs emit `''`, and `.optional()` allows only `undefined`. So `z.string().email().optional()` shows "Invalid email" once the user types into an optional field and clears it, and it blocks submit. Accept `''` (`z.literal('').or(…)`) or preprocess it to `undefined`. Don't flag a schema whose input never emits `''`. What to send for an empty field (`null`, omitted, or `''`) → `persona-api-integrity`. (FM-M2)
17. **A field registered with an undefined `name` (Change Requested).** `useField(() => props.name)` or `<Field :name="…">` where the name can be `undefined` or `''`, such as a field that mounts before its data loads. vee-validate's path code then throws during validation, so errors never show or clear and the submit state sticks. A rule that calls `.trim()` on a value that can be `undefined` fails the same way. Mount the field only once its name is known (`v-if="name"`), and guard rules against `undefined`. Don't flag a name that is a string literal or a required string prop. (FM-M6)

**Form state and keyboard side effects**

18. **Form bound straight to query data or a prop (Change Requested).** `v-model` on `query.data.value.*` or `props.item.*`, `reactive(props.x)`, or `initialValues: data.value` with no copy. Edits show in the list behind the dialog before Save, Cancel doesn't undo them, and dirty tracking reports no change because both sides are the same object. Copy into form state (`structuredClone`) and write back only through the mutation. Don't flag a read-only display. A prop mutated outside a form → `persona-code-quality` #5. (FM-N2)
19. **Parent key handler swallows typing in a nested field (Change Requested).** `@keydown.space.prevent` or `@keydown.enter.prevent` on a row, card, accordion, or drag handle that contains an input, with no check that the event target is editable. The user can't type a space in the field. Return early when the target is an input, textarea, select, or `contenteditable` element. Don't flag a container with no editable children. (FM-N8)

**Wizards**

20. **A later wizard step opens by URL with earlier steps incomplete (Change Requested).** Each step is its own route with no `beforeEnter` or `beforeEach` check, or the review step reads store values without checking they exist. Opening `/order/port/step-4` in a new tab shows an empty review or submits an incomplete order. Redirect to the first incomplete step (and guard against loops), and validate the whole order on final submit. Don't flag a wizard whose steps share one URL. (FM-O1)

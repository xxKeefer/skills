# Fixtures: boundary values and the per-form smoke script

Test data for this lane's catalogue. Cite a value from here as the failing input in a finding, or type it into the running app.

## Boundary values for any bounded number or length

For a field with lower bound `min` and upper bound `max` (value or length), try all of these. Take the bounds from the zod/yup schema, the OpenAPI spec, and the error copy. Check that all three agree (FM-D13, FM-E1).

| Value | Expect | Catches |
| --- | --- | --- |
| `min - 1` | rejected, with a message naming the bound | missing min, `<` versus `<=` (FM-D14) |
| `min` | accepted | exclusive bound where the copy says inclusive |
| `min + 1` | accepted | |
| `max - 1` | accepted | |
| `max` | accepted | off-by-one, message says one number and the rule enforces another |
| `max + 1` | rejected while typing or on blur, not only at checkout | min/max applied too late (FM-D12) |
| empty, `' '` | required error, not `0` | `v-model.number` empty is `''` (FM-D2), whitespace-only (IN-B1 (persona-text-input)) |
| `0`, `-0`, `-1` | as the domain says | falsy zero (FM-D3), negative zero (FM-D4) |

Other number inputs, from the forms research: `1e3, 1e309, '1,5', '1.5', '1.50', '01', '007', '+5', '--5', '5-', '.5', '5.', 'NaN', 'Infinity', 9007199254740991, 9007199254740993, 0.1+0.2 → 0.30000000000000004, 1.005, '١٢٣' (Arabic-Indic digits), '１２３' (full-width digits), paste '1 000', paste '$100'`.

For lengths, run `max` and `max + 1` twice: once in ASCII and once with emoji (`👨‍👩‍👧‍👦` counts as 11 UTF-16 units), because `maxlength` and `.length` count UTF-16 code units (IN-C1 (persona-text-input)).

## Per-form smoke script (about five minutes)

1. Open the form untouched. There should be no errors. Tab through: the order is logical and every focus is visible.
2. Press Enter in the first field. Check which action fires (submit, nothing, or something wrong).
3. Submit empty. Focus moves to the summary or the first error, and the errors are specific and announced.
4. For each field: try whitespace-only, max+1 length (with emoji), the boundary values above, `e`/`-0`/`1,5`, and an invalid date (`31/02`).
5. Fix one error without leaving the field. The error clears. Fix a cross-field pair from the other side.
6. Throttle to Slow 3G and double-click Submit. There should be one request. Make the API fail with a 500, then a 422: the button re-enables and the 422 maps to the field.
7. Edit, then press Esc in the dialog, click outside, press Back, click a nav link, and close the tab. Each time, the data survives or the app asks before discarding it.
8. Save, then navigate. There should be no false "unsaved" prompt. Reopen: the form is fresh and has no stale errors.
9. Change a controlling field (type, metro) and check the stale dependent values in the payload.
10. Switch locale (en, de, ja) and timezone (Sydney, LA, Kiritimati). Re-run the number and date steps.

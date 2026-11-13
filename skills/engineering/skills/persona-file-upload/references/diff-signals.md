# persona-file-upload diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-file-upload catalogue](catalogue.md)

- UP-A1: `z.instanceof(File).refine(f => f.size <= MAX)` or a size check with no `file.size === 0` lower bound → Reject `size === 0` with "The selected file is empty" [default: change-requested] (rule 2)
- UP-A2: Size limit as magic numbers in two places, help text and code limits disagreeing, or a 413 handler calling `response.json()` → One shared byte constant, client pre-check, tolerate non-JSON bodies [default: nit] (rule 2)
- UP-A3: `file.type === 'text/csv'` (or another single MIME compare) as the only type check → Allowlist several MIME types and extensions; server is the authority [default: change-requested] (rule 1)
- UP-A4: `name.endsWith('.pdf')` without lowercasing, `name.split('.')[1]`, or `includes('.csv')` as the extension check → Lowercase the segment after the last dot before comparing [default: change-requested] (rule 1)
- UP-A5: `<input type="file" accept=".pdf">` with no type check in the `@change` and `@drop` handlers → Validate type in code on both picker and drop paths [default: nit] (rule 1)
- UP-A6: `URL.createObjectURL(file)` `<img>` preview with no `@error` fallback, or an image allowlist with no answer for `image/heic` → Add a preview fallback; allow HEIC or reject it specifically [default: nit]
- UP-A7: New design-system image upload component with no `accept` prop, or `accept` including `image/svg+xml` or `.svg`, for an image other users see → Pass `accept` without SVG, or sanitise or rasterise on the server [default: change-requested] (rule 3)
- UP-B1: Remove or error handler on a custom `<input type="file">` that clears the Vue ref but not `inputRef.value.value = ''` → Reset `input.value = ''` after reading and on remove [default: change-requested] (rule 4)
- UP-B2: `selected.value = e.target.files[0]` with no empty `FileList` guard, or no `@cancel` handler on the input → Handle `cancel`; ignore an empty `FileList` when a file is chosen [default: nit] (rule 4)
- UP-B3: `@drop.prevent` only on the zone, with no window-level `dragover`/`drop` guard while the upload view is mounted → Window listeners cancelling file drops when `item.kind === 'file'` [default: nit] (rule 5)
- UP-B4: Drop highlight driven by `@dragleave="isOver = false"` or a boolean toggled on `dragenter`/`dragleave` → Use `useDropZone`, or an enter and leave counter [default: nit] (rule 5)
- UP-B5: `e.dataTransfer.files[0]` with no count check or folder check (`webkitGetAsEntry().isDirectory`) → Reject extra files and folders with a specific message [default: change-requested] (rule 5)
- UP-C1: `await api.upload(file)` with no `AbortController` `signal` wired to Cancel, and no progress handler on a large upload → Wire Cancel to `abort()`; XHR `upload.onprogress` for percent done [default: change-requested] (rule 6)
- UP-C2: A `File` inside `useStorage`, a persisted store, a query key, or `JSON.parse(JSON.stringify(values))` → Keep `File` in a `shallowRef`; persist only the server ID [default: change-requested] (rule 7)
- UP-C3: Upload mutation with no `invalidateQueries` in `onSuccess`, or an optimistic row pushed with no dedupe by server ID → Invalidate the list and replace the optimistic row by ID [default: nit] (rule 7)
- UP-C4: File chip with no `min-w-0 truncate`, or the server's file list matched back to the local `file.name` → Middle-truncate keeping the extension; key uploads by server ID [default: nit] (rule 8)
- UP-D1: `split('\n')`, `split('\r\n')`, `split(',')` or a regex split in CSV import code, or an exact header compare with no BOM strip → A real CSV parser; strip the BOM; skip empty lines [default: change-requested] (rule 9)
- UP-D2: `errors.map((e, i) => ...)` using the array index as the row number, or a bare "Import failed" message → Report the 1-based file line, column and value [default: nit] (rule 10)

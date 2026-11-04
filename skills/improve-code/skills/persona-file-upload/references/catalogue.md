# persona-file-upload catalogue: file upload and CSV import

Scope: file pickers, drop zones, uploads (documents, images, attachments), and CSV import in a Vue 3 and TypeScript single-page app (SPA) built on Reka UI, vue-router, TanStack Query, and vue-i18n.

Each item has a **Bug** (what the user sees), **Cause**, **Test** (files and steps), **Spot** (what to look for in a diff), **Fix**, and **Sources**. The test files live in `fixtures.md`.

`[uncertain]` marks a claim the cited source doesn't fully back. Check it before you rely on it.

---

## A. File checks

### UP-A1. Empty (0-byte) file accepted
- **Bug:** The upload "succeeds", then the server fails to parse it, or an empty document or CSV is stored.
- **Cause:** Only the type and maximum size are checked, never `file.size === 0`.
- **Test:** `touch empty.csv` and upload it; an empty file renamed to `.pdf`.
- **Spot:** `z.instanceof(File).refine(f => f.size <= MAX)` with no lower bound.
- **Fix:** Reject `size === 0` with "The selected file is empty".
- **Sources:** [GOV.UK Design System: File upload](https://design-system.service.gov.uk/components/file-upload/)

### UP-A2. Size limit checked only on the server, or with a mismatched unit
- **Bug:** The user waits for a 200 MB upload, then gets a 413 with a generic error. Or the help text says "10 MB", the code checks `10 * 1000 * 1000`, and the proxy limit is smaller again.
- **Cause:** No client pre-check; MB versus MiB; the proxy's body limit differs from the app's; the 413 body is HTML or empty, so `response.json()` throws.
- **Test:** Files exactly at the limit, at the limit plus 1 byte, and above the proxy limit.
- **Spot:** Magic size numbers in two places; an error handler that assumes a JSON body.
- **Fix:** One shared constant, a client pre-check, a readable size in the message ("must be smaller than 10 MB"), and tolerance for non-JSON error bodies.
- **Sources:** [GOV.UK: File upload](https://design-system.service.gov.uk/components/file-upload/), [MDN: 413 Content Too Large](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/413), [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

### UP-A3. Type check trusts `file.type` or the extension
- **Bug:** A PNG renamed `invoice.pdf` passes, then preview or processing fails. A valid file is rejected because `file.type` is `""` (an uncommon or missing extension), or because Windows maps `.csv` to an unexpected MIME type.
- **Cause:** `file.type` comes from the extension, not from the bytes.
- **Test:** Rename a `.png` to `.pdf`; a file with no extension; a CSV picked on Windows.
- **Spot:** `file.type === 'text/csv'` as the only check.
- **Fix:** Accept several MIME types and extensions, sniff magic bytes where it matters, and treat the server as the authority.
- **Sources:** [MDN: Blob/File.type](https://developer.mozilla.org/en-US/docs/Web/API/File/type), [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

### UP-A4. Uppercase or double extension handled wrongly
- **Bug:** `SCAN.PDF` or `Report.Csv` is rejected, while `scan.pdf.exe` is accepted.
- **Cause:** A case-sensitive `endsWith`, or a substring match such as `includes('.pdf')`.
- **Test:** `A.PDF`, `a.Pdf`, `a.pdf.exe`, `a.`, `.pdf`, `a..pdf`.
- **Spot:** `name.endsWith('.pdf')`, `name.split('.')[1]`, `includes('.csv')`.
- **Fix:** Take the segment after the last dot only, and lowercase it before comparing.
- **Sources:** [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

### UP-A5. `accept` attribute treated as validation
- **Bug:** The user switches the picker to "All files", or drags a file in, and the wrong type gets through.
- **Cause:** `accept` is only a hint to the file picker.
- **Test:** Pick with "All files"; drag an `.exe` onto the drop zone.
- **Spot:** `<input type="file" accept=".pdf">` with no check in the change and drop handlers.
- **Fix:** Validate in code on both the picker and drop paths, and on the server.
- **Sources:** [MDN: HTML attribute accept](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept)

### UP-A6. HEIC/HEIF photos from an iPhone
- **Bug:** A photo of a signed form is rejected, or it is accepted but the preview is broken in Chrome, Edge, and Firefox.
- **Cause:** Only Safari (17 and later) decodes HEIF; `image/heic` is missing from the allowlist; the preview has no error fallback.
- **Test:** Upload a `.heic` in Chrome and in Safari.
- **Spot:** A `URL.createObjectURL(file)` `<img>` preview with no `@error`.
- **Fix:** Allow it and convert on the server, or reject it with a specific message. Add a preview fallback.
- **Sources:** [Can I use: HEIF/HEIC](https://caniuse.com/heif)

### UP-A7. SVG accepted where a raster image is meant
- **Bug:** A logo, avatar, or branding field takes an SVG. The SVG carries a `<script>` or an external reference, and when the app later serves it from its own origin or puts the markup inline, the script runs for every user who sees it.
- **Cause:** A design-system image upload component may accept `image/svg+xml` by default, so a new picker with no `accept` prop takes SVG. An SVG is a document, not a picture: browsers turn off its script and external loads only while it's shown through `<img>` or a CSS background. Opened directly, or through `<object>`, `<iframe>`, `<embed>`, or inline markup, it runs.
- **Test:** Upload an SVG that contains `<script>alert(document.domain)</script>` and an `<image href="https://example.com/x.png">`. Open the stored file's URL directly, and check every place the image is shown.
- **Spot:** A new design-system image upload component with no `accept` prop, or an `accept` list that includes `image/svg+xml` or `.svg`, for an image other users see.
- **Fix:** Drop SVG from `accept` for raster uses. If SVG is needed, sanitise it or convert it to a raster image on the server, and serve uploads from a separate origin. Rendering the markup through `v-html` is a separate sink (persona-security).
- **Sources:** [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), [MDN: SVG as an image](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)

---

## B. Picker and drop zone

### UP-B1. Re-selecting the same file does nothing
- **Bug:** An upload fails, the user picks the same file again, and nothing happens.
- **Cause:** Re-selecting the same file fires `cancel`, not `change`. The handler only listens to `change`, and the input still holds the old value.
- **Test:** Pick file A, remove it in the UI (or let the upload fail), then pick A again.
- **Spot:** A "remove" handler that clears the Vue ref but not `inputRef.value.value = ''`.
- **Fix:** Reset `input.value = ''` after reading the files and on remove.
- **Sources:** [MDN: HTMLInputElement cancel event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/cancel_event), [MDN: change event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event)

### UP-B2. Cancelling the picker is not handled
- **Bug:** The user reopens the picker and presses Esc or Cancel. Depending on the browser, the existing selection is cleared, or the UI stays in a "choosing" state (a spinner or an open overlay) that never ends. [uncertain: per-browser clearing behaviour]
- **Cause:** Only `change` is handled; `cancel` is ignored.
- **Test:** Pick a file, reopen the dialog, and Cancel, in Chrome, Firefox, and Safari.
- **Spot:** `selected.value = e.target.files[0]` with no empty guard; no `@cancel`.
- **Fix:** Handle `cancel`, and ignore an empty `FileList` when a file is already chosen.
- **Sources:** [MDN: HTMLInputElement cancel event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/cancel_event)

### UP-B3. A file dropped outside the drop zone navigates away
- **Bug:** The user misses the zone, the browser opens the PDF in the tab, and the half-filled order is lost.
- **Cause:** No window-level `dragover` and `drop` handler calling `preventDefault`.
- **Test:** Drag a PDF onto the page header instead of the zone.
- **Spot:** `@drop.prevent` only on the zone.
- **Fix:** While the upload view is mounted, add window listeners that cancel file drops (only when `item.kind === 'file'`, so link drags still work), and set `dropEffect = 'none'` outside the zone.
- **Sources:** [MDN: File drag and drop](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop)

### UP-B4. Drop zone highlight flickers or sticks
- **Bug:** The highlight flickers when dragging over child elements, and stays on after dragging back out of the window.
- **Cause:** `dragenter` and `dragleave` fire for each child element, and `dragstart` and `dragend` don't fire for files dragged in from the OS, so a boolean toggle drifts.
- **Test:** Drag slowly across the zone's icon and text; drag in, then out of the browser window.
- **Spot:** `@dragleave="isOver = false"`.
- **Fix:** An enter and leave counter, or a `relatedTarget` and `contains` check. Reset on `drop`.
- **Sources:** [MDN: dragleave event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dragleave_event), [MDN: File drag and drop](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop)

### UP-B5. Several files or a folder dropped where one is allowed
- **Bug:** Dropping three files silently keeps the first. Dropping a folder gives an odd 0-byte "file".
- **Cause:** `dataTransfer.files[0]` with no count check or directory check.
- **Test:** Drop three files; drop a folder; drop more than the maximum on a `multiple` input.
- **Spot:** `e.dataTransfer.files[0]`.
- **Fix:** Reject with "You can only select up to N files", and detect folders with `webkitGetAsEntry().isDirectory`.
- **Sources:** [GOV.UK: File upload](https://design-system.service.gov.uk/components/file-upload/), [MDN: webkitGetAsEntry](https://developer.mozilla.org/en-US/docs/Web/API/DataTransferItem/webkitGetAsEntry)

### UP-B6. File input not reachable or not announced
- **Bug:** A styled `<div>` "Upload" can't be reached with Tab, the real input is `display:none`, the chosen filename and errors aren't announced, and voice users can't activate it.
- **Cause:** The native input is hidden completely and replaced by a non-interactive element with a click handler.
- **Test:** Keyboard only; VoiceOver after choosing a file; voice control ("click Upload").
- **Spot:** `<input type=file class="hidden">` with `@click="input.click()"` on a non-button.
- **Fix:** A visually hidden but focusable input, or a real `<button>`. Announce the filename and errors, and keep the button text short.
- **Sources:** [GOV.UK: File upload (accessibility notes)](https://design-system.service.gov.uk/components/file-upload/)

---

## C. Upload progress, state and file names

### UP-C1. No progress or cancel on large uploads
- **Bug:** A 20 MB upload shows an endless spinner with no cancel. Or "Cancel" hides the UI while the request keeps going and later attaches the file anyway.
- **Cause:** `fetch` gives no upload progress, and no `AbortController` is wired to Cancel.
- **Test:** Slow 3G, a 20 MB file, press Cancel, then check the network tab and the server record.
- **Spot:** `await api.upload(file)` with no `signal` and no progress handler.
- **Fix:** Use XHR (`xhr.upload` progress events) with percent done and a working cancel that aborts the request. NN/g: waits over 10 seconds need percent done and a way to interrupt.
- **Sources:** [MDN: XMLHttpRequestUpload progress event](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequestUpload/progress_event), [NN/g: Response Times, the 3 important limits](https://www.nngroup.com/articles/response-times-3-important-limits/)

### UP-C2. `File` object stored in serialised state
- **Bug:** After a reload or a step change, the form says a file is attached, but the payload holds `{}`.
- **Cause:** `File` has no enumerable own properties, so `JSON.stringify` gives `{}`. This happens with localStorage-backed state, query keys, and JSON-cloned form state.
- **Test:** Attach a file, move between wizard steps, reload, and inspect the request.
- **Spot:** A `File` inside `useStorage`, a query key, or `JSON.parse(JSON.stringify(values))`.
- **Fix:** Keep the `File` in a `shallowRef` outside persisted state, and persist only the uploaded ID.
- **Sources:** [MDN: JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)

### UP-C3. Upload success doesn't refresh the list, or shows the item twice
- **Bug:** The new document doesn't appear until reload, or appears twice (the optimistic row plus the refetched row).
- **Cause:** The mutation doesn't invalidate the list query, or an optimistic row is added and never replaced by the server row.
- **Test:** Upload a file and watch the list without reloading; upload two in quick succession.
- **Spot:** No `invalidateQueries` in `onSuccess`; an optimistic push with no dedupe by ID.
- **Fix:** Invalidate the list, and return the promise so the mutation stays pending until the refresh lands. Replace the optimistic row by ID.
- **Sources:** [TanStack Query: Invalidations from mutations](https://tanstack.com/query/latest/docs/framework/vue/guides/invalidations-from-mutations)

### UP-C4. Long, unusual or unicode filename breaks the file chip or the server
- **Bug:** A 200-character name pushes "Remove" off the card. `报价单 (最终版).pdf`, a name with `:`, or a name starting with `.` or `-` is rejected or mangled by the server. Long text in general is DS-A1 and DS-A6 (persona-value-display), and filenames built from user text are IN-H4 (persona-text-input); this item covers the upload chip and the round trip.
- **Cause:** No truncation on the chip, and the server sanitises names differently from how the client displays them.
- **Test:** A 255-byte name, emoji, RTL text, `a:b.pdf`, `-x.pdf`, `..pdf`.
- **Spot:** A file chip with no `min-w-0 truncate`; the server's file list matched to the local `file.name`.
- **Fix:** Middle-truncate and keep the extension, key uploads by server ID, and let the server generate its own storage name.
- **Sources:** [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

---

## D. CSV import

### UP-D1. CSV import breaks on BOM, delimiter, CRLF, or blank lines
- **Bug:** The first header reads `﻿name` and doesn't match "name". A European Excel export uses `;` and parses as one column. `\r` stays on the last field. A trailing blank line gives an "empty row" error. CSV export is covered by IN-H2 and IN-H3 (persona-text-input).
- **Cause:** A hand-written `split('\n').map(l => l.split(','))`.
- **Test:** CSV UTF-8 from Excel (with BOM), de-DE Excel (`;`), Windows CRLF, a trailing newline, and quoted fields that hold commas and newlines.
- **Spot:** `split('\n')`, `split(',')`, or a regex-based CSV parser in import code.
- **Fix:** A real parser with delimiter auto-detection and `skipEmptyLines`. Strip the BOM explicitly (Papa Parse exposes `BYTE_ORDER_MARK` but its docs don't say it strips it, so verify).
- **Sources:** [Papa Parse docs](https://www.papaparse.com/docs)

### UP-D2. Import errors don't say which row
- **Bug:** "Import failed" for a 500-row CSV, or row numbers are off by one (0-based, or the header not counted).
- **Cause:** Errors are reported without a location, or with the array index as the row number.
- **Test:** Put a bad value on file line 37 and check that the message says line 37.
- **Spot:** `errors.map((e, i) => ...)` using the array index as the row number.
- **Fix:** Report the 1-based file line, the column, and the value, and keep the user's file so they can fix it and retry.
- **Sources:** [NN/g: Error-message guidelines](https://www.nngroup.com/articles/error-message-guidelines/)

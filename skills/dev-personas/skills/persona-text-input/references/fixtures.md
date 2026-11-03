# Fixtures: strings to paste into text fields

Test data for this lane's catalogue. Cite a value from here as the failing input in a finding, or type it into the running app. Strings in the tables and code blocks are byte-exact. Some hold invisible characters: non-breaking space (NBSP), zero-width space (ZWSP), byte order mark (BOM), zero-width joiner (ZWJ), and right-to-left (RTL) override. Copy them, don't retype them.

## Strings to paste into every text field a change touches

Paste each one into every text field the diff touches. Where a character is invisible, the row names it (in brackets or in the last column). Copy the string from this file; never retype it.

| # | Input | What it probes |
| --- | --- | --- |
| T1 | `   ` (three spaces) | whitespace-only passes "required" |
| T2 | `  Acme  ` | trim on save and on compare |
| T3 | `Acme Corp` (NBSP) | NBSP not caught by naive `/ /` or `.split(' ')` |
| T4 | `Acme​Corp` (ZWSP), `﻿` (BOM), `‍` (ZWJ) | invisible chars in names, IDs, uniqueness |
| T5 | `line1\nline2` pasted into a single-line input | newline stripped silently or kept by programmatic set |
| T6 | `It’s “quoted”` and `don’t` | smart quotes from macOS/Word |
| T7 | `👍🏽`, `👨‍👩‍👧‍👦`, `🇦🇺` | `length` vs graphemes vs `maxlength`, truncation splits surrogates |
| T8 | `é` as `é` vs `é` | NFC/NFD: duplicates, search misses, length differences |
| T9 | `‮gnp.exe` and `abc‮def` | RTL override flips rendering |
| T10 | `مرحبا 123 Port` | bidi mixing in tables, truncation, ellipsis side |
| T11 | `<img src=x onerror=alert(1)>` | `v-html`, markdown, i18n HTML |
| T12 | `{{ 7*7 }}`, `{0}`, `{name}`, `@:foo`, `%s` | vue-i18n / interpolation of user text |
| T13 | `=1+1`, `+1`, `-1`, `@SUM(A1)`, `=HYPERLINK("http://x","click")` | CSV/formula injection on export |
| T14 | `１２３` (full-width), `١٢٣` (Arabic-Indic) | number parsing |
| T15 | `1,000.50`, `1.000,50`, `$1,000`, `1 000` (NBSP or U+202F thousands sep) | number paste |
| T16 | `Ⱥ` (changes length when lowercased), `ß` → `SS`, Turkish `İ` | case folding |
| T17 | `Zalgo: Z̮̞̠͙͔ͅḀ̗̞͈̻̗Ḷ͙͎̯̹̞͓G̻O̭̗̮` | vertical overflow, row height |
| T18 | `null`, `undefined`, `NaN`, `true`, `0`, `-0`, `1e3` | coercion and "falsy" checks |
| T19 | 10,000 characters with no spaces | overflow, wrapping, toasts, ReDoS |
| T20 | `O'Brien`, `Nguyễn`, `X Æ A-12`, single-character name `Q` | name validators |
| T21 | `user+tag@example.com`, `User@Example.COM`, `a@b`, `δοκιμή@παράδειγμα.δοκιμή` | email |
| T22 | `../../etc/passwd`, `CON`, `a/b?c#d` | names reused in URLs/filenames/route params |

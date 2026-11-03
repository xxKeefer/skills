# Fixtures: the upload file set

Test files for this lane's catalogue. Make them once into a scratch folder with the commands below (macOS shell), then upload each one through every picker and drop zone a change touches. Cite the file name as the failing input in a finding.

Set `LIMIT` to the documented size limit in bytes before you start (for example `LIMIT=$((10*1024*1024))` for 10 MiB, or `LIMIT=$((10*1000*1000))` for 10 MB; try both if the help text only says "10 MB").

```sh
mkdir -p "${TMPDIR:-/tmp}/upload-fixtures" && cd "${TMPDIR:-/tmp}/upload-fixtures"
LIMIT=$((10*1024*1024))
```

## Size and content

| # | File | Command | Catches |
| --- | --- | --- | --- |
| U1 | `empty.csv`, `empty.pdf` | `touch empty.csv empty.pdf` | UP-A1 |
| U2 | `at-limit.pdf` (exactly the limit) | `mkfile -n $LIMIT at-limit.pdf` | UP-A2 (accepted) |
| U3 | `over-limit.pdf` (limit + 1 byte) | `dd if=/dev/zero of=over-limit.pdf bs=1 count=0 seek=$((LIMIT+1))` | UP-A2 (rejected before upload, readable size in the message) |
| U4 | `huge.pdf` (200 MB, above most proxy limits) | `mkfile -n 200m huge.pdf` | UP-A2 (413 with a non-JSON body), UP-C1 |
| U5 | `big-20mb.pdf` for slow uploads | `mkfile -n 20m big-20mb.pdf` | UP-C1 |
| U6 | `invoice.pdf` that is really a PNG | `curl -so invoice.pdf https://www.w3.org/Graphics/PNG/nurbcup2si.png` (or copy any PNG and rename it) | UP-A3 |
| U7 | `README` (no extension) | `printf 'plain text\n' > README` | UP-A3 (`file.type` is `""`) |
| U8 | `photo.heic` | AirDrop a photo from an iPhone with Camera > Formats > High Efficiency, or `sips -s format heic in.jpg --out photo.heic` (macOS 10.13 or later [uncertain: depends on the installed `sips`]) | UP-A6 |

## Names

| # | File | Command | Catches |
| --- | --- | --- | --- |
| U9 | `SCAN.PDF`, `UPPER.CSV`, `Mixed.Pdf` | `cp at-limit.pdf SCAN.PDF; printf 'a,b\n1,2\n' > UPPER.CSV; cp SCAN.PDF Mixed.Pdf` (make `SCAN.PDF` small with `printf '%%PDF-1.4\n' > SCAN.PDF` if the limit is low) | UP-A4 |
| U10 | `a.pdf.exe` | `printf 'MZ' > a.pdf.exe` | UP-A4 (must be rejected) |
| U11 | `.pdf`, `a.`, `a..pdf` | `printf '%%PDF-1.4\n' > .pdf; cp .pdf a.; cp .pdf a..pdf` | UP-A4 |
| U12 | `报价单 (最终版).pdf` | `cp .pdf '报价单 (最终版).pdf'` | UP-C4 |
| U13 | RTL name `عرض سعر.pdf` | `cp .pdf 'عرض سعر.pdf'` | UP-C4 |
| U14 | emoji name `📄 Report ✅.pdf` | `cp .pdf '📄 Report ✅.pdf'` | UP-C4 |
| U15 | 255-byte name | `cp .pdf "$(printf 'a%.0s' {1..251}).pdf"` | UP-C4 (chip truncation, server limit) |
| U16 | `a:b.pdf` | `cp .pdf 'a:b.pdf'` (Finder shows the colon as a slash) | UP-C4 |
| U17 | `-x.pdf` | `cp .pdf ./-x.pdf` | UP-C4 |

## CSV import

| # | File | Command | Catches |
| --- | --- | --- | --- |
| U18 | `bom.csv` (UTF-8 with BOM, as Excel "CSV UTF-8" saves it) | `printf '\xEF\xBB\xBFname,speed\nItem A,1000\n' > bom.csv` | UP-D1 (first header must match `name`) |
| U19 | `semicolon.csv` (de-DE Excel) | `printf 'name;speed;price\nItem A;1000;1.234,56\n' > semicolon.csv` | UP-D1 |
| U20 | `crlf.csv` | `printf 'name,speed\r\nItem A,1000\r\nPort B,10000\r\n' > crlf.csv` | UP-D1 (`\r` left on the last field) |
| U21 | `trailing-blank.csv` | `printf 'name,speed\nItem A,1000\n\n\n' > trailing-blank.csv` | UP-D1 (no "empty row" error) |
| U22 | `quoted.csv` | `printf 'name,notes\n"Acme, Inc","line one\nline two"\n"Quote ""test""",ok\n' > quoted.csv` | UP-D1 (commas, newlines, and doubled quotes inside fields) |
| U23 | `bad-line-37.csv` (header plus rows; line 37 has a bad speed) | `{ echo 'name,speed'; for i in $(seq 2 36); do echo "Port $i,1000"; done; echo 'Port 37,fast'; for i in $(seq 38 50); do echo "Port $i,1000"; done; } > bad-line-37.csv` | UP-D2 (the message must say line 37, column `speed`, value `fast`) |

## Multiple items

| # | Item | How | Catches |
| --- | --- | --- | --- |
| U24 | a folder | `mkdir folder-drop && cp .pdf folder-drop/` then drag `folder-drop` onto the zone | UP-B5 |
| U25 | three files at once | select `SCAN.PDF`, `a..pdf`, and `bom.csv` together in Finder and drag them | UP-B5 |

## Per-upload-surface smoke script (about five minutes)

1. Keyboard only: Tab to the upload control, open the picker with Enter or Space, choose a file, and remove it. Every step works and focus is visible (UP-B6).
2. Screen reader (VoiceOver): the control has a name, and the chosen file name and any error are announced (UP-B6).
3. Pick a file, reopen the picker, and press Cancel. The selection and the UI state are still sensible (UP-B2).
4. Pick U9, remove it, and pick U9 again. The second pick is handled (UP-B1).
5. Drag U12 onto the page header, outside the zone. The page doesn't navigate away (UP-B3). Drag slowly over the zone's icon and text, then out of the window. The highlight doesn't flicker or stick (UP-B4).
6. Upload U1, U3, U6, U7, U10, and U11. Each is rejected or accepted on purpose, with a specific message (UP-A1 to UP-A5).
7. Throttle to Slow 3G, upload U5, and press Cancel. The request is aborted in the network tab and no file is attached on the server (UP-C1).
8. Attach a file, move to another wizard step and back, then reload. The file is still attached or clearly gone, never an empty `{}` in the payload (UP-C2).
9. After a successful upload, the list shows the new file once, without a reload (UP-C3).
10. For CSV import, run U18 to U23 and check the parsed rows and the error messages (UP-D1, UP-D2).

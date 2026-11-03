# Fixtures: the per-list URL, Back and refresh smoke script

Test data for this lane's catalogue. Cite a value from here as the failing input in a finding, or type it into the running app.

## Per-list smoke script: URL, Back and refresh (about five minutes)

Run on any list, table, search or tabbed page a change touches.

1. Apply a filter, type a search term, change sort, go to page 2, and switch tab. The URL should show each piece of state the page claims to keep (NV-A1). Copy the URL.
2. Refresh. Everything comes back, including the search box text (NV-I13). Paste the copied URL into a new tab: same result.
3. Press Back once. It undoes one meaningful step (a filter or a page), not one keystroke of the search (NV-B1). Press Back until you leave the page: count the presses.
4. Change a filter while on page 3. You land on page 1 (NV-J1). Filter to no results: the empty state says "no matches" and offers to clear, not "you have none" (NV-K1). Clear filters: the URL clears too (NV-K2).
5. Edit the URL by hand: `page=-1`, `page=999`, `page=abc`, `sort=zzz`, `flag=false`, a repeated key (`?status=a&status=b`), a single key where an array is expected, and a search term with `# & + % / ?` and an emoji. The page sanitises or ignores each one, with no crash and no blank screen (NV-H1 to NV-H7).
6. Open a row, scroll, press Back. You return to the same scroll position, page, and filters (NV-C1). Cmd/Ctrl-click and middle-click a row or link: it opens a new tab (NV-F1).
7. Open a modal or drawer, press Back. It closes rather than leaving the page (NV-G1). Open a detail page in a fresh tab and use the in-app Back button: it goes somewhere sensible, not nowhere (NV-B9).
8. Navigate from record A to record B on the same route (a related link, the breadcrumb). The data and any form switch to B (NV-D1, NV-D2).
9. Switch company or account while on a filtered list. Nothing from the old context stays on screen or in the URL (NV-O5).

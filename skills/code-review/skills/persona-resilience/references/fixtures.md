# Fixtures: resilience test setups

Recipes for putting the app under the conditions this lane's catalogue describes. Each recipe names the RS items it exercises. Cite the recipe in a finding so the reader can reproduce it. Chrome DevTools paths are given; Firefox and Safari have close equivalents.

## 1. Expire or revoke the session (RS-A1, RS-A3, RS-A4, RS-A7)

- **Delete the token:** DevTools > Application > Storage. Delete the access token from Local Storage, Session Storage, or Cookies (whichever the app uses), then act in the page. This gives the "next request is a 401" case without waiting.
- **Expire it in place:** if the token is a JWT the client reads, decode it, note `exp`, and set the system clock past that time (or use a fake clock in a test with `vi.setSystemTime`). Check both the client-side expiry check and the server 401 path.
- **Short session:** if the auth server or a dev config allows a short access-token lifetime (for example 60 seconds), use it for RS-A2 and RS-A7. Don't change shared environments to do this.
- **Refresh fails:** DevTools > Network > right-click the token or refresh request > Block request URL. Then expire the access token. The app must fall back to re-login without losing work (RS-A1).
- **Revoke server-side:** sign out from another browser, or revoke the session from the admin side, then act in the original tab.

## 2. Force parallel 401s (RS-A3)

1. Expire the access token (recipe 1).
2. Load the page with the most parallel queries (a dashboard or service detail).
3. Filter the Network panel by the token endpoint and count calls. Expect exactly one refresh, then every failed request replayed once.

## 3. Throttle and block requests (RS-D2, RS-D3, RS-D5, RS-D8, RS-E2)

- **Presets:** DevTools > Network > throttling menu > Slow 4G or 3G.
- **Custom latency:** throttling menu > Add > a profile with 2,000 ms latency, and another with 300 to 800 ms for race testing (RS-D8, RS-E2).
- **Block one request:** right-click a request > Block request URL (or the Network request blocking drawer with a pattern such as `*telemetry*`). Use this for one failed widget (RS-D5) and for a request that never settles (RS-D2).
- **Never-ending response:** a mock (MSW handler that awaits a promise that never resolves, or `await delay('infinite')`) for overlays and spinners with no escape (RS-D2).

## 4. Offline and flaky network (RS-D1, RS-D9)

- DevTools > Network > throttling menu > Offline. Load a page, save a form, then trigger a refetch. Restore the network and watch what fires and when.
- Flaky: toggle Offline on and off every few seconds while saving, or use an MSW handler that fails one request in three with `HttpResponse.error()`.
- Check that the UI says "offline" or "paused", and never shows "TypeError: Failed to fetch".

## 5. Two tabs, two users, company switch (RS-B1 to RS-B7, RS-C3)

- **Two tabs, same user:** open the same page in two tabs (Cmd/Ctrl-click a link, or duplicate the tab).
- **Logout elsewhere:** log out in tab A, then act in tab B without reloading (RS-B1).
- **Company switch elsewhere:** switch company in tab A, then edit and save in tab B, and check which company the change landed in (RS-B2).
- **Another user:** log out in tab A and log in as a second test user, then act in tab B (RS-B2, RS-C3).
- **Two users on one record:** use a normal window and a private window (separate storage) as two users. Edit different fields of the same record, save A, then save B, then reload (RS-B3, RS-B4).
- **Basket and checkout:** add an item in A, check out in B (RS-B5); reach the last step, duplicate the tab, submit in both (RS-B7).
- **Writing tab:** change a stored preference and check the same tab as well as the other one (RS-B6).

## 6. Private windows and blocked site data (RS-C1)

- Open the app in a private window in Chrome, Firefox, and Safari.
- Chrome: Settings > Privacy and security > Site settings > Additional content settings (or Third-party cookies and site data) > add the origin to "Not allowed to save data". Reload the app.
- Expect boot to work and preferences to fall back to memory without throwing.

## 7. Fill storage to the quota and corrupt values (RS-C1, RS-C2)

Run in the console on the app origin:

```js
// fill localStorage until it throws
try { let i = 0; const s = 'x'.repeat(1024 * 1024); while (true) localStorage.setItem('fill' + i++, s) } catch (e) { console.log(e.name) }
// corrupt every persisted key
Object.keys(localStorage).forEach(k => localStorage.setItem(k, '{not json'))
// clean up afterwards
Object.keys(localStorage).filter(k => k.startsWith('fill')).forEach(k => localStorage.removeItem(k))
```

Then boot the app, toggle each preference, and submit a form.

## 8. Seed an old persisted shape (RS-C2)

1. On the previous release (or `main` before the change), use the feature so it writes its stored state. Copy the value from DevTools > Application > Local Storage.
2. On the new build, paste that value back under the same key and reload.
3. Also try a value with a field removed, a field renamed, and a field of the wrong type (`"10"` for `10`).

## 9. Simulate a deploy and a stale chunk (RS-E1)

1. Build and serve the app locally (`pnpm nx build <app>` then serve `dist`), and open it in a tab. Visit one route only.
2. Change any source file and build again, so chunk hashes change. Delete the old hashed assets from the served folder (or serve only the new `dist`).
3. In the old tab, navigate to a route you haven't visited. Expect one reload to the target URL, not a blank page or a dead click.
4. Variant: DevTools > Network > Block request URL on one route chunk (`*/assets/EditService-*.js`) and navigate to it.
5. Variant: make the server return `index.html` for the missing JS file (an SPA fallback rewrite). Chrome reports a MIME type error and Safari reports "Importing a module script failed".
6. Check the response headers for `index.html`: it must not be cached for a long time.

## 10. Conflicts, outages, and Retry-After (RS-B4, RS-D4, RS-D7, RS-D10)

With MSW (or DevTools > Sources > Overrides, which can override response headers and bodies):

| Mock | Response | Exercises |
| --- | --- | --- |
| Save conflict | `409` with a JSON error body | RS-B4 |
| Stale ETag | `412 Precondition Failed` | RS-B3, RS-B4 |
| Maintenance | `503`, `Content-Type: text/html`, `Retry-After: 120`, an HTML body | RS-D10 |
| Outage | every request `503` with `Retry-After: 120` | RS-D4 |
| Committed then lost | the server handler completes, then the response is delayed past the client timeout | RS-D7 |
| Forbidden | `403` on a page query | RS-A4, RS-A5 |

## 11. Hidden-tab timer throttling (RS-A2, RS-A7, RS-D6)

- Open the page, then switch to another tab (or minimise the window) for more than 5 minutes. Chrome limits hidden-tab timers to about once a second, and to once a minute after 5 minutes for chained timers.
- Return and check countdowns, status badges, and the next API call.
- For a quick check, run in the console `setInterval(() => console.log(Date.now()), 100)`, hide the tab, and compare the timestamps.

## 12. Back/forward cache (RS-A6)

- Sign in, open a page with customer data, log out, and press Back.
- DevTools > Application > Back/forward cache > Test back/forward cache shows whether the page is eligible and why not.

## 13. Cancelled requests (RS-E2, RS-D8)

- With 300 to 800 ms latency, click quickly between list and detail pages, change filters several times in a row, type fast in a search box, and log out while a page is loading.
- Watch for error toasts and error states. The Network panel shows the cancelled requests as "(canceled)".

## Per-change smoke script (about five minutes)

1. Throttle to Slow 4G. Use the changed screen: is there feedback within about a second (RS-D3)?
2. Go offline and repeat the main action: does it say "offline", and what happens when you reconnect (RS-D1)?
3. Block the screen's secondary requests one at a time: does the rest still render (RS-D5)?
4. Delete the access token and submit: is the input kept, and does the action complete after re-auth (RS-A1)?
5. Open a second tab, change the same record or the company there, then save in the first tab (RS-B2, RS-B3).
6. Click away mid-load and change filters quickly: no error toasts for cancelled requests (RS-E2).
7. If the change touches stored state, corrupt it and seed the old shape (RS-C1, RS-C2).
8. If the change adds a lazy route, run the stale chunk recipe (RS-E1).

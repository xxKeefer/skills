# Browser storage rules

**Browser storage**

8. **Unguarded storage reads (Change Requested).** Look for `localStorage`/`sessionStorage` access or `JSON.parse(localStorage.getItem(k))` at module scope, in `main.ts`, or in `setup`, with no try/catch, or a change to a persisted type with no version or migration. With storage blocked (Safari private mode, a locked-down corporate browser), full, or holding last release's shape, the app fails to boot. Fix: wrap reads in a helper that returns a default on any error, and version persisted shapes. Don't flag access already inside a guarded helper. (RS-C1, RS-C2)
9. **Storage keys not scoped to the user and company (Change Requested).** Look for `useLocalStorage('draft', …)`, `useStorage('order-draft', …)`, or `localStorage.setItem('cart', …)` with a constant key, or a draft or basket not cleared on logout. The next person on a shared machine, or the same user in another company, sees the previous basket, and two tabs overwrite each other's draft. Fix: key by user and company IDs, clear on logout, and refetch the basket before checkout. Don't flag UI preferences such as theme or column widths. (RS-C3, RS-B5)

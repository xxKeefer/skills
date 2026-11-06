# Rules for pending and failed state

**What the UI shows while pending or after failure**

8. **`initialData` that fakes a loaded state (Change Requested).** `initialData: () => []` (or `{}`/a default) on a query whose real data is not yet fetched: the query reports success, the loading branch never shows, and an empty list reads as "you have none". Use `placeholderData` (still pending) or render the pending state. `initialData` is right only when the value really is the server's data (hydrated from a parent query, SSR).
9. **Last good data kept after a failure (Change Requested when it stays submittable, else Nit).** UI that reads `data` without checking `isError`, so after a refetch or a new key fails, the previous result stays on screen and can be selected or submitted as if current (prices, availability, validation results). Branch on `isError`, or clear/disable the dependent control.
10. **Empty-on-error fallback (Nit).** `data ?? []` (or `catch(() => [])` in a composable) that turns a failure into "no results" with no error branch for the user. The failure *routing* is `persona-error-handling`'s; you flag that the screen now states something false.

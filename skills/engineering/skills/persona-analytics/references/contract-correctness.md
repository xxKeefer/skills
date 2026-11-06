# Correctness of the contract

### B. Correctness of the contract

7. **Untyped path in new code (Change Requested).** New untyped capture calls, or `posthog.capture/register/setPersonProperties`, outside the wrapper. New events go in the typed event map and fire through the wrapper's `track`, flow-tracking and navigation-tracking functions. Touching an existing legacy call site without migrating it is **Future**, not a finding.
8. **Event outside the vocabulary (Change Requested).**
   - A step, reason, outcome, source or item passed as an inline string literal or an untyped variable (`flow.step(someVar)` not typed to the step union) where a constant from the project's event vocabulary belongs.
   - A new event typed with a generic catch-all event type in shipped code. It exists for exploration; a shipped event gets a real payload type.
   - Event *names* are section E.
9. **Flow lifecycle broken (Change Requested).** Trace every exit of a flow-tracking user:
   - `start()` that can re-fire for the same attempt (a watcher, a re-mount, a re-tick). It replaces the open flow and restarts the funnel. Guard it with an open-flow flag.
   - A success path with no `complete()`, or `complete()` before the request resolves (on click rather than in the success branch).
   - A cancel / close / back / route-leave / failed-submit path with no `abandon(reason)`. Nothing abandons a flow automatically, so the funnel shows neither the drop-off nor why.
   - `abandon` with a reason that is not in the flow's reason union (a new reason needs the union extended).
   - A flow handed between components with `start` in both, or with neither calling `discard()` when it hands off.
10. **Split outcome shape (Nit).** A `*_settled` event whose failure carries no `reason`, or whose success carries one. Use a discriminated union on `outcome`, `reason` only on failure, drawn from an error-code union. Never an error `message` string.
11. **New event not asserted (Nit).** (Yours, not `persona-test-design`'s.) A new event, step or reason with no spec asserting the name and payload through the project's analytics test recorder. An untested event breaks silently: the metric just goes flat. (How the spec is written is `persona-vitest`'s; you own that the contract has one.)

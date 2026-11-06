# Retry and lost causes

**Retry**

16. **Hand-rolled retry loop** beside a TanStack call: the app's shared retry function, where one exists, already encodes the policy. Nit.

**A named cause that never reaches the user**

17. **A specific failure message that a later merge or default overwrites.** A handler that builds the precise copy (an unreachable server, a rejected account) and then routes under a generic reason, where the page rebuilds its state from that reason: the specific branch is dead and nobody sees it. Trace the value from where it is built to where it renders, not just to where it is passed. Change Requested.
18. **A failure outcome the caller never acts on.** A function returning a union that includes failure (`'redirecting' | 'handled' | 'failed'`) where a call site ignores it, on a route that renders nothing: the user is left on a blank page with nothing navigating. Check every member of the union reaches a navigation, a throw, or a visible surface. Change Requested.

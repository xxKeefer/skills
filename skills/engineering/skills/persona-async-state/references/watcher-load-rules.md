# Watcher load rules (7)

7. **A load that needs two inputs but waits on one (Nit).** A watcher that fires the load when `a` changes but reads `b` too, so the load runs before `b` is ready or doesn't rerun when `b` changes. Watch both, or gate on readiness. (Whether the watcher should be a `computed` at all is `persona-vue-reactivity`'s call.)

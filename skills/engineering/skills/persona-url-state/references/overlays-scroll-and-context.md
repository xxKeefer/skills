# Overlays, scroll, and context on Back (rules 8 and 9)

8. **Back with overlays, or scroll lost (Nit).** A modal or drawer that pushes a history entry on open but doesn't pop it on close; a full-screen drawer that Back can't close; a list that returns to the top on Back because the data loads after `scrollBehavior` runs, or because the scroll container isn't the window. (NV-G1, NV-G2, NV-C1, NV-C2)
9. **Context lost on the way back (Nit).** A post-login redirect that keeps the path but drops the query or hash; a breadcrumb or "Back to list" link that goes to the bare list route instead of the filtered one. (NV-E1, NV-P1, NV-F5)

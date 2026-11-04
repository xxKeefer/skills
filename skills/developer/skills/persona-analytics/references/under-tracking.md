# Under-tracking: the milestones only the browser sees

### C. Under-tracking: the milestones only the browser sees

12. **New flow with no milestone (Change Requested when the AC ask for it / Nit otherwise).** A new wizard, stepper, multi-field form, checkout-shaped path, or confirm-dialog mutation that ships with no flow tracking and no `track`. Propose the **smallest** set that answers "where do users drop off and why":
    - `start` at the planned entry point (first meaningful interaction, not mount: a page view already counts arrivals);
    - one `step` per decision a user can abandon after, not per field;
    - `complete` on the success branch of the request;
    - `abandon(reason)` on cancel/close/leave and on submit failure, with reasons as a closed union.
    Name the proposed event, steps and reasons in `suggestion`, in the reference's grammar. Do **not** ask for a click event per button or a step per field.
13. **Browser-only signal missing on an existing tracked flow (Nit).** The diff changes a tracked flow and adds a branch the funnel cannot see: a new cancel path, a new client-side validation block that stops submit (the request never happens, so the backend never learns), a new entry point that should set `source`, a new optional step users can skip. Suggest the one property or step that closes the gap.
14. **Experiment or alternate experience with no exposure signal (Change Requested).** A flag-gated redesign or A/B branch of an existing flow with no event saying which experience rendered and which the visit started in. `feature_flags` on every event says the flag was on, not that the user saw the new UI. Fire an exposure event (`<domain>_experience_view`) and a switch event (`<domain>_experience_toggle`), or add `experience` to the flow's extras.
15. **Entry point not attributed (Nit).** A new link/CTA/menu item into a tracked flow (or a new navigation surface) with no navigation-tracking call in its click handler. The funnel will show traffic from nowhere. A new navigation surface needs an entry in the navigation-source vocabulary; a new item needs its constant.

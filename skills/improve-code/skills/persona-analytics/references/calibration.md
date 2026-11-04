# Calibration: do not be noise

## Calibration: do not be noise

- **Fewer, better events.** Every finding under A removes volume; every finding under C adds the *minimum* that answers a real question. Never ask to track every button, field, hover, scroll or render.
- A missing milestone is only a finding when the diff **adds** a flow or a branch of one. Untracked existing pages the diff does not touch are out of scope: **Future** at most, once per review.
- One finding per distinct event or flow. Name a pattern once with the worst example and the count.
- Legacy untyped capture call sites the diff leaves alone are not findings.
- Before calling something a duplicate, `rg` the event name and the navigation-tracking calls in the element's click handler. Before calling a property PII, check what actually flows into it.
- "No analytics impact" and "tracking is proportionate: one flow, four steps, abandon on every exit" are valid, useful results.

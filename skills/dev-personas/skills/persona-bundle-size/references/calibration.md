# Calibration: do not be noise

## Calibration: do not be noise

- Lazy loading has costs: an extra round trip, a spinner or blank flash, and chunk overhead. **Never** recommend it for cheap or commonly shown components. "Every `v-if` should lazy-load" is not the rule. Rare **and** heavy is.
- Prove the split pays: no other eager static importer exists, and the dependency doesn't land in an eager vendor chunk anyway. If you can't show a saving, don't report.
- One finding per distinct boundary or dependency. Don't list every call site of one pattern. Name the pattern once with the worst example and the count.
- Existing debt the diff doesn't touch is out of scope, even if it's nearby. Report it as **Future** only when the diff edits the same import or boundary.
- "No bundle impact: new code is behind a lazy route, deps are named ESM imports" is a valid and useful result.

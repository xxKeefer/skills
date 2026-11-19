# Backend lookup

The lookup steps of `persona-api-integrity`. The rule numbers are the rules of that lane.

## Which backend to read

1. **A paired backend change wins.** If a sibling checkout of the backend repo sits on a feature branch, the frontend change is probably built against that branch. Read the operation there (`git -C <backend clone> show HEAD:<path>`) and also on `origin/main`. A call that only works against the unmerged branch is finding 9.
2. Otherwise read **`origin/main`** of the backend: the sibling clone if there is one. Always `git -C <repo> fetch origin main --quiet` first and read with `git show origin/main:<path>` / `git grep … origin/main`. Local clones lag.
3. Missing clone: cloning it is the user's call, so don't do it. A missing clone is a gap in the review environment, not a defect in the code: skip the checks that need it and report the limitation once, separately from the findings (under mob-review's JSON contract, as a single `future` item with category `unchecked-backend` naming the repo).

## Finding the operation

Write down the call as the frontend sends it: **method, path template, path params, query params, body, and the schema the response is parsed with**. Then:

- **Spec.** Find the backend module's OpenAPI path index and the per-operation file it references. Search the indexes, not the file bodies, in the clone and ref *Which backend to read* chose: `git -C <backend clone> grep -n '<path template>' <ref> -- '*openapi*'` (`<ref>` is `origin/main`, or `HEAD` for a paired branch). Not there: `git grep` the other backend repos the same way. Ignore stale spec backups.
- **Handler.** Backends often keep path constants in one place and register routes with them (`router.get(PATHS.x, ...)`, `@Get(PATHS.x)`), so grep the path literal, then the constant name: `git -C <backend clone> grep -n '<constant>' <ref>`. Add a pathspec of the backend's source files only when the grep is noisy. Read the whole handler method **and the service method it delegates the check to**. Authorisation is often imperative, not annotated.
- **Path prefix.** Frontend paths are relative to the API base, so they match the spec paths as written. A path that only matches after adding or dropping a version segment is a mismatch, not a match.
- **The operation is in no spec**: report it under rule 2 and still check the handler.

# Read the plan, the tests, and the conventions

Step 1 of `SKILL.md` reads this file on each run, after it finds the branch and the base. Do items
3 to 8 in order.

3. Find the plan:
   - Use the path in `$ARGUMENTS`.
   - Else take the folder that the user's instructions name for plans or plans, with no ticket
     subfolder. With no such folder, take `.ai/` in the root that `/write-to-file` uses.
   - Search that folder and its subfolders for the file whose YAML header has `branch: <this
     branch>`. A sub-task plan can be in the folder of its parent ticket, so search each subfolder.
   - Two or more files: ask which one. No file: there is no plan.
4. From the plan, read the `## Acceptance criteria` section, the `## Test approach` section, the
   `goal` and `merge` keys of the YAML header, the done line of each step, and the two SHAs in the
   done line of the review step: the reviewed base and the reviewed head. If the header has a
   `spec` key, read the `## Intent` section of that spec with `/look-up`.
5. In a gh stack, or with a `merge` key, read [`stack.md`](stack.md). It
   gives the stack skill, the base in a stack, and the PR of each `merge` key.
6. With no plan, read the ticket whose key is in the branch name with `/look-up`, and take its
   ACs. With no key or no ticket, there are no ACs.
7. List the test files that `git diff --merge-base origin/<base> HEAD --name-only` names, and the
   test names that the diff adds or changes in them.
8. Read the PR conventions: the repo's PR template (`.github/`, `docs/`, or the root, in any case),
   the repo's contribution docs, and each git or GitHub convention skill that this session has.

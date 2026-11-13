# The report

Step 5 writes the report with these inputs. Light runs change some of them, as `light-review` says.

The coverage table shows the user what ran. Counts are after the Copilot filter. On someone
else's code, the Nit column counts the nits that Step 4 dropped:

```
Persona            CR  Nit  Future   Status
a11y                1    2       0   ran
i18n                0    0       0   ran (clean)
vue-reactivity      —    —       —   skipped (no .vue/composable changes)
...
project rubric      0    1       0   ran (rubric covers changed files)
correctness         1    0       0   ran
```

Give `/write-report` these inputs:

- `kind`: `review`.
- `key`: the ticket key from the handoff, the branch name, or the PR title. Else `pr-<n>` when the
  branch has a PR. Else the branch name with each `/` changed to `-`.
- `title`: `Review of PR #<n>`, else `Review of <branch>`.
- `skill`: `/engineering:post-review-comments` on someone else's code. On your own code,
  `/engineering:build` when Step 1 has a handoff, else `/engineering:apply-review`.
- The run:
  - `title`: `Panel run`.
  - `head`: the head SHA from Step 1. For uncommitted work, add `+ working tree`.
  - On your own code, add `Fixed in` to `meta`: the short hash of the fix commit, or
    `working tree` for a working-tree run. Leave it out when nothing was fixed.
  - `meta`: `Base` (the base branch and the base SHA), `PR` (the PR URL from
    `gh pr view --json url -q .url`, when the branch has a PR), `Folder` (the absolute path of the
    repo folder), `Spec` (the source of the acceptance criteria, when `persona-ac-check` ran), and
    `Copilot` (`dropped N (<persona>: n, …)`, when the filter dropped a finding).
    `/engineering:post-review-comments` reads `PR`, `Base`, and `Folder`. Add `Handoff` (the
    absolute handoff path) when Step 1 has a handoff. `/engineering:build` reads it.
  - `answer`: on someone else's code, the count in each tier, and what the user does next. On
    your own code, the count of fixed and open findings, and the fix commit. Ask no question. If
    every persona is clean, say so plainly. A clean panel is a valid result.
  - `visuals`: one `table` with the question "Which lanes ran, and what did each find?". It holds
    the coverage table, one row for each lane. Set `fold`, so the findings start after the answer.
  - `columns` and `rows`: below.

Give each finding one row. The `persona-ac-check` findings come first. A PR can pass every lane
and still build the wrong thing, so spec gaps do not compete in the lane ranking. The findings of
every other lane follow, in the Step 4 order. On your own code, the open rows come before the
fixed rows in each group.

| Key | Label | Holds |
|---|---|---|
| `tier` | Tier | Change Requested, Nit, or Future |
| `persona` | Persona | the name without the `persona-` prefix, such as `a11y` |
| `where` | File:line | the `file:line` of the finding. Set `mono` |
| `issue` | Issue | the summary, a blank line, then the detail |
| `recommendation` | Recommendation | on someone else's code, the one fix that the draft asks for. On your own code, the fix that the panel made, or for an open row, the fix to make later |
| `result` | Result | on your own code only. `Fixed` or `Open: <reason>` |
| `draft` | Draft reply | on someone else's code only. Set `fold` |

- Keep the personas' markdown links to `main`. If a finding cites out-of-diff code as a bare
  `path:line`, convert it to a link first (resolve the line on `origin/main`).
- Write each draft reply in the comment layout of
  [`post-review-comments`](../post-review-comments/SKILL.md#the-comment-layout), and follow the
  rules under that layout. `/engineering:post-review-comments` checks the anchor and scans the draft
  before it posts.
- Each recommendation and each draft names one fix. When a suggestion names two, pick one as
  [`FIX.md`](FIX.md) item 2 says.
- On someone else's code, give each row the tick `reply`. On your own code, give each open row the
  tick `fix`, so the user can act on it after QA. A fixed row has no tick.

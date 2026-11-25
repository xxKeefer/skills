# The report

Step 5 writes the report with these inputs.

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
- `key`: the ticket key from the plan, the branch name, or the PR title. Else `pr-<n>` when the
  branch has a PR. Else the branch name with each `/` changed to `-`.
- `title`: `Review of PR #<n>`, else `Review of <branch>`.
- `skill`: `/engineering:post-review-comments` on someone else's code. On your own code,
  `/engineering:build` when Step 1 has a plan, else `/engineering:apply-review`.
- The run:
  - `title`: `Panel run`.
  - `head`: the head SHA from Step 1. For uncommitted work, add `+ working tree`.
  - On your own code, add `Fixed in` to `meta`: the short hash of the fix commit, or
    `working tree` for a working-tree run. Leave it out when nothing was fixed.
  - `meta`: `Base` (the base branch and the base SHA), `PR` (the PR URL from
    `gh pr view --json url -q .url`, when the branch has a PR), `Folder` (the absolute path of the
    repo folder), `Spec` (the source of the acceptance criteria, when `persona-ac-check` ran), and
    `Copilot` (`dropped N (<persona>: n, …)`, when the filter dropped a finding).
    `/engineering:post-review-comments` reads `PR`, `Base`, and `Folder`. Add `Plan` (the
    absolute plan path) when Step 1 has a plan. `/engineering:build` reads it.
  - `answer`: on someone else's code, the count in each tier, and what the user does next. On
    your own code, the count of fixed and open findings, and the fix commit. Ask no question. If
    every persona is clean, say so plainly. A clean panel is a valid result.
  - `visuals`: first, `bars` with the question "How many rows does each tier hold?", one bar for
    each tier with rows. On your own code, add a bar `Fixed` with the fixed count. Then one
    `table` with the question "Which lanes ran, and what did each find?". It holds the coverage
    table, one row for each lane. Set `fold` on the table, so the findings start after the bars.
  - `columns` and `rows`: below.

Give each finding one row, except a finding that the panel fixed on your own code. A fixed
finding gets no row: the `answer` gives the fixed count and the fix commit, and the coverage table
counts it. The `persona-ac-check` findings come first. A PR can pass every lane
and still build the wrong thing, so spec gaps do not compete in the lane ranking. The findings of
every other lane follow, in the Step 4 order.

| Key | Label | Holds |
|---|---|---|
| `tier` | Tier | Change Requested, Nit, or Future |
| `persona` | Persona | the lane name from Step 4 without the `persona-` prefix, such as `a11y` |
| `where` | File:line | the `file:line` of the finding. Set `mono` |
| `issue` | Issue | the summary, a blank line, then the detail |
| `recommendation` | Recommendation | on someone else's code, the one fix that the draft asks for, then one or two sentences on how the fix removes the problem, so the user understands the comment they post. On your own code, the options, as the rule below says |
| `result` | Result | on your own code only. `Open: <reason>` |
| `draft` | Draft reply | on someone else's code only. Set `fold` |

- Keep the personas' markdown links to `main`. If a finding cites out-of-diff code as a bare
  `path:line`, convert it to a link first (resolve the line on `$BASE`).
- Write each draft reply in the comment layout of
  [`post-review-comments`](../post-review-comments/SKILL.md#the-comment-layout), and follow the
  rules under that layout. `/engineering:post-review-comments` checks the anchor and scans the draft
  before it posts.
- Each recommendation and each draft names one fix. When a suggestion names two, pick one as
  [`FIX.md`](FIX.md) item 2 says.
- On your own code, an open row gives at least two options, one on each line, the recommended
  one first: `A: <fix> (recommended: <reason>)`, then `B: leave open: <reason>`. A finding with
  only one option is not a choice. Fix it as `FIX.md` says, or drop it and name it in the coverage
  table.
- Give each row two row `visuals`, in this order, made with the rules of
  [`/primitives:show-me`](../../../primitives/skills/show-me/SKILL.md). The card shows them after
  the issue detail and before the recommendation.
  1. **How the defect happens.** Ask the question as "How does <the defect> happen?". Use a
     `mermaid` sequence diagram or flowchart. When the flow depends on state that changes step by
     step, use an `html` visual: a text diagram in a `<pre>`, then a table with the columns
     Step, What happens, and State.
  2. **What the fix changes.** Ask the question as "What changes in <the place>?". Use an `html`
     visual: a label line with the `file:line`, then a `<pre class="bg-code">` that shows the fix
     as pseudocode in a diff. Put each `+` line in `<span class="text-success">` and each `-` line
     in `<span class="text-danger">`. Write `<` as `&lt;` and `&` as `&amp;` in the `<pre>`.
  - In the pseudocode, mark each name that does not exist in the code as made up. Add a last
    line `-- made up: <name>, <name>`.
  - Before you write a diagram, check each claim in it against the code at the reviewed head.
    Read the lines at `head`, not at the working tree. Leave out a claim that the code does not
    show.
- On someone else's code, give each row the tick `reply`. On your own code, give each row the
  tick `fix`, so the user can act on it after QA.

---
name: mob-review
description: Run the full staff-engineer review panel over a PR or branch. Spawns every in-scope persona reviewer (a11y, i18n, reactivity, design-system, decisions-log, tanstack, vitest, test-quality, comments, naming, code-quality, correctness, error-handling, async-state, form-behaviour, text-input, url-state, value-display, resilience, charts, file-upload, typing, best-practice, architecture, security, shell, skills, github-actions, api-spec, production-protector, bundle-size, analytics, integration-test, browser-e2e, test-design, api-integrity, ac-check, pr-size), plus the project's own rubric when the repo names a rubric skill or has a CODING_STANDARDS.md or CONTRIBUTING.md, in parallel against the diff, and writes their findings to one ranked HTML report through /write-report. On your own branch, it fixes each finding that has a fix, commits once, and reports what it fixed and what stays open. On someone else's, it drops the nits, each finding gets a draft reply, and the ticks build a /engineering:post-review-comments prompt. In a handoff, it records the report in the review step. It never pushes and never asks you to choose a fix. Takes an optional handoff or spec path for the AC and test-design checks. Use when the user says "mob review", "mob-review", "run the panel", "full review", or wants a broad multi-lens review of the current branch.
---

# Mob Review: staff-engineer review panel

Spawn every in-scope `persona-*` reviewer in parallel over one diff, then aggregate their findings into a single ranked HTML report. Each persona is a narrow, non-overlapping specialist; this skill is the orchestrator.

`light-review` follows Steps 0 to 7 of this skill with eight lanes only, so a change to a step here also changes `light-review`.

## The panel

[`PANEL.md`](PANEL.md) lists each persona, what it reviews, and its guard. Step 2 reads it.

## Step 0: Run the panel in a clean thread

**The panel is cheap; the thread it runs in is not.** Reviewing a diff needs the diff, the ticket and the repo. Not the conversation that produced the change. Run at the tail of an implementation session, the panel pays for that whole history on every one of its hundreds of orchestration turns: spawns, every persona report, fixes, verification. Measured: the persona subagents are a fifth of a review's cost, the orchestrator's own turns are the rest, purely from running at ~320K context instead of ~45K.

- **Arriving from a session that just wrote the code** → the implementation is committed, so the branch is the whole handoff. Ask the user to `/clear` and re-run `mob-review`; nothing is lost, since the branch carries the state.
- **Already in a fresh or short thread** (a session opened to review) → straight to Step 1.
- **User declines** → run anyway. Say once that it will cost several times more, then drop it.

## Step 1: Resolve target and compute the diff scope

Accept an optional target: a PR number/URL, a branch name, or nothing. Also accept an optional handoff or spec path. Step 3 passes it to `persona-ac-check` and `persona-test-design`. A handoff has steps for `/do-next` to run, and a spec has none. With a handoff, Step 6 records the report in its review step.

**Run from inside the repo.** The panel reviews one repo's diff; one run per repo. Never check a PR out over someone's uncommitted work.

A caller can name the repo folder, such as the worktree that `/engineering:review-pr` claims. Then run every command of this skill in that folder, and add `Repo under review: <path>` to each lane brief in Step 3. The subagents start in the session's folder, not in the repo.

```bash
git fetch origin main --quiet
```

- **No arg / branch:** review the current (or named) branch vs `origin/main`.
- **Stacked PR** (`gh pr view --json baseRefName` is not `main`): review vs `origin/<baseRefName>` instead, in every git command below and in what the personas are told. The base branch's commits are its own PR's to review.
- **PR number/URL:** `gh pr checkout <n>` first (only if the working tree is clean; otherwise ask), then review that branch vs `origin/main`.

Compute the changed-file list and the diff **once, to disk**, and hand every persona those paths instead of a command each one re-runs:

```bash
SCRATCH="${TMPDIR:-/tmp}/mob-$(git rev-parse --abbrev-ref HEAD | tr / -)-$(git rev-parse --short HEAD)"
mkdir -p "$SCRATCH"
git diff --name-only --merge-base origin/main HEAD > "$SCRATCH/files.txt"
git diff        --merge-base origin/main HEAD > "$SCRATCH/diff.patch"
git diff --stat --merge-base origin/main HEAD | tail -1
cat "$SCRATCH/files.txt"
```

The path is keyed by branch **and sha**, so a later run after a fix commit computes its own patch and can never read a stale one.

**Uncommitted work.** If the branch has no commits ahead of `origin/main` but the working tree is dirty, the change hasn't been committed yet. Review the working tree instead: drop `HEAD` from the three `git diff` commands (`git diff --merge-base origin/main` includes staged and unstaged changes), and suffix `SCRATCH` with `-wt`. `/engineering:apply-review` then leaves its fixes in the working tree.

If `files.txt` is empty, report "no changes vs origin/main" and stop.

Record the two SHAs the panel reads. Step 5 prints them, so a later push step can compare the branch with what the panel read:

```bash
git rev-parse --short "$(git merge-base origin/main HEAD)"   # base
git rev-parse --short HEAD                                   # head
```

**Branch behind `main`.** A merge-base diff still carries commits that already landed on `main` by squash merge (a sibling ticket's PR, or an earlier slice of a stack), so the panel would review code that is not this PR's change. When `git rev-list --count HEAD..origin/main` is non-zero, compare `git diff --stat --merge-base origin/main HEAD` against the diff a merge would leave: `git diff --stat origin/main $(git merge-tree --write-tree origin/main HEAD | head -1)`. If the second is clearly smaller, stop and offer to merge `origin/main` first (own code) or tell the author (someone else's), then recompute the scope. Conflicts reported by `merge-tree` are part of the offer.

**Never print the patch body into this thread.** The orchestrator needs the file list (Step 2 guards) and the `--stat` line (size); the personas need the diff, and they read it from `diff.patch` themselves. A diff pasted here is re-sent on every remaining turn of the review. Every persona report, the fixes and the verification all sit behind it.

Also record **whose code this is**. It decides the ticks and the prompt of the report in Step 5:

```bash
git config user.email                                          # you
git log --format='%ae' $(git merge-base origin/main HEAD)..HEAD | sort -u   # branch authors
```

**Own code** = every commit on the branch is authored by the current git user. Anything else (a commit by another author, or a PR you checked out from someone else) is **someone else's code**. When in doubt, treat it as someone else's.

**What Copilot already said.** When the branch has a PR, read [`COPILOT.md`](COPILOT.md) and follow its Step 1. With no PR, or for uncommitted work, skip it.

## Step 2: Select in-scope personas

Read [`PANEL.md`](PANEL.md), and match the changed-file list against its Guard column. Only launch personas whose guard matches. This is a coarse pre-filter to avoid spawning obviously-irrelevant reviewers. Each persona also self-guards as a backstop and returns zero findings if truly out of scope. Note which personas you skipped and why (shown in the final table).

## Step 3: Spawn the in-scope personas in parallel

Launch **one subagent per in-scope persona, all in a single message** (multiple `Agent` tool calls) so they run concurrently. Use the `general-purpose` agent type. The harness runs at most 20 subagents at once and refuses the rest; when the panel exceeds that, launch the overflow as the first reports come back.

**Model per persona.** A persona reads a bounded diff and answers against a written rubric, so pass `model: "sonnet"` on the `Agent` call for every persona *except* the following, which stay on the default model because their misses are silent and expensive:

- `persona-security`
- `persona-production-protector`
- `persona-architecture`
- `persona-skills` (its defects are relational: it has to read across files to find them)
- `persona-api-integrity` (cross-repo and relational: it has to trace a frontend call to a spec, a handler, its service and a permission changeset)
- `persona-test-design` (a missing test is invisible in the diff: it has to reason from the source to conditions nobody wrote, and rate risk)
- `persona-correctness` (the lane for logic bugs: a miss ships a wrong result, and no step after the panel looks for it)

Ticket context in the prompt is fine. The author's beliefs about behaviour are not facts. Pass a claim like "the old component rendered aria-hidden" only as something to verify, or leave it out, because a persona that accepts it as given skips the check its lane exists for.

The persona skills ship in the same domain as this one, as sibling directories: set `PERSONAS` to the parent of this skill's base directory (shown when the skill loads) and substitute the absolute path into the prompt — a subagent cannot resolve `$SKILL_DIR` or a plugin-relative path on its own. The shared persona contract sits at `<PERSONAS>/../PERSONA-CONTRACT.md`.

Give each the same diff context and this exact brief:

> Read `<PERSONAS>/../PERSONA-CONTRACT.md`, then `<PERSONAS>/<persona-name>/SKILL.md`. Follow both as a code review of the diff below. Inside the persona file, `$SKILL_DIR` means `<PERSONAS>/<persona-name>`, and a relative link resolves from that directory.
>
> Return the JSON that the contract's "When a caller asks for JSON" section gives, as your final message.
>
> Diff scope: branch vs `origin/main`, already computed: **do not recompute it**.
> - Full patch: `<SCRATCH>/diff.patch`
> - Changed files: `<SCRATCH>/files.txt`

When Step 1 has a handoff or spec path, add one line to the `persona-ac-check` and `persona-test-design` briefs: `Handoff or spec: <absolute path>`.

**Project rubric, same message, when the repo has one.** The rubric is a review rubric skill that the repo's `CLAUDE.md` or `AGENTS.md` names. With no such skill, it is the repo's `CODING_STANDARDS.md` or `CONTRIBUTING.md`. If the diff touches code the rubric covers, spawn one more `general-purpose` subagent with `model: "sonnet"`. It reads a written rubric, like a persona:

> Invoke the `<rubric skill name>` skill via the Skill tool, or read `<absolute path to the rubric file>`. If the file states no rule about how to write code, return `{"persona":"<rubric>","inScope":false,"findings":[]}`. Apply the rubric as a **review only** of the diff at `<SCRATCH>/diff.patch` (changed files in `<SCRATCH>/files.txt`): no edits, no PR comments. Only report problems on changed lines, verified against the code. Read `<PERSONAS>/../PERSONA-CONTRACT.md`, and follow its Findings and Code references sections. Return raw JSON only (no prose, no code fences), in the form that its "When a caller asks for JSON" section gives, with `"persona"` set to the skill name or the file name, and `category` set to the rubric section. Skip a rule that the repo's tooling already enforces. Severity: a defect the rubric calls out as a bug or contract violation → `change-requested`; a standards deviation → `nit`; a larger refactor idea → `future`.

## Step 4: Aggregate

Collect each persona's JSON (`.filter(Boolean)` any that failed). Combine all `findings`. Do not re-litigate or merge across personas: lanes don't overlap by design, so duplicates indicate a persona strayed; drop the out-of-lane one.

The project rubric overlaps the personas by design. When one of its findings names the same file, line, and problem as a persona finding, keep the persona's. Its remaining findings stand.

These known persona pairs can land on the same line. Resolve them the same way every time:

- **`persona-code-quality` #10 (truthiness guard) vs `persona-value-display` #2 (null shown as a believable value)** on the same line → keep `persona-value-display`'s (it names the wrong value the user sees) and fold code-quality's `??`/`isNil` fix into its `suggestion`.
- **`persona-test-design` versus a `persona-correctness` / `persona-form-behaviour` / `persona-text-input` / `persona-url-state` / `persona-value-display` finding** on the same field → keep both: one names the defect, the other the missing test. Put them next to each other in the report.

**Drop anything Copilot already raised.** When Step 1 saved a non-empty `$SCRATCH/copilot.jsonl`, follow Step 4 of [`COPILOT.md`](COPILOT.md).

**On someone else's code, drop every nit.** Keep the count for the coverage table.

Hold the `persona-ac-check` findings apart. Step 5 puts them first. Rank the rest: **change-requested → nit → future**, then group by persona within each tier.

## Step 5: Fix your own code, then write the report

**On your own code, fix first.** The report is for QA, not for decisions, so the panel makes each
fix that a finding names and never asks the user to choose. Skip this part on someone else's code.

1. Sort each finding. A finding is **open** when the persona marked it `future`, or when its fix
   needs a product or design answer that the code and the spec do not give. Every other finding
   is **fixable**, nits included.
2. When a suggestion names two fixes, take the one the persona recommends. With no
   recommendation, take the smaller fix that removes the defect. Do not ask.
3. If the working tree has changes and Step 1 did not review the working tree, fix nothing. A fix
   commit would take in those changes. Mark each finding open, with that reason.
4. Apply each fixable finding as [`apply-review`](../apply-review/SKILL.md) Step 3 says, in the
   Step 4 order. Where that step asks the user, use item 2 of this list.
5. Run the gates as `apply-review` Step 4 says. When a fix fails a gate, or its test cannot go red
   and then green, revert that fix. Mark the finding open, with the reason.
6. Make one commit in the repo's commit convention. The body lists each fix and its finding. For
   a working-tree run, leave the fixes in the working tree. Never push.

The fix commit is the new **reviewed head**. The panel read the head from Step 1, and this step
made the fixes under the gates, so the push step finds no drift from the fix commit.

The findings go to an HTML report, not to the chat. Write the report with `/write-report`. A
second run on a new head then adds a run to the same file.

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
  Step 5 item 2 says.
- On someone else's code, give each row the tick `reply`. On your own code, give each open row the
  tick `fix`, so the user can act on it after QA. A fixed row has no tick.

Then print only these in the chat. Print no finding.

1. `Reviewed: base <base>, head <head>`. The base is the base SHA from Step 1. The head is the
   reviewed head: the fix commit, else the head SHA from Step 1. For uncommitted work, add
   `+ working tree` after the head. When the panel fixed something, add
   `(panel read <Step 1 head>)` after the line.
2. The coverage table. When the Copilot filter dropped a finding, add one line under the table:
   `Dropped N findings Copilot already raised (<persona>: n, …).` Don't list them.
3. The report path.

## Step 6: Hand over

**On someone else's code, apply nothing.** Editing another person's branch is theirs to invite,
and the findings are the deliverable. Say in one line that the panel applied no fix because the
branch is not yours. Tell the user to tick the rows to reply to in the report, then paste the
prompt that the report builds. The prompt runs `/engineering:post-review-comments` on the ticked rows.

**On your own code** (per the Step 1 ownership check), Step 5 already made the fixes. Say in one
line how many findings the fix commit holds and how many stay open. Ask nothing. The user meets
the open rows at QA. To fix one later, they tick it and paste the prompt that the report builds,
which runs `/engineering:apply-review`.

**In a handoff from Step 1**, on your own code, the review step fixes, writes the report, and
goes on. It never blocks the push step:

1. Tick the review step. Write the report path, the base SHA, and the reviewed head into its done
   line. `/create-pr` reads the two SHAs.
2. Write no `D` entry. The open rows wait in the report for QA. The prompt that the report builds
   runs `/engineering:build`, which adds a fix round for the rows that the user ticks.
3. Stop.

## Step 7: Record calibration signals (never edit)

The panel improves by watching itself. After the report, scan **this run** for signs that a persona, or this skill, got something wrong. Record each sign in the calibration backlog. **Change no persona and no part of this skill here.** `/engineering:self-improve` puts the backlog to the user, and `update-personas` applies the entries the user approves.

The backlog sits outside every repo:

```bash
BACKLOG="${XDG_STATE_HOME:-$HOME/.local/state}/self-improve/improve-personas.md"
mkdir -p "$(dirname "$BACKLOG")"
```

Signals to look for:

- **Convention conflict → false positive.** A finding contradicts a documented convention (`CLAUDE.md`, `AGENTS.md`, the lint config, or a recalled memory). The persona is missing that exception. → An exception in its "What you review". *(Example: persona-naming flags a project's API-client composables for CRUD-verb names until that exception is added.)*
- **Lane stray.** A persona reported something another lane owns (a finding you dropped in Step 4). → A tighter "Out of lane" list.
- **Mis-guard.** A persona was spawned but returned `inScope:false` (guard too loose), or a clearly-relevant persona got skipped (guard too tight). → A guard change, in the persona and in the panel table.
- **Repeated noise or miss.** A persona keeps firing the same low-value nit, or misses a pattern its lane claims. → A severity or scope change.
- **Contract slip.** A persona broke [`PERSONA-CONTRACT.md`](../../PERSONA-CONTRACT.md): a wrong `persona` name, a `file:line` from the patch instead of the branch file, or JSON that does not parse. → A check in Step 4 of this skill, or a clearer contract line.

Read the backlog before you add an entry. If an `open` entry names the same target and the same problem, add this run's evidence to it. If a `rejected` entry covers it, add nothing. Otherwise append:

```markdown
## <persona-name or mob-review>: <the problem in a few words>

- Signal: <one of the five signals above>
- Evidence: <YYYY-MM-DD>, <repo> at <head>: <what happened, with file:line>
- Edit: <one line: the change to make>
- Status: open
```

Write the Edit line in general words, with no names, paths, keys, URLs, or counts, because it becomes rule text in a shared repo. The Evidence line holds the specifics. Back each entry with evidence from this run. No speculative rewrites.

End the summary with the entries this run added or extended. If nothing surfaced, say "no calibration signals."

## Notes

- The personas themselves are read-only: they review, they never edit. The panel fixes in Step 5, and `/engineering:apply-review` fixes the open rows that the user ticks later, only on your own code.
- Personas are independently invocable too (e.g. run just `persona-tanstack`). This skill is for the full sweep.
- Scale is bounded by the diff: a small PR launches few personas; a broad one launches many. That's intended.

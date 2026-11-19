---
name: mob-review
description: >
  Run the full review panel: every in-scope persona lane, plus the project's own rubric, in
  parallel over a PR or branch diff, into one ranked HTML report. Fixes your own branch, or drafts
  replies on someone else's. Takes an optional plan or spec path. The `light` mode runs only the
  essential lanes. Use when the user says "mob review", "run the panel", or "full review", or
  "light review" or "quick review" for the light mode.
argument-hint: "[light] [PR number or URL | branch] [plan or spec path]"
---

# Mob Review: staff-engineer review panel

Spawn every in-scope `persona-*` reviewer in parallel over one diff, then aggregate their findings into a single ranked HTML report.

**Light mode.** When the arguments hold `light`, or the user asks for a light or quick review, read
[`LIGHT.md`](LIGHT.md) and follow it: it runs these steps with the lanes of the Light column of
`PANEL.md` only. Otherwise run the full panel. A change to a step here also changes the light mode.

## Step 0: Run the panel in a clean thread

**The panel is cheap. The thread it runs in is not:** each orchestration turn pays for the whole history of a long session.

- **Arriving from a session that just wrote the code** → the implementation is committed, so the branch is the whole handoff. Ask the user to `/clear` and re-run `mob-review`; nothing is lost, since the branch carries the state.
- **Already in a fresh or short thread** (a session opened to review), **or run by another skill** (the review step of `/build`) → straight to Step 1.
- **User declines** → run anyway. Say once that it will cost several times more, then drop it.

## Step 1: Resolve target and compute the diff scope

Accept an optional target: a PR number/URL, a branch name, or nothing. Also accept an optional plan or spec path. Step 3 passes it to `persona-ac-check` and `persona-test-design`. A plan has steps for `/do-next` to run, and a spec has none. With a plan, Step 6 records the report in its review step.

**Run from inside the repo.** The panel reviews one repo's diff; one run per repo. Never check a PR out over someone's uncommitted work.

A caller can name the repo folder, such as the worktree that `/engineering:pickup --review` claims. Then run every command of this skill in that folder, and add `Repo under review: <path>` to each lane brief in Step 3. The subagents start in the session's folder, not in the repo.

Set `BASE` to `origin/<base>`. The base is the plan's base branch when the plan names one, else the PR's base (`gh pr view --json baseRefName`), else `main`.

```bash
git fetch origin "${BASE#origin/}" --quiet
```

- **No arg / branch:** review the current (or named) branch vs `$BASE`.
- **PR number/URL:** `gh pr checkout <n>` first (only if the working tree is clean; otherwise ask), then review that branch vs `$BASE`.

Read [`SCOPE.md`](SCOPE.md) on each run, and run its commands. They write the changed-file list and the diff to `$SCRATCH`, and record the base and head SHAs and the branch authors. Read [`SCOPE-CASES.md`](SCOPE-CASES.md) first, and use its special cases, when one of these is true:

- The branch has no commits ahead of `$BASE`, and the working tree has changes.
- `git rev-list --count HEAD..$BASE` is not zero.

If `files.txt` is empty, report "no changes vs $BASE" and stop.

**Never print the patch body into this thread.** The personas read `diff.patch` themselves. A diff in this thread is sent again on every later turn.

Whose code this is decides the ticks and the prompt of the report in Step 5. **Own code** = every commit on the branch is authored by the current git user. Anything else (a commit by another author, or a PR you checked out from someone else) is **someone else's code**. When in doubt, treat it as someone else's.

**What Copilot already said.** When the branch has a PR, read [`COPILOT.md`](COPILOT.md) and follow its Step 1. With no PR, or for uncommitted work, skip it.

## Step 2: Select in-scope personas

Read [`PANEL.md`](PANEL.md), and match the changed-file list against its Guard column. Only launch personas whose guard matches. When the caller names the lanes, launch only those, and mark each other lane `skipped (not named by the caller)`. Note which personas you skipped and why (shown in the final table).

## Step 3: Spawn the in-scope personas in parallel

Launch **one subagent per in-scope persona, all in a single message** (multiple `Agent` tool calls) so they run concurrently. Use the `general-purpose` agent type. The harness runs at most 20 subagents at once and refuses the rest; when the panel exceeds that, launch the overflow as the first reports come back.

**Role per persona.** Set the `model` of each `Agent` call to the model of the persona's role in the `models` block of `~/.claude/AGENTS.md`, as the Model section of [`PANEL.md`](PANEL.md) says. With no `models` block, leave `model` unset, so that the session model runs.

Ticket context in the brief is fine. Pass an author's claim about behaviour only as something to verify, or leave it out. A persona that takes it as fact skips its check.

Set `PERSONAS` to the absolute parent of this skill's base directory. A subagent cannot resolve `$SKILL_DIR` or a plugin-relative path.

Give each the same diff context and this exact brief:

> Read `<PERSONAS>/../PERSONA-CONTRACT.md`, then `<PERSONAS>/<persona-name>/SKILL.md`. Follow both as a code review of the diff below. Inside the persona file, `$SKILL_DIR` means `<PERSONAS>/<persona-name>`, and a relative link resolves from that directory.
>
> Return the JSON that the contract's "When a caller asks for JSON" section gives, as your final message.
>
> Diff scope: branch vs `<BASE>`, already computed: **do not recompute it**.
> - Full patch: `<SCRATCH>/diff.patch`
> - Changed files: `<SCRATCH>/files.txt`

When Step 1 has a plan or spec path, add one line to the `persona-ac-check` and `persona-test-design` briefs: `Plan or spec: <absolute path>`. Add one line to the `persona-comments` brief from the Step 1 ownership check: `Lens: own code` or `Lens: someone else's code`.

**Project rubric, same message, when the repo has one.** Read [`RUBRIC.md`](RUBRIC.md), and follow its Step 3.

## Step 4: Aggregate

Wait until every persona subagent has returned, then collect each persona's JSON. Skip any that failed, and combine all `findings`. Write no report while a persona still runs. When two personas report one problem, one of them strayed: drop the out-of-lane finding.

When the rubric ran, follow Step 4 of [`RUBRIC.md`](RUBRIC.md).

Some persona pairs can land on the same line. Resolve each pair as the Known overlaps section of [`PANEL.md`](PANEL.md) says.

**Drop anything Copilot already raised.** When Step 1 saved a non-empty `$SCRATCH/copilot.jsonl`, follow Step 4 of [`COPILOT.md`](COPILOT.md).

**On someone else's code, drop every nit.** Keep the count for the coverage table.

Hold the `persona-ac-check` findings apart. Step 5 puts them first. Rank the rest: **change-requested → nit → future**, then group by persona within each tier.

## Step 5: Fix your own code, then write the report

1. **On your own code, fix first.** Read [`FIX.md`](FIX.md), and follow it. The report is for QA,
   not for decisions, so the panel makes each fix and never asks the user to choose.
2. **Write the report.** The findings go to an HTML report, not to the chat. Read
   [`REPORT.md`](REPORT.md), and give its inputs to `/write-report`. A second run on a new head
   adds a run to the same file.

Then print only these in the chat. Print no finding.

1. `Reviewed: base <base>, head <head>`. The base is the base SHA from Step 1. The head is the
   reviewed head: the fix commit, else the head SHA from Step 1. For uncommitted work, add
   `+ working tree` after the head. When the panel fixed something, add
   `(panel read <Step 1 head>)` after the line.
2. The coverage table. When the Copilot filter dropped a finding, add one line under the table:
   `Dropped N findings Copilot already raised (<persona>: n, …).` Don't list them.
3. The report path.

## Step 6: Hand over

**On someone else's code, apply nothing.** Say in one line that the panel applied no fix because
the branch is not yours. Tell the user to tick the rows to reply to in the report, then paste the
prompt that the report builds. The prompt runs `/engineering:post-review-comments` on the ticked rows.

**On your own code** (per the Step 1 ownership check), Step 5 already made the fixes. Say in one
line how many findings the fix commit holds and how many stay open. Ask nothing. The user meets
the open rows at QA. To fix one later, they tick it and paste the prompt that the report builds,
which runs `/engineering:apply-review`.

**In a plan from Step 1**, on your own code, the review step fixes, writes the report, and
goes on. It never blocks the push step:

1. Tick the review step. Write the report path, the base SHA, and the reviewed head into its done
   line. `/create-pr` reads the two SHAs.
2. Write no `D` entry. The open rows wait in the report for QA. The prompt that the report builds
   runs `/engineering:build`, which adds a fix round for the rows that the user ticks.
3. Stop.

## Step 7: Record calibration signals (never edit)

After the report, read [`CALIBRATION.md`](CALIBRATION.md), and record each sign in this run that a
persona or this skill got something wrong. Change no persona and no part of this skill here.

End the summary with the entries this run added or extended. If nothing surfaced, say "no
calibration signals."

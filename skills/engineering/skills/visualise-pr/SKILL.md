---
name: visualise-pr
description: Explain a PR or a finished branch against main, theme by theme in the context of the repo, and judge if the architecture gets better or worse.
disable-model-invocation: true
---

# Visualise PR

Show how a change set moves the architecture. The report starts with broad strokes: where the
change sits in the repo, and its themes. Each theme then shows how it works, and its changes
in three groups: the bad first, then the mixed, then the good.

A verdict is `better`, `worse`, `mixed`, or `no change`, in five fixed dimensions: Module shape,
Coupling, Pattern fit, Complexity, and Testability.

The report explains and judges. It is not a review: it has no ticks, no prompt, and no fix.
Correctness, security, and performance belong to `/mob-review`.

Run at the `judgement` role of the `models` block in `~/.claude/AGENTS.md`. With no `models` block,
run on the session model. `$SKILL_DIR` is this skill's base directory.

## Input

- A PR link: the change set is the PR head against its base. The local branch does not matter.
- Nothing: the change set is the committed work on the current branch against `origin/main`.

## Step 1: Fix the change set

**PR link.** Read the base, the head SHA, and the URL with
`gh pr view <n> --json baseRefName,headRefOid,url`. Run `git fetch origin <base> pull/<n>/head`,
and set `HEAD` to `headRefOid`. Never check the PR out. `<KEY>` is
`pr-<n>`. A link has the form `<url>/files#diff-<sha256 of the path>R<line>`. Get the hash with
`printf %s <path> | shasum -a 256`.

**No link.**

1. If `git status --porcelain` prints anything, stop. Ask the user to commit or stash, and write
   no report.
2. Run `git fetch origin main`. Set `HEAD` to `git rev-parse HEAD`. Unpushed commits are normal.
   Never push.
3. `<KEY>` follows the `/write-report` rule.
4. A link uses the URL form of the `Editor` role in `## Tools on this machine`, with the absolute
   path. With no `Editor` role, write `path:line` as plain text.

Set `BASE` to `git merge-base origin/<base> $HEAD`. If `git diff --name-only $BASE $HEAD` is empty,
say "no changes" and stop.

**Done when:** you have `BASE`, `HEAD`, `<KEY>`, and the link form, or you stopped.

## Step 2: Collect the shared input once

Write each file below to a scratch folder,
`${TMPDIR:-/tmp}/visualise-<KEY>-<short HEAD>`. Never print the patch into this thread.

1. `files.txt` and `diff.patch`, from `git diff --name-only` and `git diff` of `$BASE $HEAD`.
2. `why.md`: each stated reason, in this order. The PR body and its ticket, through the tracker
   role. The plan or spec for `<KEY>`. The commit messages of `$BASE..$HEAD`. The ADRs and
   `CONTEXT.md` that the changed code touches. Copy the words. Add no reason of your own.
3. `complexity.tsv`: when the `Complexity` role is `lizard`, run
   `python3 $SKILL_DIR/scripts/complexity.py $BASE $HEAD <each file in files.txt>`. It prints one
   row for each function whose numbers changed. On exit 2, or with no `Complexity` role, write no
   file. Keep the tool name and its install command for the report `meta`.
4. `themes.md`: the map of the repo and the themes of the change.
   - **Areas.** Name the top-level areas of the repo, such as apps, packages, or layers, from the
     folder tree, the workspace config, `README.md`, and `CONTEXT.md`. Give each area one line.
   - **Themes.** Group the changed files into three to seven themes. A theme is one intent that
     crosses files, such as "type the save seam" or "turn on the lint gate", named from `why.md`
     and the code, not from a folder. Give each theme a name, one line, its areas, and its files.
     Each file belongs to one theme.

**Done when:** the folder holds `files.txt`, `diff.patch`, `why.md`, and `themes.md`, plus
`complexity.tsv` or a note of the missing tool.

## Step 3: Send one subagent for each theme

Launch one subagent for each theme in one message, so that they run in parallel. Use the
`general-purpose` agent type. Set `model` to the `reviewer` role in the `models` block, else leave
it unset. Read [`BRIEF.md`](BRIEF.md), and give each subagent its brief. Each subagent judges its
theme in all five dimensions, against this yardstick:

| Dimension | Yardstick, as paths beside this skill |
| --- | --- |
| Module shape | `principle-minimize-reader-load`, `principle-laziness-protocol`, `principle-redesign-from-first-principles`, `codebase-design` |
| Coupling | `principle-boundary-discipline`, `principle-migrate-callers-then-delete-legacy-apis` |
| Pattern fit | `principle-model-the-domain`, `principle-type-system-discipline`, and `persona-decisions-log` as a checklist. Domain language goes here |
| Complexity | `principle-minimize-reader-load`, `principle-subtract-before-you-add`, `principle-explain-the-number` |
| Testability | `principle-test-behavior-not-implementation` |

**Done when:** every theme subagent has returned its JSON. Write nothing while one still runs.

## Step 4: Check and judge

1. Open each `path:line` at `$HEAD` with `git show $HEAD:<path>`. When the line does not hold the
   code that the change names, find that code, and correct the line and its link.
2. Check each `why` against `why.md`. A reason that is not in `why.md` becomes "No stated reason".
3. Give each dimension one verdict for the whole change set, from the theme verdicts.
4. Write the net verdict. It is a judgement, not a sum. Name the theme and the dimension that
   matter most for this change, and say why.

**Done when:** every link points at the code that its change names, each dimension has one
verdict, and the net verdict names one theme and one dimension.

## Step 5: Write the report

Call `/write-report` with kind `visualise`, the title `Visualise <PR #n or branch>`, and no
`skill`. So the report has no ticks and no prompt.

- **meta:** the mode with the PR link or the branch, `Base`, `Head`, and `Complexity`. With no
  `lizard`, `Complexity` says `lizard missing, install with pipx install lizard`, and each number
  in the Complexity changes says "estimate".
- **answer:** the net verdict from Step 4.
- **visuals,** the broad strokes, in this order:
  1. "Where does the change sit in the repo?": a `mermaid` map. Each area is a subgraph. Each
     touched module is a node with its theme name, marked with `classDef changed`. Follow the
     Mermaid rules in [`BRIEF.md`](BRIEF.md).
  2. "What are the themes?": a `table` with the columns Verdict, Theme, Areas, and In one line, in
     the row order below.
  3. "How does each dimension move?": `bars` of the five dimensions, in the yardstick order. Each
     label is `<verdict>, <dimension>`, such as `better, Coupling`, so the verdict sets the tone.
     The count is the number of changes in that dimension.
- **columns:** `verdict` (Verdict), `theme` (Theme), `areas` (Areas, `mono`), `story` (What it
  does: the theme in one sentence as the headline, a blank line, then how it works in the repo),
  `why` (Why), and `dimensions` (Verdict reason: each dimension that moves, with its principle).
- **rows:** one row for each theme, `worse` first, then `mixed`, `no change`, and `better`. Each
  row has these row visuals, in this order:
  1. "How does it fit the repo?": the theme's before/after `mermaid` diagram.
  2. "How does it work?": its pseudocode as an `html` visual,
     `<pre class="bg-code p-4 text-sm overflow-x-auto">…</pre>`, with `<`, `>`, and `&` escaped.
  3. "What gets worse?", "What is mixed?", and "What gets better?": one `table` for each group
     that has changes, with the columns Dimension, Where, Change, Why, and Reason. `no change`
     items go in the mixed table. Set `fold` on a table with more than about eight changes.

Then run `node $SKILL_DIR/scripts/check_mermaid.mjs <report path>`. Its first run installs Mermaid
into `~/.cache/visualise-pr`. On exit 1, fix each diagram that it names, and write the report
again. Without `node`, skip the check, and say so in the hand-over.

**Done when:** `/write-report` returns the `file://` URL of `visualise_<KEY>.html`, and
`check_mermaid.mjs` prints `ok`, or you said that it did not run.

## Step 6: Hand over

Print the net verdict in one line, then the `file://` URL. Print no row. When a theme is `worse`,
its reason can name a follow-up skill, such as `/improve-codebase-architecture` or
`/code-simplify`. Run none of them.

**Done when:** the chat shows the verdict line and the URL, and nothing else.

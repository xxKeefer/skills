---
name: resolve-feedback
disable-model-invocation: true
description: >
  Assess review feedback from AI or human reviewers, pasted or from the open threads of a PR. Write
  a verdict, a recommendation, and a draft reply for each item to a review report, whose ticks
  build the /engineering:apply-review prompt. Applies no fix.
argument-hint: "<PR number or URL | pasted feedback>"
---

# Resolve Feedback

Assess each piece of review feedback before anyone acts on it. The verdicts go to a review report,
not to the chat. The user ticks the rows to act on, and the prompt of the report runs
`/engineering:apply-review`. This skill applies no fix, posts no reply, and asks no batch question.

```
parse → assess each item → write the report → return
```

## Step 1: Parse the input

`$ARGUMENTS` can hold:

- **Pasted feedback**: review comments that the user pasted or typed.
- **A PR number or URL**: read the open review threads of the PR.
- **Nothing**: ask "Paste the feedback, or give me a PR number or URL."

Feedback can come from any source:

- **AI reviewers** (GitHub Copilot, CodeRabbit, and others). Treat them with doubt. They invent
  facts, misread control flow, and over-engineer.
- **Human reviewers**. Trust them more, but still assess each claim. A human can be wrong about
  code they do not know.
- **Self-review notes**. The user wants a second opinion on their own notes.

A caller can name the repo folder, such as a worktree. Then read the code and run each git command
in that folder, with `git -C <path>`. Else use the current folder.

For a PR:

1. Run `gh pr view <n> --json number,url,headRefName,baseRefName`.
2. If the branch of the folder is not `headRefName`, stop. Name `/engineering:pickup`, which claims the
   worktree of the PR and syncs it.
3. List the threads with the query in
   [`threads.md` section 1](../apply-review/references/threads.md#1-list-the-threads). Keep each
   thread whose `isResolved` is `false`.
4. Each open thread is one item. Read every comment in it, because a later comment can narrow or
   drop the ask. The source is the `author` of the first comment.
5. If no thread is open, say so and stop. Write no report.

For pasted feedback, each distinct comment, suggestion, or requested change is one item. A pasted
item has no thread. Read the PR of the branch with `gh pr view --json number,url,baseRefName`. A
branch with no PR is fine.

**Done when:** you have listed each item, its source, and the URL of its thread when it has one.

## Step 2: Assess each item

`/engineering:apply-review` reads the cells and the ticks of each row. A change to them needs the same
change there.

### 2a. Read the code

Read the file that the item names, and the code around it.

### 2b. Give the verdict

Trace each claim in the code before you accept it. Then give one verdict:

- **Valid**: the item finds a real issue, such as a bug, an unhandled error, or a race condition.
- **Partially valid**: the observation is correct but the fix is wrong, or the item is a nitpick
  with low impact.
- **Invalid**: the item misreads the code, asks for something worse, or does not apply.

When the fix only makes the code cleaner and changes no behaviour, the fix is cosmetic. The user
decides if it is worth the diff.

### 2c. Write the row

Give each item one row with these cells:

| Key | Label | Holds |
|---|---|---|
| `verdict` | Verdict | `Valid`, `Partially valid`, or `Invalid`. Add `, cosmetic` when the fix changes no behaviour |
| `source` | Source | the reviewer's login or name, `AI reviewer`, or `self`. Add ` (bot)` when `bot` is `true` |
| `where` | File:line | the `file:line` that the item names. Set `mono` |
| `issue` | Issue | the feedback in one line, a blank line, then why the verdict holds, in one or two sentences. For a behaviour bug, give the counterexample: the input and the wrong result |
| `recommendation` | Recommendation | the sort, then what to do and why |
| `draft` | Draft reply | the reply to the reviewer. A thread row only. Set `fold` |
| `thread` | Thread | the `url` of the first comment of the thread. A thread row only |

**The recommendation.** Start with the sort. `Small.` means the fix is mechanical or local, with
one obvious right answer. `You decide: <reason>.` means the fix changes a public contract or
untested behaviour, needs a product decision, or has two reasonable answers. For an Invalid
verdict, start with `No fix.` Then say what to do and why.
When a better fix than the reviewer's exists, name it. When two fixes are reasonable, name both.

**The draft reply.** Write it as the PR author, in one to three sentences:

- Valid or Partially valid: say what the fix changes. For Partially valid, say which part you take
  and why you leave the rest. Write no commit hash. `/engineering:apply-review` ends the reply with
  `Fixed in <short hash>.` when it fixes the row.
- Invalid: say why the code is correct, from the trace. Cite the line as `` `path:line` ``.
- A question: answer it.
- Write no praise and no apology.
- The draft must pass the scan in
  [`post-review-comments` Step 3](../post-review-comments/SKILL.md#step-3-prepare-each-draft),
  item 4.

**The ticks.** A thread row gets `fix`, `reply`, and `resolve`. A pasted row gets `fix` only,
because it has no thread to reply on.

**The order.** Put the Valid rows first, then Partially valid, then Invalid. Inside each verdict,
put a human's item before a bot's.

**Done when:** each item has a row with a verdict, an issue, and a recommendation, and each thread
row has a draft and a thread URL.

## Step 3: Write the report

Write the rows with `/write-report`. A panel run of `/engineering:mob-review` on the same branch uses
the same key, so both runs go to one file.

1. Fetch the base, and read the base SHA:

   ```bash
   git fetch origin <base> --quiet
   git rev-parse --short "$(git merge-base origin/<base> HEAD)"
   ```

   `<base>` is the `baseRefName` of the PR. Without a PR, it is the default branch of the remote.
2. Give `/write-report` these inputs:
   - `kind`: `review`.
   - `key`: the ticket key from the branch name or the PR title. Else `pr-<n>` when the branch has
     a PR. Else the branch name with each `/` changed to `-`.
   - `title`: `Review of PR #<n>`, else `Review of <branch>`.
   - `skill`: `/engineering:apply-review`.
   - The run:
     - `title`: `Threads at <short head>` when the items are PR threads, else
       `Feedback at <short head>`.
     - `head`: `git rev-parse --short HEAD`.
     - `meta`: `Base` (the base branch and the base SHA), `PR` (the PR URL, when the branch has a
       PR), and `Folder` (the absolute path of the repo folder). `/engineering:apply-review` reads all
       three.
     - `answer`: the count of each verdict. Then tell the user to tick the rows to act on and
       paste the prompt.
     - `columns` and `rows`: from Step 2. When no row has a thread, leave out `draft` and
       `thread`.

**Done when:** the report holds the new run, and its JSON block parses.

## Step 4: Return

Print only these in the chat. Print no row.

1. The count of each verdict.
2. The report path.
3. One line: tick the rows in the report, then paste its prompt. The prompt runs
   `/engineering:apply-review`, which fixes test-first and commits once. When the branch has an open
   PR, it pushes once, then replies on and resolves the ticked threads.

**Done when:** the user has the report path, and this skill applied no fix and asked no batch
question.

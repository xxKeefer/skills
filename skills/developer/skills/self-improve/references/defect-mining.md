# Defect mining

Each fix is a defect that the repo found after it shipped, so each one is a check that a reviewer
or a test could have made earlier. Three Step 2 rows use this file: fix commits, tracker bugs, and
defect hotspots. They share one trace and one classification.

- `$YEAR_START` is 365 days before the window end. The hotspots cover `$YEAR_START` to the window
  end. The themes cover the run window.
- `$SCRIPT` is `$SKILL_DIR/scripts/defect_mining.py`.

## 1. Find the tracker

1. If `state.json` has a `tracker` field, use it. `"none"` means no tracker.
2. Else look for the tracker in the repo's `CLAUDE.md` and `AGENTS.md`. If they name none, ask:
   "Which tracker holds the bugs of this repo, or none?"
3. Show the query that you will run: the resolved bugs of the bug type, resolved from
   `$YEAR_START` to the window end. Leave out each resolution that fixed nothing, such as
   "Duplicate", "Won't Do", or "Cannot Reproduce". Ask once whether to narrow the query to this
   repo, such as with a component or a label.
4. Keep the answer for Step 7: `{"name": "<tracker>", "query": "<query>"}`, or `"none"`.

## 2. Get the tracker bugs

Skip this section with no tracker.

Run the query with the tracker's tool. Get only the key, the resolution date, and the summary.
Write one JSON line for each bug to `$CACHE/tracker.jsonl`:

`{"id": "<key>", "date": "<YYYY-MM-DD>", "title": "<summary>"}`

- A large result can go to a file. Convert that file with `jq`. Do not read it into the
  conversation.
- For GitHub issues, also give each bug the merge commits of the PRs that closed it, as
  `"commits": ["<sha>"]`. Read them from `closedByPullRequestsReferences`, with
  `mergeCommit { oid }` on each PR. A commit message that names `#<n>` can name an issue or a PR,
  so the script does not match issue numbers.

## 3. Trace

```bash
REF=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo HEAD)
python3 "$SCRIPT" trace --repo-root <repo root> --ref "$REF" --since "$YEAR_START" \
  --window-start <window start> --until <window end> --cache "$CACHE" --state "$REPO_DIR" \
  [--tracker "$CACHE/tracker.jsonl"]
```

The script reads the first-parent line of the default branch, so a merged PR is one item. A
tracker bug joins each commit whose message names its key. It writes `defects.jsonl`, the miner
chunks, and `trace.json`, and it prints `trace.json`:

| Field | Meaning |
|---|---|
| `bugs`, `traced` | The tracker bugs, and the bugs that join a commit in this repo |
| `trackerInWindow` | The traced bugs resolved in the run window |
| `fixCommits`, `fixCommitsInWindow` | The commits that match `fix\|bug` and join no traced bug, in the 12 months and in the run window |
| `toClassify`, `chunks` | The items with no class in `$REPO_DIR/classified.jsonl`, and the chunk files that hold them |

The bug list is the traced tracker bugs. With no tracker, it is the fix commits of the 12 months.
Now check the floors in the Step 2 table.

## 4. Classify

Skip this section when `chunks` is empty. The script chunks each tracker bug, and each fix commit
that the themes or the hotspots use.

Spawn one `general-purpose` subagent for each chunk, all in one message, with `model: "sonnet"`.
The cheaper model is safe here, because you judge each theme in Step 4, and section 5 checks each
example condition. The brief:

> Repo: `<repo root>`. Read `<cache>/<chunk>`. Each line is one bug or one fix commit, with its
> `id`, `title`, `commits`, and `files`. Read the message of each commit with
> `git -C <repo root> show -s --format=%B <sha>`. When the title and the messages do not make the
> defect clear, read the diff of its non-test source files with
> `git -C <repo root> diff <sha>^ <sha> -- <files>`. Skip lock files and generated files.
>
> Write one JSON line for each input line to `<cache>/classified/<chunk file name>`. Then reply
> with the count of lines, and nothing else.
>
> `{"id": "<id>", "defect": true, "kind": "<the kind of defect>", "check": "<what a reviewer looks for on a changed line>", "specific": false, "escape": "<token>", "dimensions": ["<dimension>"], "condition": "<test condition>", "level": "<token>"}`
>
> - `defect`: false when the item fixed no behaviour: a typo, formatting, lint, a test-only
>   change, a version bump, or build or CI config. Write only `id` and `defect` for those.
> - `kind`: one line in general words, such as "loop bound off by one at the end of a list". No
>   names of people, customers, or companies, and no file paths.
> - `check`: `null` when no changed line shows the defect, such as a missing step in a process.
> - `specific`: true when the defect breaks a rule of this codebase or team, not a general
>   practice.
> - `escape`: the one gap that the defect escaped through, from the table below.
> - `dimensions`: the dimensions that the defect needs, such as role, plan, flag, state, or
>   locale. Name a new one when the defect shows it.
> - `condition`: one line, in the form of the test condition that would have caught the defect.
>   No names of people, customers, or companies, even when the title has one.
> - `level`: the cheapest level that would have caught it: `unit`, `integration`, `contract`,
>   `e2e`, or `none` (data or config with no code path).
>
> | `escape` | What escaped |
> |---|---|
> | `boundary` | A value or partition edge: the last day of a month, page 2, the maximum length |
> | `combination` | Two or more dimensions together: role × account type, plan × add-on |
> | `state-transition` | A change after another change: cancel then modify, an upgrade after a renewal |
> | `interruption` | Double-submit, a race, a retry, a session or account switch |
> | `contract` | The shape between a client and an API, or between two services. An event that no listener handles. Drift from the spec |
> | `authz` | One user reads or changes another user's record, cross-tenant access, a permission or role gap |
> | `data-config` | Seed data, environment config, a migration |
> | `secrets-logging` | A secret or personal data in a log, a response, or the repo |
> | `regression` | It worked before, and a later change broke it |
> | `other` | None of the types above |

The tokens match `developer/skills/tdd/risk-and-technique.md`. A change to one list needs the same
change to the other.

## 5. Build the hotspots

```bash
python3 "$SCRIPT" hotspots --cache "$CACHE" --state "$REPO_DIR"
```

The script merges the miner files into `$REPO_DIR/classified.jsonl`, drops each item older than
`$YEAR_START`, and writes `$REPO_DIR/defect-hotspots.md`. It stops and names each ID that no item
has, and each item that has no class. Run the miner of that chunk again, then run the command
again.

`defect-hotspots.md` holds the source, the coverage, and a Skewed line below 60 percent coverage.
Its tables are the top 25 areas (folders that 2 or more defects changed), the escape types, and
the top 15 dimensions. `start-ticket` and `persona-test-design` read it. Never commit it.

Then read the Example condition column. A miner can copy a name of a person, a customer, or a
company from a bug title. Fix that line in the miner file under `$CACHE/classified/`, then run the
command again.

## 6. Group the themes

`$CACHE/window-defects.jsonl` holds each defect of the run window, with `source`, `title`, `kind`,
`check`, and `specific`. Use only the lines whose source ran in Step 2: `commit` for fix commits,
`tracker` for tracker bugs.

Group the lines by `kind`. Two lines are one kind when the same check catches both. A group of two
or more is a theme. Its Signal names the sources of its lines: `fix commits`, `tracker bugs`, or
both. Keep each other defect for the report's single-fix list.

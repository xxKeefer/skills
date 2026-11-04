# Review and CI mining

Review threads show what reviewers keep asking for. Failed CI runs show what the repo keeps
catching too late. One script fetch serves both sources. They need an `origin` on GitHub and a
working `gh`. Else skip both with the reason.

## 1. Fetch the window

```bash
CACHE="$REPO_DIR/cache/<window start>--<window end>"   # the timestamps with the colons removed
python3 "$SKILL_DIR/scripts/review_mining.py" fetch --repo <owner>/<repo> \
  --since <window start> --until <window end> --cache "$CACHE"
```

Run the fetch in the background. Each `gh` call takes about 2 seconds, and a busy repo needs
about 300 calls. It prints `$CACHE/meta.json`. A second fetch of the same window reads the cache
and makes no call.

What the fetch reads:

- **Review threads**, on each PR merged in the window. It keeps the first comment of each thread,
  for up to 100 threads on each PR. A bot is an author whose type is `Bot`, or whose login ends in
  `[bot]`. Every other author is `human`, and the cache keeps no human login.
- **Outcome**, for each thread. `changed`: the code at the line changed after the comment, so the
  comment was acted on. `closed`: resolved, with no change at the line. `open`: neither. Many
  repos block a merge until every thread is resolved, so the resolved state alone tells nothing.
- **Failed runs** in the window. For the 150 newest, it also gets each failed job with its first
  failed step. It marks a run flaky when the same workflow passed on the same commit. A re-run
  that passes leaves the failure list, so the flaky count is a lower bound.

## 2. Check the floors

- Review threads: with fewer than 20 threads (`review.human.threads` plus `review.bot.threads`),
  skip the source with the reason "`<n>` review threads in the window, fewer than 20".
- Failed CI runs: with fewer than 5 failed runs (`ci.failedRuns`), skip the source with the reason
  "`<n>` failed runs in the window, fewer than 5".

## 3. Mine the review chunks

`meta.json` lists the chunk files in `chunks`. Spawn one `general-purpose` subagent for each chunk,
all in one message, with `model: "sonnet"`. The cheaper model is safe here, because the script
counts each theme, and you judge each theme in Step 4. The brief:

> Read `<cache>/<chunk>`. Each line is one review comment: `[<id>|<author>|<outcome>|<path>]
> <body>`. Group the comments into themes. A theme is two or more comments that ask for the same
> kind of change. Ignore questions, praise, and talk about this one PR. Return a JSON array, and
> nothing else:
>
> `[{"kind": "<the kind of problem>", "check": "<what a reviewer looks for on a changed line>", "specific": false, "ids": ["t12", "t48"]}]`
>
> - `kind`: one line in general words, such as "a list with no empty state". No names of people,
>   customers, or companies, and no file paths.
> - `check`: `null` when no changed line shows the problem.
> - `specific`: true when the comments enforce a rule of this codebase or team, not a general
>   practice.
> - `ids`: every comment in the theme.

## 4. Draft the CI themes

Read `ci.surfaces` in `meta.json`. Group the surfaces that fail for one reason, such as every lint
job, or the unit tests of one package. A group is one theme, and its IDs are the run IDs of its
surfaces. When most of a group's runs are flaky, the theme is a flaky theme.

## 5. Merge and rate the themes

Merge the miner themes across chunks. Two themes are one when the same check catches both. Join
their IDs. Keep human and bot themes apart. Give each theme a slug in kebab case. When
`$REPO_DIR/themes.json` exists, reuse the slug of a last-run theme that the same check catches, so
the comparison holds.

Write the themes to `$CACHE/draft.json`, then rate them:

```bash
# Each entry: {"slug", "source": "human" | "bot" | "ci", "kind", "check", "specific", "ids"}
python3 "$SKILL_DIR/scripts/review_mining.py" themes --cache "$CACHE" \
  --draft "$CACHE/draft.json" --prior "$REPO_DIR/themes.json"
```

The script stops and names each ID that the cache does not hold. Fix the draft, then run it again.
It prints the result, and writes it to `$CACHE/themes.json`. Each theme gets these fields:

| Field | Meaning |
|---|---|
| `count`, `rate` | The items in the theme, and the items per 100 items of its source: human threads, bot threads, or sampled runs |
| `floor` | True with 2 or more items and 1 or more per 100. Only these themes go to Step 3 |
| `trend` | `baseline` with no last run. Else `new`, `rising` (1.5 times the last rate or more), `declining` (the last rate divided by 1.5 or less), or `steady` |
| `changed`, `closed`, `open`, `mostlyIgnored` | Review themes only. `mostlyIgnored` is true when fewer than half the threads changed |
| `flaky` | CI themes only. The flaky runs in the theme |

`dropped` lists the last-run themes that this run did not find.

How to read the result:

- A human theme that is mostly `changed` is a strong signal.
- A bot theme with `mostlyIgnored` argues for narrowing or removing the persona rule that checks
  the same thing.
- A flaky CI theme is report only. It names the job and the step that flake.

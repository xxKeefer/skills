# Defect mining

## Fix commits

Each fix commit is a defect that the repo found after it shipped, so each one is a check that a
reviewer could have made earlier.

### 1. List the fix commits

```bash
git log --no-merges -i -E --grep 'fix|bug' --since=<window start> --until=<window end> \
  --format='%h%x09%ad%x09%s' --date=short
```

With fewer than 5 commits, skip the source with the reason "`<n>` fix commits in the window, fewer
than 5".

### 2. Mine them

Split the list into chunks of 25 commits. Spawn one `general-purpose` subagent for each chunk, all
in one message, with `model: "sonnet"`. The cheaper model is safe here, because you judge each
theme in Step 4. The brief:

> Repo: `<repo root>`. Commits: `<short SHAs>`. For each commit, read the message and the file list
> with `git -C <repo root> show --stat --format=%B <sha>`. Then read the diff of its non-test source
> files with `git -C <repo root> show --format= <sha> -- <files>`. Skip lock files and generated
> files. Return one JSON line for each commit, and nothing else:
>
> `{"sha": "<short sha>", "defect": true, "kind": "<the kind of defect>", "check": "<what a reviewer looks for on a changed line>", "specific": false}`
>
> - `defect`: false when the commit fixed no behaviour: a typo, formatting, lint, a test-only
>   change, a version bump, or build or CI config. Return only `sha` and `defect` for those.
> - `kind`: one line in general words, such as "loop bound off by one at the end of a list". No
>   names of people, customers, or companies, and no file paths.
> - `check`: `null` when no changed line shows the defect, such as a missing step in a process.
> - `specific`: true when the defect breaks a rule of this codebase or team, not a general
>   practice.

### 3. Group the themes

Group the `defect: true` lines by `kind`. Two lines are one kind when the same check catches both.
A group of two or more commits is a theme. Keep each other real fix for the report's single-fix
list.

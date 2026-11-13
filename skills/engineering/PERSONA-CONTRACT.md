# Persona contract

Every `persona-*` skill follows this contract. The persona file holds its lane: the Guard, the
lane paths and lane reads in Scope, the rules, Out of lane, Severity, and an Output section with
the category slug. This file holds the rules that every lane shares. Where a persona gives a lane
rule that differs from this file, the persona rule wins for that lane.

## Guard

Apply the persona's Guard first. If the diff is out of scope, stop. When you run alone, say in one
line why the lane does not apply. When a caller asks for JSON, return `inScope: false`.

## Scope

1. If the caller gives a patch file, read it. Do not run git to get the diff. `mob-review` writes
   the branch diff to `<SCRATCH>/diff.patch` and the changed files to `<SCRATCH>/files.txt`. To
   read the section for one file, run
   `awk '/^diff --git/{p=0} /^diff --git.*<path>/{p=1} p' <SCRATCH>/diff.patch`.
2. If the caller gives no patch file, get the branch diff:

   ```bash
   git fetch origin main --quiet
   git diff --name-status --merge-base origin/main HEAD
   git diff --merge-base origin/main HEAD -- <lane paths>
   ```

   The persona's Scope section names the lane paths. If it names none, diff the whole branch.
3. When you have a patch file, run git only for what a patch cannot show: the lines around a
   change, or a file that the diff does not touch. Each extra diff costs the panel the same bytes
   once for each persona.
4. Judge only added and changed lines. Code that the diff does not change is context, not a
   finding, unless a persona rule says otherwise.
5. You are read-only. Never edit a file, and never run a command that changes a clone.

## Findings

- Verify each finding against the changed lines. Do not speculate.
- Stay in your lane. Out of lane names the persona that owns the rest.
- Give each finding one tier from the persona's Severity section: Change Requested, Nit, or
  Future.
- `file` and `line` point at the changed line, unless the persona's Output section names another
  anchor. `line` is the line number in the file on the branch (the `+` side of the hunk), never a
  line number in the patch file. Use line 0 for a finding about the whole diff.
- `summary` is one sentence. The tier has its own field, so the summary does not repeat it.
- `detail` says why the finding matters: the concrete failure.
- `suggestion` gives one concrete fix. When two fixes work, pick one and say why in one clause. Do
  not offer a choice.
- Zero findings is a valid result. Do not invent a finding to look thorough.

### Code references

Cite code that is not a changed line of the diff as a markdown link to that line on `main`, in
`detail` or `suggestion`. This covers code in another repo, such as a spec or a sibling service,
and unchanged code in this repo.

- Use the form `[path/File.ts:42](https://github.com/<owner>/<repo>/blob/main/path/File.ts#L42)`,
  or `#L42-L50` for a range.
- Take the line numbers from `origin/main`, not from the local checkout, because local clones lag:
  `git -C <repo> fetch origin main --quiet && git -C <repo> grep -n '<pattern>' origin/main -- <path>`.
- Get `<owner>/<repo>` from `git -C <repo> remote get-url origin`.
- For a repo that is not on GitHub, give a plain `path:line` and the remote URL.
- A changed line of the diff stays in `file` and `line`, because it is not on `main` yet.
- When the caller pins a commit, such as a calibration run or a review of a merged PR, read and
  link at that commit (`blob/<sha>/...`), so the line numbers match what you read. In shell, put
  braces around the ref: `git show "${REF}:path"`. zsh reads `$REF:a...` as a path modifier, and
  the command breaks with no error.

## Output

### When you run alone

Print one findings table, most severe first:

| Tier | File:line | Summary | Detail | Suggestion |
|---|---|---|---|---|

Under the table, give the count for each tier. With zero findings, print one line that names the
persona and says it found nothing.

### When a caller asks for JSON

Return only this JSON as your final message, with no prose and no code fences:

```json
{"persona":"<name>","inScope":true,"findings":[{"severity":"change-requested|nit|future","category":"<slug>","file":"","line":0,"summary":"","detail":"","suggestion":""}]}
```

- `persona` is the persona's `name:`.
- `category` is the slug in the persona's Output section.
- `severity` is the tier in lower case.
- When the guard says out of scope, return `{"persona":"<name>","inScope":false,"findings":[]}`.

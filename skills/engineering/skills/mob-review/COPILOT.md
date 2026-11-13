# Copilot filter

The panel never re-reports an issue that Copilot has already raised on the PR. The author has seen
it there, and a second copy is noise.

## Step 1: Save what Copilot said

If the branch has a PR (`gh pr view --json number -q .number`; none, or uncommitted work → skip this), save every Copilot comment to the scratch dir, resolved and outdated ones included:

```bash
PR=$(gh pr view --json number -q .number)
{
  gh api --paginate "repos/{owner}/{repo}/pulls/$PR/comments" \
    --jq '.[] | select(.user.login | test("copilot"; "i")) | {path, line: (.line // .original_line), body}'
  gh api --paginate "repos/{owner}/{repo}/pulls/$PR/reviews" \
    --jq '.[] | select(.user.login | test("copilot"; "i")) | select(.body != "") | {path: null, line: null, body}'
} > "$SCRATCH/copilot.jsonl"
wc -l < "$SCRATCH/copilot.jsonl"
```

Review bodies count too: Copilot lists its low-confidence comments there with a file and line instead of posting them inline. Don't print the file here; Step 4 reads it.

## Step 4: Drop what Copilot raised

If Step 1 saved a non-empty `$SCRATCH/copilot.jsonl`, compare every remaining finding against it and drop the ones Copilot already covered: same file, within a few lines (or cited in a review body), and the same underlying problem, however differently worded. Severity doesn't matter. A `change-requested` that Copilot flagged as a passing remark still goes. A finding on the same line but about a different problem stays. When unsure whether it's the same problem, drop it. Keep a count of drops per persona for the Step 5 coverage table.

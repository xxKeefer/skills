# Extra brief lines

Step 3 adds these lines to the lane briefs when their condition is true.

**Plan or spec.** When Step 1 has a plan or spec path, add one line to every brief: `Plan or spec: <absolute path>. Drop a finding that its Decisions or Follow-ups already cover. Make it a Future when it only partly overlaps them.`

**Fix round.** When an earlier run of this panel on this branch wrote a review report, take the reviewed head of its last run: its `Fixed in` commit, else its `head`. Write `git diff <that head> HEAD > "$SCRATCH/since-last.patch"`, and add one line to every brief: `Last reviewed head: <sha>. Lines changed since then: <SCRATCH>/since-last.patch. Raise a finding on any other line only when it is a Change Requested defect.`

**Refactor or migration with net growth.** When the plan, the ticket, or the commits call the change a refactor or a migration, and the Step 1 stat shows more insertions than deletions, add one line to the `persona-code-quality` and `persona-test-quality` briefs: `Net growth: +<insertions> -<deletions>. Ask what this change should have deleted, and report each thing it kept that it should have deleted.`

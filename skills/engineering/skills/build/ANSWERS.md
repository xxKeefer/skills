# Record the Answers

Read this file when the user answers the entries under `## Pending Decisions` after a `/build`
run.

For each entry the user answers:

1. Write the answer into the plan, at the step the entry blocks, as a recorded decision.
2. For an entry with a patch on its `Work` line, also write whether the next run resumes from that
   patch.
3. For an `N` entry the user has done, mark its step done.
4. Delete the entry.

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.

Then go back to Step 1 of [`SKILL.md`](SKILL.md), unless the user says to stop.

**Done when:** every answered entry is gone from `## Pending Decisions`, and its answer is in the
plan.

---
name: update-plan
description: >
  Update an existing plan document in place with the current state of progress, so a fresh
  agent can cold-start from it. Takes one argument: the @-tagged file path to update. Use when
  the user says "update plan", "update the plan", or context is about to blow out.
argument-hint: "@path/to/plan.md"
---

Update the @-tagged file with the current state of progress, for the purpose of bootstrapping a
fresh agent for a cold start.

- Edit the file in place. Preserve its existing structure and headings — fold progress into the
  document it already is, don't replace it with a fresh plan.
- Mark what's done, what's in progress, and what's next. Update stale claims to match reality.
- Don't duplicate content already captured in other artifacts (PRDs, ADRs, issues, commits,
  diffs) — reference them by path or URL.
- Redact anything sensitive (keys, passwords, PII).

If the file is a plan, run `python3 $SKILL_DIR/../write-to-file/scripts/check_plan.py <absolute plan path>`. `$SKILL_DIR` is this
skill's base directory. Run it after the edit. A plan has `doctype: plan` in its YAML header, or a name that starts
with `plan_` or `handoff_`. On exit 1, stop, and give each error line. For a file with no YAML header, say that
`/write-to-file` can migrate it to the plan layout.

When the caller gives choices that the agent made with no user, record each one. Run
`python3 $SKILL_DIR/scripts/log_decision.py <absolute plan path> --decision <text> --reason <text> --evidence <text> --result <text>`
once for each choice. The script writes `decisions_<KEY>.tsv` beside the plan. The first time, add
`- Decision log: decisions_<KEY>.tsv` to `Progress`. Log each choice that the caller gives, even when the plan already records it. Skip only a choice
that the log already holds.

The reader is a cold agent with none of this conversation's context. Write so it can pick up
and continue without asking.

Write every line you add or rewrite in **Simplified Technical English**. Read
[`STE.md`](../../STE.md) before you write, and follow every rule in it. Leave untouched lines alone — this is a progress update, not a rewrite.

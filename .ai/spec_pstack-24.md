---
doctype: spec
ticket: none
status: confirmed
goal: "`webperf` reports a verdict with its limiter, or \"inconclusive\"."
---

# Spec: `benchmark`

## Intent

- Outcome: a new skill, `engineering/benchmark`, vets a performance number with seven checks before anyone reports it or acts on it. `webperf` calls it on each measurement. Inconclusive is a valid verdict.
- User: the user, and any agent that measures a speedup, a regression, or a choice between options. `webperf` takes the median of three runs and stops there.
- Why now: map unit 24 (r1.7).
- Success: `webperf` reports a verdict with its limiter, or "inconclusive" with the gap named.
- Constraint: everything-agnostic. The skill names the kind of tool (a profiler, a counter of errors), not a product. It cites `principle-explain-the-number`.
- Out of scope: a call from `loop-until` or any other skill, and a change to the principle.

## Decisions

- Adapt pstack's `benchmark-checklist`: its seven questions are the seven checks. Why not double (the limiter), was it tuned, did it break limits, did it error, does it reproduce (alternate A/B runs, five or more each), does it matter, and did it even happen (the work ran inside the timed region). Credit the source in one line of prose, as the repo `CLAUDE.md` says.
- The verdict set is faster, slower, no measurable difference, or inconclusive. Inconclusive applies when the limiter has no name, a side ran untuned, or the error check or the "did it happen" check could not run. The report names the gap.
- The skill is model-invocable, with no `disable-model-invocation`, because `webperf` calls it.
- Name no tool product in the skill: the north star is everything-agnostic. `webperf` keeps its own tool names.

## Acceptance criteria

- [ ] **A.** Read `engineering/benchmark/SKILL.md` → it holds seven checks on a perf number, among them name the limiter, alternate A/B runs, count errors, and confirm that the work ran inside the timed region. It allows the verdict "inconclusive", cites `principle-explain-the-number`, and `webperf` calls it.
- [ ] **B.** Follow the `webperf` steps on a measured page → the report gives a verdict with its limiter, or "inconclusive" with the gap named.

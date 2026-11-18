---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-24_benchmark
status: approved
goal: "`webperf` reports a verdict with its limiter, or \"inconclusive\"."
spec: .ai/spec_pstack-24.md
builds_on: pstack-23
---

# Plan: pstack-24 `benchmark`

## Goal

Add `engineering/benchmark`, a skill with seven checks on a perf number, and make `webperf` call it on each measurement. Scope: SCOPED, one PR: one new skill, one edit to `webperf`, one README row.

## Spec

`.ai/spec_pstack-24.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `engineering/benchmark/SKILL.md` → it holds seven checks on a perf number, among them name the limiter, alternate A/B runs, count errors, and confirm that the work ran inside the timed region. It allows the verdict "inconclusive", cites `principle-explain-the-number`, and `webperf` calls it.
- [x] **B.** Follow the `webperf` steps on a measured page → the report gives a verdict with its limiter, or "inconclusive" with the gap named.

## Context

- Map: `.ai/map_pstack-program.md`, unit 24. Done line: `webperf` reports a verdict with its limiter, or "inconclusive".
- Approval: the map (H0).
- Stack: this branch starts from `pstack-23_typescript-rules`, because the unit 20 to 23 PRs are not merged. The home machine sets the unit 24 PR base to that branch. Keep the unit 20 to 23 `.ai/` files.
- Intent and Decisions: see the spec. Source: pstack `skills/benchmark-checklist/SKILL.md` (https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/benchmark-checklist/SKILL.md). Its seven questions are the seven checks: why not double, was it tuned, did it break limits, did it error, does it reproduce, does it matter, did it even happen. Credit pstack in one line of prose in the skill.
- Verdicts: faster, slower, no measurable difference, or inconclusive. Inconclusive when the limiter has no name, a side ran untuned, or the error check or the "did it happen" check could not run. The report names the gap.
- The skill is model-invocable, with no ★ and no `disable-model-invocation`, because `webperf` calls it. It names no tool product, so it stays everything-agnostic.
- Fit with `webperf`: Step 1 and Step 3 of `webperf` take the median of three runs. The benchmark check asks for at least five alternating runs per side. `webperf` defers to `/benchmark` for the run count, and its Step 3 keep-or-revert reads the verdict. Not `/loop-until`: the spec puts that call out of scope.
- Principle to cite in the skill, by sibling path: `principle-explain-the-number`. Read it before step 1.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A new skill loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-24_benchmark`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill holds the seven checks and the verdicts, and `webperf` calls it | L | skill text |
| B | a `webperf` run ends in a verdict with a limiter, or "inconclusive" | M | new behaviour that an agent must follow across two skills. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a `webperf` run on a scratch page, with a fix that changes one metric, reports a verdict and its limiter, or "inconclusive" with the gap named | EP | Manual | the live run in step 2 |

### Not testing

- A: skill text. The review step reads it against its AC.
- A run on a real app: the map has no app with a URL. A scratch page served from a temp folder runs the same steps.

## Steps

- [x] **1. The `benchmark` skill and the `webperf` call.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md`, `skills/meta/skills/write-a-skill/SKILL.md`, and `skills/engineering/skills/principle-explain-the-number/SKILL.md` first. Write `skills/engineering/skills/benchmark/SKILL.md`, model-invoked, with no ★. Steps, each with a done line: 1. Before the run: write the claim in the words you would ship, read the harness, and check that the machine is quiet. 2. The seven checks, each answered with evidence from a run. 3. The verdict: faster, slower, no measurable difference, or inconclusive, with the number, its unit, the run count, the range, and the limiter. Name the gap for inconclusive. Allow one run for a ballpark the user asked for, with checks 4 and 7 still run. Name no tool product. In `webperf`, call `/benchmark` on each measurement in Step 1 and Step 3, and make the keep-or-revert in Step 3 read the verdict. Add a row to `skills/engineering/README.md`.
  - Seam: `skills/engineering/skills/benchmark/SKILL.md` and `skills/engineering/skills/webperf/SKILL.md`.
  - Done: AC A holds on a read, and the pre-commit test passes.
- [x] **2. Live run.** Kind: config. Conditions: C1. Make a scratch folder in a temp path with one HTML page that loads a large unsized image or a render-blocking script. Serve it with a local static server. Run the `/webperf` steps on it from this thread, with a lab tool run through `npx`, and one fix. Copy the verdict, the limiter or the gap, and the run count into this Done line. Stop the server, and delete the scratch folder. When no browser can run the lab tool, record the skip and its reason in Progress, and run the `/benchmark` checks on a scratch A/B command in its place.
  - Seam: the `webperf` and `benchmark` skill text, as an agent follows it.
  - Done: AC B holds. Page: a 2.1 MB script in `<head>`, fixed with `defer`, Lighthouse 12 through `npx`, mobile simulated throttling, 12 cores at load 3.2. Verdict: faster. LCP p50 11368 ms to 600 ms, 5 alternating runs for each side, range 11220 to 11371 ms before and 600 to 601 ms after. Limiter: the render-blocking script on the throttled network. The render-blocking audit gives 10.6 s for it, and 2.1 MB at the simulated 1.6 Mbps is about 10.5 s, so the gap is inside the limit (check 3). Check 4: no runtime error, and the script returned 200 on each run. Check 7: each run transferred the 2.1 MB script and ran it. TBT p50 67 ms to 84 ms, ranges 0 to 70 ms and 68 to 101 ms: close, with no clear change. CLS 0 on both sides. Server stopped, scratch folder deleted.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [ ] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-24.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-24_benchmark`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-24.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-24.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-24_benchmark`.
- Decision log: decisions_pstack-24.tsv
- 2026-11-18: playbook `map`, step 3: four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: `benchmark` skill, `webperf` calls it in Steps 1 and 3, README row added.
- 2026-11-18: step 2 done: the live `/webperf` run gave the verdict faster, with its limiter. See the step 2 Done line.
- 2026-11-18: step 3 done: the pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.

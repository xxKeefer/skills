---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-25_sharpen
status: approved
goal: "`/sharpen` on a prompt returns a deeper version."
spec: .ai/spec_pstack-25.md
builds_on: pstack-24
---

# Plan: pstack-25 `sharpen`

## Goal

Add `primitives/sharpen`, a user-only skill that rewrites a prompt to go deeper, not wider. Scope: SCOPED, one PR: one new skill and one README row.

## Spec

`.ai/spec_pstack-25.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `primitives/sharpen/SKILL.md` → it is a new user-only skill with `disable-model-invocation: true`, and it rewrites a prompt to go deeper, not wider.
- [x] **B.** Run `/sharpen` on a prompt → it returns a deeper version of the prompt.

## Context

- Map: `.ai/map_pstack-program.md`, unit 25. Done line: `/sharpen` on a prompt returns a deeper version.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-24_benchmark`, because the unit 20 to 24 PRs are not merged. The home machine sets the unit 25 PR base to that branch. Keep the unit 20 to 24 `.ai/` files.
- Intent and Decisions: see the spec. Source: pstack `skills/sharpen/SKILL.md` (https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/sharpen/SKILL.md). Its four questions: what a top professional would do that the prompt does not ask for, the rawest material they would start from, their methods and tools, and what outside the agent and the user would show the result is right. Then the skill rewrites the prompt to ask for exactly that. The rewritten prompt asks the agent to prototype a choice that an experiment can settle, and to recommend an option from what it saw. It leaves product or preference choices to the user. Credit pstack in one line of prose in the skill.
- The skill is user-only: `disable-model-invocation: true`, with no ★. It names no tool product, so it stays everything-agnostic.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A new skill loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-25_sharpen`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill exists, is user-only, and holds the deeper-not-wider method | L | skill text |
| B | a run on a prompt returns a deeper prompt | M | new behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a run of the skill steps on a short sample prompt gives the four answers and a rewritten prompt that asks for more depth on the same task, not more tasks | EP | Manual | the live run in step 2 |

### Not testing

- A: skill text. The review step reads it against its AC.

## Steps

- [x] **1. The `sharpen` skill.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` and `skills/meta/skills/write-a-skill/SKILL.md` first. Write `skills/primitives/skills/sharpen/SKILL.md`, with `disable-model-invocation: true` and no ★. Keep it short, in the size of the pstack source. Adapt its four questions and its rewrite rule, as Context says. Return the rewritten prompt in one code block, ready to paste. Name no tool product. Add a row to `skills/primitives/README.md`.
  - Seam: `skills/primitives/skills/sharpen/SKILL.md`.
  - Done: AC A holds on a read, and the pre-commit test passes.
- [x] **2. Live run.** Kind: config. Conditions: C1. In this thread, follow the `sharpen` skill text on the sample prompt "Find out why the test suite is slow." Copy the four answers in short form and the first line of the rewritten prompt into this Done line.
  - Seam: the `sharpen` skill text, as an agent follows it.
  - Done: AC B holds. A fresh agent followed the skill text on the sample prompt. Answers: 1, measure before a guess: the slowest tests, phases, and shared resources, and whether the slowness is new. 2, a timed full run with per-test and per-phase times, the CI run history, and the commit history. 3, the runner's duration report, a profiler, a trace of database, network, and disk calls, serial against parallel runs, one test alone against the full suite, and a bisect. 4, CI wall-clock times before and after, from repeated runs with the spread, a clean machine, and the same pass rate. The rewrite came in one code block. First line: "Find out why the test suite is slow." It keeps the one task, prototypes the measurable choices, and leaves the choice to remove tests or change tools to the user.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-25.md`. This step changes no code. Name `/engineering:light-review`.
  - Done: the report is `.ai/review_pstack-25_sharpen.html`. Reviewed base 71ff207, head f94c393. The light run found no defect.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-25_sharpen`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-25.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-25.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-24_benchmark`, for the branch `pstack-25_sharpen`.
- Decision log: decisions_pstack-25.tsv
- 2026-11-18: playbook `map`, step 3: three choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: `sharpen` skill and README row added.
- 2026-11-18: step 2 done: a fresh agent followed the skill on the sample prompt and returned a deeper prompt. See the step 2 Done line.
- 2026-11-18: step 3 done: the gates each exit 0.
- 2026-11-18: step 4 done: light review of 71ff207..f94c393 found no defect. Report: `.ai/review_pstack-25_sharpen.html`.
- 2026-11-18: `/blast-radius`: verdict `clear`. Safety fact: outside `.ai/`, the branch adds only the `sharpen` skill and one row in the primitives README. `sharpen` is the only skill with that name, it is user-only with no ★, its links resolve, and no file outside `primitives` calls it. Rung 4. No confirmed risk. Cleared: the root README lists domains, not skills. `find_drivers.py` matches only `verify-*` folders, and `due.py` reads only `deprecated` skills. The `sharpen` hits in `domain-modeling`, `retro`, `self-improve`, and `writing-great-skills` use the plain word. The test fixture `work-on/scripts/fixtures/map_program.md` copies the map heading only. Proof, from the repo root on this branch:
  ```
  python3 - <<'PY'
  import glob, os, re, subprocess, sys
  bad = []
  files = subprocess.run(["git","diff","--name-only","71ff207","HEAD","--",".",":!.ai"],capture_output=True,text=True).stdout.split()
  want = {"skills/primitives/README.md","skills/primitives/skills/sharpen/SKILL.md"}
  bad += [] if set(files) == want else [f"diff files: {files}"]
  names = {}
  for f in glob.glob("skills/*/skills/*/SKILL.md"):
      m = re.search(r"^name:\s*(\S+)", open(f).read(), re.M)
      names.setdefault(m.group(1) if m else None, []).append(f)
  s = "skills/primitives/skills/sharpen/SKILL.md"
  bad += [] if names.get("sharpen") == [s] else [f"sharpen name: {names.get('sharpen')}"]
  t = open(s).read()
  fm = t.split("---")[1]
  bad += [] if re.search(r"^disable-model-invocation:\s*true$", fm, re.M) and "★" not in t else ["not user-only, or has a star"]
  for link in re.findall(r"\]\(([^)]+\.md)\)", t):
      p = os.path.normpath(os.path.join(os.path.dirname(s), link))
      bad += [] if os.path.exists(p) else [f"broken link: {link}"]
  callers = subprocess.run(["git","grep","-n","-E","/sharpen\\b|primitives:sharpen","--",".",":!.ai",":!skills/primitives"],capture_output=True,text=True).stdout
  bad += [] if not callers else [f"callers: {callers}"]
  r = open("skills/primitives/README.md").read()
  bad += [] if r.count("`/sharpen`") == 1 else ["README row count"]
  print(bad or "ok"); sys.exit(1 if bad else 0)
  PY
  ```
  Output: `ok`, exit 0.

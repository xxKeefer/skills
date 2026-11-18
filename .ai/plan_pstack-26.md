---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-26_fork-rule
status: approved
goal: "A grill looks up a fact instead of asking it."
spec: .ai/spec_pstack-26.md
builds_on: pstack-25
---

# Plan: pstack-26 the fork rule

## Goal

`grill`, `spec`, and the `plan` route classify each question before they ask it. A fact goes to a lookup or a prototype, and only a decision goes to the user. Scope: SCOPED, one PR: three skill edits.

## Spec

`.ai/spec_pstack-26.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `grill`, `spec`, and `plan` → each classifies a question before it asks: an observable fact goes to a lookup or a prototype, and only a decision goes to the user.
- [x] **B.** Run a grill on a plan that turns on a fact in the corpus → the grill looks up the fact and does not ask it.

## Context

- Map: `.ai/map_pstack-program.md`, unit 26. Done line: a grill looks up a fact instead of asking it.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-25_sharpen`, because the unit 20 to 25 PRs are not merged. The home machine sets the unit 26 PR base to that branch. Keep the unit 20 to 25 `.ai/` files.
- Intent: see the spec. Source: pstack `skills/poteto-mode`, its fork rule. Before a question, classify it. An observable fact goes to a prototype or a lookup, not the user. Credit pstack in one line of prose in `grill`.
- Decisions: the HITL line is on actions (map Decision "Autonomy and the HITL line"). The pause list stays in the `pause-list.md` rule. This unit does not change it.
- One source for the rule: `grill` holds the fork rule. `spec` Step 3 already follows `/grill`, and gets one line that applies the rule to its gaps. `plan` holds no steps of its own, because `/start-ticket` does the work, so the line for the plan route goes into `start-ticket`, beside its "No questions" rule. `plan` itself does not change.
- The three classes: a fact that the corpus holds (look it up), a fact that a run or a prototype can settle (run it, then report what it showed), and a decision (ask the user, with a recommended answer). `grill` already says to look up a corpus fact. The new parts are the classify-first step and the prototype class.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-26_fork-rule`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the three skills hold the classify-first rule | L | skill text |
| B | a grill looks up a corpus fact and does not ask it | M | behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a fresh agent follows the `grill` text on a short plan whose first open point is a fact in this repo. It looks the fact up and asks only a decision | EP | Manual | the live run in step 3 |

### Not testing

- A: skill text. The review step reads it against its AC.

## Steps

- [x] **1. The fork rule in `grill`.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` first. In `skills/primitives/skills/grill/SKILL.md`, replace the fact line with the fork rule: before each question, classify it. A fact that the corpus holds: look it up. A fact that a run or a prototype can settle: run it, and report what it showed. A decision: ask the user, with a recommended answer. Credit pstack's `poteto-mode` in one line of prose. Keep the skill short and everything-agnostic.
  - Seam: `skills/primitives/skills/grill/SKILL.md`.
  - Done: AC A holds for `grill` on a read, and the pre-commit test passes.
- [x] **2. `spec` and the plan route.** Kind: docs. In `skills/engineering/skills/spec/SKILL.md` Step 3, add one rule: classify each gap by the `/grill` fork rule first, and ask only the decisions. In `skills/engineering/skills/start-ticket/SKILL.md`, beside the "No questions" rule, add one line: before a question to the user, classify it by the `/grill` fork rule. Search the repo for other copies of the old `grill` fact line, and update each one.
  - Seam: the two skill files.
  - Done: AC A holds for `spec` and the plan route on a read.
- [x] **3. Live run.** Kind: config. Conditions: C1. Give a fresh agent the `grill` text and this plan: "Add a `## See also` section to every skill in the `primitives` domain." Tell it to return the questions it would ask, and each fact it looked up instead, with the file it read. Copy the result in short form into this Done line.
  - Seam: the `grill` skill text, as an agent follows it.
  - Done: AC B holds. A fresh agent followed the `grill` text on the sample plan. It looked up six facts and asked none of them: 16 primitives skills (`ls`), no `See also` section in any skill (`grep`), no deprecated primitive, the section headings in use, the base-layer rule in `skills/primitives/CLAUDE.md`, and the credit convention. It needed no run. It asked six decisions, each with a recommended answer: which skills, what an entry holds, links to other domains, where the section goes, who keeps links true, and the README.
- [x] **4. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [x] **5. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-26.md`. This step changes no code. Name `/engineering:light-review`.
  - Done: report `.ai/review_pstack-26_fork-rule.html`. Reviewed base 8d3326c, head d06734a. Light run: 0 change requested, 1 nit open. The nit: `start-ticket/SKILL.md` is 10,014 bytes, over the 10 KB threshold.
- [x] **6. Push.** Push-only map: run `git push -u origin pstack-26_fork-rule`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line. Pushed head 48281ca to `origin/pstack-26_fork-rule`.

## Suggested skills

- `/build @.ai/plan_pstack-26.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-26.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-25_sharpen`, for the branch `pstack-26_fork-rule`.
- Decision log: decisions_pstack-26.tsv
- 2026-11-18: playbook `map`, step 3: three choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: fork rule in grill.
- 2026-11-18: step 2 done: fork rule in spec and start-ticket. No other copies of the old fact line.
- 2026-11-18: step 3 done: the live run proves AC B. See the step 3 Done line.
- 2026-11-18: step 4 done: the gates each exit 0.
- 2026-11-18: step 5 done: light review of 8d3326c..d06734a. 1 nit open, in the report.
- 2026-11-18: `/blast-radius`: verdict `clear`. Safety fact: outside `.ai/`, the branch changes only prose in `grill`, `spec`, and `start-ticket`. No frontmatter or heading changes, and no file cites the old `grill` fact line or a `spec` Step 3 rule number. Rung 4. No confirmed risk. Cleared: each other `/grill` caller (`diagnose`, `refine-ticket`, `do-next`, the journal, scribe, meta, and projects skills) now gets the fork rule too. That is the intent. A run that settles a fact is still under the `pause-list.md` rule. The `rule 4` hits in the persona `diff-signals.md` files cite persona rules, not `spec`. Open nit from the review: `start-ticket/SKILL.md` is 10,014 bytes. Proof, from the repo root on this branch:
  ```
  python3 - <<'PY'
  import re, subprocess, sys
  base = "8d3326c"
  bad = []
  def show(rev, f):
      return subprocess.run(["git","show",f"{rev}:{f}"],capture_output=True,text=True).stdout
  files = subprocess.run(["git","diff","--name-only",base,"HEAD","--",".",":!.ai"],capture_output=True,text=True).stdout.split()
  want = {"skills/primitives/skills/grill/SKILL.md","skills/engineering/skills/spec/SKILL.md","skills/engineering/skills/start-ticket/SKILL.md"}
  bad += [] if set(files) == want else [f"diff files: {files}"]
  for f in files:
      old, new = show(base, f), show("HEAD", f)
      if old.split("---")[1] != new.split("---")[1]: bad.append(f"frontmatter changed: {f}")
      h = lambda t: re.findall(r"^#+ .*$", t, re.M)
      if h(old) != h(new): bad.append(f"headings changed: {f}")
  hits = subprocess.run(["git","grep","-n","-F","If a _fact_ can be found by exploring the corpus","--",".",":!.ai"],capture_output=True,text=True).stdout
  bad += [] if not hits else [f"old line cited: {hits}"]
  cite = subprocess.run(["git","grep","-n","-i","-E","spec.{0,40}(rule|item) [45]","--",".",":!.ai"],capture_output=True,text=True).stdout
  bad += [] if not cite else [f"spec rule cited: {cite}"]
  for f in ["skills/engineering/skills/spec/SKILL.md","skills/engineering/skills/start-ticket/SKILL.md"]:
      bad += [] if "`/grill` fork rule" in show("HEAD", f) else [f"no fork-rule pointer: {f}"]
  bad += [] if "Before each question, classify it" in show("HEAD","skills/primitives/skills/grill/SKILL.md") else ["grill has no fork rule"]
  print(bad or "ok"); sys.exit(1 if bad else 0)
  PY
  ```
  Output: `ok`, exit 0.
- 2026-11-18: `/ship` checks gave go (push-only, no Stack check). The review covers the head: `git patch-id --stable` gives one ID for the reviewed range and the branch range, outside `.ai/`. Pushed 48281ca.
- 2026-11-18: unit 26 ticked on the map. Playbook `map`, stop H5: `/retro` offered on the batch. Next: the user runs `/retro` or says no, then `/work-on @.ai/map_pstack-program.md` starts the next batch at step 1.

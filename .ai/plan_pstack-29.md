---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-29_why
status: approved
goal: "`/why` on a line returns its history with citations."
spec: .ai/spec_pstack-29.md
builds_on: pstack-28
---

# Plan: pstack-29 `/why`

## Goal

A new skill, `skills/engineering/skills/why/SKILL.md`, answers why a line, a block, or a file is the way it is. It reads the commits and the PR threads that touched the target, cites the author of each source, and says what the record does not answer. Scope: SCOPED, one PR: one new skill and its README row.

## Spec

`.ai/spec_pstack-29.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `engineering/why` → it is a new skill that answers why from the commits and the PR threads of the target.
- [x] **B.** Read `engineering/why` → it cites the author of each source, and says what the record does not answer.
- [x] **C.** Run `/why` → the skill name is `why`.
- [x] **D.** Run `/why` on a line → it returns the history of the line, with a citation for each claim.

## Context

- Map: `.ai/map_pstack-program.md`, unit 29. Done line: `/why` on a line returns its history with citations.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-28_unslop`, because the unit 20 to 28 PRs are not merged. The home machine sets the unit 29 PR base to that branch. Keep the unit 20 to 28 `.ai/` files.
- Intent: see the spec. Source: pstack `skills/why` (research row r1.22). `explain` builds its why layer from reasoning, not from history. Credit pstack `why` in one line of prose in the skill.
- Decisions: the map names none for this unit.
- Out of scope: a change to `primitives/explain`. The research row suggested the explain why layer, but the map puts the skill in `engineering` as `why`.
- Where it lands: `engineering`, because it reads a repo and its code host. The skill names the code host as a tool role, not a product.
- Sources, in order: `git blame` for the target lines, `git log -L` for the history of the range, each commit's message, the PR that merged each commit (from a merge commit subject, or the code host), and that PR's description and review threads. A source that the agent cannot read goes into the unanswered part of the answer, with the reason.
- Answer shape: the answer first, then the history from oldest to newest, then what the record does not answer. Each claim cites its source: a short SHA or a PR number, and the author.
- Invocation: callable by the model, because it only reads. It writes no file and posts nothing.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-29_why`. The build machine runs no `gh` command on this repo, so the live run reads PR numbers from merge commit subjects, and lists the unread thread text as unanswered.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill reads commits and PR threads | L | skill text |
| B | the skill cites authors and names the gaps | L | skill text |
| C | the skill name is `why` | L | frontmatter |
| D | `/why` on a line returns its history with citations | M | behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | D | a fresh agent follows `why/SKILL.md` on one line of this repo that two or more commits touched. The answer cites a SHA or a PR number and an author for each claim, and lists what the record does not answer | EP | Manual | the live run in step 2 |

### Not testing

- A, B, C: skill text. The review step reads each against its AC.

## Steps

- [x] **1. The skill.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` and `skills/engineering/skills/codebase-news/SKILL.md` first. Write `skills/engineering/skills/why/SKILL.md` with `name: why`, the sources and the answer shape from Context, and one line of prose that credits pstack `why`. Add a `/why` row to the Skills table in `skills/engineering/README.md`.
  - Seam: `skills/engineering/skills/why/SKILL.md`.
  - Done: ACs A, B, and C hold on a read, and the pre-commit test passes.
- [x] **2. Live run.** Kind: config. Conditions: C1. Pick one line of this repo that two or more commits touched. Give a fresh agent the new `why/SKILL.md` and that line. Copy the result in short form into this Done line.
  - Seam: the `why` skill text, as an agent follows it.
  - Done: AC D holds. Run 1 on `codebase-news/SKILL.md:3-5` found a defect: the merge lookup read the newest merges (PRs 64 to 66). Fix 0a325e9 reads the first merge with `--reverse`. Run 2 cited f9d72c5, cfacd58, and bc205ca with author xxKeefer, and PR 32 and PR 39, which match a manual check. It listed the unread PR threads and the bc205ca reason as unanswered.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-29.md`. This step changes no code. Name `/engineering:light-review`.
  - Done: report `.ai/review_pstack-29_why.html`, base e85b601, head fdf4f62. Light run: persona-skills ran clean, no finding, no fix.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-29_why`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-29.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-29.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-28_unslop`, for the branch `pstack-29_why`.
- Decision log: decisions_pstack-29.tsv
- 2026-11-18: playbook `map`, step 3: four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done (c8ee6a3): `why/SKILL.md` and the README row. Pre-commit test passes. Next: step 2, live run.
- 2026-11-18: step 2 done: run 1 found the merge lookup defect, fix 0a325e9, run 2 passed.
- 2026-11-18: step 3 done: the gates each exit 0.
- 2026-11-18: step 4 done: light review ran the `persona-skills` lane, clean. Build loop stopped by rule 7.3. QA checklist skipped: the diff changes only skill text. Next: playbook step 5, `/blast-radius`.
- 2026-11-18: `/blast-radius`: verdict `clear`. Safety fact: outside `.ai/`, the branch adds one model-invocable skill with a unique name `why`, and one README row with the same column count as its neighbours. No script reads the engineering README table. Rung 4. No confirmed risk. Cleared: the `why` description can match a general "why" question about code, but the skill only reads, so the cost is one unneeded history read. The pre-commit hook passes on the tree. Proof, from the repo root on this branch:
  ```
  python3 - <<'PY'
  import re, subprocess, sys, glob
  base = "pstack-28_unslop"
  run = lambda *a: subprocess.run(list(a), capture_output=True, text=True).stdout
  bad = []
  files = set(run("git", "diff", "--name-only", base, "HEAD", "--", ".", ":!.ai").split())
  if files != {"skills/engineering/skills/why/SKILL.md", "skills/engineering/README.md"}: bad.append(f"diff files: {files}")
  readme = run("git", "diff", "-U0", base, "HEAD", "--", "skills/engineering/README.md")
  changed = [l for l in readme.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
  if len(changed) != 1 or not changed[0].startswith("+| `/why` |"): bad.append(f"README change: {changed}")
  cols = lambda l: len(l.strip().strip("|").split("|"))
  near = [l for l in open("skills/engineering/README.md") if l.startswith(("| `/work-on`", "| `/why`"))]
  if len({cols(l) for l in near}) != 1: bad.append("README row has a different column count")
  fm = open("skills/engineering/skills/why/SKILL.md").read().split("---")[1]
  if not re.search(r"^name: why$", fm, re.M) or "disable-model-invocation" in fm: bad.append("frontmatter")
  names = [m.group(1) for f in glob.glob("skills/*/skills/*/SKILL.md") if (m := re.search(r"^name: (\S+)", open(f).read(), re.M))]
  if names.count("why") != 1: bad.append("name why not unique")
  if subprocess.run(["sh", ".githooks/pre-commit"]).returncode: bad.append("pre-commit hook fails")
  print(bad or f"ok: {len(names)} skill names, why unique"); sys.exit(1 if bad else 0)
  PY
  ```
  Output: `ok: 180 skill names, why unique`, exit 0.
- 2026-11-18: `/ship` checks gave go (push-only, no Stack check). Plan: each build step done, no Pending Decisions. Tests: the three gates each exit 0 on the head. Review: `git patch-id --stable` gives one ID for the reviewed range e85b601..fdf4f62 and the branch range, outside `.ai/`. Constraints: no `CONSTRAINTS.md`. Tree: clean.

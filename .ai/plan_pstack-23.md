---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-23_typescript-rules
status: approved
goal: "`/install-rules` installs the TypeScript rule."
spec: .ai/spec_pstack-23.md
builds_on: pstack-22
---

# Plan: pstack-23 TypeScript rules

## Goal

Add a type section to `install-rules/rules/typescript-conventions.md`: six type rules, each with the principle behind it. Scope: SCOPED, one PR: one rule file edit.

## Spec

`.ai/spec_pstack-23.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `typescript-conventions.md` → it has a type section with six rules: branded primitives, discriminated unions, exhaustive checks with `never`, `satisfies` before `as`, parse at the boundary, and the simplest total type.
- [x] **B.** Read `typescript-conventions.md` → each of the six rules names the principle behind it.
- [x] **C.** Run the `/install-rules` steps → the installed `typescript-conventions.md` matches the source, byte for byte.

## Context

- Map: `.ai/map_pstack-program.md`, unit 23. Done line: `/install-rules` installs the rule.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-22_loop-until`, because the unit 20 to 22 PRs are not merged. The home machine sets the unit 23 PR base to that branch. Keep the unit 20 to 22 `.ai/` files.
- Intent and Decisions: see the spec. Extend the existing file. Cite each principle by name, not by path, because the rule installs to `~/.claude/rules/`.
- Principles to cite: `principle-type-system-discipline` (brands, unions, parse at the boundary), `principle-model-the-domain` (discriminated unions in place of flags), `principle-boundary-discipline` (parse at the boundary, trust inside), `principle-laziness-protocol` or `principle-minimize-reader-load` (the simplest total type). Read each one before the step cites it.
- Fit with the existing file: the `as const` object pattern and the bang-operator section stay. `satisfies` before `as` matches the user's rule that a cast is a last resort and needs a reason.
- The rule names no employer code, and no library that only one project uses. The scrub hook checks the names.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A rule changes only after the user runs `/install-rules`, and loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-23_typescript-rules`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the rule holds the six type rules | L | rule text |
| B | each rule names its principle | L | rule text |
| C | the install copies the rule unchanged | L | `cp` of a file that the skill already installs |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | C | the `/install-rules` steps, run with `HOME` set to a temp folder, leave a `typescript-conventions.md` that `cmp` finds equal to the source | EP | Manual | the install check in step 2 |

### Not testing

- A and B: rule text. The review step reads each against its AC.
- The install into the real `~/.claude/rules/`: the map Trial runs `/install-rules` after the last unit. A temp `HOME` runs the same commands with no change to the live rules.

## Steps

- [x] **1. The type section.** Kind: docs. Read the four principles in Context first. In `skills/utility/skills/install-rules/rules/typescript-conventions.md`, add a `## Types` section after `## Code Style`. One short rule for each: brand a semantic primitive; model variants as a discriminated union, not as flags; end each `switch` on a union with an exhaustive `never` check; use `satisfies` before `as`, and give a reason for each `as`; parse external data at the boundary into a typed model, then trust the type; use the simplest type that covers every value, with no optional field that is always set and no `any`. Give each rule one short bad and good TypeScript example where the rule is not clear without one. End each rule with the principle name it follows.
  - Done: AC A and B hold on a read, and the pre-commit test passes.
- [x] **2. Install check.** Kind: config. Conditions: C1. Run the commands of `/install-rules` Steps 1, 3, and 4 with `HOME` set to a new temp folder and `CLAUDE_SKILL_DIR` set to the skill folder. Delete the temp folder.
  - Done: AC C holds. The Step 4 check prints no `MISMATCH` line.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-23.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line. Report: `.ai/review_pstack-23_typescript-rules.html`. Base d0d44a5, head d3c0a07.
- [x] **4a. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-23.md`. Run the `persona-skills` lane, and each lane whose guard matches a file that changed after d3c0a07. This step changes no code. Name `/engineering:light-review`.
  - Done: the report path and the reviewed base and head SHAs are in this line. Report: `.ai/review_pstack-23_typescript-rules.html`. Base d0d44a5, head 1f39448.
- [x] **5. Push.** Push-only map: run `git push -u origin pstack-23_typescript-rules`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line. Pushed head 4c21dbb to `origin/pstack-23_typescript-rules`.

## Suggested skills

- `/build @.ai/plan_pstack-23.md`: every step, then the test and review loop, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-23_typescript-rules`.
- Decision log: decisions_pstack-23.tsv
- 2026-11-18: playbook `map`, step 3: four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: `## Types` section added with six rules, each naming its principle.
- 2026-11-18: step 2 done: install run with a temp HOME printed no MISMATCH line; temp folder deleted.
- 2026-11-18: step 3 done: the gates are green.
- 2026-11-18: step 4 done: light review ran persona-skills only, with no finding; report `.ai/review_pstack-23_typescript-rules.html`, base d0d44a5, head d3c0a07.
- 2026-11-18: build loop stopped at rule 7.3: the review has no open row. QA checklist skipped: the diff changes only rule text. After the review, a `tsc --strict` run on the Types examples found that the good `load` example did not compile (TS2355, a `User` return with an empty body). Fixed in 8176215: both `load` examples are now declarations. Each good example compiles. Next: playbook step 5, `/blast-radius`.
- 2026-11-18: `/blast-radius`: verdict `clear`. Safety fact: outside `.ai/`, the branch only adds lines to `typescript-conventions.md` and keeps its `paths:` frontmatter, so the rule loads for the same files as before; each principle that the Types section names exists; and each good example compiles under `tsc --strict`. Rung 4. No confirmed risk. Cleared: the only reader of the rule outside `.ai/` is the pointer in `principle-type-system-discipline/SKILL.md:16`, which the new section now fills; no script parses the rule; `/install-rules` copies `rules/*.md` byte for byte (step 2); the `satisfies` rule agrees with the user's rule that a cast is a last resort. Proof, from the repo root on this branch:
  ```
  python3 - <<'PY'
  import os, re, subprocess, sys, tempfile
  F = "skills/utility/skills/install-rules/rules/typescript-conventions.md"
  bad = []
  num = subprocess.run(["git","diff","--numstat","d0d44a5","HEAD","--",".",":!.ai"],capture_output=True,text=True).stdout.split()
  bad += [] if num == ["125","0",F] else [f"diff outside one add-only file: {num}"]
  s = open(F).read()
  old = subprocess.run(["git","show",f"d0d44a5:{F}"],capture_output=True,text=True).stdout
  bad += [] if s.split("---")[1] == old.split("---")[1] else ["paths frontmatter changed"]
  sec = s[s.index("\n## Types\n"):s.index("## Separation of Concerns")]
  bad += [f"missing {p}" for p in set(re.findall(r"`(principle-[a-z-]+)`", sec)) if not os.path.exists(f"skills/engineering/skills/{p}/SKILL.md")]
  lab, good = None, []
  for part in re.split(r"(bad:\n|good:\n)", sec):
      if part in ("bad:\n","good:\n"): lab = part; continue
      for b in re.findall(r"```ts\n(.*?)```", part, re.S):
          if lab != "bad:\n": good.append(b)
          lab = None
  src = "type Order = { id: string };\ndeclare function parseOrder(x: unknown): Order;\n" + "\n".join(good)
  src = src.replace("type Request","type Req").replace("request: Request","request: Req")
  src = src.replace("const order = parseOrder(await response.json());","async function f(response: Response) { return parseOrder(await response.json()); }")
  d = tempfile.mkdtemp(); open(f"{d}/t.ts","w").write(src + "\nexport {};\n")
  r = subprocess.run(["npx","-y","-p","typescript","tsc","--noEmit","--strict","--target","es2022","--lib","es2022,dom",f"{d}/t.ts"],capture_output=True,text=True)
  bad += [] if r.returncode == 0 else ["tsc: " + r.stdout]
  print(f"good examples: {len(good)}"); print(bad or "ok"); sys.exit(1 if bad else 0)
  PY
  ```
  Output: `good examples: 6`, `ok`, exit 0.
- 2026-11-18: `/ship` check gave no-go on Review: 8176215 changed the rule after the reviewed head d3c0a07. Step 4a added: a new review round on the current head.
- 2026-11-18: step 4a done: light review ran persona-skills only, with one open nit (row r2.1: add a line that says where the principles live); report `.ai/review_pstack-23_typescript-rules.html`, base d0d44a5, head 1f39448. The step changes no code, so the row stays open.
- 2026-11-18: `/ship` checks gave go (push-only, no Stack check). Pushed 4c21dbb. Review row r2.1 (nit) stays open for the user: the bare `Principle:` lines give an agent with only the `utility` plugin no path to the principle.
- 2026-11-18: unit 23 ticked on the map. Playbook `map`, stop H5: `/retro` offered on the batch. Next: the user runs `/retro` or says no, then `/work-on @.ai/map_pstack-program.md` starts the next batch at step 1.

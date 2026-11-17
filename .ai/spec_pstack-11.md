---
doctype: spec
ticket: none
status: confirmed
goal: /create-verification-skill on a small app writes a driver that passes its own proof run, and /verify finds it from a diff.
---

# Spec: /verify and the drivers

Unit 11 of `.ai/map_pstack-program.md` (r1.5). The user approved the map at H0, so this spec is
confirmed.

## Intent

- Outcome: a repo app gets a driver, a skill named `verify-<repo>-<app>` that launches the app, drives it the way a user does, and keeps the evidence. `/verify` finds the drivers for a diff and runs them.
- User: the user, and each skill that must see a change live: `/test`, `/interrogate`, `/blast-radius`, and `/qa-screenshots`.
- Why now: no skill can run the real app, so "saw it live" (rung 5 of `/blast-radius`) has no route, and a test step can only read code (r1.5).
- Success: `/create-verification-skill` on a small app writes a driver that passes its own proof run, and `/verify` finds that driver from a diff.
- Constraint: `/verify` is a thin router. It holds no drive steps of its own. Each driver is a plain skill.
- Out of scope: the `benchmark` skill (unit 24) calls `/verify` when it exists. A driver for this repo. The formal-verification skills of pstack.

## Decisions

- Sources: pstack `create-verification-skill`, `maintain-verification-skill`, and `references/feature-map-example`, adapted to this repo. pstack writes to `.cursor/skills/`. This repo writes to the locations below.
- Name: a driver is `verify-<repo>-<app>`. `<repo>` is the repo name from `git remote get-url origin`. An app or a library each get one driver. A library is driven as its consumer uses it: Storybook, a PTY, or a scratch consumer script.
- Location: a work repo keeps its drivers in `~/.claude/skills/`. The user's own repo keeps them in the repo's `.claude/skills/`, committed. A repo is the user's own when its remote owner is an owner that `~/.claude/AGENTS.md` names as the user's. Else, the driver goes in `~/.claude/skills/`, so no driver lands in a team repo by mistake.
- Paths: a driver's frontmatter holds `app-paths:`, a list of globs from the repo root. `/verify` matches the diff paths against these globs. The repo already uses a custom frontmatter key (`deprecated:`), so a custom key has a precedent.
- `/verify` reads the repo from `git remote`, finds the apps from the diff paths, and runs each matched driver. A script does the match, so the match is deterministic and tested. With no match, it returns `no driver`, and the caller's test step writes that in the plan's `Progress`. `/retro` then proposes `/create-verification-skill`.
- A driver's `SKILL.md` has Launch, Doctor, Drive, Evidence, Cleanup, and Helpers. `features/README.md` indexes one file per feature. Each feature file has `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. A script checks this layout, so `create` and `maintain` both run one check.
- `/verify` drives run at the `verifier` role of the `models` block. With no `models` block, they use the session model.
- No skill of the three has `disable-model-invocation`: other skills call `/verify`, and `/retro` proposes the other two (map decision: the HITL line is on actions, not skills).
- `maintain-verification-skill` ships its fix as a commit on the agent's own branch, and a draft PR for a driver in the repo. A driver in `~/.claude/skills/` gets the edit in place, with no PR. Both are off the pause list.

## Acceptance criteria

- [ ] **A.** Read `engineering/verify` → it reads the repo from `git remote`, finds the drivers from the diff paths with a script, runs each one, and returns `no driver` when none matches.
- [ ] **B.** Read `engineering/create-verification-skill` → it interviews the repo, writes a driver with the six sections and a feature map, picks the location by the owner rule, and proves the driver by one run before it hands it over.
- [ ] **C.** Read `engineering/maintain-verification-skill` → it keeps a driver and its feature map true to the app, with a source wave, a live pass, and the outcome `clean`, `changed`, or `blocked`.
- [ ] **D.** Read `/test`, `/interrogate`, `/blast-radius`, and `/qa-screenshots` → each calls `/verify` where it must see the change live. On `no driver`, the test step writes that in `Progress`, and `/retro` proposes `/create-verification-skill`.
- [ ] **E.** Run the layout check on a driver with a missing section → it exits 1 and names the section.
- [ ] **F.** Run `/create-verification-skill` on a small app, then `/verify` on a diff of that app → the driver passes its own proof run, and `/verify` finds it from the diff.

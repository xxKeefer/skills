---
name: retro
description: >
  Run a retrospective on a coding session to improve the agent's whole setup: the skills repo, its
  hooks and rules, and the global steering files. Read the session, find what slowed or misled the
  agent, route each finding to the place that fixes it, put every proposal in one table, then
  apply and commit the approved ones.
disable-model-invocation: true
argument-hint: "[session id or transcript path]"
---

# Retro

`/self-improve` sharpens the review panel from a repo's history. `/retro` improves everything
else that shapes a run: the skills, the hooks, the rules, and the steering files. It reads one
session and asks what in the setup would have made that session faster or right the first time.

`$SKILL_DIR` is this skill's base directory. `$SKILLS_ROOT` is the root of the skills repo:
`git -C "$SKILL_DIR" rev-parse --show-toplevel`. If `$SKILL_DIR` is not in a git repo, ask the
user for the path of the skills repo.

```
read the guide → read the session → find → route → one table → apply → commit
```

## Step 1: Read the guide

Read `$SKILLS_ROOT/skills/meta/skills/writing-great-skills/SKILL.md`, if it exists. Each
proposal that edits a skill follows it.

**Done when:** you read the guide, or found that it does not exist.

## Step 2: Read the session

1. Take the session from `$ARGUMENTS`: a session id or a transcript path. Else use the current
   session.
2. For another session, find its transcript among the session logs on this machine.
3. Read the primary record: each user message, each tool call and its result, each correction,
   and each retry. Note the repo that the session ran in.
4. Read the steering files that the session loaded: the global `CLAUDE.md` or `AGENTS.md`, the
   repo's, and each rule file.

**Done when:** you have the session record, its repo, and its steering files.

## Step 3: Find the candidates

Look for each kind below. Back each candidate with a moment in the session: the turn, the tool
call, or the user's words. No candidate without one.

| Kind | Look for |
| --- | --- |
| **Skill gap** | The user did a task by hand that a skill could own, or a skill was missing a step that the agent had to work out. |
| **Skill misfire** | A skill step misled the agent, ran in the wrong order, contradicted another skill, or did not trigger when it should have. |
| **Navigation** | The agent took long to find a file or a fact. A pointer in a skill, a reference, or a steering file would have saved the search. |
| **Automated check** | The agent made a mistake that a check could catch: a hook, a pre-commit check, a lint rule, a test. First read the checks that exist (`.githooks/`, the lint config, the CI workflow). A check that exists but is not wired, or is broken, is the finding. |
| **Review miss** | A mistake reached the user that a reviewer should have caught, or a reviewer flagged something it should not have. |
| **Steering bloat** | A line in a global or repo steering file belongs in a rule, a skill, or a check. A line that changes no behaviour is a no-op, so cut it. |
| **Tool economy** | A tool call that cost a lot of tokens and could be cheaper, or a tool that returns far more than the agent uses. |
| **Information access** | A fact the agent needed but could not reach, such as a log, a service, or a doc. |

Classify each check-shaped mistake first. A **mechanical** one, such as a banned pattern, an
import shape, or a file location, gets a check, not a sentence. Keep prose rules for judgement
calls that no check can make.

Keep the split between building and reviewing in mind. The agent that builds carries the most
context. The reviewer gets only a diff. So a coding standard goes to the reviewer, not to a
steering file that the builder must carry.

**Done when:** each candidate has a kind and a moment in the session.

## Step 4: Route each candidate

Give each candidate one route:

| Candidate | Route | On yes |
| --- | --- | --- |
| Skill misfire, skill gap in an existing skill, navigation inside a skill | Edit that skill in `$SKILLS_ROOT` | Step 6 makes the edit |
| A task that no skill owns, seen in this session and likely to repeat | A new skill in `experimental`, through `/write-a-skill` | Step 6 runs `/write-a-skill` |
| Mechanical mistake | A hook through `/write-a-hook`, or a path rule through `/write-a-rule` | Step 6 runs that skill |
| Review miss | An entry in the calibration backlog of `/self-improve` | Step 6 appends the entry |
| Steering bloat, no-op | Move the line to a rule, a skill, or a check, or cut it | Step 6 edits the steering file |
| Tool economy | `/audit-workflow` for spend, or the skill that made the call | Report only, or Step 6 edits the skill |
| Specific to the session's repo, not to the setup | That repo's `CLAUDE.md`, `AGENTS.md`, or lint config | Report only |
| Information access | The tool or access to add | Report only |

A review miss goes to the backlog at
`${XDG_STATE_HOME:-$HOME/.local/state}/self-improve/improve-personas.md`, in the entry format of
`$SKILLS_ROOT/skills/code-review/skills/mob-review/SKILL.md` Step 7. Read the backlog first. If an
`open` entry names the same target and problem, add this session's Evidence line to it. If a
`rejected` entry covers it, drop the candidate.

The skills repo is public. Write each edit that lands in it in general words, with no names of
people, employers, clients, repos, paths outside the repo, keys, or URLs. The specifics stay in
the table and the Evidence line.

**Done when:** each candidate has one route.

## Step 5: Put every proposal to the user

Print one table, ordered by severity, the costliest first, numbered from 1:

| # | Kind | Target | Proposal | Evidence |
| --- | --- | --- | --- | --- |

- Target: a skill, a hook, a rule, a steering file, the backlog, a new skill, or another repo.
- Proposal: the edit in one or two lines.
- Evidence: the moment in the session, in a few words.

Then ask once: "Name the rows to apply. A row you do not name is dropped." A report-only row
changes nothing.

**Done when:** the user named the rows to apply.

## Step 6: Apply and commit

1. For each approved row, make the change through its route. A skill edit bumps the version of
   its domain in `plugin.json`. A new skill adds a row to the domain's `README.md`.
2. Run the scrub check in `$SKILLS_ROOT/.githooks/pre-commit` on the staged tree. Fix each match.
3. Commit the changes in `$SKILLS_ROOT`, one commit for each domain. A steering file outside the
   repo gets no commit.
4. Show each path that changed, and the commits.

**Done when:** each approved row is applied, and each change in `$SKILLS_ROOT` is committed.

## Step 7: Return

Print the count of rows applied and dropped, the commits, and each steering file outside the repo
that changed.

**Done when:** the user has the summary.

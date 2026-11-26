# 0018 Skills depend on named CLI tools through tool roles

**Status:** Accepted, 2026-11-26.

## Context

The north star says that a skill depends on no tool beyond the agent. Some skills already broke
that rule through tool roles: the tracker, the code host, the browser, and the notifier. A skill
names the role, and the `## Tools on this machine` block of `~/.claude/AGENTS.md` names the
product.

`/visualise-pr` needs two more tools. It measures complexity for each function with a CLI, and it
opens a file at a line in the editor. An agent estimate of complexity is not repeatable, and a
link to the code host fails for commits that are not on the remote.

## Decision

- The suite can depend on a named CLI tool. A skill reaches the tool only through a tool role.
- Add two roles: `Editor`, for a URL that opens a file at a line, and `Complexity`, for a CLI that
  measures complexity for each function. On the author's machine they are Zed and `lizard`.
- `install-agents-md` holds the generic row and the hydrate rule for each role. The machine values
  stay in `~/.claude/agents-md.values.json`.
- When a role is `none`, or its tool does not run, the skill says so in its output, gives the
  install command, and labels each value that it estimates instead.

Options not chosen:

- Name the tool in the skill. A machine with a different tool then needs a skill edit.
- Keep every skill tool-free. Complexity numbers are then estimates in each run.

## Consequences

- A machine must run `/install-agents-md` again to get the new rows.
  Until then, a skill that reads the role finds no row, and treats the role as `none`.
- A new role costs one row in `sections/tools.md` and two keys in `HYDRATE.md`.
- `/write-report` accepts `zed://file/` links, because the `Editor` role on this machine is Zed. A
  new editor scheme needs a change to `check_report.py` and `template.html`.

# Playbook: Parallel

Take two or more tickets to one stack of draft PRs and one QA pass. Each ticket builds alone, on
its own branch from the default branch, at the same time as the others. The stack forms once, at
the end. The stops are the stops in [`SKILL.md`](../SKILL.md).

The user sees two stops: the plans, and the finished stack with its QA report. Between them, the
run asks nothing. A ticket never waits for another ticket, and never rebases onto one, until
step 4.

## Steps

| # | Step | Stop after the step |
| --- | --- | --- |
| 1 | For each ticket with no approved plan, run `/plan <ticket key>`. It claims a worktree on a new branch from the remote default branch. In each plan's `## Progress`, write the playbook `parallel` and the plan path of each other ticket in the batch, so that `/work-on @<plan path>` on any one plan continues the whole batch. | H2, once for the batch: the user approves every plan in one answer. |
| 2 | Run the `/build` of each plan side by side. Each plan has its own worktree, so one step subagent for each plan runs at the same time. Inside one plan, run one subagent at a time, as `/build` says. When two plans need the same code, such as a shared call, each plan builds what it needs. Step 4 keeps one copy. | No stop. A plan that ends on a `D` entry waits. The other plans go on. |
| 3 | For each plan, run `/blast-radius @<plan path>`. When the verdict is `risk` and each confirmed risk has a clear fix, add one fix step for each, and run `/build @<plan path>`. Run `/interrogate @<plan path>` only when a confirmed risk has no clear fix. When its report keeps a finding, run `/build @<report path> <each kept row ID>`. | H3, once for the batch, after every plan stops: give every open `D` entry of every plan in one list. After the answers, run steps 2 and 3 again for those plans only. |
| 4 | Stack the branches once. Order them: a plan that depends on another goes above it, else the order in which the plans finished step 3. From the bottom, rebase each branch onto the one below, fix the conflicts, keep one copy of shared code, and run the gates. When a conflict fix changes runtime behaviour, add a test and review round to that plan, as `/build` Step 1 item 7 says, and run `/build @<plan path>`. Then join the stack as [`create-pr/references/stack.md`](../../create-pr/references/stack.md) says. | No stop. |
| 5 | From the bottom of the stack, check out each branch and run `/ship @<plan path>`. It opens a draft PR with no stop. | H3 when `/ship` gives no-go. H4, only before an action on the pause list. |
| 6 | Run `/happy-path` once over the diff from the default branch to the top of the stack, then `/sad-path` when its guard matches. Both write one QA report for the whole stack. Give the user one table (ticket, PR, status) and the QA report URL. | H4: the user runs the one QA pass, then marks the stack ready and merges. |
| 7 | Offer `/retro` on the batch. The user runs it, or says no. | H5, when the user runs `/retro`. |

**Done when:** each ticket has a draft PR in one stack, the user has one QA report for the whole
stack, and the user has the `/retro` offer.

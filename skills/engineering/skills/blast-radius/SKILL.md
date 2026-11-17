---
name: blast-radius
description: >
  Find what a change can break outside its diff, prove by a run the one fact that makes it safe,
  and give a verdict of clear or risk. Applies no fix. Use when the user says "blast radius",
  "what could this break", or wants a small diff checked, or when /work-on runs it after the build
  loop.
argument-hint: "[@<plan path> | <scope>]"
---

# Blast radius

A change can break code that the diff does not show. This skill finds that breakage. It also finds
the one fact that makes the change safe, and proves that fact with a run. A write-up that sounds
right proves nothing. Report the findings and apply no fix.

Principle: **principle-prove-it-works** ([`../principle-prove-it-works/SKILL.md`](../principle-prove-it-works/SKILL.md)). Read the file before you apply it, and name it in the reply when it shaped a choice.

Adapted from pstack `blast-radius`.

Run at the `prover` role of the `models` block in `~/.claude/AGENTS.md`. With no `models` block,
use `opus` at high effort, else the session model.

## The ladder

For each fact that the safety of the change depends on, climb as far as is cheap. Say which rung
you reached.

1. **Said so.** You state it. This proves nothing.
2. **Pointed at it.** You cite a real `file:line`, or the source of the library.
3. **Showed it cannot happen.** You walked the failure step by step, and it does not reach.
4. **Ran it.** A script or a test calls the real code, and exits non-zero when you are wrong.
5. **Saw it live.** You reproduced it in the running app, through `/verify` when the repo has a
   driver. With no `/verify` skill, or no driver, rung 4 is the top rung.

```
read the change → find the safety fact → look past symbol search → rate each risk → prove the fact → verdict → output
```

## Step 1: Read the change

1. Find the scope. It is what the user names. Else it is the diff of the current branch from its
   merge base with the base branch, plus the working tree. With a plan path, the base is the plan's
   base branch when it names one.
2. List each symbol that the change adds, changes, or deletes. State what the code now does
   differently, and include the part that the diff does not show.

**Done when:** you can state what the change does, including the part that is not in the diff.

## Step 2: Find the one safety fact

Most risky changes are safe because of one fact. An example: "this call drops only dead cache
entries and does nothing else". Find that fact. When it holds, it clears most of the risks at
once. Spend your time here, not on a long list of maybes.

**Done when:** you have written the safety fact in one sentence.

## Step 3: Look where a symbol search stops

A list of callers is not the job. Look for the breakage that a search does not show:

- The source of each library that the change calls, its pinned version, and any local patch.
- When code runs: start-up, teardown, async ordering.
- Data that other code reads: an API response, a database column, a wire format, another language
  that reads the same bytes.
- A feature flag, a config key, and code three calls downstream.

**Done when:** you checked each place in the list that applies, and wrote what you found.

## Step 4: Rate each risk

1. Give each risk a real chance of happening and a real cost when it does.
2. Cite a real `file:line`. A search that finds nothing is an answer. Never invent a caller or an
   API.
3. Keep two lists: the risks that you confirmed, and the risks that you checked and cleared, each
   with its reason.

**Done when:** each risk is in the confirmed list or in the cleared list.

## Step 5: Prove the safety fact

Write a script or a test that calls the real code, and exits non-zero when the fact is false. Run
it. Keep the exact command and its output. When you cannot get to rung 4, say which rung you
reached and why.

**Done when:** you have the rung reached, and for rung 4 or 5, the command and its output.

## Step 6: Give the verdict

- `risk`: a confirmed risk exists, or the safety fact is below rung 4.
- `clear`: the safety fact is at rung 4 or 5, and no confirmed risk exists.

**Done when:** the verdict is one word, `clear` or `risk`.

## Step 7: Write the output

Give these parts, in this order:

1. **Verdict.** `clear` or `risk`.
2. **What it does.** What changed, including the part that is not in the diff.
3. **Safety fact.** The fact, the rung reached, and the command that proved it. When it is
   unproven, write `unproven`.
4. **Risks.** Each confirmed risk: how it breaks, the `file:line`, the chance, the cost, and how to
   check it.
5. **Cleared.** Each risk that you checked, with its reason.
6. **Before you merge.** The cheapest test or repro that catches the real bug.

With a plan path, run `/update-plan` on the plan and record in its `## Progress`: the verdict, the
safety fact, the rung, the command, and each confirmed risk. With no plan, write the output in the
reply only. Write no other file.

**Done when:** the output names the rung reached and the command that proved it, and each
principle that shaped a choice.

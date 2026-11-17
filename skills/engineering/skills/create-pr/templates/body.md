# PR body

The structure of the body that `create-pr` writes. Step 4 writes the top sections, and Step 3
writes the AC block.

## Top sections

```markdown
## Why

<the goal, as one or two sentences>

## Summary

<one sentence>

<visual>

## Evidence

**Before:** <failing test, output, or screenshot>
**After:** <passing test, output, or screenshot>

## Merge danger

**Door:** <one-way | two-way>. <why, when not obvious>
**Blast radius:** <one word, such as localised, module, app, or consumers>. <what can break>
```

### Merge danger rules

A two-way door is cheap to roll back: revert and redeploy. A one-way door is not. Each of these
makes a one-way door, even in a small diff:

- A schema or data migration, or a delete or rewrite of stored data.
- A message that leaves the system, such as an email, a notification, or a webhook.
- A change to a published contract, such as a public API, an event shape, or a released
  package.
- A change to a secret, a permission, or billing.

The blast radius is what a bad merge can break, and for whom. Think about each consumer of the
changed code: callers, other apps, layout and mobile, and stored data.

## AC block

Put the AC table in a collapsed block. Keep a blank line after `<summary>` and before
`</details>`:

```markdown
**Gaps:** <None | n>
- <condition>: <reason or follow-up>

<details>
<summary>Acceptance criteria: <n>, <n> high risk, <all tested | n not tested (B, C)></summary>

| AC | Risk | Tested by | Conditions |
| --- | --- | --- | --- |
| **A.** <AC, short> | H | Unit: `<test file>` › <test name> | C1 quantity 1 and 99 · C2 0 and 100 |
| — | <behaviour that no AC covers> | … | … |

</details>
```

### AC table rules

- One row for each AC letter. A sub-check gets its own row only when a different test proves it.
  A struck-through AC gets no row.
- One `—` row for each `—` row of the Test approach.
- **Risk** comes from the Risks table.
- **Tested by** is the level, the test file, and the test name, from the step done lines and the
  test names from Step 1 of `SKILL.md`. Use `Manual: <why>` only when no test can prove the AC.
- **Conditions** lists the condition IDs that a test in the diff covers, each with a few words.
- **Gaps** lists each planned condition with no test in the diff, and each Not testing item. Each
  gap has a reason or a follow-up. If the plan gives no reason, write `reason needed`, and the
  gate asks for it. Write `**Gaps:** None` only when that is true.

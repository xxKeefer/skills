# PR body

The structure of the body that `create-pr` writes. The body uses progressive disclosure. The
masthead is open: Summary, Why, and Details. Each other section is a collapsed block, and its
`<summary>` line gives the result, so a reviewer can stop at the masthead.

## Masthead

Step 4 writes the masthead.

```markdown
# Summary

<one sentence>

<visual>

## Why

<the goal, as one or two sentences>

## Details

- **Merge order:** <merge line>
- **FF:** <`flag_name`. what sits behind it | None>
- **User-facing change:** <Yes | No>
  - <what a user sees, one bullet each>
- **Functional change:** <Yes | No>
  - <what the system does differently, one bullet each>
- **Gaps:** <None | n>
  - <condition>: <reason or follow-up>
```

### Details rules

- **Merge order** shows only with a `merge` key or in a gh stack. `references/stack.md` gives the
  merge line.
- **FF** names the feature flag that gates the change, from the plan's gates, else from the diff.
  Write `None` only when no flag gates the change.
- **User-facing change** is what a user can see or do. **Functional change** is what the system
  does that a user cannot see, such as calls, storage, or lifecycle. With `No`, write no bullets.
- **Gaps** lists each planned condition with no test in the diff, and each Not testing item. Each
  gap has a reason or a follow-up. If the plan gives no reason, write `reason needed`, and the
  gate asks for it. Write `**Gaps:** None` only when that is true. With no ACs, leave out the
  line.

## Collapsed blocks

Put each block after the masthead, in this order. Leave out a block that has nothing to say. Keep
a blank line after `<summary>` and before `</details>`:

```markdown
<details>
<summary><Name>: <result></summary>

<content>

</details>
```

| # | Block | `<summary>` result | Content |
| --- | --- | --- | --- |
| 1 | Merge danger | `<one-way \| two-way> door, <blast radius>` | The door and the blast radius, as the merge danger rules say |
| 2 | Evidence | what the proof is, such as `screenshot` or `test fails before, passes after` | **Before:** and **After:** lines |
| 3 | Acceptance criteria | `<n> ACs, <n> high risk, <n> tested manually (<letters>)` | The AC table |
| 4 | Testing | the test levels, then ` · ` and the verification line, such as `1508 of 1508 spec files pass` | The testing notes, then the template's testing section and its checkboxes |
| 5 | Description | `<n> areas` | The template's description: one bullet for each area of the change |
| 6 | Each other template section | a count or a short result | That section |
| 7 | Related tickets | `<n> ticket, <n> links` | The ticket links |
| 8 | Follow-ups | `<n>` | Each entry of the plan's `Follow-ups` section |
| 9 | Commits | `<n> (<count of each type>)` | One bullet for each commit |

Write Merge danger in bold in its `<summary>` line when the door is one-way, so a reviewer sees it
without opening the block.

### Merge danger rules

```markdown
**Door:** <one-way | two-way>. <why, when not obvious>
**Blast radius:** <one word, such as localised, module, app, or consumers>. <what can break>
```

A two-way door is cheap to roll back: revert and redeploy. A one-way door is not. Each of these
makes a one-way door, even in a small diff:

- A schema or data migration, or a delete or rewrite of stored data.
- A message that leaves the system, such as an email, a notification, or a webhook.
- A change to a published contract, such as a public API, an event shape, or a released
  package.
- A change to a secret, a permission, or billing.

The blast radius is what a bad merge can break, and for whom. Think about each consumer of the
changed code: callers, other apps, layout and mobile, and stored data.

### AC table rules

```markdown
| # | AC | Old behaviour | Risk | Implementation | Tested by | Conditions |
| --- | --- | --- | --- | --- | --- | --- |
| A | <AC, short> | <what happened before> | H | <where the change delivers it> | Unit: `<test file>` › <test name> | <condition> · <condition> |
| — | <behaviour that no AC covers> | … | … | … | … | … |
```

- One row for each AC letter. A sub-check gets its own row only when a different test proves it.
  A struck-through AC gets no row.
- One `—` row for each `—` row of the Test approach.
- **Old behaviour** is what a user or the system saw before the change. A new surface gets
  `None (new <surface>)`. A row that keeps behaviour gets `None (behaviour kept)`.
- **Risk** comes from the Risks table.
- **Implementation** names the module, function, or component that delivers the AC, in one
  clause. Write a different clause for each row. Do not write "Same as A".
- **Tested by** is the level, the test file, and the test name, from the step done lines and the
  test names from Step 1 of `SKILL.md`. Add `Manual: <what>` for each AC that a person also
  checked by hand. Use `Manual` alone only when no test can prove the AC.
- **Conditions** lists what a test in the diff covers, a few words each, split by ` · `.

### Testing notes

Put these lines before the template's checkboxes. Leave out a line that has nothing to say:

```markdown
**Existing behaviour:** <the existing specs that still pass, and any mock that this PR removes><br>
**Variations:** <each dimension and its values, from the Test approach><br>
**Notes:** <a fact that a tester needs, such as placeholder copy>
```

### Related tickets rules

One line for each link, each with a verb and one clause on why it matters:

```markdown
**Ticket:** [<KEY>](<url>): <title><br>
**Fixes:** [<KEY>](<url>): <title>. <how this PR fixes it><br>
**Stacked on:** #<n> ([<KEY>](<url>)). <why><br>
**Uses:** #<n> ([<KEY>](<url>)). <what it takes from it><br>
**Unblocks:** [<KEY>](<url>). <what it needs from this PR><br>
**Epic:** [<KEY>](<url>): <title>
```

Write each ticket key as a link, in the body and in every block.

### Commits rules

List the commits from `git log --reverse --format='%h %s' "$(git merge-base origin/<base> HEAD)"..HEAD`,
one bullet each, with the short SHA in backticks.

---
name: sad-path
description: >
  Generate a manual QA checklist that tries to break the current changeset, built from the test
  data of the edge-case personas. Each item names the exact input or key and cites a catalogue ID.
  Use when the user says "sad path", asks which edge cases to try by hand, or wants to break a
  form before closing out.
---

# Sad Path

Produce a manual QA checklist of the inputs and keys that break the changed screens. It is the
other half of `/happy-path`. The test data lives with the personas, so the review panel and this
checklist share one copy.

## Lanes

| Lane | Persona (read its Guard) | Fixtures | Catalogue |
|---|---|---|---|
| `form-behaviour` | [`persona-form-behaviour`](../persona-form-behaviour/SKILL.md) | [`fixtures.md`](../persona-form-behaviour/references/fixtures.md) | [`catalogue.md`](../persona-form-behaviour/references/catalogue.md) |
| `text-input` | [`persona-text-input`](../persona-text-input/SKILL.md) | [`fixtures.md`](../persona-text-input/references/fixtures.md) | [`catalogue.md`](../persona-text-input/references/catalogue.md) |

## Step 1: Read the Changeset

Find the changeset:

1. If `$ARGUMENTS` holds a commit range, use it.
2. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. It prints
   `origin/<name>`. Fall back to `main`.
3. Off the default branch, diff against `git merge-base HEAD <default>`.
4. On the default branch, use the uncommitted diff, `git diff HEAD`.
5. If that diff is empty, ask the user for a range.

Read the `--stat`, then the diff of the non-test source files. If `$ARGUMENTS` holds resource
links, invoke `/look-up` for them.

**Done when:** you have the changed non-test source files and their hunks.

## Step 2: Pick the Lanes

For each lane, read only the Guard section of its persona. The rest of the persona is a code
review, and this skill writes a checklist.

A lane runs when a changed hunk in any non-test source file shows one of the Guard's code
signals, such as a form control, a schema rule, or a key handler. The Guard's path filter and
file types do not apply here. Its rule about hunks that do not count still applies.

For each lane that runs, list what the change touches: each form, each field by the label the
user sees, and each field's bounds and rules.

**Done when:** each lane is marked run, with the signal and the changed line, or skip.

## Step 3: Build the Items

For each lane that runs:

1. Read its fixtures file.
2. List the `###` headings of its catalogue. Each heading holds an ID and a short name. A
   catalogue is large, so read an item's full text only when Step 3.4 sends you to it.
3. For each changed form and field, take the fixture rows and smoke-script steps that fit it.
4. Take the expected result from the fixture, when it gives one, or from the schema or copy in
   the diff. Else read the catalogue item and take it from the Fix. Every expected result has one
   of these three sources.
5. Tag the item with the one catalogue ID that names the defect it probes. Use the ID that the
   fixture row cites, when it cites one. When an item only points at another ID, use that ID.
   The item goes under the lane whose catalogue holds its ID.
6. Rank the items: data saved wrong or work lost, then a wrong action, then a cosmetic fault.
   Keep the first 8. Merge items that send the same class of input to one field.

**Done when:** each kept item names a field, an input or key, an expected result, and one
catalogue ID, and no lane has more than 8 items.

## Step 4: Print the Checklist

Format:

```
## Sad path: {short description of changeset}

Lanes run: {lane (signal)}. Skipped: {lane}. Cut by the cap: {lane: items past 8}, or none.

### {lane}: {form or area}
- [ ] {do X} → {expect Y} ({catalogue ID})
- [ ] {do A} → {expect B} ({catalogue ID})
```

Rules:

- Each item is an action in the running app. A check of the code belongs to `/mob-review`.
- Quote each input byte-exact from the fixtures. When an input holds invisible characters, also
  name the fixture row and each invisible character, such as "T4 (zero-width space)", so the
  tester copies it from the fixtures file.
- No setup instructions the user already knows.

**Done when:** each lane that ran has its items under its own heading, and each item ends with a
catalogue ID.

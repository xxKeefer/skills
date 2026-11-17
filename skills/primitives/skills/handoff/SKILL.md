---
name: handoff
description: >
  Compact the current conversation into a handoff document for another agent to pick up. Use when
  the user says "handoff", or wants a new session to continue this work.
argument-hint: "What will the next session be used for?"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it with `/write-to-file`, doctype `plan`.

Write a short plan in the layout of the `/write-to-file` plan [template](../write-to-file/templates/plan.md): the YAML header, `## Goal`, `## Steps`, and `## Progress`. Add an optional section only when the conversation holds its content. In the header, `worktree` is the current worktree root, or the current folder outside a git repo. `branch` is the current branch, or `none` outside a git repo. `ticket` is the key, or `none`. `status` is `building` when a step is done, else `draft`.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

When the steps change code:

- End with a review step, then the push step: the step that pushes or opens a PR.
- Write "Depends on every earlier step." in the review step. Also write that the review gets this handoff's path.
- The review step changes no code. Its done line: each fix that the user picks is a step before the push step.
- In the suggested skills section, name `/mob-review` for the review step, if this session has it.
- Each step that changes behaviour names `Seam: <seam>` and `Conditions: <IDs>`, or `Conditions: none` when the handoff lists no conditions. Its done line names the tests it adds.

Give every step a `  - Done: <line>` sub-line. A step that changes no code, such as research or a draft, takes `Kind: docs`, `Kind: config`, or `Kind: mechanical`, whichever is closest, and needs no seam. The plan check fails a step with no done line, and a step with no `Kind` and no seam.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

Write the document in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and follow every rule in it. The reader is a cold agent, so a sentence it can misread is a sentence that costs a session.

---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it with `/write-to-file`, doctype `handoff`.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

When the steps change code:

- End with a review step, then the push step: the step that pushes or opens a PR.
- Write "Depends on every earlier step." in the review step. Also write that the review gets this handoff's path.
- The review step changes no code. Its done line: each fix that the user picks is a step before the push step.
- In the suggested skills section, name `/mob-review` for the review step, if this session has it.
- Each step that changes behaviour names its seam, and the IDs of its test conditions if the handoff lists them. Its done line names the tests it adds.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

Write the document in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and follow every rule in it. The reader is a cold agent, so a sentence it can misread is a sentence that costs a session.

---
name: sharpen
description: Rewrite a prompt to go deeper, not wider, before you hand it to an agent.
disable-model-invocation: true
---

Rewrite the prompt in `$ARGUMENTS`, or the last prompt in the conversation, to go deeper on the
same task. Add no new task. Ask the user no question.

Answer four questions about the task:

1. What would a top professional do that the prompt does not ask for?
2. What is the rawest material they would start from?
3. What methods and tools would they use?
4. What outside the agent and the user would show that the result is right?

Then rewrite the prompt to ask for exactly those answers. In the rewrite:

- Name the raw material to start from.
- Ask the agent to prototype each choice that an experiment can settle, and to recommend an option from what it saw.
- Leave each product or preference choice to the user.
- Ask for the outside proof.

Return the answers in short form, then the rewritten prompt in one code block, ready to paste.

Adapted from the pstack `sharpen` skill.

Write the answers in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you
write, and follow every rule in it.

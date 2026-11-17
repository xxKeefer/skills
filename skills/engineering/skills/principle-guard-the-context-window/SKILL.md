---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, or fan-out planning. Route bulk work to subagents, and keep summaries in the main thread."
disable-model-invocation: true
---

# Guard the Context Window

Context overflow lowers the quality of reasoning, adds compression errors, and stops progress. Guard the window before it fills.

- Size each phase and cap its scope. Limit the files in a phase, and count the cost of each tool.
- Send bulk work to a subagent: a large search, a long file, a run of similar edits, or a test log. The subagent returns a short summary. Keep raw output out of the main thread.
- Read a file once. Take the lines that you need, not the whole file.
- Before the window is full, run `/checkpoint`. It saves the state of the work, so that a fresh session continues from it.

If `/checkpoint` is not installed, write the state into the plan with `/update-plan`.

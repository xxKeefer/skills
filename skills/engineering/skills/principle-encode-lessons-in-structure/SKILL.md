---
name: principle-encode-lessons-in-structure
description: "Apply when you write the same instruction a second time, or see a correction come back. Fix the cause in the code, not in more text."
disable-model-invocation: true
---

# Encode Lessons in Structure

When you write the same instruction a second time, stop. A mistake class counts after two times. Fix it at the highest rung that works:

1. Architecture. Make the mistake impossible to write.
2. Types.
3. A lint or check whose error names the fix.
4. A test.
5. Docs, last.

If the lesson needs judgement and a tool cannot hold it, make the instruction more prominent. Add an example of the failure.

**Corollary:** if the fix is structural, use only the structural fix. The instruction is the symptom.

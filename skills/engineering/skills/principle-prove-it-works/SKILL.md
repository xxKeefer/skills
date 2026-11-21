---
name: principle-prove-it-works
description: "Apply after you complete a task, before you say it is done. Check the real artifact: run the feature, read the actual value, inspect the diff. A proxy does not count."
disable-model-invocation: true
---

# Prove It Works

Check each output on the real thing. Run the feature, read the actual value, or inspect the diff. A proxy does not count. File times, self-reports, cached output, and "it compiles" are proxies. When a check fails, suspect the way you observed before you suspect the system.

Script the check when you can. A deterministic script that repeats the comparison beats a one-time look. Keep its output where the user can see it. Commit it only when the trail must stay auditable.

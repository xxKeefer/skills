---
name: benchmark
description: >
  Vet a performance number with seven checks before you report or act on it: limiter, tuning,
  limits, errors, repeatability, relevance, and whether the work happened. Use when you produce a
  speedup, a regression, or a choice between options from a measurement, or when /webperf measures.
argument-hint: "[the claim to vet]"
---

# Benchmark

A performance number can measure something other than the work. This skill gives seven checks that
rule that out. Answer each check with evidence from a run, not with a guess about the code.

Principle: **principle-explain-the-number** ([`../principle-explain-the-number/SKILL.md`](../principle-explain-the-number/SKILL.md)).

## Step 1: Before the run

1. Write the claim in the words you would ship, such as "export is 30% faster at p50 on the 60k-row
   dataset". The checks test that sentence.
2. Read the measurement script. Note what it times, what it counts, and what it ignores.
3. Check the load average and the core count. If the machine is busy, find what runs on it. If you
   cannot stop it, interleave the sides so both see the same noise, and say so in the report.

**Done when:** the claim is written, the script is read, and the machine state is known.

## Step 2: The seven checks

1. **Why not double?** Name the limiter. Find it in a run that you do not report, because profilers
   and tracers slow the work. Use CPU for each process, a runtime profiler, I/O wait, and syscall
   counts. Map the hot spot to source. Watch the load generator too: if it saturates first, you
   measured the load generator. If a change did not move the number, the limiter says why.
2. **Was it tuned?** Run each side as production runs it: release builds, production flags and
   environment, batching and transaction settings, connection pools, caches as warm or cold as in
   production, and the same versions and data. A side on defaults makes the test a comparison of
   configurations, not of implementations. A limiter that is a setting, such as a commit for each
   row, a debug build, or a missing index, means that side is untuned. Tune it and measure again.
   If you cannot tune it, pick no winner from that run. When the user chooses what to adopt,
   narrowing the claim to today's settings does not fix this.
3. **Did it break limits?** Do the arithmetic. Compare bytes a second with disk and network
   bandwidth. Compare operations a second times the cost of each operation with the cores. Compare
   the time saved with the time that the changed piece took: removing a piece that takes 10% of
   the run makes the run at most about 11% faster. A result past a limit measured something other
   than the work, such as a cache, a no-op, or a bug.
4. **Did it error?** Count the failures and the non-success responses. Check that the outputs are
   correct, not only present. Rejections are often fast, and timeouts and retries are slow. If the
   script does not count errors, add the count.
5. **Does it reproduce?** Run each side at least 5 times, alternating (A, B, A, B, and so on), so
   warmup, lazy initialisation, caches, and drift favour neither side. Report the median and the
   range. A gap smaller than the run-to-run spread is no measurable difference. When the call is
   close, use a rank-sum test or the harness's own statistics.
6. **Does it matter?** Next to a micro result, measure the end-to-end path that a user waits on,
   with realistic data sizes and concurrency. Report the micro result as a share of the whole. A
   helper that takes 1% of a request makes the request at most 1% faster.
7. **Did it even happen?** Confirm that the work ran inside the timed region: the request reached
   the server, the rows were written, the bytes were read, and the code used the result. Lazy code
   and timeouts give numbers for work that never ran.

For a quick ballpark that the user asked for, one run is enough. Still run checks 4 and 7, and say
that it is one run. Skip the other checks unless the run looks wrong. A choice between options is
never a ballpark.

**Done when:** each check has an answer with evidence, or the ballpark rule names the checks that
you skipped.

## Step 3: The verdict

Lead the report with one verdict: faster, slower, no measurable difference, or inconclusive.

Give the number with its unit, the run count, the range, and the limiter. For example: "p50 41 ms
to 33 ms, median of 7 runs for each side, range 32 to 35 ms after, bound by JSON parsing on one
core."

Give the verdict inconclusive in each of these cases, and name the gap:

- You claim a difference but cannot name the limiter.
- A side ran untuned.
- Check 4 or check 7 could not run.

Keep a PR body to one primary number. Put the runs, the range, and the limiter evidence in a linked
file or in notes.

**Done when:** the report holds a verdict, and, for a verdict other than inconclusive, the number,
its unit, the run count, the range, and the limiter. An inconclusive verdict holds the gap.

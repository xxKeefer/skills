---
name: webperf
description: >
  ★ Webperf: measure a web page's performance first, find the one bottleneck, fix it, then measure
  again and keep or revert the fix. Use when the user says "webperf", or a page is slow.
argument-hint: "<URL> [page or flow]"
---

# Webperf

Make a web page faster with evidence. Measure first, fix one bottleneck at a time, and keep a fix
only when the numbers show it helped.

Principle: **principle-explain-the-number** ([`../principle-explain-the-number/SKILL.md`](../principle-explain-the-number/SKILL.md)).

## Step 1: Measure

1. Get the URL from `$ARGUMENTS`. If there is none, ask for it. If the app has no URL, such as a
   CLI or a library, stop and say that this command does not apply.
2. Use the project's own performance tool when it has one. Else use a lab tool such as Lighthouse,
   if it is installed. If no tool is installed, ask before you install one.
3. Run the tool at least five times. Record the Core Web Vitals and their limits: LCP ≤ 2.5 s,
   INP ≤ 200 ms, CLS ≤ 0.1. Record the bytes shipped and the main-thread time too.
4. Vet the baseline with `/benchmark` checks 1, 3, 4, and 7. A baseline has one side, so it gets no
   verdict. Record its limiter.

**Done when:** you have the median and the range for each metric, and the limiter of the baseline.

## Step 2: Find the bottleneck

Find the cause of the worst metric. Trace it to code: a large bundle, a render-blocking resource, an
unsized image, a slow request chain, a long task, or a layout shift. Read the code before you name
the cause.

Show the user the metrics, the worst one, and its cause, with the file and line. Propose one fix.

**Done when:** the user has one cause and one proposed fix.

## Step 3: Fix and measure again

After the user says yes:

1. Make the fix.
2. Run the project's tests.
3. Measure again with the same tool and the same conditions. Run the fixed page and the baseline
   in alternation, at least five runs each, and vet the comparison with `/benchmark`.
4. Read the verdict. Keep the fix if the verdict is faster and no other metric got worse. Revert it
   on slower or no measurable difference, and say so. On inconclusive, report the gap that
   `/benchmark` names. Close it once and measure again if you can. Else revert the fix, mark it
   open with its gap, and go to the next metric.
5. Commit a kept fix, with the before and after numbers in the commit message.

Go back to Step 2 for the next worst metric that is not open, until each metric is inside its limit
or open, or the user stops.

**Done when:** each fix is kept with its verdict and limiter or reverted, and the user has a table
of each metric before and after. A fix with an inconclusive verdict is open, with its gap named.

## Step 4: Guard

Offer to add the metric limits to `CONSTRAINTS.md` through `/constraints`, so a later change cannot
make the page slower without a finding.

**Done when:** the user has answered.

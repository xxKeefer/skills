---
name: diagnose
disable-model-invocation: true
description: >
  Trace a bug with no obvious cause to a proven root cause, written to `.ai/`. For faults in
  recent changes where the cause is roughly known, use /fix instead.
---

# Diagnose

Go from bug report to proven root cause. Assess the report critically, trace the code until the
fault is isolated, capture the findings in a local artifact, then hand off to the right fixer.

This is the investigation skill for **head-scratchers** -- bugs nobody understands yet. It
deliberately stops at root cause: `/fix` and `/implement` own the fix. If the cause is already
roughly known, `/diagnose` is overkill -- route to `/fix`.

> **Tracker:** "the project's tracker" means whatever issue system the repo's CLAUDE.md declares — a
> GitHub issue via `gh`, a Jira ticket via the Atlassian MCP, etc. Read it to learn which tracker is
> in use and how to create and reference tickets. Default to GitHub issues via `gh` if nothing is
> declared.

## Step 1: Parse the Report

`$ARGUMENTS` may contain any combination of:

- **Error messages or stack traces** — pasted directly
- **Bug report / user feedback** — observed vs expected behaviour
- **Tracker tickets** — references in the project's tracker; fetch via `/look-up`
- **Log output** — runtime logs showing the failure
- **Reproduction steps or screenshots** — user-provided observations

If `$ARGUMENTS` is empty, use **AskUserQuestion**:

> What's the bug? Give me an error, stack trace, ticket, reproduction steps, or description.

**Done when:** you have the report and every ticket it references.

## Step 2: Assess the Report

Check each claim in the report against the code before you hunt. Bug reports are symptoms filtered
through human interpretation — the reporter may be wrong about what's broken, where, or why.

- **Verify the symptom is real.** Can the described behaviour actually occur from the code?
- **Separate observation from interpretation.** The reporter says "X is broken" — is X the
  problem, or is the failure upstream?
- **Check for stale information.** Has the code changed since the report? Already fixed?
- **Identify what's missing.** What does the report NOT tell you?
- **Gauge confidence:**
  - **Clear** — exact reproduction steps, expected vs actual, specific error
  - **Partial** — symptom described but cause unclear
  - **Vague** — "it doesn't work", no specifics

Present the assessment:

```
## Bug Assessment

**Symptom:** <one-line summary of the reported problem>
**Confidence:** Clear | Partial | Vague
**Reporter's interpretation:** <what they think is wrong>
**My read:** <what I think is actually going on, or "aligned">
**Missing info:** <what I'd need to confirm — or "none">
```

Then route:

- **Cause already roughly known** (fault clearly sits in recent changes, obvious culprit) → this
  is `/fix` territory. Say so and offer to switch.
- **Vague** → invoke `/grill` with the report and the gaps you identified. All questions
  resolved before hunting begins.
- Otherwise → hunt.

**Done when:** you have presented the assessment and picked one route.

## Step 3: Hunt

Work from symptom to cause. Keep going until you can **show** the fault, not just point near it.

1. **Locate the symptom** — find the code path producing the observed behaviour (error message,
   wrong output, crash site)
2. **Reproduce if possible** — a failing test or minimal reproduction turns the hunt from
   speculation into measurement
3. **Trace upstream** — follow data flow and control flow backward from the symptom. Where does
   the bad state originate?
4. **Check boundaries** — inputs, type conversions, edge cases, error handling at each layer
5. **Widen when stuck** — history of the suspect code, similar patterns elsewhere, tests that
   should have caught this

Use Explore subagents for broad sweeps; targeted search for specific symbols. Record dead ends as
you go — ruled-out causes belong in the artifact.

Finish the reported bug. Record any other bug you find for a separate hunt.

Present findings:

```
## Root Cause

**Location:** <file:line or module>
**What happens:** <1-2 sentences — the actual fault>
**Why:** <1-2 sentences — why the fault exists (missing guard, wrong assumption, race, etc.)>
**Blast radius:** <what else is affected by the same root cause>
```

If the root cause remains unproven, present the best hypothesis with supporting and contradicting
evidence, and ask the user what they can confirm.

**Done when:** a traced code path shows the root cause, or you have marked it as a hypothesis.

## Step 4: Write the Hunt Artifact

Use `/write-to-file` to write `hunt_{terse-description}.md` to `.ai/` (prefer the tracker id when
the work has one, per `/write-to-file`'s naming convention — e.g. `hunt_ENG-123.md`).

This is a **local, short-lived artifact** — file paths and line numbers are welcome here, unlike
tracker content. Its job is to carry the investigation into `/fix` or `/implement` intact. The fix
and its regression test replace the hunt doc, so the skill that consumes it deletes it.

```markdown
# Hunt: {symptom}

> {one-line root cause}

**Hunted:** {date}
**Status:** active | consumed

## Report

Symptom, confidence, reporter's interpretation vs what was actually found.

## Root Cause

Location, what happens, why the fault exists.

## Evidence

The traced code paths that prove it — how bad state travels from origin to symptom.

## Ruled Out

Dead ends investigated and why they're not the cause, so nobody re-hunts them.

## Blast Radius

What else the same root cause affects. Other instances of the faulty pattern.

## Fix Direction

1-2 sentences of direction — NOT a plan. /implement owns decomposition; /tdd owns tests.
```

**Done when:** the hunt doc exists, and each template section holds its findings or "none".

## Step 5: Hand Off

Present a summary:

> **Hunt complete: `{symptom}`**
>
> **Root cause:** {one-line}
> **Artifact:** `.ai/hunt_{name}.md`
>
> Where to next?

Offer:

1. **`/fix`** — the fix is now small and obvious
2. **`/implement @.ai/hunt_{name}.md`** — the fix needs decomposition
3. **Ticket** — on request, create a tracker ticket (or subtask of the originating ticket) with a
   durable summary: modules, behaviours, and contracts — no file paths or line numbers. The
   shared tracker is not a dumping ground; only what survives codebase change goes in.
4. **Done** — leave the artifact for a future session

**Done when:** the user has picked one of the four options, and any ticket they asked for exists.

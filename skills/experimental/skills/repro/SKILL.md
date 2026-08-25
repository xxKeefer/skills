---
name: repro
description: >
  Give the shortest path to reproduce an issue: numbered steps from a cold start to the moment the
  fault shows. Traces the code for the gates, the route, and the exact labels. Usage: repro
  <topic>. Use when the user says "repro", "steps to reproduce", "how do I hit this", or asks how
  to see a bug or a surface for themselves.
---

# Repro

Turn a named surface or fault into steps a human can follow with no knowledge of the code.

## Step 1: Find the target

Locate `<topic>` in the code — a component, a route, a function, or a symptom the user named. Read
enough to know what renders it and who reaches it.

**Done when:** you can name the file that owns the behaviour and its entry point in the product.

## Step 2: Walk back to a cold start

From that entry point, walk outward until you reach a screen or command available in a fresh
session. Collect every **gate** on the path:

- Feature flags and config toggles.
- Roles, permissions, and account or company state.
- Data the account must already hold (an active record, a saved item, a non-terminal state).

Read the condition that enforces each gate in the source, and keep the flag name or field name it
tests.

**Done when:** every gate on the path traces to the code that enforces it.

## Step 3: Collect the exact labels

Take the visible text for every step from the source — templates, i18n files, route paths, CLI
argument definitions. Use the string the user reads on screen.

**Done when:** every navigation and action step names a string that exists in the code.

## Step 4: Write the repro

Lead with the title `Repro: <target>`. State the gates in one line before the list. Then give the
numbered steps.

Rules for the list:

- One action per step, imperative, under 20 words.
- Order from cold start to fault: open the gates, navigate, act.
- Put a condition before its command ("For a service already in a Project, click …").
- End on the **trigger**, the step that exposes the fault.

For a surface with no UI, the steps are commands and requests with real arguments.

Write in **Simplified Technical English**: active voice, short common words, no contractions, no
em dash.

**Done when:** a person with an account and no code access can follow the list end to end.

---
name: qa-it
description: >
  Generate a concise manual QA test plan focused on user-visible behavior.
  Use when the user says "qa it", "test plan", "manual test plan", "qa test plan",
  or wants a QA-ready checklist for a feature.
---

# QA It

Generate a manual QA test plan that any team member or dedicated QA person can follow.

## Inputs

- Feature description, ticket reference, or conversation context about what was built
- Optional: args can specify the feature or ticket directly

## Audience

This test plan serves three readers:

1. **The dev** (you) — documents what you manually tested before handing off
2. **Code reviewer** — sees what was validated beyond the diff
3. **QA engineer** — starting point for deeper exploration, not an exhaustive script

Write for all three. Be specific enough that a reviewer knows what you checked, but trust QA to explore beyond the happy path.

## Step 1: Understand the Feature

Research the feature to understand the user-facing flows:

1. If a ticket or feature name is provided, explore the relevant code to understand the UI flows
2. **Identify the feature, not the diff.** A code change enables a user-facing capability — test the capability. Ask: "What can the user now do that they couldn't before?" If the diff is small, the feature it enables is often much larger than the diff itself. Trace outward from the change to the full user journey it affects.
3. Focus on **what the user sees and does** — not implementation details
4. **Enumerate every distinct actor.** Most features have multiple actors with separate journeys (provider/consumer, admin/user, sender/receiver, owner/viewer). List them explicitly before writing any flows. Each actor gets their own flow — never merge two actors into one flow.
5. **For each actor, trace the full end-to-end journey starting from zero.** The first step is creating/provisioning the resource, not interacting with a resource that already exists. Ask: "What is the very first thing this actor must do before anything else can happen?" If the answer is "order a NAT Gateway" or "create a marketplace profile", that's step 1 — not an assumed precondition. If Flow 1 creates something that Flow 2 needs, don't restate it as a prerequisite — the tester will understand the dependency from the flow order.
6. **Order flows by dependency chain.** If Actor B can only act after Actor A publishes/creates something, Actor A's flow comes first. The flow that makes the feature *exist* precedes the flow that *uses* it.
7. Identify a small number of non-obvious edge cases

**Common trap 1:** Reading a one-line change and writing test steps that mirror the code paths (e.g. "test each branch of the switch statement"). This produces a plan that tests code, not behavior. Instead, zoom out: what UI workflow does this change unblock or fix? Test that workflow end-to-end.

**Common trap 2:** Collapsing multiple actors into a single flow (e.g. "connect to a marketplace listing" without separating who lists it vs who connects to it). If two different people (or accounts) are involved, they need separate flows with separate steps.

**Common trap 3:** Adding regression flows for code paths the change didn't touch. Only test the happy path of what changed. Existing tests and QA exploration cover regressions — don't pad the plan with them.

**Common trap 4:** Starting the journey where the code change sits instead of where the user's journey starts. A one-line fix in a marketplace connection handler doesn't mean the test starts at "click Connect". Zoom out: the user first had to create the resource, list it on the marketplace, and *then* another user connects to it. If you read the diff and start writing steps from the code's location, you'll miss the beginning of the story.

Do NOT deep-dive into code internals. Only read enough to understand the user journeys.

## Step 2: Draft the Test Plan

Output format is markdown suitable for a PR description or ticket comment.

### Structure

- **H3 headers** (`###`) for each distinct flow, named as `Flow N: {Actor} — {Goal}` (e.g. "Flow 1: Seller — List Product on Marketplace", "Flow 2: Consumer — Order Product from Marketplace"). The actor label is mandatory — if you can't name a distinct actor, reconsider whether you've identified the flows correctly.
- **No "Prerequisites" sections.** Setup steps are just the first numbered steps of the flow. If Flow 1 creates something Flow 2 needs, the ordering implies the dependency — don't restate it.
- **Numbered list** under each flow: `{action} -> {expected outcome}`
- **One "Edge Cases" section** at the end as a numbered list with the same format

### Principles

- **User-visible only** — describe what to click, what to see. No code references, no variable names, no API details.
- **Name the actual UI elements** — "configure VXC name, speed, VLANs" not "configure the connection". If the user fills in specific fields, name them. If they click a specific button, name it.
- **Terse** — each step is one line. If a step needs explanation, it's too granular — combine or simplify.
- **Trust the tester** — don't spell out obvious preconditions. If a flow involves connecting *to* something, the tester knows they need something to connect to. Only state non-obvious setup.
- **Happy paths only in flows** — cover only the success paths enabled by the change. Edge cases go in the edge cases section.
- **Brevity over completeness** — 3-5 steps per flow is ideal. QA people know how to explore.
- **Edge cases are selective** — only list non-obvious ones. 2-4 is plenty. Don't list every validation rule.
- **No regression flows** — only test the feature the change enables. Trust existing tests and QA exploration for regressions.

### Anti-patterns

- Do NOT include dev-tools checks, network tab inspection, or API response verification
- Do NOT reference file names, function names, or code paths
- Do NOT add "Prerequisites" headers or blocks — weave setup into the flow steps
- Do NOT add setup instructions for dev environments — assume the app is running
- Do NOT pad with "verify the page loads" type steps unless it's genuinely at risk
- Do NOT mirror code branches as test cases (e.g. "test product type X, test product type Y") — this is testing the switch statement, not the feature
- Do NOT use internal terminology the QA person wouldn't see in the UI (e.g. enum values, connect types, API field names). If a term doesn't appear on screen, it doesn't belong in the test plan.
- Do NOT write a "regression" flow that just enumerates other code paths unchanged by the feature — trust existing tests for that
- Do NOT add generic steps like "connection is live and functional" — be specific about what "functional" means in the UI (e.g. "appears on both consumer's cart and sellers's services")
- Do NOT reference internal state in edge cases (e.g. "Product with explicit serviceType from the API"). If the user can't trigger the scenario from the UI, it's not a QA edge case — it's a unit test

## Step 3: Present and Iterate

Present the test plan directly (not in a file). Ask if anything should be added or trimmed.

Iterate toward brevity — if the user says it's too verbose, aggressively cut. The goal is a test plan someone will actually read.

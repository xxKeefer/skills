---
name: brief
description: >
  Write a cold-start prompt that hands one piece of work to a fresh agent in a new session, and
  copy it to the clipboard. Use when the user asks for a prompt for a fresh agent or another
  session, or when the work needs a tool that this session does not have.
---

# Brief

Hand one piece of work to a fresh agent. The fresh agent knows nothing that this session knows,
so the brief carries all of it. The user pastes the brief and does not explain more.

## Step 1: Find the work

1. Take the work from the user's words, else from the last open task in the conversation.
2. When the work needs a tool that this session lacks, such as a browser or a service, name the
   tool. The brief tells the fresh agent to check that it has the tool before it starts.

**Done when:** you can state the work and its done line in one sentence each.

## Step 2: Write the brief

Write the brief in this order. Leave out a section that has nothing in it.

1. **Goal:** the work, in one or two sentences.
2. **Why:** the reason for the work, and the decision that it serves.
3. **Read first:** each absolute path, URL, row ID, or commit that the fresh agent needs. Give
   each one with what it holds.
4. **What worked:** the accounts, data, flags, commands, and settings that this session found to
   work. Also say what failed and why, so the fresh agent does not try it again.
5. **Ask first:** each action that needs a yes from the user, such as a write to shared data.
6. **Stop:** when the fresh agent stops and reports, such as a sign-in wall or a result that does
   not match the expected result.
7. **Done when:** a checkable end state, and what the fresh agent reports back.

Use no "this", "above", or "earlier". The fresh agent cannot see this conversation. Give each fact
in full where the brief uses it.

**Done when:** each section is filled in or left out, and the brief has no reference to this
conversation.

## Step 3: Hand it over

1. Copy the brief to the system clipboard with the clipboard command of the platform.
2. Show the brief in one fenced block.
3. Say that the brief is on the clipboard. Name each placeholder (`<…>`) that the user must fill in
   before they paste it.

**Done when:** the brief is on the clipboard, and the user has it in the chat.

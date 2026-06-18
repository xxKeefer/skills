---
name: look-up
description: >
  Fetch and ingest resources the agent needs before executing a task. Accepts one or many links of
  any kind — local files, web pages, tracker tickets, wiki/doc pages, MCP resources. Model-invocable
  — other skills delegate resource gathering here instead of managing it themselves.
---

Receive one or more resource links, fetch each one, and surface the content so the calling skill or
agent can act on it.

## Behaviour

1. Accept a list of resource links from the caller (args, conversation context, or user input)
2. For each link, determine its type and fetch accordingly:
   - **Local file path** → Read the file
   - **Web URL** → Fetch the page content
   - **Tracker ticket** → fetch via the project's issue tracker. Which tracker (and how to reach it)
     is defined by the repo's CLAUDE.md — e.g. a GitHub issue (`#42`) via `gh`, a Jira key
     (`ENG-12345`) via the Atlassian MCP, or whatever the project declares
   - **Wiki / doc page** → fetch via the project's documentation system (e.g. Confluence via MCP, a
     local docs tree, a wiki URL)
   - **MCP resource URI** → Read via MCP resource tools
3. Present the fetched content clearly, labelled by source
4. If a resource cannot be fetched, report the failure and continue with the rest

## Tracker resolution

A "tracker ticket" is only meaningful relative to the project. Read the repo's CLAUDE.md to learn
which tracker the project uses and how identifiers look (issue numbers, ticket keys, etc.). Don't
assume GitHub or Jira — use whatever the project declares. If no tracker is defined and the
identifier is ambiguous, ask.

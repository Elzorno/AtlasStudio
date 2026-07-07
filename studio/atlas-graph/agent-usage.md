# Atlas Graph Agent Usage

## Purpose

This document explains how AI agents should use the Atlas Graph.

## General Rule

Agents should treat the graph as shared project memory.

Before changing canon, implementation targets, or production dependencies, agents should inspect the relevant graph files or use graph tools when available.

## GPT Usage

GPT should use the graph to:

- Avoid conflicting story details
- Find existing characters, regions, and factions
- Add draft canon nodes from story work orders
- Connect quests, NPCs, locations, and concepts
- Identify missing world relationships

GPT should avoid:

- Writing engine-specific bridge facts unless assigned
- Promoting draft facts to canon without approval

## Claude Code Usage

Claude Code should use the graph to:

- Design schemas
- Build graph validators
- Build query tools
- Refactor storage or tooling
- Create migration paths
- Analyze production dependencies

Claude Code should avoid:

- Making final story decisions
- Editing large canon sets without a story/design work order

## Codex Usage

Codex should use the graph to:

- Translate approved design nodes into implementation tasks
- Generate RPG Maker bridge work orders
- Validate that implementation targets match canon
- Update bridge graph facts after implementation

Codex should avoid:

- Changing core canon while implementing engine files
- Overwriting protected implementation targets

## GitHub Copilot Usage

GitHub Copilot should use graph-related files for local coding context.

Best uses:

- Completing schema fields
- Writing boilerplate validators
- Assisting with repetitive JSON edits

Copilot should not be treated as the final graph authority.

## Ollama / Local Model Usage

Local models can help with:

- Consistency scans
- Summaries
- Orphan detection
- Draft relationship suggestions
- Low-risk graph expansion

Local model outputs should be reviewed before canon approval.

## Human Creator Usage

The human creator approves:

- Major canon facts
- Story direction
- Region names
- Major faction roles
- Retiring or replacing canon
- Promotion from draft to canon

## Agent Write Protocol

When an agent edits graph files, it should report:

1. Nodes added
2. Nodes changed
3. Edges added
4. Edges changed
5. Facts left as draft
6. Facts requiring approval
7. Source documents used

## Canon Promotion Rule

Draft graph facts become canon only after review.

Recommended promotion path:

```text
draft → proposed → approved → canon
```

## Conflict Rule

If an agent finds conflicting facts, it should not silently choose one.

It should mark or report the conflict and create or recommend a work order to resolve it.

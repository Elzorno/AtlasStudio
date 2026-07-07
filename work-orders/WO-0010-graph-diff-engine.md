---
work_order_id: WO-0010
title: Graph Diff Engine
status: proposed
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0010 - Graph Diff Engine

## Purpose

Design and implement a graph diff engine that explains changes between two Atlas Graph states.

## Player-Facing Goal

Indirect. Better graph diffing helps agents understand how canon, production state, and bridge mappings changed before those changes affect implementation.

## Background

As AtlasStudio grows, graph changes will become as important as code changes. Agents need a way to understand what nodes and relationships were added, removed, changed, deprecated, or promoted to canon.

## Scope

### In Scope

- Compare graph files between two Git refs, commits, or directories.
- Report added, removed, and changed nodes.
- Report added, removed, and changed edges.
- Highlight status changes such as draft → canon or proposed → accepted.
- Highlight changed source references.
- Produce human-readable report output.

### Out of Scope

- GUI visualization.
- Automatic conflict resolution.
- Database migration.
- Pull request automation unless explicitly approved later.

## Inputs

- `tools/atlas_graph/`
- `studio/atlas-graph/storage-model.md`
- `studio/atlas-graph/query-model.md`

## Deliverables

- Graph diff design or implementation under `tools/atlas_graph/` or `tools/atlas_diff/`.
- Documentation for command usage.
- Optional sample report.

## Acceptance Criteria

- Tool can compare two graph states.
- Tool clearly identifies added, removed, and changed graph facts.
- Tool distinguishes canon changes from production-only changes.
- Output is useful for agent handoff and QA review.

## Verification Steps

Example future commands:

```bash
python3 tools/atlas_graph/diff_graph.py --base HEAD~1 --head HEAD
python3 tools/atlas_graph/diff_graph.py --base-dir old_graph --head-dir projects/the-last-sword-protocol/graph
```

## Allowed Changes

- `tools/atlas_graph/`
- `tools/atlas_diff/`
- `docs/` or `studio/atlas-graph/` documentation if needed

## Protected Areas

- Do not modify project canon.
- Do not modify RPG Maker repositories.

## Notes for Assigned Agent

Design this as a reusable Atlas Core feature, not a Last Sword Protocol-specific feature.

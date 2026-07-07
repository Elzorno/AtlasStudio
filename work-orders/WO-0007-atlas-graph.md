---
work_order_id: WO-0007
title: Atlas Graph Architecture
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: high
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0007 - Atlas Graph Architecture

## Purpose

Design the Atlas Graph: the shared knowledge and production memory layer for AtlasStudio.

## Player-Facing Goal

Indirect. A reliable shared graph should help agents produce more consistent worlds, quests, NPCs, maps, and builds.

## Background

AtlasStudio is moving beyond Markdown-only documentation. Markdown is useful for human-readable design, but agents need structured, queryable relationships between regions, locations, characters, quests, factions, story beats, ancient infrastructure, work orders, providers, and builds.

The Atlas Graph should become the shared memory that all agents can read and eventually write through controlled workflows.

## Scope

### In Scope

- Define graph purpose and boundaries.
- Define initial node types.
- Define initial relationship types.
- Define storage approach for v0.
- Define sync relationship between Markdown and graph data.
- Define query requirements.
- Define validation requirements.
- Define how agents should use the graph.

### Out of Scope

- Full database implementation.
- Live UI.
- Automated provider dispatch.
- Engine-specific RPG Maker implementation.
- Replacing all Markdown documents.

## Inputs

- `studio/vision.md`
- `studio/workflow.md`
- `studio/agent-roles.md`
- `projects/the-last-sword-protocol/world-model.md`
- `projects/the-last-sword-protocol/home-region.md`
- `work-orders/WO-0006-world-atlas.md` if present

## Deliverables

- `studio/atlas-graph/overview.md`
- `studio/atlas-graph/node-types.md`
- `studio/atlas-graph/relationship-types.md`
- `studio/atlas-graph/storage-model.md`
- `studio/atlas-graph/query-model.md`
- `studio/atlas-graph/agent-usage.md`
- Initial seed graph files under `projects/the-last-sword-protocol/graph/`

## Acceptance Criteria

- The graph is clearly positioned as shared memory, not a replacement for all documents.
- The model supports world canon and production tracking.
- Nodes and relationships are simple enough for agents to edit safely.
- Storage can begin as files in Git.
- The design can later migrate to a graph database without changing the project philosophy.
- Agents can answer basic questions from the graph, such as:
  - Which locations are in Ashford Vale?
  - Which NPCs know about the First Relay?
  - Which work orders affect the RPG Maker bridge?
  - Which regions border the Iron Marches?

## Verification Steps

Manual architecture review.

Optional future validation:

```bash
python tools/atlas_graph/validate_graph.py
python tools/atlas_graph/query_graph.py --node region.ashford_vale
```

## Allowed Changes

- `studio/atlas-graph/`
- `projects/the-last-sword-protocol/graph/`
- `schemas/`
- `tools/atlas_graph/` only if implementation is explicitly approved later

## Protected Areas

- Do not modify RPG Maker game repositories.
- Do not migrate existing Markdown into graph data yet.
- Do not introduce a database dependency in this work order.

## Notes for Assigned Agent

Start simple. The v0 graph should be Git-friendly, human-readable, and easy for multiple agents to reason about. Prefer JSON or YAML files before considering a database.

## Submission Record

Submitted 2026-07-07 by claude-code.

Delivered:

- All six `studio/atlas-graph/` design documents (overview, node types, relationship types, storage model, query model, agent usage).
- Seed graph under `projects/the-last-sword-protocol/graph/`: canon, production, and bridge node/edge files matching the storage model layout.

Verification performed (inline script; no `tools/` files added, per Allowed Changes):

- All six graph JSON files parse, node and edge IDs are unique, and no edge references a missing node (24 nodes, 25 edges).
- Acceptance queries confirmed answerable from graph data:
  - Locations in Ashford Vale: ashford_village, hidden_cave, glassfield_ruins, rustshore_dock (CONTAINS).
  - NPC knowledge of the First Relay: character.rowan MISUNDERSTANDS infrastructure.first_relay.
  - Work orders affecting the RPG Maker bridge: work_order.wo_0005 CREATES bridge.rpg_maker_mz.
  - Region borders: the BORDERS relationship type is defined; no border edges are seeded because the Iron Marches and neighboring regions are not yet canon. Seeding them would require a canon revision (Canon Change Rule), deferred to a future world-atlas work order.

Awaiting QA review and acceptance per the work order lifecycle.

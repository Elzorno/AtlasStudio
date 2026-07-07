---
work_order_id: WO-0008
title: Atlas Graph Validation and Query Tools
status: accepted
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0008 - Atlas Graph Validation and Query Tools

## Purpose

Implement the first local tooling layer for Atlas Graph v0.

## Player-Facing Goal

Indirect. Reliable graph checks and queries should help agents produce more consistent worlds, quests, NPCs, maps, and builds.

## Background

WO-0007 defined the Atlas Graph architecture and intentionally deferred implementation of `tools/atlas_graph/` until a later approved work order. This work order completes that first implementation pass.

## Scope

### In Scope

- Add a JSON graph loader for the v0 file layout.
- Add a validator for node and edge files.
- Add a command-line query tool for common graph questions.
- Update production graph records for the new work order and tools.
- Keep the implementation dependency-free and Git-friendly.

### Out of Scope

- Database-backed graph storage.
- UI or dashboard work.
- Automated provider dispatch.
- Canon promotion or story changes.
- RPG Maker implementation changes.

## Inputs

- `work-orders/WO-0007-atlas-graph.md`
- `studio/atlas-graph/storage-model.md`
- `studio/atlas-graph/query-model.md`
- `studio/atlas-graph/agent-usage.md`
- `projects/the-last-sword-protocol/graph/`

## Deliverables

- `tools/atlas_graph/atlas_graph.py`
- `tools/atlas_graph/validate_graph.py`
- `tools/atlas_graph/query_graph.py`
- Production graph updates for `work_order.wo_0008`, `tool.atlas_graph_validator`, and `tool.atlas_graph_query`

## Acceptance Criteria

- Validator parses all current graph JSON files.
- Validator detects duplicate IDs, missing required fields, missing edge endpoints, and missing source paths.
- Query tool can show a node with incoming/outgoing edges.
- Query tool can list neighbors, incoming edges, outgoing edges, shortest paths, work-order impact, statuses, orphans, and missing sources.
- Tools use only the Python standard library.
- Current graph validates successfully.

## Verification Steps

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py get region.ashford_vale
python3 tools/atlas_graph/query_graph.py impact work_order.wo_0008
python3 tools/atlas_graph/query_graph.py path character.rowan infrastructure.first_relay
python3 tools/atlas_graph/query_graph.py missing-sources
```

## Allowed Changes

- `tools/atlas_graph/`
- `work-orders/WO-0008-atlas-graph-tools.md`
- `studio/atlas-graph/`
- `projects/the-last-sword-protocol/graph/nodes/production.nodes.json`
- `projects/the-last-sword-protocol/graph/edges/production.edges.json`

## Protected Areas

- Do not modify RPG Maker game repositories.
- Do not change core story canon.
- Do not add database or package dependencies.

## Notes for Assigned Agent

Prefer small, transparent scripts over infrastructure. The tools should make the graph safer for future agents without changing the graph's v0 file-based philosophy.

## Submission Record

Submitted 2026-07-07 by Codex.

Delivered:

- Dependency-free Atlas Graph loader shared by the tool scripts.
- Validator for parseability, required fields, duplicate IDs, edge references, and source paths.
- Query CLI for entity lookup, neighbors, typed outgoing/incoming edges, shortest paths, work-order impact, status scans, orphan detection, and source checks.
- Production graph records for WO-0008 and the two created tools.

Verification performed:

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py get region.ashford_vale
python3 tools/atlas_graph/query_graph.py impact work_order.wo_0008
python3 tools/atlas_graph/query_graph.py path character.rowan infrastructure.first_relay
python3 tools/atlas_graph/query_graph.py missing-sources
```

Accepted by human instruction to complete WO-0008 on 2026-07-07.

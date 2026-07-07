---
work_order_id: WO-1000
title: First Playable Hour Master Plan
status: accepted
project: the-last-sword-protocol
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-1000 - First Playable Hour Master Plan

## Purpose

Design the complete production blueprint for the first playable hour of The Last Sword Protocol: the milestone definition, chapter roadmap, and production plan (implementation plan, dependency map, work breakdown) that AtlasStudio will use to coordinate all future work toward a polished vertical slice.

This is not an implementation work order. It is the master production plan.

## Player-Facing Goal

Indirect. This work order produces no playable content itself. It exists so that every future implementation work order toward the First Playable Hour has a shared, consistent blueprint, reducing rework and conflicting direction across agents.

## Background

AtlasStudio has canon (`projects/the-last-sword-protocol/game-vision.md`, `story-reset.md`, `world-model.md`, `home-region.md`), a working Atlas Graph with the Home Region already modeled in canon (world, region, locations, characters, item, concepts), and a growing set of production tools (Studio Doctor, Atlas Graph Validator/Query/Diff, Canon Linter, Immutable Formatting Guard, Planning Engine, Agent Scheduler design). What has been missing is a single master plan connecting canon to a concrete, staffable production sequence for the studio's first proof-of-concept vertical slice.

## Scope

### In Scope

- A milestone definition for the First Playable Hour covering all eleven required beats (opening sequence through end-of-prototype credits), each with gameplay purpose, narrative purpose, cybersecurity concepts taught, required maps, NPCs, monsters, items, music, events, implementation dependencies, and acceptance criteria.
- A chapter roadmap sequencing the milestone with pacing targets, gating logic, and optional/deferred content.
- A production plan decomposing the milestone into a small number of logical implementation work packages (not one work order per asset), each with size, recommended capability, suggested providers, prerequisites, and completion definition.
- A dependency map showing how those packages relate to each other and to external blockers (the RPG Maker bridge, canon gaps, existing tooling).
- An implementation plan describing phased execution and explicit multi-provider parallelization rules.

### Out of Scope

- Writing or modifying any RPG Maker MZ implementation, maps, events, or JSON.
- Modifying game code in any engine-specific repository.
- Changing existing canon graph facts.
- Creating the downstream implementation work orders themselves - this work order defines the packages that would become those work orders, not the work orders.

## Inputs

- `projects/the-last-sword-protocol/game-vision.md`
- `projects/the-last-sword-protocol/story-reset.md`
- `projects/the-last-sword-protocol/world-model.md`
- `projects/the-last-sword-protocol/home-region.md`
- `projects/the-last-sword-protocol/graph/` (canon, production, and bridge graph facts)
- `studio/agent-roles.md`
- `studio/scheduling/agent-scheduler-design.md`
- `work-orders/WO-0005-rpg-maker-bridge.md`

## Deliverables

- `projects/the-last-sword-protocol/milestones/first-playable-hour.md`
- `projects/the-last-sword-protocol/roadmap/chapter-01-roadmap.md`
- `projects/the-last-sword-protocol/production/implementation-plan.md`
- `projects/the-last-sword-protocol/production/dependency-map.md`
- `projects/the-last-sword-protocol/production/work-breakdown.md`

## Acceptance Criteria

- The milestone document covers all eleven required beats (opening sequence, Ashford Village, Ashford Vale overworld, Hidden Cave, Sword Shrine, Last Sword acquisition, Glassfield Ruins, First Relay activation, Rustshore, boat departure, end of prototype credits) with every required field per beat.
- The roadmap sequences the milestone using only existing canon gating (`UNLOCKS`, `CONTAINS`, `CONNECTED_TO` edges), with no invented gates that contradict canon.
- The work breakdown decomposes the milestone into a small set of logical packages (delivered: thirteen), not one work order per asset, each with size, capability, provider, prerequisite, and completion definition.
- The dependency map identifies the RPG Maker bridge (`WO-0005`) as a blocking dependency for engine-specific packages and identifies any canon gaps discovered during planning.
- The implementation plan explicitly supports multiple providers (Claude Code, Codex, GPT, GitHub Copilot, Ollama, Human) working simultaneously, with concrete rules for what can run in parallel and why it is safe.
- No canon graph file is modified. No RPG Maker repository is touched. No game code is written.

## Verification Steps

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py missing-sources
python3 tools/atlas_graph/query_graph.py get region.ashford_vale
python3 tools/atlas_graph/query_graph.py impact work_order.wo_1000
python3 tools/atlas_graph/diff_graph.py --base HEAD
git diff --stat -- projects/the-last-sword-protocol/graph
```

The last two commands confirm the only graph changes are the new `work_order.wo_1000` production node and its edges - no canon file diff.

## Allowed Changes

- `projects/the-last-sword-protocol/milestones/`
- `projects/the-last-sword-protocol/roadmap/`
- `projects/the-last-sword-protocol/production/`
- `projects/the-last-sword-protocol/graph/nodes/production.nodes.json` and `graph/edges/production.edges.json` (to register this work order)
- `work-orders/WO-1000-first-playable-hour-master-plan.md`

## Protected Areas

- Do not modify game code.
- Do not modify RPG Maker repositories.
- Do not change existing canon (`projects/the-last-sword-protocol/graph/nodes/canon.nodes.json`, `graph/edges/canon.edges.json`).

## Notes for Assigned Agent

This is a planning and production architecture work order only. Ground every beat, gate, and package in existing canon graph facts rather than inventing new lore. Where canon is genuinely missing (for example, a location named in prose docs but not yet a graph node), flag it explicitly as a gap for a future small canon work order rather than creating it here.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `projects/the-last-sword-protocol/milestones/first-playable-hour.md` - all eleven beats fully specified, grounded in the existing canon graph, with two canon gaps (Elara's House, Old North Road) explicitly flagged rather than resolved.
- `projects/the-last-sword-protocol/roadmap/chapter-01-roadmap.md` - critical path, pacing targets, gating logic table, optional/deferred content (Fogfen Marsh, Watchtower), and chapter boundary.
- `projects/the-last-sword-protocol/production/work-breakdown.md` - thirteen work packages (WP-01 through WP-13) covering the entire milestone, each with size, capability, providers, prerequisites, and completion definition.
- `projects/the-last-sword-protocol/production/dependency-map.md` - full dependency graph, external blockers (RPG Maker bridge, canon gaps), critical path through the package graph, and risk notes.
- `projects/the-last-sword-protocol/production/implementation-plan.md` - five-phase execution plan with an explicit multi-provider parallelization table and coordination rules.
- Production graph record for `work_order.wo_1000`, with `DEPENDS_ON` edges to `work_order.wo_0002` (Story Reset), `work_order.wo_0003` (Home Region Design), and `work_order.wo_0005` (RPG Maker Bridge Design), and `ASSIGNED_TO agent.claude_code`.

Canon graph files were not touched. No RPG Maker repository or game code was touched.

Formatting: preserved existing house style; graph JSON changes are pure additions; no broad reformatting performed.

Verification performed:

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py missing-sources
python3 tools/atlas_graph/query_graph.py get region.ashford_vale
python3 tools/atlas_graph/query_graph.py impact work_order.wo_1000
python3 tools/atlas_graph/diff_graph.py --base HEAD
git diff --stat -- projects/the-last-sword-protocol/graph
```

Accepted by human review on 2026-07-07.

---
work_order_id: WO-0009
title: Studio Doctor
status: submitted
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0009 - Studio Doctor

## Purpose

Build the first AtlasStudio diagnostic command that reports project health across graph integrity, production state, orphaned work orders, missing sources, incomplete canon, and implementation readiness.

## Player-Facing Goal

Indirect. A useful Studio Doctor helps the team identify what to build next and prevents AtlasStudio from drifting into disconnected documents, orphaned tasks, or incomplete game systems.

## Background

WO-0008 created Atlas Graph validation and query tooling. During verification, the graph surfaced `work_order.wo_0004` as an orphan node. This is valuable project intelligence. AtlasStudio should not merely validate graph syntax; it should explain project health.

Studio Doctor is the first Phase 3 Studio Intelligence tool.

## Scope

### In Scope

- Create a diagnostic command or script for AtlasStudio.
- Reuse existing graph loading/validation logic from `tools/atlas_graph/`.
- Report graph integrity summary.
- Report orphan nodes, especially orphaned work orders.
- Report missing sources.
- Report draft/proposed/submitted/accepted work order counts if available from graph data.
- Report bridge readiness signals.
- Report project-specific implementation gaps for The Last Sword Protocol using currently available graph data only.
- Produce a readable Markdown or console report.

### Out of Scope

- Automated work order creation.
- Live dashboard.
- Provider API integration.
- RPG Maker repository modification.
- Deep natural-language analysis of all Markdown.
- Changing canon to fix findings.

## Inputs

- `tools/atlas_graph/`
- `projects/the-last-sword-protocol/graph/`
- `studio/atlas-core.md`
- `studio/atlas-graph/`

## Deliverables

- `tools/atlas_doctor/doctor.py` or equivalent command structure.
- Optional wrapper script such as `tools/atlas_doctor/atlas_doctor.py`.
- Report output that can be saved under `reports/atlas-doctor/`.
- Update README or tool documentation with usage instructions.
- Update graph production nodes/edges to include the Studio Doctor tool.

## Acceptance Criteria

- Running the tool produces a readable Studio Health report.
- The report includes graph totals: node count, edge count, missing sources, orphan nodes.
- The report explicitly flags `work_order.wo_0004` as orphaned if still orphaned.
- The report separates findings into sections such as Canon, Production, Implementation, Tools, and Recommendations.
- The tool exits successfully when findings are warnings rather than fatal validation errors.
- The tool returns a nonzero exit code only for structural graph errors or unreadable graph files.
- The tool does not modify graph, Markdown, or project files unless an explicit output path is provided.

## Verification Steps

Expected examples:

```bash
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_doctor/doctor.py --project the-last-sword-protocol
python3 tools/atlas_doctor/doctor.py --output reports/atlas-doctor/latest.md
```

Also run:

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py missing-sources
```

## Allowed Changes

- `tools/atlas_doctor/`
- `reports/atlas-doctor/`
- `README.md`
- `studio/atlas-core.md` if a minor documentation update is needed
- `projects/the-last-sword-protocol/graph/nodes/production.nodes.json`
- `projects/the-last-sword-protocol/graph/edges/production.edges.json`

## Protected Areas

- Do not modify TheLastSwordProtocol-Game.
- Do not modify Atlas v1 repositories.
- Do not change story canon.
- Do not automatically close or rewrite existing work orders.

## Notes for Assigned Agent

Start with deterministic checks over the existing graph files. Do not introduce a database or dependency-heavy framework. Studio Doctor should feel like a project health command, not a full application.

## Submission Record

Submitted 2026-07-07 by Codex.

Delivered:

- `tools/atlas_doctor/doctor.py`, a dependency-free Studio Doctor command.
- Readable Studio Health report sections for Graph Integrity, Canon, Production, Implementation, Tools, Missing Sources, and Recommendations.
- Optional report output support via `--output`.
- README usage instructions.
- Production graph records for `work_order.wo_0009` and `tool.studio_doctor`.

Verification performed:

```bash
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_doctor/doctor.py --project the-last-sword-protocol
python3 tools/atlas_doctor/doctor.py --output reports/atlas-doctor/latest.md
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py missing-sources
```

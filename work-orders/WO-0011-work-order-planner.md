---
work_order_id: WO-0011
title: Work Order Planner
status: submitted
project: atlasstudio
recommended_agent: gpt
agent_role: creative-systems-designer
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0011 - Work Order Planner

## Purpose

Implement the first AtlasStudio planner that recommends next work orders from graph state, project health, dependencies, and milestone goals.

## Player-Facing Goal

Indirect. Better planning should move the project toward playable milestones instead of disconnected artifacts.

## Background

AtlasStudio should eventually suggest useful work rather than waiting for the human creator to identify every next step. The planner should begin with deterministic recommendations, not autonomous execution.

## Scope

### In Scope

- Define planner inputs.
- Define recommendation criteria.
- Define priority scoring.
- Define work order suggestion format.
- Use Studio Doctor findings as one input.
- Use graph orphan/dependency signals as one input.
- Keep human approval required.

### Out of Scope

- Automatically creating work orders without approval.
- Provider dispatch.
- Full scheduling system.
- Replacing human creative direction.

## Inputs

- `studio/workflow.md`
- `studio/work-order-format.md`
- `studio/atlas-core.md`
- `tools/atlas_doctor/` after WO-0009
- Atlas Graph production data

## Deliverables

- `studio/planning/work-order-planner-design.md`
- Optional proposed schema for planner recommendations.
- Optional future implementation work order for Codex.

## Acceptance Criteria

- Planner can explain why a work order is recommended.
- Planner distinguishes must-fix, should-do, and nice-to-have work.
- Planner supports project milestones such as First Playable Hour.
- Planner keeps human approval in the loop.

## Verification Steps

Manual review of planner design.

## Allowed Changes

- `studio/planning/`
- `schemas/`
- `work-orders/` only for proposed follow-up work orders if explicitly requested

## Protected Areas

- Do not auto-create implementation work.
- Do not change project canon.
- Do not modify game repositories.

## Notes for Assigned Agent

This began as a design work order and was implemented as Planning Engine v1 by human instruction. The planner must recommend work without creating work orders automatically.

## Submission Record

Submitted 2026-07-07 by Codex.

Delivered:

- `tools/atlas_planner/planner.py`, a deterministic Planning Engine v1 command.
- Transparent priority scoring for milestone impact, dependency value, technical debt, player value, and core platform value.
- Evidence-backed recommendations using work-order metadata, graph relationships, Studio Doctor signals, and Canon Linter findings.
- Recommended agent output where metadata or rule context supports it.
- Optional Markdown report support with sample output at `reports/atlas-planner/latest.md`.
- Production graph records for `work_order.wo_0011` and `tool.planning_engine`.

Verification performed:

```bash
python3 tools/atlas_planner/planner.py
python3 tools/atlas_planner/planner.py --project the-last-sword-protocol
python3 tools/atlas_planner/planner.py --output reports/atlas-planner/latest.md
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
```

Formatting: preserved existing house style; no broad reformatting performed.

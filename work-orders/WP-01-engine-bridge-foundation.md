---
work_order_id: WP-01
title: Engine Bridge Foundation
status: submitted
project: the-last-sword-protocol
source_work_order: WO-1000
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: true
created: 2026-07-07
---

# WP-01 - Engine Bridge Foundation

## Purpose

Create the first executable RPG Maker MZ bridge and handoff foundation for The Last Sword Protocol's First Playable Hour work packages.

## Player-Facing Goal

Indirect. The bridge foundation should make future RPG Maker implementation packages safer, clearer, and easier to verify.

## Background

WO-1000 identifies WP-01 as the blocking engine bridge foundation for all engine-specific First Playable Hour packages. WO-0005 delivered the accepted RPG Maker MZ bridge design documents under `bridges/rpg-maker-mz/`.

This package turns those bridge docs into a read-only handoff generator that can prepare implementation checklists without touching the RPG Maker game repository.

## Scope

### In Scope

- Read AtlasStudio graph and production work package data.
- Read RPG Maker bridge design, ownership, and handoff-format docs.
- Produce safe RPG Maker implementation handoff/checklist output.
- Respect ownership states, treating unknown targets as protected until audited.
- Prepare for `TheLastSwordProtocol-Game` as the implementation target.
- Register production graph facts for the new bridge foundation tool.

### Out of Scope

- Building maps.
- Writing RPG Maker JSON.
- Modifying RPG Maker repositories.
- Changing story or canon graph files.
- Auto-creating downstream work orders.

## Inputs

- `work-orders/WO-1000-first-playable-hour-master-plan.md`
- `projects/the-last-sword-protocol/production/work-breakdown.md`
- `bridges/rpg-maker-mz/bridge-design.md`
- `bridges/rpg-maker-mz/ownership-model.md`
- `bridges/rpg-maker-mz/handoff-format.md`
- `projects/the-last-sword-protocol/graph/`

## Deliverables

- `tools/rpg_maker_bridge/handoff_generator.py`
- `tools/rpg_maker_bridge/README.md`
- `reports/rpg-maker-bridge/wp-01-handoff-foundation.md`
- Production graph facts for `work_order.wp_01` and `tool.rpg_maker_bridge_handoff_generator`
- Bridge graph facts for `implementation_target.the_last_sword_protocol_game`

## Acceptance Criteria

- Tool reads graph/project data and bridge docs.
- Tool can produce handoff/checklist output for engine-facing work packages.
- Output identifies source graph nodes, target RPG Maker areas, ownership assumptions, protected areas, checklist items, and verification steps.
- Tool does not modify RPG Maker repositories.
- Tool does not modify canon.
- Formatting guard reports no formatting-only churn introduced by this package.

## Verification Steps

```bash
python3 tools/rpg_maker_bridge/handoff_generator.py
python3 tools/rpg_maker_bridge/handoff_generator.py --package WP-03
python3 tools/rpg_maker_bridge/handoff_generator.py --output reports/rpg-maker-bridge/wp-01-handoff-foundation.md
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_format/format_guard.py --check
```

## Protected Areas

- Do not modify RPG Maker repositories.
- Do not modify project canon.
- Do not run broad formatters.

## Submission Record

Submitted 2026-07-07 by Codex.

Delivered:

- Read-only RPG Maker MZ handoff generator.
- README documentation.
- Sample handoff foundation report.
- Production graph records for the work package and tool.

Formatting: preserved existing house style; no broad reformatting performed.

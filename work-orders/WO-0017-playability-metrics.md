---
work_order_id: WO-0017
title: Playability Metrics and Player-Visible Progress
status: proposed
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
required_capabilities:
  - python-development
  - graph-analysis
  - qa-review
preferred_capabilities:
  - planning
produces:
  - tool.playability_metrics
  - doctor_section.playability
---

# WO-0017 - Playability Metrics and Player-Visible Progress

## Purpose

Add player-visible progress tracking to AtlasStudio so the project does not drift back into producing artifacts about the game instead of producing the game itself.

## Player-Facing Goal

Indirect. This work should make AtlasStudio report whether the First Playable Hour is becoming playable, not just whether its documentation is complete.

## Background

Atlas v1 produced useful artifacts but did not produce enough playable game. AtlasStudio now has strong planning, graph, bridge, and validation infrastructure. The next core enhancement should make playability visible in project health reports.

The Player-Visible Production Rule establishes that every implementation cycle should end with something the player can see, hear, interact with, or feel.

## Scope

### In Scope

- Add support for `player_visible` and `produces` metadata in future work orders or work packages.
- Define a simple playability checklist model for the First Playable Hour.
- Add a playability section to Studio Doctor or a companion report.
- Track milestone beats such as Ashford Village, Ashford Vale overworld, Hidden Cave, Sword Shrine, Glassfield Ruins, First Relay, Rustshore, boat departure, and prototype credits.
- Report whether each beat is not started, designed, handed off, implemented, verified, or accepted.
- Use existing graph facts when possible.
- Keep the first version deterministic and conservative.

### Out of Scope

- Measuring fun automatically.
- Modifying RPG Maker repositories.
- Creating maps or events.
- Changing story canon.
- Auto-generating implementation work orders.
- Reformatting graph files.

## Inputs

- `studio/governance/player-visible-production-rule.md`
- `projects/the-last-sword-protocol/milestones/first-playable-hour.md`
- `projects/the-last-sword-protocol/production/work-breakdown.md`
- Atlas Graph production and bridge data
- Studio Doctor
- Planning Engine

## Deliverables

- A playability metric design or implementation under `tools/` if appropriate.
- A Studio Doctor playability section or companion report.
- Documentation for `player_visible` and `produces` metadata.
- Production graph facts for the new metric/tool if implemented.
- Sample report under `reports/playability/` or included in Doctor output.

## Acceptance Criteria

- AtlasStudio can report player-visible progress for the First Playable Hour.
- Report distinguishes documentation-only completion from playable implementation completion.
- Report lists major First Playable Hour beats and their status.
- Report can identify when infrastructure is advancing but playability is not.
- Tooling respects the Immutable Formatting Rule.
- No RPG Maker files are modified.

## Verification Steps

Expected examples if implemented as tooling:

```bash
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_playability/playability.py --project the-last-sword-protocol
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `tools/atlas_doctor/`
- `tools/atlas_playability/`
- `reports/playability/`
- `studio/governance/`
- documentation files
- production graph files if needed

## Protected Areas

- Do not modify RPG Maker repositories.
- Do not change story canon.
- Do not run broad formatters.
- Do not create implementation content.

## Notes for Assigned Agent

This work exists to keep AtlasStudio honest. The goal is not another vanity metric. The goal is to make it obvious whether the game is becoming more playable.

---
work_order_id: WP-03-preflight
title: RPG Maker Map Quality and Passability Preflight
status: proposed
project: the-last-sword-protocol
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: true
created: 2026-07-07
required_capabilities:
  - rpg-maker-json
  - graph-analysis
  - qa-review
preferred_capabilities:
  - python-development
produces:
  - report.map_quality_preflight
  - validator.requirements.map_passability
---

# WP-03-preflight - RPG Maker Map Quality and Passability Preflight

## Purpose

Prepare the implementation pipeline for high-quality RPG Maker MZ map work before Ashford Village is built.

## Player-Facing Goal

Indirect. This work should prevent the project from producing sloppy, uninspired, or passability-broken maps.

## Background

The previous prototype created maps that were technically present but did not meet the desired quality bar. Some maps also had passability problems, including visually blocking tiles that allowed player movement.

The desired target is map quality comparable to polished RPG Maker MZ demo/sample maps, adapted to The Last Sword Protocol's Dragon Quest-style exploration and story.

## Scope

### In Scope

- Review the accepted RPG Maker map quality standard.
- Review the accepted passability rule.
- Inspect TheLastSwordProtocol-Game read-only for current tileset data and passability defaults.
- Identify which validation scripts are needed before WP-03B.
- Define required route checks for Ashford Village implementation.
- Define the acceptance checklist for Ashford Village map quality and passability.
- Produce a preflight report.

### Out of Scope

- Creating maps.
- Editing RPG Maker map files.
- Editing `Tilesets.json`.
- Changing passability settings.
- Deleting old maps.
- Changing story canon.
- Generating visual assets.

## Inputs

- `bridges/rpg-maker-mz/map-quality-standard.md`
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/target-readiness-guidance.md`
- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`
- TheLastSwordProtocol-Game data files, read-only

## Deliverables

- `reports/rpg-maker-bridge/map-quality-passability-preflight.md`
- Recommended route checks for WP-03B.
- Recommended validation tooling work order if needed.
- Update bridge guidance only if clarification is required.

## Acceptance Criteria

- Preflight report identifies the relevant RPG Maker tilesets and passability assumptions.
- Report states whether default RPG Maker passability appears usable.
- Report defines required Ashford Village route checks.
- Report defines map quality acceptance criteria for WP-03B.
- Report identifies any blocker before implementation.
- No RPG Maker files are modified.
- No canon files are modified.

## Verification Steps

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_format/format_guard.py --check
```

If read-only inspection scripts are created, they must not write to TheLastSwordProtocol-Game.

## Allowed Changes

- `reports/rpg-maker-bridge/`
- `bridges/rpg-maker-mz/` documentation if needed
- production graph files if needed
- read-only inspection tooling under `tools/rpg_maker_bridge/` if needed

## Protected Areas

- Do not modify TheLastSwordProtocol-Game.
- Do not modify RPG Maker data files.
- Do not modify tileset passability.
- Do not create maps.
- Do not change story canon.
- Do not run broad formatters.

## Notes for Assigned Agent

This is a safety and quality gate. It exists because map appearance and passability must both be correct before game implementation begins.

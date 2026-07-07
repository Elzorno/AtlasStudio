---
work_order_id: WP-03-preflight
title: RPG Maker Map Quality and Passability Preflight
status: submitted
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

## Submission Record

Submitted 2026-07-07 by Claude Code.

**Primary finding - read before using any other output from this package or from `WP-03A`/`WP-03`:** this preflight discovered that `TheLastSwordProtocol-Atlas` (a sibling repository) is an independently canonical, actively-in-progress design and production system for the exact same first village, with a different protagonist (Kai, not "the Hero"), a different Elara ("Grandmother Elara," not a peer-age guardian), no Rowan character anywhere in that repository, and real hand-authored RPG Maker maps already built against its own version (`data/Map001.json`/`Map002.json`, marked `hand_authored` in `map_ownership.json`, produced under its own `WO-0025`/`WO-0026`/`WO-0035`/`WO-0036`). `work-orders/WP-02-implementation-target-readiness-audit.md` had already flagged this as an undecided question ("Decide whether the target project follows the older `TheLastSwordProtocol-Atlas` Home Island export, the current AtlasStudio first-playable-hour plan, or a merged transition plan") before `WP-03A` and `WP-03` were completed without resolving it. **AtlasStudio does not currently have enough information to responsibly finalize WP-03B for Ashford Village** until a human/Production Director makes this choice explicitly. See `reports/rpg-maker-bridge/implementation-preflight.md`'s Executive Summary and Primary Blocker section for the full evidence and options.

Delivered:

- `reports/rpg-maker-bridge/implementation-preflight.md` - the primary blocker (above), the full remaining blocker list, recommended tilesets grounded in the target repo's real `Tilesets.json` (IDs 2/Outside and 3/Inside, not generic role language), passability assumptions, engine constraints, event and transfer conventions observed directly in the real, already-implemented Map001/Map002, an honest answer on implementation reusability (the existing Ashford Exterior map already follows Dragon Quest-style overworld-connected architecture, not a Zelda-style screen chain - nothing needed rejecting on architectural grounds, only on canon/roster grounds), and concrete recommendations.
- `reports/rpg-maker-bridge/sample-project-analysis.md` - average map sizes, decoration density, environmental storytelling, landmark usage, interior layouts, and event density extracted from the official sample project (99 maps inspected), with an explicit finding that the sample project is a better composition/scale reference than an event-density reference, and that the real target repository's own maps should be used for event-density benchmarking instead. No sample content was reproduced.
- `reports/rpg-maker-bridge/ashford-village-route-validation.md` - required routes validated in two parts: Part A, the routes already real and implemented in Map001 today (six transfers, five NPCs, confirmed by direct JSON inspection); Part B, the routes AtlasStudio's `WP-03` package specified, explicitly marked pending the primary blocker's resolution. Includes a direct comparison of the two route sets and future validation requirements (an automated passability validator, a cross-repository route consistency check, and a reciprocal-transfer check).

No file in `TheLastSwordProtocol-Game`, `TheLastSwordProtocol-Atlas`, or AtlasStudio's canon graph was modified. This was read-only throughout, verified directly rather than assumed.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_format/format_guard.py --check
```

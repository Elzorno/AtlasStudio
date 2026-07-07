# RPG Maker MZ Target Readiness Guidance

## Purpose

This document captures documentation-only bridge updates suggested by the WP-02 implementation target readiness audit.

The goal is to prevent AtlasStudio handoffs from treating an RPG Maker repository as writable before its engine version, ownership ledger, dirty files, and implementation ranges are known.

## Readiness Gate

Before any RPG Maker implementation handoff may modify a game repository, the handoff should record:

- Target repository path.
- RPG Maker engine version.
- Git status or equivalent dirty-file summary.
- Map ownership ledger status.
- Target map IDs and file paths.
- Target database rows or reserved ranges.
- Target switch and variable ranges.
- Plugin list and plugin file availability.
- Files that are explicitly human-owned.
- Files that are suitable for automated generation.
- Verification steps for the exact changed files.

If the target repository has uncommitted map, database, system, or ownership-ledger changes, the handoff should stop before writes unless the production director explicitly accepts that state.

## TheLastSwordProtocol-Game Baseline

The WP-02 audit found the target repo at:

```text
/Users/christopherzornes/Documents/GitHub/TheLastSwordProtocol-Game
```

Current baseline signals:

- RPG Maker MZ version: `1.10.0`.
- Plugins: none configured; `js/plugins/` is empty.
- Maps: 17 map files.
- Map ownership: 2 `hand_authored`, 15 `generated`.
- Data JSON parse status: all inspected data JSON files parsed successfully.
- Existing dirty target files at audit time: `data/Map001.json`, `data/Map002.json`, `data/System.json`, `map_ownership.json`.

## Ownership Rules From Audit

- `data/Map001.json` and `data/Map002.json` should be treated as hand-authored and protected.
- Generated map files may be automated only when their ledger state is still `generated` and the specific file is clean immediately before the work begins.
- `data/System.json`, `map_ownership.json`, and `js/plugins.js` should remain human-owned or production-owned unless a work order authorizes a narrow edit.
- Existing common events, switches, variables, and database rows should be preserved unless a work order names the exact row or range.

## Recommended Mapping Docs

Create bridge mapping docs before game-repo writes:

- `bridges/rpg-maker-mz/mappings/maps.md`
- `bridges/rpg-maker-mz/mappings/switches.md`
- `bridges/rpg-maker-mz/mappings/variables.md`
- `bridges/rpg-maker-mz/mappings/database.md`
- `bridges/rpg-maker-mz/mappings/plugins.md`

Map mapping rows should include:

- RPG Maker map ID.
- RPG Maker file path.
- RPG Maker map name.
- Atlas screen ID, if present.
- AtlasStudio graph node ID, if present.
- Ownership state.
- Safe edit zones.
- Protected event IDs.
- Current manual test route.

## First Safe Handoff Shapes

Good first handoffs after target baseline approval:

- Atlas-side map mapping documentation.
- Generated-map pilot on `data/Map003.json` or `data/Map013.json`.
- Common event reservation for rows 7-49, preserving rows 1-6.
- Database row reservation for enemies, troops, items, skills, animations, weapons, and states.
- Additive asset manifest work for new image, audio, or effect files.

Do not use maps 1 or 2 as automated write targets.

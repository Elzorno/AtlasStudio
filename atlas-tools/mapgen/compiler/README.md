# Atlas Map Compiler Foundation

WO-0025 adds the first deterministic compiler stage for Atlas overworld work. It does not generate a finished RPG Maker map. Its job is to convert canon-aware world intent into an intermediate terrain model that can be audited before any tile painter touches `MapXXX.json`.

## Pipeline

1. World spec: `specs/home_island.world.json` describes canonical locations, gates, required routes, and the intended island shape.
2. Spec parser: `spec_parser.py` validates the minimum contract with stdlib JSON only.
3. Terrain model: `models.py` stores land, elevation, biome, road, water, feature, walkability, locations, and route intent.
4. Terrain planner: `planner.py` builds the island landmass, elevation, rivers, biomes, landmarks, roads, bridges, mountain passes, and deterministic trail bends.
5. Quality auditor: `quality_auditor.py` rejects missing locations, unreachable landmarks, overly straight coasts or roads, rectangular terrain blocks, floating landmarks, and known bad RPG Maker overworld candidates.
6. Tile painter: `tile_painter.py` is an explicit deferred boundary. WO-0025 stops before RPG Maker tile IDs.
7. Semantic assembler: `assembler.py` resolves WO-0056 gameplay graphs, layout families, and reusable modules into deterministic, engine-neutral `MapPlan` candidates through typed connectors and bounded search.
8. MapVision/TileAssembly integration (WO-0071): `tile_assembly_catalog.py` and `map_vision_resolution.py` let `assembler.py` optionally resolve an approved `MapVision` + visual constraint profile into catalog-enabled `TileAssembly` bindings per semantic tag, deterministically selected via the existing `building_selection` seed stream and attached to the output `MapPlan`/`GenerationManifest` as provenance. See `WO-0071-IMPLEMENTATION-NOTES.md` for the architecture and judgment calls.
9. Dual quality gate (WO-0072): `quality_gate.py` runs two independent audits over a `MapPlan` + `GenerationManifest` -- `audit_structural` (retained route/collision/ownership/manifest hard gates) and `audit_visual_proxy` (MapVision-derived checks computable from `tile_assembly_*` provenance: complete/verified assemblies, building height/family, dominant landmark). Neither can offset the other's failure; only `apply_human_decision(..., decided_by="Chris")` may record final acceptance. Checks requiring an actual rendered image (first-camera salience, color/material share, density/path-rhythm) are explicitly listed in `NOT_YET_AUTOMATABLE`, not silently skipped.

## Prototype Outputs

- `prototypes/home_island_terrain.json` is the generated Home Island intermediate terrain plan.
- `audits/home_island_terrain_audit.json` is the quality audit for that terrain plan.
- `audits/map027_negative_audit.json` records why the rejected WO-0024 `Map027.json` is not an acceptable compiler output.

## Commands

```sh
python3 atlas-tools/mapgen/compiler/cli.py generate-prototype \
  --spec atlas-tools/mapgen/compiler/specs/home_island.world.json \
  --output atlas-tools/mapgen/compiler/prototypes/home_island_terrain.json

python3 atlas-tools/mapgen/compiler/cli.py audit-terrain \
  --spec atlas-tools/mapgen/compiler/specs/home_island.world.json \
  --terrain atlas-tools/mapgen/compiler/prototypes/home_island_terrain.json \
  --output atlas-tools/mapgen/compiler/audits/home_island_terrain_audit.json

python3 atlas-tools/mapgen/compiler/cli.py audit-map \
  --map ../TheLastSwordProtocol-Game/data/Map027.json \
  --output atlas-tools/mapgen/compiler/audits/map027_negative_audit.json
```

Regenerate the WO-0058 three-seed JSON, ASCII, and SVG fixtures with:

```sh
python3 atlas-tools/mapgen/compiler/generate_wo0058_fixtures.py
```

Regenerate the WO-0071 Ashford exterior-settlement fixtures (real approved
MapVision + TileAssembly catalog, disposable output only) with:

```sh
python3 atlas-tools/mapgen/compiler/generate_wo0071_fixtures.py
```

The assembler requires an explicit `AssemblyBudget`; incompatible connectors,
missing required zones, unreachable routes, missing parent zones, unsatisfied
module clearance, and exhausted search budgets fail with structured diagnostics.

The `audit-map` command should fail for the current `Map027.json`. That map is retained as a negative example after human rejection.

## Design Notes

- The compiler uses the RPG Maker movement assumption of cardinal passability when auditing routes.
- Forest and marsh are walkable terrain classes unless later object placement adds blockers.
- Rivers are normally non-walkable, but planned roads can convert crossings into bridge features.
- Mountains are impassable unless a planned route converts a cell into a hill-like mountain pass.
- The planner produces design intent only. Future work should implement a tile painter that maps this terrain model to the project's RPG Maker MZ overworld tileset.

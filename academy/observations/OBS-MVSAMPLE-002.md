# OBS-MVSAMPLE-002 - Official Overworld Construction Lessons

Status: Submitted

Source:

- `references/rpg-maker-mz-samples/official sample project/MV_SampleMap_en/data/Map001.json`
- `academy/observations/OBS-MVSAMPLE-001.json`

Purpose:

Capture the official RPG Maker MZ sample-map lessons that should guide the Atlas Map Compiler before it emits any finished Home Island overworld.

## Observations

The official sample world map is large, layered, and purpose-built for overworld composition. Its professional read does not come from a single base fill. The base layer is mostly deep ocean and plain grass, while the visible richness comes from overlays: shallow coastal water, mountains, forests, snow, cliffs, and regional landmark stamps.

The coastline is a transition, not a hard border. Shallow water overlays surround land before the deep ocean takes over, which prevents the island from reading as a cutout pasted on water.

Mountains are not one impassable texture. The sample uses multiple mountain families and separates passable foothill-like terrain from harder impassable peaks. That gives mountain ranges silhouette, edge variation, and readable traversal logic.

Forests are terrain, not walls. The observed world forest tiles are passable in the sample tileset; movement restriction should come from sparse object blockers or explicit gates, not from treating every forest cell as a hard barrier.

Landmarks are integrated into terrain composition. Castles, villages, caves, towers, and ruins sit inside biome context and road logic instead of floating as isolated icons.

## Compiler Requirements Derived From The Sample

- Plan terrain intent before tile IDs.
- Require an intermediate model with land, elevation, biome, water, road, feature, and walkability data.
- Audit for natural composition before map generation.
- Reject rectangular forests, blocky mountains, straight coasts, straight roads, floating landmarks, and unreachable required locations.
- Treat roads and bridges as composition and passability structures, not decorative afterthoughts.
- Keep tile painting as a separate stage so Atlas can verify geography before choosing RPG Maker tiles.

## Negative Example

The current `../TheLastSwordProtocol-Game/data/Map027.json` is a rejected WO-0024 foundation. It found useful story/progression targets, but it does not meet the visual or compositional bar set by the official sample or by the reference poster. WO-0025 retains it only as an audit target that must fail quality review.

## Output For WO-0025

These lessons feed `atlas-tools/mapgen/compiler/`:

- `specs/home_island.world.json`
- `prototypes/home_island_terrain.json`
- `audits/home_island_terrain_audit.json`
- `audits/map027_negative_audit.json`

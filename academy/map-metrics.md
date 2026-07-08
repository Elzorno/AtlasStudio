# Atlas Academy Map Metrics Framework

## Status

Documentation and schema only, per `work-orders/WO-2003-map-metrics-framework.md`. This framework defines what a future metrics analyzer should compute and how its output should be recorded. It does not implement that analyzer, inspect a new map, or grade any map.

## Purpose

Atlas Academy needs repeatable measurements that can support map review without replacing human design judgment. A metric answers a narrow question such as "what percentage of the shell is walkable?" or "how many transfer events are present?" It does not answer "is this map good?"

The key rule is separation of concerns:

- `academy/observation-model.md` records facts and grounded observations.
- This document defines computed summaries and measurements derived from those facts or from the same source data.
- `WO-2002` composition analysis explains why a layout works or fails.
- `WO-2005` grading decides outcomes and recommendations.

## Source Discipline

Metrics must be computed from reproducible evidence:

- RPG Maker map JSON (`data/MapXXX.json`) for dimensions, layers, events, transfers, regions, and encounter data.
- RPG Maker tileset data (`data/Tilesets.json`) for passability flags when needed.
- Observation records conforming to `schemas/academy-observation.schema.json`, when the metric depends on already-recorded zones, focal points, furniture groups, or subjective labels.
- Supplementary screenshots only for human review. A screenshot may illustrate a metric report, but it must not be the only evidence for a metric value.

If a metric depends on a heuristic rather than direct data, the record must say so with `method.is_heuristic: true`, a plain-language explanation, and a confidence value below `high` unless a later validation set proves the heuristic.

## Metric Groups

### Geometry

Geometry metrics describe the shape of the map and its usable area.

| Metric | Definition | Primary source |
|---|---|---|
| `map_tile_count` | `width * height` from the map JSON. | `MapXXX.json` |
| `shell_tile_count` | Number of tiles considered inside the designed room or field shell. | Observation record or map-layer heuristic |
| `void_tile_count` | Tiles outside the designed shell, such as black border or unused margin. | Observation record or map-layer heuristic |
| `map_edge_usage` | Count or percentage of map edges used by entrances, exits, cliffs, water, walls, or other meaningful boundaries. | Map JSON plus observation categories |

### Traversal

Traversal metrics describe where the player can move and how clearly paths connect.

| Metric | Definition | Primary source |
|---|---|---|
| `walkable_percentage` | Walkable tiles divided by shell tiles. | Tileset passability plus event blockers |
| `blocked_percentage` | Blocked tiles divided by shell tiles. | Tileset passability plus event blockers |
| `empty_floor_ratio` | Visually open floor tiles divided by shell tiles. | Map layers plus structural-object observations |
| `average_aisle_width` | Mean width of player-traversable corridors between blockers. | Walkability grid heuristic |
| `door_to_focal_point_distance` | Shortest path length from primary entrance/spawn to the declared focal point. | Observation record plus walkability grid |
| `critical_route_count` | Number of required routes named by an implementation contract or observation record. | Contract/observation linkage |

### Events And Interaction

Event metrics summarize interactive density and routing complexity.

| Metric | Definition | Primary source |
|---|---|---|
| `event_density` | Event count divided by shell tile count. | Map JSON |
| `transfer_count` | Count of events with transfer commands. | Map JSON event command lists |
| `npc_count` | Count of NPC-style events, excluding pure transfers and invisible collision helpers when identifiable. | Map JSON plus naming/observation rules |
| `interaction_count` | Count of events with action-button interaction or player-touch interaction relevant to gameplay. | Map JSON event pages |
| `interaction_distance_mean` | Average shortest path from entrance/spawn to required interaction points. | Walkability grid plus observation record |

### Composition Inputs

These metrics are inputs to composition analysis, not composition verdicts.

| Metric | Definition | Primary source |
|---|---|---|
| `decoration_density` | Decorative object count divided by shell tile count. | Observation record or tile classification |
| `furniture_cluster_count` | Number of furniture/object clusters under an explicit clustering method. | Observation record or adjacency heuristic |
| `room_zone_count` | Number of declared room zones. | Observation record |
| `focal_point_count` | Count of declared focal points. | Observation record |
| `negative_space_ratio` | Open, non-interactive visual space divided by shell tile count. | Observation record plus map layers |

### RPG Maker Production Health

These metrics catch technical risk without deciding acceptance.

| Metric | Definition | Primary source |
|---|---|---|
| `encounter_count` | Count of random encounter entries. | Map JSON |
| `region_id_count` | Count of distinct nonzero region IDs used. | Map JSON region layer |
| `tileset_family_match` | Boolean or enum showing whether the map uses the expected tileset family. | Map JSON plus contract/observation |
| `event_page_count` | Total pages across all events. | Map JSON |
| `missing_reverse_transfer_count` | Count of transfer exits without a recorded reciprocal route, when route data is available. | Map JSON plus contract/observation |

## Required Metric Record Fields

`schemas/academy-map-metrics.schema.json` is authoritative. In summary, a metric record includes:

- `metric_record_id`
- source provenance matching the Academy observation model
- optional links to an observation record, implementation contract, and playtest/acceptance record
- one or more metric groups
- individual metric entries with value, unit, method, evidence, confidence, and caveats
- downstream links to composition, grading, or case-study files

Metric entries must identify whether they are direct counts, derived ratios, pathfinding values, or heuristic classifications. A future analyzer should prefer simple direct metrics before heuristic metrics.

## Units

Use explicit units:

- `tiles` for counts of tiles or path lengths.
- `ratio` for values between `0` and `1`.
- `percent` only when the value is already scaled from `0` to `100`.
- `count` for event, object, zone, or cluster counts.
- `boolean` for true/false checks.
- `enum` for closed categorical results.

Do not mix ratio and percent in the same metric name. The preferred internal unit is `ratio`; reports may display percentages.

## Confidence

Metric confidence describes whether the measurement method is trustworthy, not whether the map is good.

| Confidence | Meaning |
|---|---|
| `high` | Directly computed from stable source data with little or no classification ambiguity. |
| `medium` | Reproducible, but depends on a named heuristic or observation record. |
| `low` | Useful as a warning signal, but requires human review before use in analysis. |

Examples:

- `map_tile_count` from width and height is `high`.
- `furniture_cluster_count` from adjacency classification is usually `medium`.
- `negative_space_ratio` from tile appearance alone is usually `low` until the tile-classification method is validated.

## Accepted, Rejected, And Reference Maps

The same metrics vocabulary applies to accepted maps, rejected maps, and official references, but the interpretation changes:

- Official reference maps establish comparison ranges, not mandatory targets.
- Accepted maps may become project-specific comparison evidence once a human playtest/acceptance record exists.
- Rejected maps may be measured only to understand the failure reason. Their metric values are not positive examples unless explicitly framed as "avoid this pattern."

This follows `academy/README.md`'s accepted/rejected rules and does not create a new acceptance vocabulary.

## Common Mistakes

- Treating a metric threshold as a grade. A high event density can be correct in a market and wrong in a bedroom.
- Comparing maps across incompatible source classes without saying so.
- Computing passability from tile IDs without checking tileset flags and event blockers.
- Using screenshots as primary evidence.
- Reporting a heuristic metric without its method and caveat.
- Letting rejected maps influence implementation targets as if they were accepted references.

## Future Analyzer Shape

A future analyzer should:

1. Read the map JSON and related tileset data.
2. Optionally read an Academy observation record for zones, focal points, and classified objects.
3. Compute the smallest reliable metric set first: dimensions, event counts, transfer counts, encounter counts, and raw layer/region counts.
4. Add passability and path metrics only when a stable walkability model is available.
5. Add composition-input metrics only when the object/zone classification method is explicit.
6. Emit a record conforming to `schemas/academy-map-metrics.schema.json`.

## Non-Goals

- This framework does not implement code.
- This framework does not choose acceptance thresholds.
- This framework does not modify Atlas, `TheLastSwordProtocol-Game`, or any map.
- This framework does not replace the Design Pattern Library or the pattern-aware contract format.

## References

- `academy/README.md`
- `academy/observation-model.md`
- `academy/grading-rubric.md`
- `academy/references/README.md`
- `schemas/academy-observation.schema.json`
- `schemas/academy-map-metrics.schema.json`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `bridges/rpg-maker-mz/passability-rule.md`
- `work-orders/WO-2002-composition-analysis-framework.md`
- `work-orders/WO-2005-map-grading-system.md`
- Created by `work-orders/WO-2003-map-metrics-framework.md`

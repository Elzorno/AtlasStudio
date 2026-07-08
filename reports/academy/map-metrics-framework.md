# Map Metrics Framework Report

## Summary

`WO-2003` creates Atlas Academy's map metrics layer as documentation and schema only. The framework defines metrics as reproducible measurements derived from RPG Maker map data, tileset data, and Academy observation records. It explicitly does not implement an analyzer, grade maps, modify Atlas canon, modify `TheLastSwordProtocol-Game`, or create maps.

## Deliverables

- `academy/metrics/README.md`
- `academy/map-metrics.md`
- `schemas/academy-map-metrics.schema.json`
- `reports/academy/map-metrics-framework.md`
- `work-orders/WO-2003-map-metrics-framework.md`

## Framework Decisions

### Metrics Are Evidence, Not Verdicts

The framework keeps metrics separate from composition analysis and grading. A metric can say that a map has a high empty-floor ratio; it cannot say the map is bad. That interpretation belongs to the future `WO-2002` composition framework and `WO-2005` grading system.

### Observation Records Are The Preferred Bridge

Simple metrics can come directly from RPG Maker JSON. More interpretive inputs, such as room zones or focal points, should come from `academy/observation-model.md` records rather than being guessed inside a metrics report.

### Heuristics Must Be Named

Some useful metrics, including furniture clusters and negative space, require classification. The schema requires each metric entry to state its method, whether that method is heuristic, and any caveats.

### One Vocabulary For Source Classes

Accepted maps, rejected maps, and official references can all be measured with the same vocabulary. Their authority differs. Rejected maps are measured to understand the failure, not to become positive examples.

## Metric Groups Defined

- Geometry
- Traversal
- Events and interaction
- Composition inputs
- RPG Maker production health

These groups cover every example metric named in `WO-2003`: walkable percentage, blocked percentage, event density, decoration density, empty floor ratio, average aisle width, door-to-focal-point distance, furniture cluster count, transfer count, room-zone count, and map edge usage.

## Schema Scope

`schemas/academy-map-metrics.schema.json` defines a metric record with:

- source provenance
- optional links to observation, contract, and acceptance records
- metric groups and metric entries
- method and evidence fields
- confidence and caveats
- downstream links to composition analysis, grading, or Academy case studies

The schema is deliberately an output contract for a future analyzer, not an analyzer implementation.

## Verification

Performed:

```bash
node -e "JSON.parse(require('fs').readFileSync('schemas/academy-map-metrics.schema.json','utf8')); console.log('schema ok')"
python3 tools/atlas_format/format_guard.py --check
```

## Protected Scope

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. No map was created or edited. No Atlas canon file or Design Pattern document was modified.

## Follow-Up Work

- `WO-2002` should use metrics as evidence when defining composition analysis, while preserving the distinction between measurement and interpretation.
- `WO-2005` should use metric records as one input to grading, but should define thresholds and outcomes in the grading system rather than here.
- A later implementation work order may build an analyzer that emits records conforming to the schema.

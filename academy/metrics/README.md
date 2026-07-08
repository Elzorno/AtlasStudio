# Atlas Academy Metrics

## Purpose

This directory defines Atlas Academy's map metrics vocabulary. Metrics are reproducible measurements a future analyzer can compute from RPG Maker map data, observation records, and supplementary renders. They are not grades, acceptance outcomes, or composition verdicts.

`academy/map-metrics.md` is the human-readable framework. `schemas/academy-map-metrics.schema.json` is the structured record format a future analyzer should emit.

## What Belongs Here

- Metric definitions and metric-group documentation.
- Notes about how a metric should be computed, which source data it depends on, and which caveats make it incomplete.
- Future metric-set examples, once a later work order authorizes actual analyzer output.

## What Does Not Belong Here

- Analyzer code. `WO-2003` is documentation and schema only.
- Map grades or pass/fail decisions. Those belong to `academy/grading-rubric.md` today and the future `WO-2005` grading system.
- Composition interpretation. Metrics may feed `WO-2002` composition analysis, but they do not decide whether a composition works.
- Copied maps, screenshots as primary evidence, or edits to `TheLastSwordProtocol-Game`.

## Metric Record Lifecycle

1. A source map is observed under `academy/observation-model.md`.
2. A future analyzer computes metrics from map JSON, event data, tileset data, and/or the observation record.
3. The analyzer emits a record conforming to `schemas/academy-map-metrics.schema.json`.
4. A human or later system may use that record as evidence for composition analysis, pattern extraction, or grading.

## Filing Convention

Future instance files should use a stable metric record id, for example:

```text
MET-ITEMSHOP-001.json
MET-ASHFORD-INN-REJECTED-001.json
```

No instance files are created by `WO-2003`.

## References

- `academy/map-metrics.md`
- `academy/observation-model.md`
- `academy/grading-rubric.md`
- `schemas/academy-map-metrics.schema.json`
- `work-orders/WO-2003-map-metrics-framework.md`

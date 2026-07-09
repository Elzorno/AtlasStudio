---
work_order_id: WO-2003
title: Map Metrics Framework
status: accepted
priority: future
phase: Atlas Academy
recommended_agent: codex
risk_level: medium
player_facing: false
---

# WO-2003 - Map Metrics Framework

## Objective

Design the measurable map metrics that Atlas Academy should eventually compute from RPG Maker map data and screenshots.

## Purpose

AtlasStudio should support map review with repeatable measurements where possible.

## Example Metrics

- walkable percentage
- blocked percentage
- event density
- decoration density
- empty floor ratio
- average aisle width
- door-to-focal-point distance
- furniture cluster count
- transfer count
- room-zone count
- map edge usage

## Deliverables

Create:

- `academy/metrics/README.md`
- `academy/map-metrics.md`
- `schemas/academy-map-metrics.schema.json`
- `reports/academy/map-metrics-framework.md`
- `work-orders/WO-2003-map-metrics-framework.md`

## Constraints

Documentation and schema only.

Do not implement code unless explicitly approved in a later work order.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create maps.

Preserve Immutable Formatting Rule.

## Success Criteria

A future analyzer can compute consistent metrics for accepted maps, rejected maps, and official reference maps.

---

## Submission Record

Submitted 2026-07-08 by Codex.

Delivered:

- `academy/metrics/README.md` - directory purpose, lifecycle, filing convention, and scope boundaries for future metric records.
- `academy/map-metrics.md` - the map metrics framework: source discipline, metric groups, required record fields, units, confidence rules, source-class interpretation, common mistakes, and future analyzer shape.
- `schemas/academy-map-metrics.schema.json` - JSON Schema (2020-12) for future metric analyzer output, including source provenance, metric groups, individual metric entries, method/evidence/confidence/caveat fields, and downstream links.
- `reports/academy/map-metrics-framework.md` - summary report describing decisions, metric groups, schema scope, verification, protected scope, and follow-up work.
- This work order, marked `submitted`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. No map was created or edited. No Atlas canon file or Design Pattern document was modified. No analyzer code was implemented.

Formatting: preserved existing `WO-2000`-series style; no broad reformatting performed.

Verification performed:

```bash
node -e "JSON.parse(require('fs').readFileSync('schemas/academy-map-metrics.schema.json','utf8')); console.log('schema ok')"
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every file in this work order's Deliverables list exists on disk and is non-empty, and every JSON schema deliverable parses as valid JSON. Verified by a full-text read of this Submission Record against the actual repository state, not by re-running the commands listed above.

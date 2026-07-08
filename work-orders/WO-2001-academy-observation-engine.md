---
work_order_id: WO-2001
title: Atlas Academy Observation Engine
status: submitted
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2001 - Atlas Academy Observation Engine

## Objective

Design the observation model for map study.

The Observation Engine records factual map observations before any interpretation or grading occurs.

## Purpose

AtlasStudio should separate facts from conclusions.

Examples of observations:

- map dimensions
- door coordinates
- room zones
- event count
- walkable percentage
- furniture groups
- counter placement
- window count
- transfer locations

## Deliverables

Create:

- `academy/observation-model.md`
- `academy/observations/README.md`
- `schemas/academy-observation.schema.json`
- `work-orders/WO-2001-academy-observation-engine.md`

## Required Content

Define:

- observation fields
- evidence requirements
- source map provenance
- screenshot references
- JSON references
- distinction between objective and subjective notes
- how observations feed pattern extraction

## Constraints

Documentation and schema only.

Do not write analysis code.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create or edit maps.

Preserve Immutable Formatting Rule.

## Success Criteria

A future tool or agent can record a map observation without mixing factual measurements with design judgment.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `schemas/academy-observation.schema.json` - a JSON Schema (2020-12, `additionalProperties: false` throughout, matching the style of `schemas/design-pattern.schema.json` and `schemas/work-order-routing.schema.json`) formalizing the observation record: `source` provenance (repo, file path, map name, tileset, reference class per `academy/references/README.md`, capture date, ownership-ledger state at capture, a version anchor via `provenance_ref`), a structurally separate `objective_observations` array (each entry carrying a category drawn from `PATTERN_EXTRACTION_GUIDE.md`'s "What to Measure" list plus one addition, `room_zone`, justified by `inn.pattern.md`'s existing two-zone finding; a JSON-reference-shaped `evidence` object; and an explicit `is_inferred` flag with required reasoning when true) and `subjective_observations` array (each entry required to name what objective observation(s) it is `grounded_in`), a `screenshot_references` array fixed to `illustrative_only` so a screenshot can never substitute for map-data evidence, and a `feeds` object linking a record forward to an extraction report, pattern candidates, or an Academy case study.
- `academy/observation-model.md` - the prose specification covering every item `WO-2001`'s Required Content names (observation fields, evidence requirements, source map provenance, screenshot references, JSON references, the objective/subjective distinction, and how observations feed pattern extraction), plus a worked example (`OBS-ITEMSHOP-001`) built entirely from already-published facts in `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, read-only) rather than a new extraction pass - explicitly marked as such, per this work order's "do not write analysis code" constraint. The worked example was checked against the schema (required fields, `additionalProperties: false`, enums) before submission and passes.
- `academy/observations/README.md` - filing convention (`<observation_id>.json`) and the three-way distinction between this directory (raw structured facts), `academy/reports/` (interpreted case studies), and the existing pre-Academy `reports/map-analysis/`/`reports/design-patterns/` prose-report locations.
- This work order, marked `submitted`.

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - the Item Shop analysis was read-only. No existing Design Pattern document was modified. No map was created or edited. No analysis code was written - the worked example is static, hand-verified JSON illustrating the schema, not the output of a script.

One deliberate scope boundary: `academy/README.md`'s directory-structure listing (a `WO-2000` deliverable, not a `WO-2001` one) still marks `observation-model.md` and `observations/` as "not yet created." This work order does not edit that file, since it is not in `WO-2001`'s own deliverables list - flagging the staleness here rather than silently expanding scope to fix it. A future small edit (or `WO-2002`, which touches the same directory) should update it.

Formatting: preserved existing house style, including this file's own leaner `WO-2000`-series frontmatter shape. No existing file was reformatted.

Verification performed:

```bash
find academy/observations schemas/academy-observation.schema.json -type f
python3 -c "import json; json.load(open('schemas/academy-observation.schema.json')); print('valid json')"
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```

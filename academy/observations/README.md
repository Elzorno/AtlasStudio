# Atlas Academy Observations

## Purpose

This directory holds individual observation records - instance data conforming to `schemas/academy-observation.schema.json`, one file per observation pass over one source map. It is the populated counterpart to `academy/observation-model.md`, which defines the model, and `academy/curriculum.md`, whose Level 1 ("Recognize") produces the records that belong here.

## What Belongs Here

- One JSON file per observation record, each a valid instance of `schemas/academy-observation.schema.json`.
- Nothing else. This directory is data, not prose - a record's own `feeds.extraction_report` field is where it points to any narrative write-up, rather than that write-up living alongside the record itself.

## Filing Convention

Name each file after its `observation_id`, e.g. `OBS-ITEMSHOP-001.json`. This keeps the directory listing itself a readable index and keeps every file trivially traceable back to the identifier every other Academy document (a case study's `feeds.case_study`, a curriculum entry, a future tool) would reference it by.

## Relationship to Other Directories

- `academy/observations/` (here): raw, structured observation records - facts only, per `academy/observation-model.md`'s objective/subjective split.
- `academy/reports/`: case studies built *from* one or more observation records, judged against `academy/grading-rubric.md`'s eligibility criteria - interpretation and lessons, not raw facts.
- `reports/map-analysis/`, `reports/design-patterns/` (existing, pre-Academy locations): prose extraction reports and corpus reviews, per `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`'s existing output format. An observation record here may cite one of these via `feeds.extraction_report`, or a future extraction pass may produce both a prose report there and a structured record here side by side - this foundation does not require one before the other.

## Validation

Every file here should validate against `schemas/academy-observation.schema.json`. No validator tool is built by this work order (`WO-2001` is documentation and schema only, per its own constraints) - until one exists, validate by inspection against the schema's `required` fields, `additionalProperties: false` constraints, and enums, the same way `academy/observation-model.md`'s worked example was checked before that document was submitted.

## Current Contents

- `OBS-ASHFORDINN-001.json` - the first real file filed here, per this section's own prior instruction: an actual Level 1 observation pass over `TheLastSwordProtocol-Game/data/Map026.json`, produced for `academy/reports/ashford-inn-revisit-001.md`. `academy/observation-model.md`'s worked example (`OBS-ITEMSHOP-001`) remains illustrative and inline in that document, not a file here, since it re-expresses an existing report's facts rather than resulting from a new observation pass.
- `OBS-ASHFORDINN-002.json` - a companion pass over the same target, adding the map's first-ever engine-faithful render as evidence and cross-checking `OBS-ASHFORDINN-001`'s tile-level findings against it. Feeds `academy/case-studies/lsp-map-inspection-001.md` and `academy/grades/GRD-ASHFORDINN-003.json`.
- `OBS-ASHFORDINN-003.json` - corrects `OBS-ASHFORDINN-001`'s structural_object tile identification (the "three mismatched beds" were disassembled pieces of one sofa; the "incomplete fireplace" was a mirror and shelf; the "picture frames" were pillars/crates/rubble), found while rebuilding the map's furniture using tile IDs verified by direct pixel crop rather than trusted from the prior record. Confirms the original 2026-07-08 human rejection reasons were accurate. Feeds `academy/grades/GRD-ASHFORDINN-004.json`.

## References

- `academy/observation-model.md`, `curriculum.md`, `reports/README.md`
- `schemas/academy-observation.schema.json`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- Created by `work-orders/WO-2001-academy-observation-engine.md`

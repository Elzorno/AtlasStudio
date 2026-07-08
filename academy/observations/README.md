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

None yet. This directory is created empty by `work-orders/WO-2001-academy-observation-engine.md`. `academy/observation-model.md`'s worked example (`OBS-ITEMSHOP-001`) is illustrative and lives inline in that document, not as a file here, since it re-expresses an existing report's facts rather than resulting from a new observation pass - the first real file filed here should come from an actual Level 1 curriculum pass, not be backfilled from this example.

## References

- `academy/observation-model.md`, `curriculum.md`, `reports/README.md`
- `schemas/academy-observation.schema.json`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- Created by `work-orders/WO-2001-academy-observation-engine.md`

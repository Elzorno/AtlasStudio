# Atlas Academy Grades

## Purpose

This directory holds individual filed map-grade records - instance data conforming to `schemas/academy-map-grade.schema.json`, one file per grading pass over one target. It is the populated counterpart to `academy/grading-system.md` and `academy/grading-rubric.md`, which define the model and checklist, per the same relationship `academy/observations/README.md` describes between itself and `academy/observation-model.md`.

## What Belongs Here

- One JSON file per grade record, each a valid instance of `schemas/academy-map-grade.schema.json`.
- Nothing else. A grade's own `overall_recommendation.summary` is the synthesis; a longer write-up belongs in `academy/reports/` and may cite the grade file rather than duplicate it.

## Filing Convention

Name each file after its `grade_id`, e.g. `GRD-ASHFORDINN-002.json`. A target graded more than once (a rejected pass, then a revised one) gets a new `grade_id` and a new file each time - grades are never overwritten in place, per `schemas/academy-map-grade.schema.json`'s own field description.

## Validation

Every file here should validate against `schemas/academy-map-grade.schema.json`. No validator tool is built by this work order; until one exists, validate by inspection against the schema's `required` fields, `additionalProperties: false` constraints, and enums, the same way `academy/observations/`'s records are checked.

## Current Contents

- `GRD-ASHFORDINN-002.json` - re-grade of `TheLastSwordProtocol-Game/data/Map026.json` using `academy/observations/OBS-ASHFORDINN-001.json` as evidence, compared against the worked example `GRD-ASHFORDINN-001` (`reports/academy/map-grading-system.md`). See `academy/reports/ashford-inn-revisit-001.md`. This is the first grade filed here - `atlas academy grade` previously reported no `academy/grades/` directory at all.

## References

- `academy/grading-system.md`, `grading-rubric.md`
- `schemas/academy-map-grade.schema.json`
- `academy/observations/README.md` - the equivalent convention for observation records this directory mirrors.
- `academy/reports/ashford-inn-revisit-001.md` - the case study `GRD-ASHFORDINN-002` was produced for.

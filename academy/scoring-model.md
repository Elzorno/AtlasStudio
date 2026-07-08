# Atlas Academy Composition Scoring Model

## Status

Documentation only, per `work-orders/WO-2008-composition-validator.md`. Defines the scale and confidence discipline `academy/composition-validator.md` and `schemas/composition-review.schema.json` use. Does not score any real map on its own.

## The Scale

Each of `academy/composition-validator.md`'s ten evaluation areas is scored 1 (fails this area badly) to 5 (exemplary), matching `academy/grading-system.md`'s existing 1-5 convention rather than introducing a second incompatible scale alongside it. A score may instead be `null` with `confidence: insufficient_evidence`, per "Scoring Without Complete Evidence" below.

| Score | Meaning |
|---|---|
| 1 | The area actively undermines the map - actively confuses, clutters, or contradicts the composition's own apparent intent. |
| 2 | The area is weak - present but not doing useful work, or contradicted by at least one clear observation. |
| 3 | The area is adequate - functional, unremarkable, no notable strength or failure. |
| 4 | The area is strong - a clear, deliberate choice that visibly serves the map's purpose. |
| 5 | The area is exemplary - the kind of choice worth citing as evidence in a future Design Pattern proposal. |

## Confidence Tiers

Matches `schemas/academy-map-grade.schema.json`'s existing confidence enum, unchanged: `high`, `medium`, `low`, `insufficient_evidence`. A reviewer states confidence independently of the score itself - a `2` can be `high` confidence (clearly, verifiably weak) or `low` confidence (weakly implied, not directly observed), and the record must distinguish them.

## Scoring Without Complete Evidence

Not every evaluation area can be scored for every target, particularly for a map with no observation record or metrics record on file. A `null` score with `confidence: insufficient_evidence` is the correct, honest output when nothing on file supports a number - matching the discipline `academy/grading-system.md` already established and `academy/case-studies/official-map-001.md` (`WO-2007`) already applied to two metrics (decoration density, room utilization). A Composition Review with several `insufficient_evidence` areas is an accurate review, not a failed one, and it doubles as a work list for what future observation or metrics work would resolve.

## Evidence Discipline

A score is only as strong as its citation. For the six evaluation areas with a direct `academy/composition-analysis.md` topic match (Visual Hierarchy, Traffic Flow, Negative Space, Furniture Grouping, Room Zoning, Environmental Storytelling), the corresponding `academy/composition-rubric.md` Holds/Gap/N/A verdict must be cited as evidence - a score that contradicts its own cited rubric verdict without explanation is not valid. For the four new areas (Landmarks, Navigation, Atmosphere, Project Identity), evidence should cite an observation record, a metrics record, or the map's governing Design Pattern/Implementation Packet directly, per `schemas/composition-review.schema.json`'s `evidence` field.

## Overall Composition Summary

Not an eleventh score. A short synthesis connecting the ten area verdicts into one statement of why the composition succeeds or fails, per `academy/composition-validator.md`'s Step 3. This is the field a future `academy/grading-system.md` grade's `composition` category should cite directly.

## What This Model Does Not Decide

- It does not decide `outcome` (`accepted`/`accepted_with_notes`/`rejected`/`deferred`) - that remains `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s human decision, mediated through `academy/grading-system.md`, unchanged.
- It does not decide `remediation_tags` - those are a full-grade concept (`academy/grading-system.md`), not a composition-review concept.
- A high Project Identity score does not by itself satisfy `academy/grading-system.md`'s `project_fit` category, which checks broader packet/tileset/element-list compliance a Composition Review does not assess (see `academy/composition-validator.md`'s Ten Evaluation Areas table).

## References

- `academy/composition-validator.md`
- `academy/composition-analysis.md`, `composition-rubric.md`
- `academy/grading-system.md`
- `schemas/academy-map-grade.schema.json`, `composition-review.schema.json`
- `academy/case-studies/official-map-001.md`
- `reports/academy/composition-validator-design.md`
- Created by `work-orders/WO-2008-composition-validator.md`

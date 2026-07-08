# Atlas Academy Composition Validator

## Status

Documentation and schema only, per `work-orders/WO-2008-composition-validator.md`. This document defines the formal scoring model for a standalone composition review; `academy/scoring-model.md` defines the scale and confidence discipline it uses; `schemas/composition-review.schema.json` formalizes the record shape. None of these implement a validator tool, edit a map, or modify `TheLastSwordProtocol-Atlas`/`TheLastSwordProtocol-Game`.

## Purpose

`work-orders/WO-2008`'s own Objective states this directly: "Create the framework for evaluating map composition... This validator critiques maps. It does not generate maps." `academy/composition-analysis.md` (`WO-2002`) already defines ten topics for discussing composition qualitatively, and `academy/composition-rubric.md` gives each topic a fast Holds/Gap/N/A checklist verdict. Neither produces a scored, citable record of its own - the closest thing today is `academy/grading-system.md`'s (`WO-2005`) single `composition` category, one score among nine in a full map grade. This work order fills the gap between those two: a standalone, deeper composition scoring pass with its own record shape, whose result becomes the evidence a full map grade's `composition` category cites, rather than a third independent judgment competing with either existing document.

## Ten Evaluation Areas, Reconciled

`work-orders/WO-2008`'s Evaluation Areas list names ten items. Six correspond directly to an existing `academy/composition-analysis.md` topic; four do not exist there yet and are defined here for the first time, each scoped narrowly enough to avoid duplicating an existing `academy/grading-system.md` category's authority.

| Evaluation area | Relationship to existing Academy documents |
|---|---|
| Visual Hierarchy | Direct match: `academy/composition-analysis.md` Topic 8. |
| Traffic Flow | Direct match: `academy/composition-analysis.md` Topic 3. |
| Negative Space | Direct match: `academy/composition-analysis.md` Topic 2. |
| Furniture Grouping | Direct match: `academy/composition-analysis.md` Topic 5. |
| Room Zoning | Direct match: `academy/composition-analysis.md` Topic 6. |
| Environmental Storytelling | Direct match: `academy/composition-analysis.md` Topic 10, but **narrowed here** to the compositional contribution only (does object placement visually support the location's tone and use). The full four-silent-questions treatment (who controls it, what changed recently) stays with `academy/grading-system.md`'s `environmental_storytelling` category and `academy/templates/map-study-template.md`'s Section 7, which this validator does not duplicate. |
| Landmarks | New. Grounded in `academy/knowledge/observation-rules.md`'s cognitive-mapping material and `academy/templates/map-study-template.md`'s Section 5 (`WO-2007`) - what memorable, re-orientable elements the composition provides. Not a `composition-analysis.md` topic; closest partial relative is Topic 1 (Focal Point), which this area extends from "one dominant point" to "the set of elements a player would use to reacquire orientation." |
| Navigation | New, and **deliberately narrow**: whether composition choices (aisle width, sight lines, door alignment, zoning) support wayfinding. This is not the same as `academy/grading-system.md`'s `readability` category, which `academy/grading-rubric.md` already defines as "broader than composition's own Entry Readability topic - whole-map wayfinding and legibility." This validator's Navigation area answers a narrower question - does the *composition itself* support navigation - and is one input to, not a replacement for, a full `readability` grade. |
| Atmosphere | New, and **deliberately narrow**: composition's contribution to mood through density, rhythm, and decoration choices (`academy/composition-analysis.md` Topic 9, Decoration Balance, plus the rhythm concept recorded in `academy/knowledge/composition-rules.md`). Distinct from the full `environmental_storytelling` grading category, which also covers narrative-state questions this area does not score. |
| Project Identity | New, and **deliberately narrow**: whether the map's composition specifically follows its governing pattern's own Composition Rules section (for example `shop.pattern.md`'s bilateral-organization and density-rhythm rules) and its location's stated tone (per `LOC-*` canon). This is **not** the same as `academy/grading-system.md`'s `project_fit` category, which is broader - governing Implementation Packet compliance, tileset family, and named element lists, not composition specifically. A map can score well on Project Identity here (composition matches its pattern's rules) while still failing `project_fit` overall (wrong tileset, missing required element) - the two are related but not interchangeable, and a Composition Review must not be cited as satisfying `project_fit` on its own. |

## Relationship to `academy/grading-system.md`

A Composition Review (this document's output, formalized by `schemas/composition-review.schema.json`) is **evidence a full map grade's `composition` category cites**, per `academy/grading-rubric.md`'s existing instruction: "Composite verdict across `academy/composition-rubric.md`'s ten topics. Cite that rubric's own Holds/Gap/N/A verdicts as evidence, not a fresh judgment." A Composition Review does not issue an `outcome` (`accepted`/`rejected`/etc.) and does not carry acceptance authority on its own - `PLAYTEST_AND_ACCEPTANCE.md`'s human decision remains the only source of that, unchanged by this work order, exactly as `academy/grading-system.md` already established for the grading model as a whole.

## Relationship to `academy/composition-rubric.md`

`academy/composition-rubric.md`'s Holds/Gap/N/A checklist remains the fast, first-pass form - a reviewer works through it before attempting a full Composition Review. A Composition Review is the deeper, scored form: it takes each of this document's ten evaluation areas, assigns a 1-5 score and a confidence tier (per `academy/scoring-model.md`), and requires citing the corresponding `composition-rubric.md` verdict (where the evaluation area has a direct topic match) as supporting evidence rather than re-deriving it from nothing.

## How a Composition Review Is Produced

1. Gather what evidence already exists for the target: an `academy/composition-rubric.md` checklist pass, an `academy/observations/` record, any `academy/map-metrics.md` Composition Inputs group values, and the map's governing Design Pattern and Implementation Packet.
2. Score each of the ten evaluation areas against that evidence, per `academy/scoring-model.md`'s scale, citing evidence per area, or mark `insufficient_evidence` where nothing on file supports a score - never invent one.
3. Write an `overall_composition_summary` connecting the ten area verdicts into one reasoned statement about why the composition succeeds or fails, per this work order's own Success Criteria: "Atlas Academy can explain why a map succeeds or fails."
4. File the record per `schemas/composition-review.schema.json`. This record is citable evidence, not a grade and not an acceptance decision - a future `academy/grading-system.md` grade's `composition` category should cite it directly rather than re-deriving a verdict from raw evidence a second time.

## Non-Goals

- This document does not evaluate any real map on its own. `reports/academy/composition-validator-design.md` applies it to one worked example, using only evidence already on file.
- This document does not implement a validator tool or analysis code.
- This document does not edit, generate, or modify any map.
- This document does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, `academy/composition-analysis.md`, `composition-rubric.md`, or `academy/grading-system.md`.
- A Composition Review does not grant `project_fit` or `readability` verdicts it has not actually assessed; see the Ten Evaluation Areas table above for the exact scope boundary on each of the four new areas.

## References

- `academy/composition-analysis.md`, `composition-rubric.md`
- `academy/grading-system.md`, `grading-rubric.md`
- `academy/scoring-model.md`
- `schemas/composition-review.schema.json`
- `academy/knowledge/observation-rules.md`, `composition-rules.md`
- `academy/templates/map-study-template.md`
- `academy/map-metrics.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `reports/academy/composition-validator-design.md`
- Created by `work-orders/WO-2008-composition-validator.md`

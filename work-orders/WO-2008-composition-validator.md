---
work_order_id: WO-2008
title: Composition Validator
status: accepted
priority: high
phase: Atlas Academy
recommended_agent: claude_code
risk_level: medium
player_facing: false
---

# WO-2008 - Composition Validator

## Objective

Create the framework for evaluating map composition.

This validator critiques maps.

It does not generate maps.

## Deliverables

Create:

- `academy/composition-validator.md`
- `academy/scoring-model.md`
- `schemas/composition-review.schema.json`
- `academy/reports/composition-validator-design.md`
- `work-orders/WO-2008-composition-validator.md`

## Evaluation Areas

Include:

- Visual Hierarchy
- Traffic Flow
- Negative Space
- Furniture Grouping
- Room Zoning
- Landmarks
- Navigation
- Environmental Storytelling
- Atmosphere
- Project Identity

## Constraints

Documentation and schema only.

No implementation.

No map editing.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Preserve Immutable Formatting Rule.

## Success Criteria

Atlas Academy can explain why a map succeeds or fails.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/composition-validator.md` - the model. Reconciles all ten named Evaluation Areas: six map directly to an existing `academy/composition-analysis.md` topic; four (Landmarks, Navigation, Atmosphere, Project Identity) are new and each is stated explicitly to be narrower than the nearest similarly-named `academy/grading-system.md` category (`readability`, `environmental_storytelling`, `project_fit` respectively) so the two frameworks do not silently compete for the same evidence. States directly that a Composition Review is evidence a full map grade's `composition` category should cite, not a third, independent scoring authority, and that it carries no `outcome` or `remediation_tags` of its own.
- `academy/scoring-model.md` - a 1-5 scale matching `academy/grading-system.md`'s existing convention, the same four-tier confidence vocabulary, an evidence-citation requirement (the six directly-matched areas must cite their `academy/composition-rubric.md` verdict), and an honest `insufficient_evidence`/`null` fallback.
- `schemas/composition-review.schema.json` - a JSON Schema (2020-12, matching this project's schema style and closely mirroring `schemas/academy-map-grade.schema.json`'s shape) for a single composition review, with a ten-value `area` enum and a `governing_pattern` field for the Project Identity area's citation.
- `reports/academy/composition-validator-design.md` - the evidence report, including a full worked review (`CMP-ITEMSHOP-001`) against Map021, reusing `academy/case-studies/official-map-001.md` (`WO-2007`) rather than performing new inspection. All ten areas scored; the `project_identity` score is explicitly flagged as near-tautological (the map is the governing pattern's own source), with a named recommendation for a future non-circular test.
- This work order, marked `submitted`.

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - the existing Map021 extraction report was read only. No existing Design Pattern, `academy/composition-analysis.md`, `composition-rubric.md`, or `academy/grading-system.md` was modified. No map was created, edited, or generated. No implementation performed - this work order delivers documentation and a schema only.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
python3 -c "import json; json.load(open('schemas/composition-review.schema.json')); print('valid json')"
# structural check: all required fields present, additionalProperties: false respected,
# all ten area enum values scored exactly once, score bounds 1-5 or null+insufficient_evidence
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every file in this work order's Deliverables list exists on disk and is non-empty, and every JSON schema deliverable parses as valid JSON. Verified by a full-text read of this Submission Record against the actual repository state, not by re-running the commands listed above.

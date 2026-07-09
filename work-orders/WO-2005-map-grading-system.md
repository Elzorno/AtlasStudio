---
work_order_id: WO-2005
title: Map Grading System
status: accepted
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2005 - Map Grading System

## Objective

Create a formal grading model for maps reviewed by Atlas Academy.

## Purpose

Accepted and rejected maps should produce reusable learning data. The grading system records why a map passes or fails.

## Example Categories

- composition
- traffic flow
- readability
- visual hierarchy
- passability
- environmental storytelling
- project fit
- RPG Maker quality
- Dragon Quest exploration feel when applicable
- overall recommendation

## Deliverables

Create:

- `academy/grading-system.md`
- `academy/grading-rubric.md`
- `schemas/academy-map-grade.schema.json`
- `reports/academy/map-grading-system.md`
- `work-orders/WO-2005-map-grading-system.md`

## Required Outcomes

Define:

- Accepted
- Accepted with Notes
- Rejected
- Deferred
- Needs Art Direction
- Needs Functional Fix

## Constraints

Documentation and schema only.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create or edit maps.

Preserve Immutable Formatting Rule.

## Success Criteria

A future playtest or review can grade a map consistently and produce structured feedback for future improvements.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/grading-system.md` - reconciles all ten Example Categories (nine independently-scored 1-5 axes plus "overall recommendation" as a synthesis field, not a tenth score) and all six Required Outcomes (the four `PLAYTEST_AND_ACCEPTANCE.md` outcomes, kept unchanged rather than replaced, plus two independent remediation tags - `Needs Art Direction`, `Needs Functional Fix` - rather than two additional competing top-level outcomes). States explicitly why that reconciliation was made this way (preserving `PLAYTEST_AND_ACCEPTANCE.md`'s existing recorded authority over acceptance rather than fracturing it with a sixth competing state) and defines "Grading Without Complete Evidence" so a category can be honestly marked `insufficient_evidence` instead of guessed.
- `academy/grading-rubric.md` - rewritten to supersede the `WO-2000` foundation-level version, per that document's own stated intent: preserves the four-outcome vocabulary and foundation-level case-study eligibility criteria unchanged, and adds the nine-category checklist and two-tag vocabulary.
- `schemas/academy-map-grade.schema.json` - a JSON Schema (2020-12, matching this project's existing schema style) for a single grading result, cross-referencing `schemas/academy-observation.schema.json` and `academy-map-metrics.schema.json` as the evidence a score must trace to, with `outcome` constrained to `PLAYTEST_AND_ACCEPTANCE.md`'s four values and `remediation_tags` as the separate, independent dimension.
- `reports/academy/map-grading-system.md` - the evidence report, including a full worked grade (`GRD-ASHFORDINN-001`) against the real Map026 Ashford Inn rejection, validated against the schema before inclusion. The grade honestly scores four of nine categories `insufficient_evidence` (traffic flow, readability, visual hierarchy, passability) rather than guessing, and finds - sharper than `WO-2002`'s earlier partial treatment of the same rejection - that the evidence most directly and confidently supports an `rpg_maker_quality` failure (high confidence) and a `project_fit` deviation from `IMP-HOM-020`'s own named element list (medium confidence), with the `needs_functional_fix` tag deliberately omitted since nothing in the recorded rejection reason touches passability or event logic.
- This work order, marked `submitted`.

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - `map_ownership.json` and the cited canon/packet files were read only, and `Map026.json` itself was not inspected (consistent with this Academy series' established discipline of not performing new analysis passes outside a proper observation record). No existing Design Pattern document was modified. No map was created or edited.

One deliberate scope boundary, consistent with prior submissions in this series: `academy/README.md` is not edited here, since it is not a `WO-2005` deliverable.

Formatting: preserved existing house style, including this file's own leaner `WO-2000`-series frontmatter shape. No existing file was reformatted; `academy/grading-rubric.md` was fully rewritten (not reformatted) as its own `WO-2000`-anticipated supersession, not an incidental edit.

Verification performed:

```bash
find schemas/academy-map-grade.schema.json academy/grading-system.md reports/academy/map-grading-system.md -type f
python3 -c "import json; json.load(open('schemas/academy-map-grade.schema.json')); print('valid json')"
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every file in this work order's Deliverables list exists on disk and is non-empty, and every JSON schema deliverable parses as valid JSON. Verified by a full-text read of this Submission Record against the actual repository state, not by re-running the commands listed above.

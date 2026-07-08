# Atlas Academy References

## Status

Foundation-level rules created by `work-orders/WO-2000-atlas-academy-foundation.md`, now extended by `work-orders/WO-2004-reference-library-governance.md`.

Full governance lives in:

- `academy/references/reference-governance.md`
- `academy/references/source-classes.md`
- `academy/references/gold-standard-maps.md`
- `schemas/academy-reference-source.schema.json`

## Purpose

A reference source is anything Atlas Academy studies to extract or corroborate a design lesson. Not every reference should carry equal weight - `WO-2004`'s brief names this directly ("Not every reference map should have equal weight"). This document states the two source kinds already in active use, and the one discipline that governs citing either of them, ahead of that fuller governance work.

## Reference Sources In Use Today

### Official RPG Maker MZ sample maps

The primary reference source for the current Design Pattern Library. Every accepted interior pattern (`studio/design-patterns/interiors/*.pattern.md`) is derived from one or more official sample maps bundled with the engine, extracted per `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` and cited by exact map file and tile coordinates in each pattern's `Source`/`Observed Maps` sections.

### AtlasStudio's own accepted builds

A second reference source, used once a build reaches **Accepted** or **Accepted with Notes** with a human playtest pass on file (`academy/grading-rubric.md`). `studio/design-patterns/README.md` already names this as the Pattern Library's own stated future direction ("and, over time, from AtlasStudio's own accepted builds") - Atlas Academy is where that direction is operationalized, not a new idea introduced here. No AtlasStudio build currently qualifies: Ashford Village's `hand_authored` maps (`Map001`, `Map002`) are not yet playtest-certified (`reports/production-review/ashford-shop-production-review.md`, `studio/governance/production-readiness.md`), so this source class is named and ready, not yet populated.

## What Is Not Yet a Governed Reference Source

`WO-2004` now governs three further source classes: rejected project maps, design references, and comparative JRPG references. Rejected project maps are diagnostic-only unless a source record explicitly says otherwise; design references and comparative JRPG references are context sources, not automatic implementation authority. See `source-classes.md`.

## The One Discipline That Applies to Any Source, Governed or Not

Regardless of source class, every Atlas Academy citation follows `PATTERN_EXTRACTION_GUIDE.md`'s existing discipline, unchanged:

- Every claim traces to a specific source file and, wherever possible, specific tile coordinates or event IDs.
- Objective observations (directly verifiable from data) are kept separate from subjective ones (interpretive judgments, labeled as such).
- An inferred fact (e.g. a spawn position with no incoming transfer to confirm it) is stated as inferred, never silently upgraded to confirmed.
- A pattern's or finding's confidence is only as strong as its citation count and quality, per `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` - single-source evidence stays flagged as such rather than reads as settled.

## References

- `work-orders/WO-2004-reference-library-governance.md`
- `academy/references/reference-governance.md`, `source-classes.md`, `gold-standard-maps.md`
- `schemas/academy-reference-source.schema.json`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`, `README.md`
- `academy/README.md`, `curriculum.md`, `grading-rubric.md`
- `reports/production-review/ashford-shop-production-review.md`, `studio/governance/production-readiness.md`
- Created by `work-orders/WO-2000-atlas-academy-foundation.md`

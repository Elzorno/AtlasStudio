# Atlas Academy Compositions

## Purpose

This directory holds per-map composition analyses - the write-up produced by applying `academy/composition-analysis.md`'s ten topics and `academy/composition-rubric.md`'s checklist to one specific source map. It is the interpreted counterpart to `academy/observations/`, the same way `academy/reports/` is the interpreted counterpart to raw facts more broadly - the distinction here is narrower: this directory is composition-specific, while `academy/reports/` holds full case studies that may span composition, passability, and other categories together.

## What Belongs Here

- One write-up per map per composition pass, applying the ten-topic checklist from `academy/composition-rubric.md` with a Holds/Gap/N/A verdict and cited reason for each topic.
- Nothing that duplicates `academy/observations/`'s raw facts - a composition analysis here should cite an observation record (`feeds` field, per `schemas/academy-observation.schema.json`) rather than restating its facts inline, per this project's standing "point, don't paraphrase" citation discipline.

## Relationship to Other Directories

- `academy/observations/` (facts, per `WO-2001`) feeds this directory (interpretation, per `WO-2002`).
- This directory, in turn, may feed `academy/reports/` (`WO-2000`) once a composition analysis becomes part of a fuller accepted/rejected case study, or feeds a future `work-orders/WO-2005-map-grading-system.md` category score directly.
- `reports/academy/composition-analysis-framework.md` is not filed here - it is the framework-level evidence synthesis behind `academy/composition-analysis.md` itself, not a per-map analysis. See `academy/reports/README.md`'s existing note on the `academy/reports/` versus `reports/academy/` distinction; the same distinction applies here: per-map composition write-ups belong in `academy/compositions/`, framework-level work belongs in `reports/academy/`.

## Filing Convention

Name each file after the map or screen it analyzes and the date of the pass, e.g. `SCR-HOM-ASH-004-2026-07-08.md`, so a room analyzed more than once (a rejected build, then a revised one) keeps both passes distinguishable rather than one overwriting the other.

## Current Contents

None yet. This directory is created empty by `work-orders/WO-2002-composition-analysis-framework.md`. Ashford Inn's rejected `Map026` build (see `reports/academy/composition-analysis-framework.md`) is a strong candidate for the first real entry here, once a full observation record exists to ground it - this work order does not perform that pass itself.

## References

- `academy/composition-analysis.md`, `composition-rubric.md`, `observations/README.md`, `reports/README.md`
- `reports/academy/composition-analysis-framework.md`
- Created by `work-orders/WO-2002-composition-analysis-framework.md`

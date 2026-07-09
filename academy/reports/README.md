# Atlas Academy Reports

## Purpose

This directory holds Atlas Academy's own case-study output: written lessons from specific reviewed maps, filed per `academy/curriculum.md`'s levels and `academy/grading-rubric.md`'s eligibility criteria. A case study here is the record of what a specific accepted or rejected build actually taught, distinct from the standing methodology documents in `academy/` itself (the curriculum, the rubric, the reference rules) that a case study is produced *under*.

## What Belongs Here

- **Level 1 extraction reports**, once a case study (not just a standalone Pattern Library extraction, which continues to live at `reports/map-analysis/` or `reports/design-patterns/` per existing convention) is built around one.
- **Level 2 comparison notes**: an accepted build checked against its governing contract's cited pattern layer(s), with a held/exception verdict per rule.
- **Level 3 diagnoses**: a rejected build or a documented contract-level gap, traced to a specific rule, layer, or missing pattern - `BUILD-0043` and the Ashford Inn Required Conditions finding (`academy/README.md`, "Why This Exists Now") are the two model cases this directory's first real entries should match in rigor.
- **Level 4 proposal pointers**: once a case study's findings are routed into `studio/design-patterns/PATTERN_REVIEW_PROCESS.md`'s proposal path, this directory keeps a short pointer to the resulting pattern work order rather than duplicating the proposal itself.

## Relationship to `reports/academy/`

`work-orders/WO-2002-composition-analysis-framework.md` names a deliverable at `reports/academy/composition-analysis-framework.md` - a top-level `reports/<topic>/` path, matching this project's existing convention for work-order-produced analysis reports (`reports/design-patterns/`, `reports/production-review/`, `reports/atlas-doctor/`, and so on). This directory (`academy/reports/`) and that convention are not the same thing, and this foundation does not merge them:

- `academy/reports/` (here) is Academy's own internal home for individual map/build case studies, produced under Academy's curriculum.
- `reports/academy/` (top-level, per `WO-2002`'s precedent) is where framework-level analysis reports - the kind a work order like `WO-2002` or `WO-2003` produces about the *methodology itself*, not about one specific map - are expected to land, consistent with how every other AtlasStudio subsystem files its own reports.

A future work order may find reason to consolidate these two locations. This foundation states the distinction plainly rather than picking one silently, since both are already named in this project's own work orders (`WO-2000`'s brief names `academy/reports/README.md` directly; `WO-2002`'s brief names `reports/academy/composition-analysis-framework.md` directly) and neither should be treated as a typo for the other.

## Filing Discipline

Every report filed here follows `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`'s citation discipline: point to the source build, contract, and (where applicable) pattern document by exact path, keep objective and subjective observations visibly separate, and label any inference as inferred rather than upgrading it to fact. A report that cannot meet `academy/grading-rubric.md`'s foundation-level eligibility criteria is not yet ready to file here - fix the underlying gap first, per that document's own closing discipline (borrowed from `studio/contracts/PATTERN_APPLICATION_CHECKLIST.md`'s "Using This Checklist": a criterion that cannot honestly be checked means the work is not ready, not a formality to route around).

## Current Contents

- `ashford-inn-revisit-001.md` - the first case study filed here: a Level 3 diagnosis of `TheLastSwordProtocol-Game/data/Map026.json`'s rejected build, built on `academy/observations/OBS-ASHFORDINN-001.json` and `academy/grades/GRD-ASHFORDINN-002.json`, checked against `academy/grading-rubric.md`'s foundation-level eligibility criteria before filing.

## References

- `academy/README.md`, `curriculum.md`, `grading-rubric.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_REVIEW_PROCESS.md`
- `studio/contracts/PATTERN_APPLICATION_CHECKLIST.md`
- `work-orders/WO-2002-composition-analysis-framework.md` - source of the `reports/academy/` precedent this document distinguishes itself from.
- Created by `work-orders/WO-2000-atlas-academy-foundation.md`

# Atlas Academy Grading Rubric

## Status

Supersedes the foundation-level version of this file created by `work-orders/WO-2000-atlas-academy-foundation.md`, per that document's own stated intent: "When `WO-2005` is executed, it supersedes this file; it should reconcile against it explicitly rather than starting over, since this file's four-outcome vocabulary is not a placeholder to be discarded." This version keeps every commitment the foundation version made - `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s four outcomes, unchanged, and the foundation-level case-study eligibility criteria - and adds the nine-category checklist and remediation-tag vocabulary `academy/grading-system.md` (`WO-2005`) defines.

## Purpose

`academy/grading-system.md` defines the grading model. This document is the checklist a reviewer actually works through, matching `academy/composition-rubric.md`'s relationship to `academy/composition-analysis.md` - a fast, concrete companion to a longer specification, not a replacement for it.

## The Four Outcomes (Unchanged)

Atlas Academy still does not define a competing outcome vocabulary. `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s four outcomes, exactly as that document defines them, remain the only values `schemas/academy-map-grade.schema.json`'s `outcome` field accepts:

| Outcome | What it means for Atlas Academy |
|---|---|
| **Accepted** | Eligible as a positive reference case (Curriculum Level 2) once a human playtest pass is on file. |
| **Accepted with Notes** | Eligible the same way; the notes are read as Academy input in their own right. |
| **Rejected** | Eligible as a negative reference case (Curriculum Level 3) only when the recorded reason is specific and falsifiable. |
| **Deferred** | Not yet eligible either way - real and in-flight, not yet judged. |

## The Two Remediation Tags (New)

Per `academy/grading-system.md`'s reconciliation of `WO-2005`'s six Required Outcomes: **Needs Art Direction** and **Needs Functional Fix** are not a fifth and sixth outcome. They are independent tags, zero, one, or both of which may attach to any outcome above, most usefully to Rejected or Accepted with Notes:

```text
□ Needs Art Direction
    Composition, asset, or tile-correctness issue - low composition
    or rpg_maker_quality category score, or a tile_usage-category
    observation finding. Routes to a composition/asset follow-up.

□ Needs Functional Fix
    Passability, event, or transfer-logic issue - low passability
    or traffic_flow category score. Routes to a passability/
    engineering follow-up, per bridges/rpg-maker-mz/passability-rule.md.
```

## The Nine Scored Categories

For each category, record a score (1-5) and a confidence (`high`/`medium`/`low`/`insufficient_evidence`), per `schemas/academy-map-grade.schema.json`. Never invent a score to fill a category with no supporting evidence - record `insufficient_evidence` and `score: null` instead, per `academy/grading-system.md`'s "Grading Without Complete Evidence."

```text
□ Composition
    Composite verdict across academy/composition-rubric.md's ten
    topics. Cite that rubric's own Holds/Gap/N/A verdicts as evidence,
    not a fresh judgment.

□ Traffic Flow
    Does composition (aisles, door alignment, furniture edges)
    predict the actual reachable set? Cite academy/map-metrics.md's
    Traversal group (average_aisle_width, door_to_focal_point_distance)
    where available.

□ Readability
    Whole-map wayfinding and legibility - broader than composition's
    own "Entry Readability" topic. Can a first-time player form a
    working mental model within a short exploration window?

□ Visual Hierarchy
    Can a viewer name what they notice first, second, third? Ties to
    academy/composition-analysis.md Topic 8.

□ Passability
    Per bridges/rpg-maker-mz/passability-rule.md directly - this
    project's existing, unchanged standard. Not a new Academy
    invention; cite that document's Required Validation list.

□ Environmental Storytelling
    Does the map answer what happens here, who controls it, what is
    allowed here, and what changed recently - and does it carry its
    governing location's specific canon tone (e.g. LOC-ASH-001's
    "warm, ordinary, quietly strange" for an Ashford interior)?

□ Project Fit
    Does the map satisfy its governing Implementation Packet and
    Design Pattern citations, including any recorded
    PATTERN_RESOLUTION_RULES.md exception? A build that ignores its
    own governing packet fails this category regardless of how it
    otherwise looks.

□ RPG Maker Quality
    Per bridges/rpg-maker-mz/map-quality-standard.md's existing bar:
    "Would this be believable as a polished RPG Maker MZ sample map
    adapted to The Last Sword Protocol's story?"

□ Dragon Quest Exploration Feel (when applicable)
    Score only when the target has a stated Dragon Quest-style
    exploration requirement (e.g. a governing DDR). Not applicable to
    every target - record overall_recommendation
    .dragon_quest_exploration_feel_applicable: false rather than
    forcing a score where none is required.
```

## Overall Recommendation

Not a tenth score. A short synthesis connecting the nine category verdicts into one recommendation, plus the selected `outcome` and `remediation_tags` - per `schemas/academy-map-grade.schema.json`'s `overall_recommendation.summary` field.

## Foundation-Level Case-Study Eligibility (Unchanged)

The five criteria the `WO-2000` version of this document stated for when a case study is ready to file under `academy/reports/` still apply, unchanged: the outcome is real and recorded (not inferred from ownership state alone); a Rejected reason traces to a specific rule or gap; an Accepted comparison states a held/exception verdict per rule; every claim cites its source; and a systemic finding is cross-filed to `studio/governance/production-readiness.md`'s backlog, not kept only inside the case study.

## Worked Example: Grading the Map026 Rejection

See `reports/academy/map-grading-system.md` for the full worked grade, produced honestly against only the evidence currently on file - several categories score `insufficient_evidence` rather than a guessed number, and the result closes the loop `academy/composition-rubric.md`'s own earlier, partial treatment of this same rejection left open.

## References

- `academy/grading-system.md` - the full model this checklist operationalizes.
- `academy/composition-analysis.md`, `composition-rubric.md`, `map-metrics.md`, `references/reference-governance.md`
- `schemas/academy-map-grade.schema.json`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `map-quality-standard.md`
- `reports/academy/map-grading-system.md`
- Created by `work-orders/WO-2000-atlas-academy-foundation.md`; superseded and expanded by `work-orders/WO-2005-map-grading-system.md`.

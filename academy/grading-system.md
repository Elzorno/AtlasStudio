# Atlas Academy Map Grading System

## Status

Documentation and schema only, per `work-orders/WO-2005-map-grading-system.md`. This document defines the formal grading model; `schemas/academy-map-grade.schema.json` formalizes it; `academy/grading-rubric.md` is the checklist a reviewer actually works through. None of these build a grading tool, grade a real map, or modify `TheLastSwordProtocol-Atlas`/`TheLastSwordProtocol-Game`.

## Purpose

`academy/grading-rubric.md` (`WO-2000`) established foundation-level Accepted/Rejected eligibility criteria for an Academy case study, explicitly deferring the full multi-category model to this work order. `academy/composition-rubric.md` (`WO-2002`) checks composition specifically. `academy/map-metrics.md` (`WO-2003`) defines computed measurements. `academy/references/reference-governance.md` and `source-classes.md` (`WO-2004`) govern what evidence may be cited and at what confidence. This document is where all four combine into one map's actual recommendation - the piece `work-orders/WO-2005`'s own Purpose names directly: "Accepted and rejected maps should produce reusable learning data. The grading system records why a map passes or fails."

## The Ten Categories, Reconciled

`work-orders/WO-2005`'s Example Categories list names ten items. Nine are independently scoreable axes; the tenth is not a parallel score, and this document states that reconciliation explicitly rather than forcing a tenth number where none belongs:

| Category | Scored 1-5? | Primary source |
|---|---|---|
| Composition | Yes | `academy/composition-analysis.md`, `composition-rubric.md` (`WO-2002`) - this category's score is the composite verdict across that document's ten finer-grained topics. |
| Traffic flow | Yes | `academy/composition-analysis.md` Topic 3, plus `academy/map-metrics.md`'s Traversal metric group (`average_aisle_width`, `door_to_focal_point_distance`). |
| Readability | Yes | Broader than `academy/composition-analysis.md`'s Topic 7 ("Entry Readability") - whole-map wayfinding and legibility, grounded in `references/atlas_academy_jrpg_map_research.md`'s Part 4/Part 10 wayfinding synthesis. |
| Visual hierarchy | Yes | `academy/composition-analysis.md` Topic 8. |
| Passability | Yes | `bridges/rpg-maker-mz/passability-rule.md` directly - this project's existing, unchanged passability standard, not a new Academy invention. |
| Environmental storytelling | Yes | `academy/composition-analysis.md` Topic 10, grounded in the target's own governing canon (e.g. `LOC-ASH-001`'s tone requirement for an Ashford interior). |
| Project fit | Yes | Whether the map satisfies its governing Implementation Packet, Design Pattern citations (including any recorded `PATTERN_RESOLUTION_RULES.md` exception, per `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`'s own precedent), and repository-authority boundaries. |
| RPG Maker quality | Yes | `bridges/rpg-maker-mz/map-quality-standard.md`'s existing bar directly: "Would this be believable as a polished RPG Maker MZ sample map adapted to The Last Sword Protocol's story?" |
| Dragon Quest exploration feel | Yes, when applicable | Per `WO-2005`'s own "when applicable" qualifier - scored only when the target has a stated Dragon Quest-style exploration requirement (e.g. `DDR-0005`'s explicit framing for Ashford's building-submap model). Not applicable to every target; forcing a score where none applies is itself a grading error, not thoroughness. |
| Overall recommendation | No - this is the synthesis | Not a tenth independent measurement. It is the `overall_recommendation.summary` field in `schemas/academy-map-grade.schema.json`: the reasoning that connects the other nine scores into one recommendation, plus the `outcome` and `remediation_tags` fields below. |

Each of the first nine is scored 1 (fails this category badly) to 5 (exemplary), adapted from `references/atlas_academy_jrpg_map_research.md`'s Part 10 proposed five-axis 1-5 rubric - cited at that document's own stated confidence tier (research hypothesis for the numeric scale itself; higher for the underlying design principles it draws on), not upgraded to a settled AtlasStudio standard. A category may instead carry `confidence: insufficient_evidence` and `score: null` when nothing on file actually supports a number - see "Grading Without Complete Evidence" below.

## Required Outcomes, Reconciled

`work-orders/WO-2005`'s Required Outcomes list names six items: Accepted, Accepted with Notes, Rejected, Deferred, Needs Art Direction, Needs Functional Fix. The first four are `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s existing, unchanged outcome vocabulary - `academy/README.md` and `academy/grading-rubric.md` (`WO-2000`) already committed Atlas Academy to reusing that vocabulary rather than inventing a competing one, and this document keeps that commitment rather than quietly abandoning it under a new work order.

The remaining two are not a fifth and sixth outcome sitting beside the first four - they are **remediation tags**, a second, independent dimension recording *why* an outcome landed where it did, and what kind of follow-up it needs:

- **Needs Art Direction** - the map's failure or open issue is primarily composition, asset, or tile-correctness in nature (low `composition` or `rpg_maker_quality` category scores; a `WO-2001` `tile_usage`-category finding). Routes to a follow-up composition/asset pass.
- **Needs Functional Fix** - the map's failure or open issue is primarily passability, event logic, or transfer correctness (low `passability` or `traffic_flow` category scores). Routes to a follow-up implementation/engineering pass, per `bridges/rpg-maker-mz/passability-rule.md`.

A grade's `outcome` is always one of the four `PLAYTEST_AND_ACCEPTANCE.md` values; its `remediation_tags` array (zero, one, or both tags) is orthogonal and gives that outcome actionable routing `PLAYTEST_AND_ACCEPTANCE.md`'s own vocabulary does not by itself provide. Both tags may apply to the same rejected map - a build can simultaneously need an art pass and a passability fix. Reconciling six required items into "four outcomes plus two independent tags" rather than a flat six-value enum is a deliberate design decision, made explicit here rather than left for a schema reader to reverse-engineer: `PLAYTEST_AND_ACCEPTANCE.md` already has recorded authority over what "Accepted" and "Rejected" mean project-wide (evidence requirements, documentation requirements, follow-up requirements per that document), and a grading system introducing a fifth or sixth competing top-level state would fracture that authority rather than extend it.

## Grading Without Complete Evidence

Not every category can be scored for every target. A category scored from evidence that does not yet exist is worse than a category honestly marked `insufficient_evidence` - this is the same discipline `academy/composition-rubric.md`'s own worked Map026 example already demonstrated for one category at a time; this document generalizes it across all nine. A grade with several `insufficient_evidence` entries is not an incomplete or failed grade - it is an accurate one, and it doubles as a work list: each `insufficient_evidence` category names exactly what future `academy/observations/`, `academy/compositions/`, or metrics work would need to produce before that category could be scored for real.

## How a Grade Is Produced

1. Gather what evidence already exists for the target: an `academy/observations/` record (`WO-2001`), an `academy/compositions/` analysis (`WO-2002`), any metric records (`WO-2003`), and its governing Implementation Packet, Design Pattern citations, and canon (per `academy/references/reference-governance.md`'s "When References Can Influence Implementation Contracts" rules, applied here to grading rather than contracting).
2. Score each of the nine categories against that evidence, citing it per-category in `evidence`, or mark `insufficient_evidence` where nothing supports a score.
3. Write `overall_recommendation.summary`, connecting the scored categories into one reasoned recommendation - not a restatement of each score, but why they add up the way they do.
4. Select `outcome` from `PLAYTEST_AND_ACCEPTANCE.md`'s four values, and `remediation_tags` per the reconciliation above.
5. File the record. This grade is a recommendation, not the acceptance decision itself - per the same "recommend, never dispatch" principle already governing the Work Order Router and Agent Scheduler, a human still records the actual `PLAYTEST_AND_ACCEPTANCE.md` decision separately.

## Relationship to Other Atlas Academy Documents

- `academy/grading-rubric.md` - the checklist form of this document, and the file `WO-2000`'s foundation-level version explicitly anticipated being superseded here.
- `academy/composition-analysis.md`, `composition-rubric.md` - primary evidence for the `composition` category and contributing evidence for three others.
- `academy/map-metrics.md` - primary evidence for `traffic_flow` and supporting evidence for several others.
- `academy/references/reference-governance.md`, `source-classes.md` - govern what a `rejected_project_map` source (like Map026) may and may not be cited for within a grade; see `reports/academy/map-grading-system.md` for that governance applied directly.
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md` - the outcome vocabulary this system reuses unchanged, and the actual human decision authority this system's `outcome` field only recommends toward.

## Non-Goals

- This document does not grade any real map. `reports/academy/map-grading-system.md` applies it to Ashford Inn's Map026 as a worked example, using only evidence already on file, honestly marking what cannot yet be scored.
- This document does not build a grading tool or analysis code.
- This document does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, any existing Design Pattern, or create/edit any map.
- This document does not grant a grade any acceptance authority `PLAYTEST_AND_ACCEPTANCE.md` does not already assign to a human Production Director decision.

## References

- `academy/grading-rubric.md`, `composition-analysis.md`, `composition-rubric.md`, `map-metrics.md`, `references/reference-governance.md`, `source-classes.md`, `curriculum.md`
- `schemas/academy-map-grade.schema.json`, `academy-observation.schema.json`, `academy-map-metrics.schema.json`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `map-quality-standard.md`
- `references/atlas_academy_jrpg_map_research.md`
- `reports/academy/map-grading-system.md`
- Created by `work-orders/WO-2005-map-grading-system.md`

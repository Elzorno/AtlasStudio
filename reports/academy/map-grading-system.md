# Map Grading System - Evidence Report

Status: submitted

Scope: `WO-2005`. Synthesizes the evidence behind `academy/grading-system.md`'s nine-category, four-outcome-plus-two-tag model, and applies it as a full worked grade against the same real, current case `WO-2002`'s evidence report used: Ashford Inn's rejected `Map026` build. This report closes the loop that `reports/academy/composition-analysis-framework.md` deliberately left open - that report scored one category (composition) against the rejection reason and stopped; this report scores all nine, honestly, against the same limited evidence.

This report is analysis and evidence, not implementation guidance. It does not direct any build against `TheLastSwordProtocol-Game` or `TheLastSwordProtocol-Atlas`, and it does not modify either repository, any existing Design Pattern, or any map.

## Coverage Check

`academy/grading-system.md` reconciles all ten items in `work-orders/WO-2005`'s Example Categories list (nine scored categories plus the overall recommendation, which is a synthesis field rather than a tenth score) and all six items in its Required Outcomes list (the four `PLAYTEST_AND_ACCEPTANCE.md` outcomes, unchanged, plus two remediation tags rather than two additional competing outcome values). Every category's primary evidence source is named in that document's reconciliation table - four categories (`composition`, `traffic_flow`, `visual_hierarchy`, `environmental_storytelling`) draw primarily on `WO-2002`'s existing composition framework; `passability` and `rpg_maker_quality` draw on this project's own pre-existing, unchanged bridge standards; `project_fit` draws on the governing Implementation Packet and Design Pattern citation discipline already established by `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`; `readability` and `dragon_quest_exploration_feel` draw most heavily on `references/atlas_academy_jrpg_map_research.md`'s synthesis, since the existing pattern corpus does not independently corroborate them as deeply - the same asymmetry `reports/academy/composition-analysis-framework.md` already flagged, inherited honestly rather than hidden.

## Worked Grade: Ashford Inn, Map026

Produced entirely from evidence already on file: `map_ownership.json`'s recorded rejection reason, `IMP-HOM-020`, `SCR-HOM-ASH-004`, `DDR-0005`, `LOC-ASH-001`, and `bridges/rpg-maker-mz/map-quality-standard.md`. **No new inspection of `Map026.json` itself was performed** - per this work order's "documentation and schema only" constraint and this Academy series' established discipline (`WO-2001`, `WO-2002`) of not performing new analysis passes outside a proper observation record. Several categories are honestly scored `insufficient_evidence` rather than guessed.

```json
{
  "schema_version": "0.1.0",
  "grade_id": "GRD-ASHFORDINN-001",
  "target": {
    "repo": "TheLastSwordProtocol-Game",
    "file_path": "data/Map026.json",
    "map_name": "INT_Ashford_Inn",
    "ownership_state_at_capture": "hand-authored",
    "captured_at": "2026-07-08"
  },
  "grader": "atlas-academy-worked-example",
  "created": "2026-07-08",
  "category_scores": [
    {
      "category": "composition",
      "score": 2,
      "confidence": "low",
      "rationale": "Rejection reason includes 'sofa/furniture rendering is poor,' a weak signal toward a furniture-grouping or decoration-balance issue, but 'rendering' is ambiguous between asset quality and placement logic. No observation record or composition analysis exists yet to confirm which.",
      "evidence": ["TheLastSwordProtocol-Game/map_ownership.json (Map 26 rejection_reason)"]
    },
    {
      "category": "traffic_flow",
      "score": null,
      "confidence": "insufficient_evidence",
      "rationale": "The rejection reason contains no statement about walkability, aisle width, or reachability. No metric or observation record exists for this build.",
      "evidence": []
    },
    {
      "category": "readability",
      "score": null,
      "confidence": "insufficient_evidence",
      "rationale": "No wayfinding-relevant detail in the rejection reason.",
      "evidence": []
    },
    {
      "category": "visual_hierarchy",
      "score": null,
      "confidence": "insufficient_evidence",
      "rationale": "'Rocks appear in the room' may indicate an intrusive, unintended focal element, but this is speculative without a composition pass confirming rock placement relative to the intended focal point (the counter, per IMP-HOM-020).",
      "evidence": []
    },
    {
      "category": "passability",
      "score": null,
      "confidence": "insufficient_evidence",
      "rationale": "The rejection reason names no functional, transfer, or event complaint. Absence of a stated functional complaint is not equivalent to a verified passability pass - a human art-focused review may not have exercised passability at all.",
      "evidence": []
    },
    {
      "category": "environmental_storytelling",
      "score": 2,
      "confidence": "medium",
      "rationale": "IMP-HOM-020 requires a warm-stone vent/hearth and domestic furniture consistent with LOC-ASH-001's 'warm, ordinary, quietly strange' tone; unrequested rocks in an Inn interior directly work against that tone rather than serving it.",
      "evidence": [
        "TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md",
        "TheLastSwordProtocol-Atlas/atlas/docs/02_World/Locations/Home_Island/Ashford.md",
        "TheLastSwordProtocol-Game/map_ownership.json (Map 26 rejection_reason)"
      ]
    },
    {
      "category": "project_fit",
      "score": 2,
      "confidence": "medium",
      "rationale": "IMP-HOM-020 specifies the Inside tileset family and a named element list (counter, bed alcoves, warm-stone vent) with no rocks named. 'Interior tiles are incorrect' plausibly indicates the wrong tileset family or an element outside the packet's list was used, though this is not confirmed by direct file inspection.",
      "evidence": [
        "TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md",
        "TheLastSwordProtocol-Game/map_ownership.json (Map 26 rejection_reason)"
      ]
    },
    {
      "category": "rpg_maker_quality",
      "score": 2,
      "confidence": "high",
      "rationale": "The rejection reason directly and specifically fails bridges/rpg-maker-mz/map-quality-standard.md's own bar ('would this be believable as a polished RPG Maker MZ sample map') - incorrect tiles, out-of-place objects, and poor furniture rendering are exactly what that standard names as disqualifying.",
      "evidence": [
        "TheLastSwordProtocol-Game/map_ownership.json (Map 26 rejection_reason)",
        "bridges/rpg-maker-mz/map-quality-standard.md"
      ]
    },
    {
      "category": "dragon_quest_exploration_feel",
      "score": null,
      "confidence": "insufficient_evidence",
      "rationale": "Applicable per DDR-0005's building-submap exploration model, but the rejection reason concerns interior asset correctness, not the exploration model itself. No evidence either way.",
      "evidence": ["TheLastSwordProtocol-Atlas/atlas/docs/99_Reference/Decision_Records/DDR-0005_Ashford_Inn.md"]
    }
  ],
  "overall_recommendation": {
    "summary": "The recorded rejection is best explained as an RPG Maker Quality and Project Fit failure (both medium-to-high confidence, both scoring low) - the build used incorrect tiles and included at least one element (rocks) not called for by IMP-HOM-020, undermining Environmental Storytelling as a secondary effect. No evidence supports or rules out issues in Traffic Flow, Readability, Visual Hierarchy, or Passability - the rejection reason simply does not address them, which is itself notable: this was very likely an art/asset-focused review, not a full functional pass. Composition proper is only weakly implicated pending an actual observation record.",
    "dragon_quest_exploration_feel_applicable": true
  },
  "outcome": "rejected",
  "remediation_tags": ["needs_art_direction"],
  "notes": "Worked example only, built entirely from map_ownership.json's one-line rejection reason and each category's governing document, per reports/academy/map-grading-system.md. No observation record, composition analysis, or metrics record exists yet for Map026 - several categories are honestly insufficient_evidence rather than guessed. needs_functional_fix is deliberately omitted: nothing in the rejection reason indicates a functional/passability complaint."
}
```

This example was checked against `schemas/academy-map-grade.schema.json` (required fields, `additionalProperties: false`, enums, numeric bounds) before inclusion and passes.

## What This Grade Adds Beyond the Composition Report

`reports/academy/composition-analysis-framework.md` reached a narrower conclusion: the Map026 rejection is "predominantly a tile_usage/asset-correctness finding... rather than a composition finding this framework primarily covers." This grade sharpens that into something more directly actionable:

- **`rpg_maker_quality`**, not `composition`, is the category the evidence most directly and confidently supports (`high` confidence versus `composition`'s `low`) - the rejection reason is close to a verbatim restatement of `map-quality-standard.md`'s own bar.
- **`project_fit`** surfaces a second, independently useful reading: the failure may be a direct deviation from `IMP-HOM-020`'s own named element list and tileset requirement, not merely "the room doesn't look good" in the abstract.
- **The `needs_functional_fix` tag's absence is itself a finding.** Nothing in the recorded rejection reason touches passability, transfers, or events - worth stating explicitly, since it means whatever follow-up work addresses this rejection can reasonably start from "assume passability is probably fine, focus on tiles and placed objects" rather than re-auditing everything from zero. That assumption should still be confirmed, not taken on faith - hence `passability` itself remains `insufficient_evidence`, not a passing score.

## Recommendations for Future Academy Work

- The concrete next step named in `reports/academy/composition-analysis-framework.md` still stands and would resolve most of this grade's `insufficient_evidence` categories at once: a Level 1 observation record for `Map026.json` (read-only inspection; the file remains `hand_authored`/protected), followed by a composition pass under `academy/compositions/`.
- Once that observation record exists, re-run this grade (as a new `grade_id`, per `schemas/academy-map-grade.schema.json`'s no-overwrite convention) and compare against `GRD-ASHFORDINN-001` - the `insufficient_evidence` categories becoming scored, confident categories is itself a useful measure of how much this grading system's value depends on the Observation Engine and Composition framework actually being used, not just existing.
- This is a strong candidate for the first real entry under `academy/reports/` (per `academy/README.md` and `academy/reports/README.md`), once a follow-up build exists to compare it against.

## Constraints Observed

- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. `map_ownership.json` and the cited canon/packet files were read only; `Map026.json` itself was not inspected.
- No existing Design Pattern document was modified.
- No map was created or edited.
- Documentation and schema only.

## References

- `academy/grading-system.md`, `grading-rubric.md`, `composition-analysis.md`, `composition-rubric.md`, `map-metrics.md`
- `schemas/academy-map-grade.schema.json`
- `reports/academy/composition-analysis-framework.md`, `map-metrics-framework.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `map-quality-standard.md`
- `TheLastSwordProtocol-Game/map_ownership.json` (read-only)
- `TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md`, `atlas/docs/02_World/Locations/Home_Island/Ashford.md`, `atlas/docs/99_Reference/Decision_Records/DDR-0005_Ashford_Inn.md` (all read-only)
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- Created by `work-orders/WO-2005-map-grading-system.md`

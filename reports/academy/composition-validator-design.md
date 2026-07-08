# Composition Validator Design - Evidence Report

Status: submitted

Scope: `WO-2008`. Synthesizes the evidence behind `academy/composition-validator.md`'s ten-evaluation-area model and `academy/scoring-model.md`'s scale, and applies both as a full worked Composition Review against Map021 ("Item Shop") - the same map `academy/case-studies/official-map-001.md` (`WO-2007`) already studied, reused here rather than performing a second independent inspection pass.

This report is analysis and evidence, not implementation guidance. It does not direct any build against `TheLastSwordProtocol-Game` or `TheLastSwordProtocol-Atlas`, and it does not modify either repository, any existing Design Pattern, or any map.

## Why This Framework Needed Careful Reconciliation

`work-orders/WO-2008` is marked `risk_level: medium`, higher than the other Atlas Academy work orders in this series - and the reason is visible directly in its Evaluation Areas list. Six of the ten areas (Visual Hierarchy, Traffic Flow, Negative Space, Furniture Grouping, Room Zoning, Environmental Storytelling) already exist as `academy/composition-analysis.md` topics or overlap an existing `academy/grading-system.md` category. Left unreconciled, this work order would have produced a **third** scoring surface duplicating ground `WO-2002` and `WO-2005` already cover - the exact failure mode `academy/grading-system.md` explicitly named and avoided for outcomes ("a grading system introducing a fifth or sixth competing top-level state would fracture that authority rather than extend it"). `academy/composition-validator.md`'s Ten Evaluation Areas table performs that same reconciliation for composition scoring specifically: six areas map directly to an existing topic; four (Landmarks, Navigation, Atmosphere, Project Identity) are new, and each is deliberately scoped narrower than the nearest existing `academy/grading-system.md` category it could otherwise be mistaken for (`readability`, `environmental_storytelling`, `project_fit`) - stated explicitly in that table so a future reader does not have to reverse-engineer the boundary.

## Coverage Check

All four required deliverables were produced: `academy/composition-validator.md` (the model), `academy/scoring-model.md` (the scale and evidence discipline), `schemas/composition-review.schema.json` (the record shape), and this report. All ten named Evaluation Areas appear in the schema's `area` enum and are scored in the worked example below.

## Worked Composition Review: Map021 ("Item Shop")

Produced entirely from evidence already on file: `academy/case-studies/official-map-001.md` (`WO-2007`) and `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md`. **No new map inspection was performed.** This choice - reusing the same map WO-2007 already studied - lets this report test the scoring model itself rather than conflate model design with a fresh evidence-gathering pass, matching the same methodological choice `reports/academy/official-corpus-methodology.md` made for Map021's original selection.

```json
{
  "schema_version": "0.1.0",
  "review_id": "CMP-ITEMSHOP-001",
  "target": {
    "repo": "TheLastSwordProtocol-Game",
    "file_path": "data/Map021.json",
    "map_name": "Item Shop",
    "ownership_state_at_capture": "hand-authored",
    "captured_at": "2026-07-08"
  },
  "reviewer": "atlas-academy-worked-example",
  "created": "2026-07-08",
  "governing_pattern": "PAT-INTERIOR-SHOP",
  "area_scores": [
    {
      "area": "visual_hierarchy",
      "score": 4,
      "confidence": "medium",
      "rationale": "Bilateral organization around x8 is a directly observed coordinate fact (door, aisle, rug, and back wall all on or near the centerline); that this composition 'reads as balanced' to a player is an inference on top of that fact, not itself directly measured.",
      "evidence": ["academy/case-studies/official-map-001.md#2-composition", "TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"]
    },
    {
      "area": "traffic_flow",
      "score": 4,
      "confidence": "high",
      "rationale": "Source report states directly: entry at bottom center, move north to central aisle, branch left/right, return to centerline and exit - 'no maze and no hidden path.' This is a stated observation, not an inference.",
      "evidence": ["TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"]
    },
    {
      "area": "negative_space",
      "score": 4,
      "confidence": "high",
      "rationale": "Source report states directly that open floor 'is not empty filler; it is the customer path' - negative space is functionally assigned, not leftover.",
      "evidence": ["TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"]
    },
    {
      "area": "furniture_grouping",
      "score": 5,
      "confidence": "high",
      "rationale": "Goods are grouped by surface and purpose with no scattered isolated objects observed: left potions/medicine, right baskets/scrolls/jewelry-like items, back wall shelves/crates - matching shop.pattern.md's own clustering rule exactly.",
      "evidence": ["TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md", "studio/design-patterns/interiors/shop.pattern.md"]
    },
    {
      "area": "room_zoning",
      "score": 3,
      "confidence": "low",
      "rationale": "Zones (entry threshold, center aisle, browse loop, wall stock, focal back wall) are inferable from coordinate clustering but are not explicitly labeled as zones in the source report - an adequate, not confirmed-strong, score.",
      "evidence": ["academy/case-studies/official-map-001.md#2-composition"]
    },
    {
      "area": "environmental_storytelling",
      "score": 4,
      "confidence": "medium",
      "rationale": "Composition-only scope: object placement (display-first, no counter, no back-office) visually supports 'retail browsing' as the map's function. Broader narrative questions (who controls it, what changed recently) are out of this area's scope per academy/composition-validator.md and are not scored here.",
      "evidence": ["academy/case-studies/official-map-001.md#7-environmental-storytelling"]
    },
    {
      "area": "landmarks",
      "score": 4,
      "confidence": "medium",
      "rationale": "The animated flame (EV001) and central rug provide two clear, distinct re-orientation cues appropriate to the room's small scale; no additional landmark exists, which is adequate rather than a gap given the room's size.",
      "evidence": ["academy/case-studies/official-map-001.md#5-landmarks"]
    },
    {
      "area": "navigation",
      "score": 4,
      "confidence": "high",
      "rationale": "The enumerated walkable-tile set forms a single connected loop from spawn through every browse cluster back to the exit, with no isolated pocket - directly supports wayfinding.",
      "evidence": ["academy/case-studies/official-map-001.md#6-passability", "TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"]
    },
    {
      "area": "atmosphere",
      "score": 4,
      "confidence": "medium",
      "rationale": "Documented density gradient (dense wall and side clusters, medium central display, sparse walking lane) plus one animated decorative detail (flame) together read as a stocked, inhabited room without gameplay logic - matches shop.pattern.md's rhythm rule.",
      "evidence": ["TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"]
    },
    {
      "area": "project_identity",
      "score": 5,
      "confidence": "high",
      "rationale": "This map's composition matches PAT-INTERIOR-SHOP's own Composition Rules by definition, since that pattern was derived directly from this same map. This score confirms internal consistency, not independent corroboration - it must not be read as a second source validating the pattern's confidence tier, per academy/composition-validator.md's Relationship to academy/grading-system.md section and PATTERN_CONFIDENCE_MODEL.md's two-source bar.",
      "evidence": ["studio/design-patterns/interiors/shop.pattern.md"]
    }
  ],
  "overall_composition_summary": "Map021's composition is strong and internally coherent: bilateral symmetry, purpose-driven furniture clustering, and a clean single-loop navigable path together produce a room that reads immediately as a small, stocked shop. The one caveat worth naming explicitly is that this review cannot independently corroborate PAT-INTERIOR-SHOP, since the pattern and this review share the same single source map - a genuinely independent test of this composition's rules would require scoring a different map built to the same pattern.",
  "notes": "Worked example only, built entirely from academy/case-studies/official-map-001.md and TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md - no new map inspection was performed, per reports/academy/composition-validator-design.md."
}
```

This example was checked against `schemas/composition-review.schema.json` (required fields, `additionalProperties: false`, enums including all ten `area` values present exactly once, numeric bounds) before inclusion and passes.

## What Choosing an Already-Patterned Map Costs This Worked Example

Unlike `WO-2005`'s Map026 worked example (a rejected build with no governing pattern derived from it), Map021 is the *source* of its own governing pattern. This makes nine of the ten area scores genuinely informative but makes the tenth (`project_identity`) close to tautological, as the record's own rationale states directly. A future Composition Review against a map that merely *cites* `PAT-INTERIOR-SHOP` (an Ashford shop build, for instance, once one exists and is playtested) would give `project_identity` real diagnostic power this worked example cannot demonstrate. This is recorded as a finding for future Academy work, not resolved here.

## Recommendations for Future Academy Work

- The strongest next Composition Review candidate is a map that cites an existing pattern without being that pattern's own source - this would test `project_identity` non-circularly for the first time.
- Once `academy/grading-system.md`'s `composition` category is next exercised on a real target, it should cite a Composition Review's `overall_composition_summary` directly rather than re-deriving a verdict from raw evidence, per `academy/composition-validator.md`'s stated relationship between the two documents.

## Constraints Observed

- Documentation and schema only. No implementation, no map editing.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified; `item-shop-analysis.md` was read only.
- No existing Design Pattern, `academy/composition-analysis.md`, `composition-rubric.md`, or `academy/grading-system.md` was modified.
- No map was created, edited, or generated.

## References

- `academy/composition-validator.md`, `scoring-model.md`
- `schemas/composition-review.schema.json`
- `academy/case-studies/official-map-001.md`
- `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md` (read-only)
- `studio/design-patterns/interiors/shop.pattern.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `academy/grading-system.md`, `grading-rubric.md`, `composition-analysis.md`, `composition-rubric.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- Created by `work-orders/WO-2008-composition-validator.md`

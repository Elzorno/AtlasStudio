# Ashford Inn Revisit - Level 3 Diagnosis

## Status

Filed 2026-07-09. Level 3 diagnosis (`academy/curriculum.md`), first real entry under `academy/reports/` per that directory's own README - the first case study filed since `academy/README.md` and `academy/reports/README.md` were created empty by `WO-2000`.

## Scope

This is the concrete next step `reports/academy/composition-analysis-framework.md` (`WO-2002`) and `reports/academy/map-grading-system.md` (`WO-2005`) both named and left undone: a real Level 1 observation record for `data/Map026.json` (`TheLastSwordProtocol-Game`'s rejected Ashford Inn interior build), followed by a re-grade compared against the worked example those reports produced from the rejection reason alone.

Two new filed records back this report:

- `academy/observations/OBS-ASHFORDINN-001.json` - the observation record.
- `academy/grades/GRD-ASHFORDINN-002.json` - the re-grade, compared against `GRD-ASHFORDINN-001` (`reports/academy/map-grading-system.md`).

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. `data/Map026.json` remains `hand-authored`/protected and was read-only, as were `data/Tilesets.json` and the tileset images `img/tilesets/Inside_B.png` and `img/tilesets/Inside_A5.png`.

## What Changed Since GRD-ASHFORDINN-001

`GRD-ASHFORDINN-001` was produced entirely from `map_ownership.json`'s one-line rejection reason ("interior tiles are incorrect; rocks appear in the room; sofa/furniture rendering is poor") and each category's governing document - explicitly, deliberately, without inspecting `Map026.json` itself, per this Academy series' established discipline of not performing new analysis outside a proper observation record.

`OBS-ASHFORDINN-001` is that proper observation record. It inspects `Map026.json`'s actual tile data, cross-references `Tilesets.json`, and visually confirms specific tile-sheet regions against `Inside_B.png`/`Inside_A5.png` directly (coordinates, not guesses). Three concrete, tile-ID-level findings result:

### Finding 1: A truncated fireplace

`Inside_B.png` rows 7-8, columns 13-15 form one continuous fireplace/hearth graphic - a pediment spanning all three columns, with a pillar at each end (columns 13 and 15). Map026 places only tile IDs from columns 14-15 at map tiles (8,2)-(9,3). Column 13 (the object's left pillar) is never placed anywhere on this map. The rendered result is a fireplace missing its left pillar - asymmetric and structurally incomplete, not the polished landmark IMP-HOM-020 calls for ("a warm-stone vent or small hearth, echoing Ashford's established village motif").

### Finding 2: Three mismatched, incomplete bed placements

`Inside_B.png` row 5 (bed) / row 6 (curtain) contains several visually distinct bed styles as separate single-column graphics, each normally paired with a matching shelf tile above (row 4) and side-table tile below (row 7). Map026 uses three different styles - column 8 (a blue-curtained bed), columns 9-10 (a cream-and-orange-striped bed), and columns 11-12 (a gray tarp-covered bed) - placed immediately adjacent to each other at (2,4)-(2,5), (5,4)-(6,5), and (11,4)-(12,5), and none of the three uses its matching shelf or table tile. IMP-HOM-020 asks for "two to three bed alcoves... suggesting private rooms beyond" - three is within that count, but three different, individually-incomplete bed styles placed side by side reads as a mismatched furniture pile, not alcoves suggesting private rooms.

### Finding 3: Wall art placed at floor level

`Inside_B.png` row 1 contains wall-mounted picture-frame graphics (a world-map chart, a landscape painting, a portrait), normally paired with a cabinet/dresser tile below (row 2). Map026 places the picture-frame tiles alone on the map's upper layer at y=7, x=6-10, with no cabinet tile beneath them at y=8. The result is wall art rendered at floor height with nothing to sit on or hang from.

### What did not change

`OBS-ASHFORDINN-001` found no tile ID, on any layer this map uses, that corresponds to a rock, stone-debris, or rubble graphic on either sheet this map draws from (`Inside_B.png`, `Inside_A5.png`), and no event uses a rock-like character graphic. The rejection reason's specific "rocks appear in the room" claim is **not corroborated** by this pass. This is stated as an open finding, not resolved by inference - see Open Question below.

The tileset family assignment itself (`tilesetId: 3`, `Inside`) is confirmed correct against `Tilesets.json` and matches IMP-HOM-020's requirement. `GRD-ASHFORDINN-001`'s "wrong tileset family" hypothesis under `project_fit` is not supported and is retracted in `GRD-ASHFORDINN-002`.

## Grade Comparison

| Category | GRD-001 (rejection-text only) | GRD-002 (with OBS-ASHFORDINN-001) | Why |
|---|---|---|---|
| composition | 2, low | 2, medium | Same score, stronger grounding: three concrete tile-level defects instead of one ambiguous word ("rendering"). |
| traffic_flow | insufficient_evidence | insufficient_evidence | Unchanged - no metrics pass performed. |
| readability | insufficient_evidence | insufficient_evidence | Unchanged - no wayfinding data gathered. |
| visual_hierarchy | insufficient_evidence | 2, medium | Now scoreable: the truncated fireplace undermines the intended focal point named by IMP-HOM-020. The old "rocks as focal element" speculation is retracted. |
| passability | insufficient_evidence | insufficient_evidence | Unchanged, but now with a partial positive signal (6 blocker events at furniture edges) noted rather than no evidence at all. |
| environmental_storytelling | 2, medium | 3, medium | Raised: the required hearth element is present and functional (the `!Flame` event), even though its tile graphic is truncated - a mixed finding, not a pure failure. The "rocks undermine tone" reasoning is retracted. |
| project_fit | 2, medium | 3, medium | Raised: tileset family and required-element count are both confirmed correct. The remaining deviation is execution quality, now captured under `rpg_maker_quality` instead of counted here too. |
| rpg_maker_quality | 2, high | 2, high | Same score, same confidence, now backed by three named, coordinate-anchored defects instead of a paraphrase of the rejection text. |
| dragon_quest_exploration_feel | insufficient_evidence | insufficient_evidence | Unchanged - not addressed by a single-room observation pass. |
| **outcome** | rejected | rejected | Unchanged - nothing was fixed. This pass re-diagnoses the same rejected build, it does not remediate it. |
| **remediation_tags** | `needs_art_direction` | `needs_art_direction` | Unchanged. |

## Open Question: "Rocks"

`OBS-ASHFORDINN-001` could not locate any rock, stone-debris, or rubble graphic anywhere in Map026's tile data or event list. Three possibilities, none confirmed:

1. The human reviewer used "rocks" informally to describe the visually broken/disjointed furniture fragments (Findings 1-2) - fragments can read as debris when small.
2. Something about the rendered appearance (autotile assembly, lighting, or a screenshot the reviewer saw) differs from what static tile-ID inspection can determine - this map has no rendered screenshot on file, unlike Map001/Map002 (`academy/rendering-pipeline.md`, `WO-2010`).
3. The reviewer's note used shorthand for something this pass's category coverage does not reach.

This is recorded as unresolved, per this Academy series' discipline against guessing. Resolving it would need either the original reviewer's clarification or a rendered screenshot of Map026 to compare against - the latter is a concrete, low-cost follow-up (`rpgmakerLSP`'s render pipeline, per `WO-2010`'s precedent with Map001/Map002) this report recommends but does not perform.

## Systemic Finding

This map's three concrete defects (Findings 1-3) are all instances of the same failure mode: a multi-tile tileset object (fireplace, bed-plus-shelf-plus-table kit, picture-frame-plus-cabinet kit) used incompletely - some but not all of its paired tiles placed. This is a structural, tile-ID-level fact, checkable directly from the map JSON and the tileset's own geometry (`id = row * 16 + col`), without needing a rendered image or human judgment. Per `academy/grading-rubric.md`'s eligibility criterion that a systemic finding be cross-filed rather than kept only inside the case study, this is now recorded in `studio/governance/production-readiness.md`'s Near-Term backlog: run an Academy Level 1 pass *before* a build goes to human review, not only after a rejection, since this exact class of defect is catchable at zero cost beyond the pass itself.

## Constraints Observed

- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. `data/Map026.json`, `data/Tilesets.json`, `img/tilesets/Inside_B.png`, and `img/tilesets/Inside_A5.png` were read only.
- No Design Pattern document was modified or created.
- No map was created or edited.
- `studio/governance/production-readiness.md` received one new Near-Term backlog bullet (see Systemic Finding above); no other line in that document was changed.

## References

- `academy/observations/OBS-ASHFORDINN-001.json`, `academy/grades/GRD-ASHFORDINN-002.json`
- `reports/academy/map-grading-system.md` (`GRD-ASHFORDINN-001`, the prior worked example)
- `reports/academy/composition-analysis-framework.md` (the earlier, narrower composition-only pass over the same rejection)
- `TheLastSwordProtocol-Game/map_ownership.json`, `data/Map026.json`, `data/Tilesets.json`
- `TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `studio/governance/production-readiness.md` (Near-Term backlog, new bullet)
- `academy/grading-rubric.md`, `academy/grading-system.md`, `schemas/academy-observation.schema.json`, `schemas/academy-map-grade.schema.json`

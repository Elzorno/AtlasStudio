# Official Map Study 001: Item Shop (Map021)

Status: submitted

Filled from `academy/templates/map-study-template.md`, per `work-orders/WO-2007-official-rpgmaker-corpus-study.md`. Studies exactly one official RPG Maker MZ sample map, as required; does not attempt the full corpus.

## Evidence Basis

This study performs **no new map inspection**. It is built entirely from two already-verified, already-cited sources: `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md` (the original reverse-engineering pass against `data/Map021.json`) and `studio/design-patterns/interiors/shop.pattern.md` (`PAT-INTERIOR-SHOP`, `WO-0024`, the pattern already derived from that same map). Map021 is chosen as the first official-map study specifically because it is the most thoroughly documented single official sample already on file - it also underlies `academy/observation-model.md`'s worked example `OBS-ITEMSHOP-001` (`WO-2001`) - which lets this study establish the review methodology (this work order's actual objective) without re-deriving facts a prior, correct pass already established.

Map identity: `TheLastSwordProtocol-Game/data/Map021.json`, map tree name "Item Shop," tileset `Inside` (`tilesetId: 3`), 17x13 tiles, RPG Maker MZ official sample project.

## 1. Observation

- Door placement: centered on the bottom axis at x8, using a stairs/threshold tile at `(8,10)` and a floor/door tile at `(8,11)` carrying the exit transfer event. **[Observed Fact]**
- Player spawn: inferred `(8,10)`, one tile inside the doorway - labeled inferred because no explicit spawn-position field was found; the inference rests on the sibling Village 1 interiors' shared centered-bottom-door convention. **[Inference]**
- Playable architectural shell occupies roughly x4-x12, y1-y11, inside the full 17x13 map bounds; the remainder is void/darkness. **[Observed Fact]**
- Counter/display placement: a 3-tile horizontal display at `(7,5)`-`(9,5)`, an L-shaped left display around `(5,6)`-`(6,8)`, an L-shaped right display around `(10,8)`-`(11,6)`. **[Observed Fact]**
- Shelf placement: back-wall clusters at `(5,3)`-`(6,4)` (left) and `(10,3)`-`(11,4)` (right), terminating cleanly into the wall. **[Observed Fact]**
- No explicit shopkeeper NPC or cabinet object exists; storage is expressed through shelves, crates, table displays, sacks, bottles, baskets, and a jewelry case. **[Observed Fact]**

## 2. Composition

Applying `academy/composition-analysis.md`'s ten topics against the source report's own Composition findings:

| Topic | Verdict | Basis |
|---|---|---|
| Focal point | Holds | Centered entry pulls the eye to the central rug/back-wall flame-and-window cluster. **[Inference]**, grounded in observed door/rug/flame coordinates. |
| Negative space | Holds | Center aisle and rug-area tiles are deliberately open and correspond to the customer path, not leftover filler. **[Inference]** |
| Traffic flow | Holds | Entry -> center aisle -> left/right browse -> return to centerline -> exit; no maze, no hidden path. **[Observed Fact]** (directly stated in source) |
| Sight lines | Holds | Door aligns with central aisle, rug, and back-wall focal cluster - room purpose is visible on entry. **[Inference]** |
| Furniture grouping | Holds | Goods grouped by surface/purpose: left potions/medicine, right baskets/scrolls/jewelry-like items, back-wall shelves/crates. **[Observed Fact]** |
| Room zones | Holds | Entry threshold, center aisle, browse loop, wall stock, and focal back wall are each distinguishable. **[Inference]**, grounded in observed coordinate clusters. |
| Entry readability | Holds | Threshold tile plus transfer event plus one-tile spawn offset makes entry/exit unambiguous. **[Observed Fact]** |
| Visual hierarchy | Holds | Bilateral organization around x8; door, aisle, rug, and back wall on or near centerline; side clusters counterbalance without exact mirroring. **[Observed Fact]** for the coordinate symmetry; **[Inference]** for "reads as balanced." |
| Decoration balance | Holds | Density gradient: dense wall/side clusters, medium central display, sparse walking lane. **[Observed Fact]** |
| Environmental storytelling | See Section 7 below | Deferred to its own section per this template's structure. |

This is the first time `academy/composition-rubric.md`'s Holds/Gap/N/A form has been applied to an **accepted-pattern-source** map rather than a rejected build (contrast `academy/composition-rubric.md`'s own Map026 worked example, which is a Gap-heavy rejected case). Every topic here reads Holds, which is expected: this map is the corroborating source of `shop.pattern.md`'s Composition Rules, so checking the map against a pattern derived from itself is close to circular and is recorded honestly as such - this section demonstrates the review method, it does not independently validate the pattern.

## 3. Traffic Flow

Entrance `(8,11)` to focal zone (central rug, roughly row 5-6): approximately 4-5 tiles of vertical travel from spawn `(8,10)` to the rug's near edge at row 6. **[Inference from stated coordinates]** - not a pathfinding-verified distance, since no new inspection was performed.

Aisle width varies by zone: the door/centerline is single-file (1 tile wide, e.g. `(8,10)`, `(8,9)`), while the open browse rows widen to 5 tiles (`(6,7)`-`(10,7)`, `(6,6)`-`(10,6)`). This range - narrow at the threshold, wide in the browse loop - matches `shop.pattern.md`'s Layout Rule to "maintain at least a one-tile-wide customer lane... widen to two-plus tiles where the lane branches into a browsing loop." **[Observed Fact]** for the coordinate spans; the width figures themselves are direct counts from the source report's own enumerated tile list.

## 4. Negative Space

The source report states outer darkness consumes 122 of the map's 221 total tiles, but that darkness sits entirely outside the architectural shell and is not counted as in-room negative space. **[Observed Fact]** Within the shell, the source report states plainly that open tiles correspond to the customer path rather than unused filler - "the negative space is not empty filler; it is the customer path." **[Observed Fact]**, directly quoted from the source's own Composition section.

## 5. Landmarks

- The animated `!Flame` event (`EV001`, `(7,2)`) is the map's only dynamic visual element and sits at the back-wall focal cluster - the clearest re-orientation cue in the room. **[Observed Fact]**
- The central rug (`A2 Rug C`, `(7,5)`-`(9,6)`) is a static floor-accent landmark marking the browse/focal zone. **[Observed Fact]**
- No other landmark-grade element (no statue, no unique prop, no NPC) exists in this interior; it is a small enough space that the flame and rug alone are sufficient for orientation. **[Inference]**

## 6. Passability

Reachable tile set, as enumerated in the source report (not independently re-verified against raw tile collision data in this study - see the Metrics caveat below): door/centerline `(8,11)`, `(8,10)`, `(8,9)`; lower display approach `(7,8)`-`(9,8)`; middle aisle `(6,7)`-`(10,7)`; upper aisle `(6,6)`-`(10,6)`; side approaches `(5,5)`, `(6,5)`, `(10,5)`, `(11,5)`. **[Observed Fact]**, as reported.

Reachability ring: every display cluster checked in the source report (shelves, table displays, side clusters) has at least one adjacent reachable tile; back-wall stock behind the shelves is deep and unreachable, and is treated as visual mass rather than a broken interactable, per `shop.pattern.md`'s own reachability-ring rule. **[Observed Fact]**

Transfer events: exactly one, `EV002` at `(8,11)`, player-touch trigger, `Move1` sound, transfer to map 2 at `(20,15)`. No incoming transfer to this map exists in current project data. **[Observed Fact]**

Region/encounter data: region ID 0 across the map (per the broader corpus review, `reports/design-patterns/interior-pattern-corpus-review.md`) - zero encounters, consistent across the whole official interior corpus, not unique to this map. **[Observed Fact]**

## 7. Environmental Storytelling

- **What happens here?** Retail browsing - the room reads as a small general/item shop through its display and shelf arrangement, without a shopkeeper event confirming commerce mechanically. **[Inference]**
- **Who controls it?** Unstated by the map itself - no NPC or ownership marker exists. **[Observed Fact: absent]**
- **What is allowed here?** Public browsing is implied by the open, easily reachable aisle; the back-wall stock (deep, unreachable) implies restricted/staff-only handling by spatial logic alone. **[Inference]**
- **What changed recently?** No evidence either way - the map carries no wear, damage, or narrative-state markers. `insufficient_evidence`.

This section illustrates a limit worth naming for future studies: an official sample map, built to teach spatial composition rather than narrative state, will often answer only two of these four questions with any confidence. That is not a flaw in the map; it is a scope boundary this template should expect for atmosphere-first samples, distinct from a narrative-heavy project map.

## 8. Metrics

All values below are approximations derived from the source report's own stated coordinate lists, not a fresh tile-by-tile recount against `data/Map021.json`. Per `academy/map-metrics.md`'s Source Discipline, each is flagged as heuristic in prose rather than filed as a formal metrics record.

| Metric | Value | Basis |
|---|---|---|
| Walkable percentage (of full 17x13 = 221 tile map) | ~9% (20 of 221 enumerated reachable tiles) | Heuristic - the 20-tile reachable list in the source report is described as "a compact browse loop," not stated to be an exhaustive walkability recount, so this is a lower bound, not a verified figure. |
| Walkable percentage (of ~99-tile interior shell) | ~20% (20 of ~99) | Same caveat; shell size itself is approximate ("roughly x4-x12, y1-y11" per source). |
| Average aisle width | 1 tile (threshold) to 5 tiles (open browse rows) | Direct count from enumerated tile spans; range, not a single average, since no full tile grid was recounted. |
| NPC density | 0 per 100 walkable tiles | Exact - zero NPC events is a direct, confirmed fact, not an estimate. |
| Event count | 2 total (1 decorative, 1 transfer) | Exact, directly stated in source. |
| Decoration density (objects per 100 walkable tiles) | `insufficient_evidence` | Source report describes density qualitatively ("dense... medium... sparse") but does not give a discrete object count suitable for this metric. |
| Room utilization (% of shell in an identifiable function zone) | `insufficient_evidence` (qualitatively high) | Source report implies most of the shell is functionally zoned, but gives no floor-area percentage. |

## 9. Lessons Learned

- This map is the direct, sole source (`observed_maps`, confidence `medium`) of `studio/design-patterns/interiors/shop.pattern.md` (`PAT-INTERIOR-SHOP`). This study corroborates that pattern's existing Layout, Composition, and Passability Rules against the same source they were already derived from - it does not add a second independent source, so it does not change `shop.pattern.md`'s confidence tier. A genuine confidence-tier change would need a *different* map (a second official sample or an accepted project build), per `PATTERN_CONFIDENCE_MODEL.md`'s two-source bar - this is the same caveat already recorded in `reports/design-patterns/interior-pattern-corpus-review.md`'s confidence review section.
- The clearest transferable finding for the **review methodology itself** (this work order's actual objective, not a new design finding): a single-map study is fastest and most reliable when a prior extraction report and a derived pattern document already exist, because the study becomes a structured re-application of already-verified facts rather than new inspection. Where neither exists yet, "Evidence Basis" above would instead have to state a first-pass direct inspection, and every `[Observed Fact]` tag would carry the added burden of being a first citation rather than a confirmed one.
- The Environmental Storytelling section's two-of-four-questions limit (Section 7) is itself a reusable methodology finding: this template should not treat an unanswered silent question as a defect in an atmosphere-first official sample map.

## Non-Goals

- Does not propose a change to `shop.pattern.md` or any other Design Pattern.
- Does not generate or modify any map.
- Does not modify `TheLastSwordProtocol-Game` or `TheLastSwordProtocol-Atlas`.

## References

- `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md` (read-only)
- `studio/design-patterns/interiors/shop.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `academy/templates/map-study-template.md`
- `academy/composition-analysis.md`, `composition-rubric.md`, `map-metrics.md`, `observation-model.md`
- `academy/knowledge/observation-rules.md`, `composition-rules.md`
- `bridges/rpg-maker-mz/passability-rule.md`
- `reports/academy/official-corpus-methodology.md`
- Created by `work-orders/WO-2007-official-rpgmaker-corpus-study.md`

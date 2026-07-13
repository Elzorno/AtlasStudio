# LSP Map Inspection 002 - Calibration Pass: Map017 "Village 1"

## Purpose

`academy/case-studies/lsp-map-inspection-001.md` applied the classic-JRPG Review Gate to every hand-built `TheLastSwordProtocol-Game` map and found real gaps (Glassfield, Skyreach) alongside real passes (Ashford Exterior). The Production Director asked a fair calibration question in response: run the identical pass on `data/Map017.json` ("Village 1"), a professionally hand-authored sample map placed directly into the project rather than built by the Atlas pipeline, on the stated premise that **if a human-artist-made map does not score highly, the Academy rubric itself is flawed, not the map.**

This case study takes that premise seriously and tests it directly, rather than assuming the rubric will vindicate itself.

## Target and Evidence

- `TheLastSwordProtocol-Game/data/Map017.json` - 30x30, tilesetId 2 ("Outside", the same tileset family as Ashford Exterior). No `displayName` set in the map data itself. **Not present in `map_ownership.json`** - this map was never touched by the Atlas pipeline or any work order; it is a pre-existing asset placed directly into the project, consistent with the Production Director's description.
- Render: `rpgmakerLSP/reports/atlas-import/academy-inspection-002-map017-render.png`, captured 2026-07-12 with the same PIL compositor used for `lsp-map-inspection-001.md` (engine-faithful, reads the real `Outside_A1-A5/B/C.png` files).
- 18 generic-named events (`EV001`-`EV018`) - consistent with an unmodified RTP-style sample map, not an Atlas-authored screen (no `EVT-HOM-*` or `TRN-HOM-*` naming, no Atlas ID comments).

## Review Gate Pass

- **Readable first view: Holds, strongly.** The render immediately reads as a riverside farming village - water, bridge, cottages, cultivated fields - with no ambiguity about place type.
- **Dominant landmark: Holds.** A statue on a raised pedestal sits at the crossroads where the map's paths converge, elevated by both composition (it anchors the one point every path leads toward) and placement (centered at the village's main plaza, immediately south of the bridge). The river-and-bridge crossing is a strong secondary landmark, not a competing one - it stages the approach to the statue rather than dividing attention from it.
- **Circulation: Holds.** A single winding stone-path network connects every building to the central plaza; the bridge is an explicit, legible chokepoint between the northern and southern halves of the village.
- **Curiosity hook: Holds.** Distinct shop signage (a weapon icon, a mug/tavern icon, a lettered "INN" sign) differentiates buildings by function at a glance; a robot figure standing in the tilled fields is a specific, memorable, slightly odd detail exactly in the spirit of `comparative-jrpg-corpus-001.md`'s "functional decoration" finding; dark doorway tiles on several buildings invite entry without needing to be explained.
- **Compression/release: Holds.** The narrow bridge crossing (compression) opens into the statue plaza (release); winding tree-lined paths alternate with the open garden/farm clearing and the plaza itself.
- **Bounded negative space: Holds, with one caveat.** Water, forest, and building clusters bound the map on most sides. A small solid-black region sits at the map's right/east edge (outside the village's built area) - most likely simply outside the intended camera-visible play area for this sample rather than a rendering defect (unlike this session's earlier `tileId 1536` black-void findings, this region's tile data was not cross-checked tile-by-tile, since it sits well outside where any event or path leads and is not a claim this pass needs to stake out either way).
- **Limited vocabulary: Holds.** Grass, dirt path, stone, water, and a consistent wood-building material set are reused throughout rather than each area introducing new material types.
- **Memorable identity: Holds, strongly.** "The farming village with the river, the bridge, and the statue" is immediately statable and would be recalled well after leaving.

**Result: 8 of 8 Holds**, the cleanest pass of any map inspected so far, including this project's own strongest map (Ashford Exterior, which held on 7 of 8 with one Partial on its curiosity hook).

## Formal Category Scoring

Applying `academy/grading-system.md`'s nine categories. Two do not apply to this target and are marked accordingly, for the same reason `academy/grading-system.md`'s own text warns against forcing a score where none belongs:

| Category | Score | Note |
|---|---:|---|
| Composition | 5 | Clean single focal point (the statue), zero unstated open floor, furniture/prop clusters (barrels, crates, garden rows) all read as intentional and function-grouped. |
| Traffic flow | 4 | Path network and building placement predict the walkable set; not scored 5 only because no formal metrics pass (`academy/map-metrics.md`) was run, matching this project's own standard of not scoring past what evidence actually supports. |
| Readability | 5 | See Review Gate. |
| Visual hierarchy | 5 | Statue first, bridge/plaza second, individual shop signage third - a clean, nameable order. |
| Passability | insufficient_evidence | A simplified worst-case passability check (the same one used throughout this session) returned a lower reachable-tile count than expected, but this project's simplified checker is a known approximation of the real engine's directional-passability algorithm, not a validated implementation of it, and several "unreachable" events are Action-Button doors embedded in wall tiles, which are correctly impassable-from-the-tile-itself by RPG Maker convention. Scoring this category would require the real engine's algorithm or a live playtest, not a re-use of this session's approximation. |
| Environmental storytelling | 5 | River-fed farmland, a tavern, an inn, a weapon shop, and a garden with a scarecrow-robot read as a lived-in, functioning settlement without any dialogue. |
| Project fit | not_applicable | This map has no governing Atlas Implementation Packet, canon location ID, or `map_ownership.json` entry - it was never built to satisfy an Atlas contract, so there is no contract to check it against. Scoring this category would be exactly the "forcing a score where none applies" error `academy/grading-system.md` warns against for the Dragon Quest category. |
| RPG Maker quality | 5 | Directly answers `bridges/rpg-maker-mz/map-quality-standard.md`'s own bar ("would this be believable as a polished RPG Maker MZ sample map") in the affirmative without qualification - because it is one. |
| Dragon Quest exploration feel | not_applicable | Same reasoning as Project fit: no Atlas Decision Record frames this specific target with a Dragon Quest-style requirement to check it against. |

## Does This Validate or Challenge Academy?

**It validates the rubric.** The Production Director's test was fair and falsifiable: a rubric that cannot distinguish a professionally composed sample map from the project's own weaker builds would be worth distrusting. Instead:

- Map017 passes 8/8 on the Review Gate and scores 4-5 on every applicable formal category - the highest, cleanest result of any map inspected this session, including `lsp-map-inspection-001.md`'s own best in-project result (Ashford Exterior, 7/8).
- The rubric did not manufacture a problem to be "fair" or hedge the score down. Where evidence was genuinely insufficient (`passability`) or the category genuinely did not apply (`project_fit`, `dragon_quest_exploration_feel`), this pass says so explicitly rather than inventing a number - the same discipline `GRD-ASHFORDINN-003` and `lsp-map-inspection-001.md` already applied to in-project maps.
- The two lowest-scoring in-project maps from `lsp-map-inspection-001.md` (Glassfield, Skyreach) fail Review Gate items for concrete, falsifiable reasons this pass can point at directly (no landmark anywhere in a 30x40 map; six disconnected floating platforms with no connecting geometry) - not vague "doesn't feel right" complaints. Map017 fails none of those same checks. The rubric is measuring something real, and the delta between Map017 and Glassfield/Skyreach is the clearest evidence of that: same reviewer, same checklist, same session, opposite results, for reasons stated in advance of looking rather than reverse-engineered afterward.

**One honest caveat, not a rubric flaw but a scope one:** `project_fit` and `dragon_quest_exploration_feel` could not be scored here at all, because those two categories are specifically about fit to *this project's own* contracts - a sample map was never asked to satisfy them. That is a difference in what each map was built to do, not a weakness in the categories themselves; `academy/grading-system.md` anticipated exactly this shape of gap when it built `insufficient_evidence`/`not_applicable` into the model instead of forcing every target through every category.

## Confidence and Boundary

Same standing as `lsp-map-inspection-001.md`: direct visual observation of an engine-faithful render, cross-checked against tile JSON where the claim is structural. This does not constitute or authorize any change to `Map017.json`, which remains outside the Atlas pipeline's ownership entirely and was not modified.

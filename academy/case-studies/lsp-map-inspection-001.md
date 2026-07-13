# LSP Map Inspection 001 - Applying the Classic-JRPG Corpus to Our Own Builds

## Purpose

`academy/case-studies/comparative-jrpg-corpus-001.md` studied nine external NES/SNES maps and distilled `academy/knowledge/classic-jrpg-feel.md`'s doctrine and Review Gate. This case study turns that doctrine back on `TheLastSwordProtocol-Game`'s own hand-built maps, using engine-faithful renders (a PIL compositor that reads the real tileset PNGs and reproduces `rmmz_core.js`'s `_addAutotile`/`_addNormalTile`/`_addTableEdge` source-rect math) rather than the tile-JSON alone. This is the first time most of these maps have been visually inspected as rendered images at all - several were built and accepted from JSON review and BFS reachability checks without a picture.

The Production Director asked, after this session's Sealed Node work (`WO-0055`), for an inspection pass across all hand-built maps against the new corpus, to see whether scores change.

## Evidence Basis

Engine-faithful renders captured 2026-07-12, working tree of `TheLastSwordProtocol-Game` at base commit `65b381c` plus this session's uncommitted `WO-0054`/`WO-0055` changes:

| Map | File | Render |
|---|---|---|
| Ashford Exterior | `data/Map001.json` | `rpgmakerLSP/reports/atlas-import/academy-inspection-001-map001-render.png` |
| Elara House Interior | `data/Map002.json` | `...-map002-render.png` |
| Ashford Shop Interior | `data/Map003.json` | `...-map003-render.png` |
| Skyreach Hill Path | `data/Map004.json` | `...-map004-render.png` |
| Hidden Cave Entrance | `data/Map005.json` | `...-map005-render.png` |
| Hidden Cave Trials | `data/Map006.json` | `...-map006-render.png` |
| Sword Sanctum | `data/Map007.json` | `...-map007-render.png` |
| Glassfield Ruins Exterior | `data/Map008.json` | `...-map008-render.png` |
| Sealed Node Upper/CorePath/Guardian/RelayCore | `data/Map009-012.json` | `rpgmakerLSP/reports/atlas-import/wo-0055-map009..012-render.png` |
| Rustshore Docks | `data/Map013.json` | `rpgmakerLSP/reports/atlas-import/wo-0054-map013-render.png` |
| Mainland Departure | `data/Map014.json` | `...wo-0054-map014-render.png` |
| Ashford Inn Interior | `data/Map026.json` | `...-map026-render.png` (first render ever captured for this map) |

All images are `engine_faithful_render` type per `academy/rendering-pipeline.md`'s three-category split - reproducible, no camera/lighting variance. The compositor script itself is scratchpad-only (not committed to either repo), consistent with the disposition of the same technique in `wo-0052-hidden-cave-terrain-report.md`.

## Per-Map Review Gate Pass

Applying `academy/knowledge/classic-jrpg-feel.md`'s eight-item Review Gate and `academy/case-studies/comparative-jrpg-corpus-001.md` Section 8's anti-pattern list. Verdicts: **Holds** / **Gap** / **Partial**, matching `academy/composition-rubric.md`'s vocabulary.

### Ashford Exterior (Map001) - Town

- Readable first view: **Holds.** Central stone plaza with a well, two lamp posts, and three buildings (shop, house, barn) is immediately legible as a village square.
- Dominant landmark: **Holds.** The well at the plaza's center, reinforced by the paved-stone silhouette against surrounding grass.
- Circulation: **Holds.** Roads run in clear N-S/E-W spurs off the plaza; buildings face the paved area.
- Curiosity hook: **Partial.** A fenced garden plot with a campfire (west) and a walled farmyard read as points of interest, but neither is strongly staged relative to the plaza.
- Compression/release: **Holds.** Narrow road spurs (fence-lined) alternate with the open plaza and the farmyard enclosure.
- Bounded negative space: **Holds.** A full hedge/tree border encloses the map; open grass reads as edge padding, not wasted interior space.
- Limited vocabulary: **Holds.** Grass, stone paving, hedges, three building shells - a small, consistent set.
- Memorable identity: **Holds.** "The village with the well" is a clean, statable identity.
- Anti-patterns: none of Section 8's list clearly apply. **This is the strongest map in the corpus and a reasonable in-house reference point for what "Holds" looks like.**

### Elara House Interior (Map002) / Ashford Shop Interior (Map003) - Interiors

- Both read cleanly: Elara's House zones a bed nook, kitchen counter, and dining table around the room's perimeter with open floor as circulation, not undefined space. The Shop's counter blocks direct approach to the shopkeeper and goods shelves line both side walls, with a rug marking the customer path - a textbook `composition-rubric.md` Topic 5 (Furniture Grouping, wall-anchored for a shop) pass.
- Dominant landmark: **Holds** for both (bed nook; counter).
- Anti-patterns: none observed. These two interiors read as intentional, inhabited spaces.

### Ashford Inn Interior (Map026) - Interior, previously rejected

See the dedicated re-grade below (`GRD-ASHFORDINN-003`). Summary: the first-ever render corroborates `OBS-ASHFORDINN-001`'s tile-level findings rather than contradicting them - no rock/boulder tile exists anywhere in the data, but the gray, lumpy tarp-style third bed variant is visually easy to mistake for one at a glance (this inspection pass made that exact mistake on first look and had to re-verify against the tile data before writing this line - a useful, falsifiable data point for why "reads as X" claims need tile-level grounding, per this document's own evidence discipline). Composition remains a clear **Gap**: an incomplete fireplace, three mismatched bed styles crowded together, and floor-placed wall art.

### Skyreach Hill Path (Map004) - Outdoor route

- Readable first view: **Partial.** Grass + a winding stone path is legible as "a hill trail," but nothing marks it as "Skyreach" specifically.
- Dominant landmark: **Gap.** No landmark exists anywhere on the render - no shrine, marker stone, overlook, or silhouette change across the entire 30x40 map. Four decorative event markers sit in open grass with no supporting terrain feature.
- Circulation: **Holds** narrowly - the path is the only through-route and is unambiguous.
- Curiosity hook: **Gap.** Nothing beside the path invites a detour or a second look.
- Compression/release: **Gap.** The path is a single, roughly uniform width from end to end - no chamber, overlook, or wide-narrow alternation.
- Bounded negative space: **Partial.** The hedge border bounds the map, but the large grass fields on either side of the path have no stated purpose (`composition-rubric.md` Topic 2 - unstated open floor is a Gap).
- Limited vocabulary / memorable identity: **Gap.** Grass and one path-stone texture only; nothing a player would recall as "Skyreach" afterward.
- Anti-pattern hit directly: **"Long traversal with no landmark, decision, encounter pressure, or changing view."** This is this map's core problem, named almost verbatim by `comparative-jrpg-corpus-001.md` Section 8.

### Glassfield Ruins Exterior (Map008) - Outdoor ruins

- Readable first view: **Gap.** Six disconnected grey stone-paved rectangles float in an open grass field with a wood-fence border. Nothing reads as "ruins" - no rubble, broken walls, pillars, or silhouette suggesting a collapsed structure.
- Dominant landmark: **Gap.** No feature is visually stronger than any other; the six paved rectangles compete equally (the exact "over-decoration"/competing-elements failure `composition-rubric.md` Topic 8 names, inverted - here it's competing *emptiness* rather than competing detail).
- Circulation: **Gap.** With no connecting paths between the paved patches, the intended route across the map is not visually inferable from the render alone (their connectivity may exist in the passability data, but nothing on screen communicates it).
- Curiosity hook, compression/release, limited vocabulary, memorable identity: **Gap**, for the same root reason - this reads as an unfinished placeholder, not an authored ruin field, despite `map_ownership.json` recording it as `hand_authored`.
- Anti-pattern hit: **"Every biome or terrain type appearing in one local area"** (inverted: one bare terrain type standing in for what should be a ruin), and **"modern spaciousness that leaves ... story nodes far apart without experiential purpose."**
- This is the single sharpest score-moving finding in this pass: Glassfield is ledger-accepted (`hand_authored`, no `review_status` caveat) but fails almost every Review Gate item once actually rendered - the same class of gap the Sealed Node ledger entries now explicitly flag for other maps, but undetected here because no render existed until this pass.

### Hidden Cave Entrance / Trials / Sword Sanctum (Maps005-007) - Dungeon

- Readable first view: **Partial.** The render shows a bright orange/red mottled floor (confirmed by direct pixel sampling of `Dungeon_A2.png` - this is the sheet's lava/magma-rock kind, not a neutral stone kind) inside a wood-lattice-fence border. "Lava floor with a wooden fence wall" is an internally inconsistent material pairing for a stone cave - the fence reads as a garden trellis, not rock.
- Dominant landmark: **Gap** on Map005/Map006 (undifferentiated colored floor throughout, no chamber-defining feature visible in the render); **Partial** on Map007 (Sword Sanctum's single enclosed chamber at least reads as a distinct destination by virtue of being smaller and enclosed, even without a rendered pedestal - the Sword Pedestal is an event, not a tile feature, so it is invisible to a tile-only render).
- Compression/release: **Partial.** Map006's cross-shaped hall does vary width (the anti-pattern corpus praises exactly this kind of chamber/connector alternation), but the material choice undercuts the read.
- Anti-pattern note: this is not a new problem introduced by this session - Maps005-007 predate `WO-0054`/`WO-0055` and were accepted (`data_audit_passed_pending_human_playtest`) without a render. This pass is the first time the lava-floor/fence-wall material mismatch has been visible to anyone.

### Sealed Node Upper / Core Path / Guardian / Relay Core (Maps009-012) - Dungeon, this session's `WO-0055`

- Readable first view: **Holds** narrowly - stone floor, dark brick/metal walls read clearly as "sealed stone chamber," a correct material read (unlike Hidden Cave).
- Dominant landmark: **Gap** on all four. `WO-0055`'s own report already flagged this: "all four rooms are a uniform stone-floor rectangle with straight corridor notches, not the varied cave-to-machine silhouette the screen specs describe." No room has a visually distinct feature - the Guardian arena and the Relay Core chamber are structurally identical rectangles to the entry corridor.
- Circulation: **Holds** - straightforward, unambiguous.
- Curiosity hook: **Gap.** No side paths, no visible secrets, no material shift toward "old-world infrastructure" (the screen specs' own required visual element - cracked walls, embedded metal/glass, unstable red lights - none of which made it into this pass's terrain, only into the still-unused `SF_Inside_B`/`SF_Inside_C` contact-sheet catalog from `WO-0055`).
- Compression/release: **Gap.** All four rooms are the same width and proportion; nothing compresses before the Guardian fight or releases after it.
- Limited vocabulary: **Holds**, arguably too well - one floor kind and one wall kind across all four maps is legible but monotonous.
- Memorable identity: **Gap.** A player leaving Map011 (Guardian defeated) could not describe anything distinctive about the room beyond "stone room with the boss."
- Anti-pattern hit directly, and self-admitted at build time: **"Dungeons built from one repeated corridor width and interchangeable rooms."** `WO-0055` chose this deliberately as a risk-reduction move after two prior live-editor rejections on this tileset - correct triage at the time (get something that renders correctly at all, first), but the doctrine confirms the next pass on these four maps needs shape/landmark variety, not just correct materials.

### Rustshore Docks (Map013) / Mainland Departure (Map014) - `WO-0054`, this session

- Rustshore: readable first view **Holds** (dock, hut, sea north and south read clearly), dominant landmark **Holds** (the Dockmaster's hut, roofed and walled, is the strongest single feature on any exterior map in this pass), but compression/release is **Gap** - the dock area itself is one large open rectangle with no width variation between the hut, the boat landing, and the lighthouse corner. Curiosity hook is **Partial** - the lighthouse corner is under-detailed relative to its narrative importance (it is represented only by character-sprite events, not terrain).
- Departure: correctly minimal per its own screen spec ("small limited dock and boat transition strip" - a short cutscene corridor is not supposed to carry landmark weight). Review Gate mostly **N/A** here rather than **Gap** - applying the full doctrine to a 10-second transition screen would be forcing a criterion where `composition-rubric.md`'s own "N/A for a single-zone room" allowance applies.

## Cross-Map Findings

1. **The single clearest, most consistent problem across this whole pass is missing or weak dominant landmarks in outdoor/dungeon maps, not tile-technical defects.** Every map this session already caught and fixed a technical defect on (Rustshore, Sealed Node) renders *correctly* now - no black voids, no wrong-tileset garbage. The doctrine's Review Gate catches a different, higher-level problem the render-first technical workflow was never designed to catch: several *already-accepted, technically correct* maps (Skyreach, Glassfield, Hidden Cave's material choice) read as flat or internally inconsistent once actually looked at as a picture, and this is the first time anyone has looked.
2. **Materials-reading is a distinct failure mode from black-void bugs.** Hidden Cave's lava-floor-with-fence-wall pairing is not broken (both tiles are real, intentional, correctly-addressed sheet content) - it is a *readability* problem the JSON-only, reachability-only acceptance process used for Maps005-007 had no way to catch.
3. **Sealed Node's uniform-room choice was the right call under the constraints it was made under** (two prior live-editor rejections on an isolated tileset; correctness-first was the sane triage) but is now the clearest, most explicitly self-diagnosed Gap in the whole corpus for follow-up landmark/shape work.
4. **Ashford Exterior remains the strongest map in the project** and is a reasonable internal reference point for "what Holds looks like" the next time a build claims the classic-JRPG target.

## Did the Scores Change?

Only one map in this project (`Map026`, Ashford Inn) had a prior formal Academy grade (`GRD-ASHFORDINN-002`) to compare against - see `GRD-ASHFORDINN-003` for that direct before/after. For the other thirteen hand-built maps, no formal grade existed before this pass, so there is no numeric score to diff; what changed is that **most of them have never been looked at as a picture until now**, and two (Glassfield, Skyreach) fail the classic-JRPG Review Gate substantially harder than their `hand_authored`/`data_audit_passed` ledger status would suggest. That gap between "passed the checks that exist" and "reads well as a place" is this inspection pass's main finding, independent of any single number.

## Confidence and Boundary

Findings are direct visual observations of engine-faithful renders, cross-checked against the underlying tile JSON where a claim is structural (per `academy/image-analysis.md`'s governing rule and `academy/screenshot-guidelines.md`'s comparison workflow). Verdicts on landmark/identity/curiosity are comparative-doctrine judgments (`low`-to-`medium` confidence per `academy/references/reference-governance.md`'s tiering for `comparative_jrpg_reference`-derived criteria), not RPG Maker construction facts. They do not override passability validation, `atlas.py validate`, or a human playtest, and they do not by themselves authorize any further map edit - per `PLAYTEST_AND_ACCEPTANCE.md`, a human Production Director decision is still required to act on any of them.

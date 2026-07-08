# Screenshot Analysis Pipeline Design - Evidence Report

Status: submitted

Scope: `WO-2010`. Synthesizes the evidence behind `academy/rendering-pipeline.md`, `image-analysis.md`, and `screenshot-guidelines.md`, and demonstrates the design against two real, already-existing engine-faithful renders - `rpgmakerLSP/reports/atlas-import/wo-0036-map001-render.png` and `wo-0035-map002-render.png`. Both images were viewed directly for this report. This report is analysis and evidence, not implementation guidance; it does not modify either rendered image, the maps they depict, or `TheLastSwordProtocol-Atlas`/`TheLastSwordProtocol-Game`.

## Why This Design Starts From Real Precedent, Not a Blank Proposal

`work-orders/WO-2010`'s Objective could be read as asking for a rendering capability this project does not yet have. It already has one: `wo-0036-gate-a-ashford-exterior-production-map.md`'s build report documents an "engine-faithful render" of Map001, generated from real map JSON and tileset data using RPG Maker MZ's own autotile tables, and the same report for `WO-0035` produced an equivalent render of Map002. Designing this pipeline as if no rendering method existed would ignore working, proven capability and risk specifying something incompatible with it. `academy/rendering-pipeline.md` instead specifies what a **committed, reusable** version of that same method would need, and names the one documented gap directly: the render script "ran from the session scratchpad... so it cannot be re-run over the hand-authored map."

## The Reconciliation This Design Required

`studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` already states: "Work from the actual map data file... not from a screenshot or memory of the tileset." Read carelessly, `WO-2010`'s premise ("analyze rendered maps rather than relying only on RPG Maker JSON") could be mistaken for overturning that rule. `academy/image-analysis.md`'s "Governing Boundary" section states explicitly that it does not: the JSON-first rule stands unchanged for every structural fact (tile IDs, passability, event logic, transfers, regions); what this design adds is a narrow, named set of questions - emergent visual read, visual hierarchy, atmosphere, landmark distinctiveness - where an image is a *better* source than a tile-ID list, specifically because those questions are about perception, not data presence. `academy/rendering-pipeline.md` separately reconciles against `bridges/rpg-maker-mz/map-quality-standard.md`'s existing "Image Generation Role" section, keeping AI-generated concept art fully outside this pipeline's evidentiary scope, exactly as that document already requires.

## Worked Example: Two Real Renders, Analyzed Within the Stated Boundary

Both images below are engine-faithful renders (Type: `engine_faithful_render`, per `academy/screenshot-guidelines.md`'s provenance requirement), sourced from `TheLastSwordProtocol-Game/data/Map001.json` and `data/Map002.json` respectively, as documented in `rpgmakerLSP/reports/atlas-import/wo-0036-gate-a-map001-build-report.md` and the equivalent `WO-0035` report. Ownership state at capture: both maps are `hand_authored`, per those same reports.

### `wo-0036-map001-render.png` (Ashford Exterior, Map001)

- **[Observed Fact]** The map shows a cobblestone plaza at the visual center, with a well and two matching lamp-post streetlights placed near its edges, and a vertical stone road extending north from the plaza toward a forest gap.
- **[Observed Fact]** Three buildings are visually distinguished primarily by roof color/pattern: a solid orange-tan roof (bottom, the Elara/Kai house), a multi-color "patchwork" roof (top-middle), and a solid yellow roof (right, the shop).
- **[Inference]** The multi-color patchwork roof reads as visually busier than its two solid-color neighbors when viewed at the same scale - a genuine composition observation about perceived contrast between three buildings that a tile-ID listing alone would not obviously surface, since "patchwork" is an emergent visual property of many individual tile placements, not a single labeled attribute in the JSON. This is exactly the category of finding `academy/image-analysis.md`'s "What an Image Can Support" section names.
- **[Observed Fact]** A dense forest border fully encloses the map on all four sides, with visually clear gaps at the road exits, matching `wo-0036`'s own build-report description of "four readable route openings."
- **Boundary check, per `academy/image-analysis.md`:** this render does not and cannot show whether the forest border is collision-blocking, whether the road tiles are correctly walkable, or whether the well/streetlights carry any event logic - those remain claims only the build report's own BFS collision check and the map's JSON can support, and this image analysis does not assert them.

### `wo-0035-map002-render.png` (Elara/Kai House Interior, Map002)

- **[Observed Fact]** A large, saturated red/pink rug occupies a prominent block near the room's upper-center, larger in proportion to the room than the central rug in `academy/case-studies/official-map-001.md`'s Item Shop study.
- **[Observed Fact]** A bed occupies the lower-left corner; a table with two chairs occupies the lower-right area; a bookshelf and additional storage sit along the top wall; the lower-center third of the room is comparatively open floor.
- **[Inference]** The rug's size and saturation make it the room's strongest visual focal point, more dominant than the bed or table despite the bed presumably being the room's primary domestic furniture - worth flagging as a candidate `visual_hierarchy` finding (per `academy/composition-validator.md`) for a future Composition Review of this map, though this report does not file one, since that is a separate curriculum step this design does not perform on its own.
- **Boundary check:** whether the open lower-center floor is a deliberate negative-space/traffic-flow choice or simply undecorated area cannot be determined from the image alone; that would require the map's JSON-derived walkable-tile data, per `academy/image-analysis.md`'s stated limitation.

## What This Demonstrates

Both worked findings are things a JSON-only reading would either miss entirely (the patchwork roof's emergent visual busyness) or would require substantially more effort to notice (the rug's disproportionate visual dominance, versus a coordinate-only description of "a rug at these tiles"). Both findings also respect the governing boundary: neither claims anything about passability, event logic, or exact tile data the image cannot support. This is the intended shape of an Academy image analysis pass, and both existing renders were sufficient to demonstrate it without requiring any new render to be produced.

## Coverage Check

All seven named Topics are addressed: Rendering and Image provenance (`academy/rendering-pipeline.md`), Screenshot capture and Comparison workflow and Human review and Future AI integration (`academy/screenshot-guidelines.md`), Visual hierarchy (`academy/image-analysis.md`'s "What an Image Can Support," demonstrated directly in the worked example above).

## Constraints Observed

- Documentation only. No image-processing code was written or run; both images were viewed for analysis, not generated, edited, or re-rendered.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified.
- The two cited renders under `rpgmakerLSP/reports/atlas-import/` were read only, not modified.
- No map was created or edited.
- No existing Design Pattern, `academy/composition-analysis.md`, `composition-validator.md`, or `grading-system.md` was modified.

## References

- `academy/rendering-pipeline.md`, `image-analysis.md`, `screenshot-guidelines.md`
- `rpgmakerLSP/reports/atlas-import/wo-0036-map001-render.png`, `wo-0035-map002-render.png` (read-only)
- `rpgmakerLSP/reports/atlas-import/wo-0036-gate-a-ashford-exterior-production-map.md` (read-only, referenced by title in that repo's build report)
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`, `passability-rule.md`
- `academy/composition-analysis.md`, `composition-validator.md`, `case-studies/official-map-001.md`
- Created by `work-orders/WO-2010-screenshot-analysis-pipeline.md`

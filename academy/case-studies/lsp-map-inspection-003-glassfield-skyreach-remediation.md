# LSP Map Inspection 003 - Glassfield and Skyreach Remediation

## Purpose

`lsp-map-inspection-001.md` found Glassfield Ruins Exterior (Map008) and Skyreach Hill Path (Map004) as the two sharpest Review Gate failures among hand-built maps. `lsp-map-inspection-002-calibration-village1.md` validated the rubric against `data/Map017.json`, a professionally hand-authored sample map. The Production Director then set direction plainly: bring the pipeline's own maps up to Map017's detail level. This case study documents that remediation pass on the two worst offenders and re-runs the identical Review Gate to check whether the score actually moved, not just whether the work felt like an improvement.

## What Changed

Both maps kept their existing event positions and (for Skyreach) existing path geometry untouched - this was an additive decoration and, for Glassfield, a connectivity pass, not a redesign from scratch.

**Skyreach Hill Path (Map004)**, Outside tileset (shared with Map017 and Ashford Exterior - low technical risk, direct sampling):
- A standing-stone circle (Outside_C tiles 16-18, the same grey/mossy standing-slab graphics visually identified in Map017's own tileset) at the Geometric Stones / Carved Warning Stones event cluster - the map's first dominant landmark.
- Dark rock dressing around the cave entrance and the west cliff overlook.
- ~24 scattered rocks, grass tufts, bushes, and trees along the path shoulders (never on the path itself - checked programmatically and any collisions removed before rendering), sampled from tile IDs actually used in Map017.

**Glassfield Ruins Exterior (Map008)**, SF Outside tileset (isolated to this one map - same risk profile as Sealed Node's `WO-0055`, so contact-sheet-verified rather than assumed):
- The five surviving disconnected cracked-panel patches, plus the west entry and north exit, connected into one continuous path network using the material already in use (no new floor kind introduced).
- Rubble, metal-debris, cracked-panel, flower, and glow-light decoration placed around each required-visual-element event (half-buried metal ribs, broken concrete ridge, cracked glass panel, sealed lower entrance), sourced from labeled `SF_Outside_B`/`SF_Outside_C` contact sheets rendered and visually inspected before use, not assumed from another tileset.

Both: BFS reachability re-verified after the change (Skyreach 876 open cells, Glassfield 1280, all events reachable/adjacent), `atlas.py validate` clean (0/0), route audit unchanged from the existing project baseline (`found=228 missing=21 warning=9`, no new regressions).

Renders: `rpgmakerLSP/reports/atlas-import/academy-inspection-003-map004-render.png`, `...-map008-render.png`.

## Re-Running the Review Gate

### Skyreach Hill Path - before vs. after

| Criterion | Before (`lsp-map-inspection-001`) | After |
|---|---|---|
| Readable first view | Partial | **Holds** - a stone circle and cave dressing now signal "sacred/forbidden hill," not just "grass with a path." |
| Dominant landmark | **Gap** - nothing on the entire map | **Holds** - the standing-stone circle at the Geometric Stones cluster is a clear, nameable anchor. |
| Curiosity hook | Gap | **Partial** - the stone circle and cave dressing now invite a look; still no side path or hidden item. |
| Compression/release | Gap | **Partial** - the path's existing width variation (already present in the geometry, previously undecorated) now reads as intentional because the wide sections are where the landmark and rock clusters live. |
| Bounded negative space | Partial | **Holds** - the grass shoulders now carry scattered rocks/grass/bush, so open space reads as "hillside," not "unused padding." |
| Limited vocabulary | Holds | Holds (unchanged - still a small, consistent material set). |
| Memorable identity | Gap | **Holds** - "the hill path with the stone circle" is now statable. |

**5 of 8 Holds, 2 Partial, 0 Gap** - up from 1 Holds / 2 Partial / 5 Gap.

### Glassfield Ruins Exterior - before vs. after

| Criterion | Before | After |
|---|---|---|
| Readable first view | **Gap** - six disconnected paved rectangles, nothing read as "ruins" | **Holds** - one connected ruin path threading through rubble, cracked panels, and flowers reads as an actual explorable ruin field. |
| Dominant landmark | Gap | **Partial** - the sealed-entrance dark opening is now a legible destination; no single landmark yet dominates the whole 42x34 field the way Skyreach's stone circle does. |
| Circulation | Gap | **Holds** - the path network is now fully connected end to end; the intended route is visually inferable without cross-checking passability data. |
| Curiosity hook | Gap | **Partial** - rubble/flower/glow clusters invite a look at each required-visual-element location; still no side reward. |
| Compression/release | Gap | **Partial** - the connecting corridors are narrower than the original patches, so a corridor/chamber rhythm now exists, though it wasn't deliberately tuned. |
| Limited vocabulary | Gap | **Holds** - grass, one path material, and a small rubble/flower/light prop set, reused consistently. |
| Memorable identity | Gap | **Partial** - "the connected ruin field with the sealed door" is more statable than before but still thinner than Skyreach's landmark or Map017's statue. |

**2 of 8 Holds, 4 Partial, 1 Partial-landmark** (no remaining flat Gap) - up from 0 Holds / 0 Partial / 8 Gap, the worst score in the original pass.

## Did the Scores Actually Change?

Yes, on both maps, and the delta is falsifiable the same way the original findings were: Skyreach went from zero landmarks anywhere on a 30x40 map to one legible stone-circle anchor; Glassfield went from six disconnected floating platforms to one connected, decorated ruin path. Neither map now reads as Map017-level (no map in this project does yet - Map017 passed 8/8 outright), but neither map fails the gate almost completely anymore either, which is what both did in `lsp-map-inspection-001.md`.

## Honest Remaining Gaps

- Neither map has a landmark as strong as Map017's central statue or Ashford Exterior's plaza-and-well. Glassfield in particular still lacks one dominant anchor across its full 42x34 footprint - the sealed entrance is a destination, not yet a landmark visible from most of the map.
- Glassfield's decoration draws on `SF_Outside_B`/`SF_Outside_C`, files isolated to this one map (same category of risk that took Sealed Node two attempts to get right on `SF_Inside`). This pass used the safer technique from that lesson (contact-sheet first, no cross-tileset assumption) but has not yet had a live-editor human look - the ledger now says so explicitly (`renderer_verified_pending_human_review`), matching Sealed Node's convention rather than claiming plain acceptance.
- Skyreach's compression/release and curiosity hook only reached Partial, not Holds - the path's width variation was inherited from the existing geometry rather than deliberately re-authored around the new landmark, and there is still no side path, hidden item, or second point of interest beyond the stone circle.
- Neither map's `passability` category was formally re-scored past the same simplified BFS approximation used throughout this session; a live playtest remains the actual acceptance gate per `PLAYTEST_AND_ACCEPTANCE.md`.

## Confidence and Boundary

Same standing as prior Academy case studies this session: direct observation of engine-faithful renders, cross-checked against tile JSON where structural. Does not itself authorize acceptance - `map_ownership.json`'s `renderer_verified_pending_human_review` / `data_audit_passed_pending_human_playtest` statuses and a human Production Director decision remain the actual gate.

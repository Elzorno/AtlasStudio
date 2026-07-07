# Ashford Village Map Brief

## Purpose

This brief translates `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md` into concrete map-implementation targets for **WP-03B**, per `bridges/rpg-maker-mz/map-quality-standard.md`'s Map Brief Requirement. It covers the exterior village map and its four interiors. It does not draw a map or specify exact tile IDs - it specifies what Codex must achieve, leaving tile-level execution to implementation.

**Comparable quality target: Official RPG Maker MZ sample maps.**

Concretely, this means the exterior should read like the reference sample project's "Normal Town" and "Village House" maps under `references/rpg-maker-mz-samples/official sample project/` in composition, density, and passability discipline - studied for quality, never copied for content, per WP-03's constraints.

## Reference Study Notes (Composition Benchmarks Only)

From the sample project, studied for scale and structure, not copied:

- The sample "Normal Town" map is 40x40 tiles on an exterior/town tileset. Ashford Village should be **smaller and denser** than this - see Target Dimensions below - because `projects/the-last-sword-protocol/design/exploration-principles.md`'s density rule and the anti-pattern of "giant empty overworlds" both call for a map sized to its actual content (one home, three other buildings, one green), not a generic town-sized canvas.
- The sample interior house/shop maps range roughly 13x11 to 21x18 tiles on a distinct interior tileset. Ashford Village's four interiors should sit in this same order of magnitude.
- Sample NPC events use Action Button trigger and "same as characters" priority with walking animation enabled for a normal, human-scale NPC - the baseline Codex should start from for every named NPC here unless a specific interaction calls for something else (see `ashford-village-event-plan.md`).

## Target Dimensions

| Map | Target Size (tiles) | Tileset Role |
| --- | --- | --- |
| Ashford Village (exterior) | approx. 32x28 to 36x32 | Exterior town/nature tileset |
| Rowan's Cottage (interior) | approx. 13x11 to 15x13 | Interior/house tileset |
| General Store (interior) | approx. 11x9 to 13x11 | Interior/shop tileset |
| Blacksmith (interior) | approx. 11x9 to 13x11 | Interior/shop tileset |
| Inn (interior) | approx. 15x12 to 17x14 | Interior/shop tileset |

**Tileset note:** exact numeric tileset IDs in `TheLastSwordProtocol-Game`'s own `Tilesets.json` have not been verified against this brief - `WP-03-preflight-map-quality-passability` is the designated read-only inspection step for that data and should be completed (or its findings otherwise obtained) before WP-03B assigns concrete tileset IDs. This brief specifies tileset *roles* (exterior vs. interior/house vs. interior/shop), matching the sample project's own separation (its Normal Town map used one tileset; its house and shop interiors shared a second), not specific IDs.

## Visual Goals

- **Ashford Village (exterior):** warm, lived-in, small-scale - a place that reads as home, not a generic RPG town. Should achieve the bible's "comfort, belonging, curiosity" emotional targets (Section 1 of the specification) through composition alone, before any NPC is even reached.
- **Rowan's Cottage:** cozy, cluttered-but-tidy, evidence of two people's lives overlapping (a historian's clutter plus a guardian's practical order) - fireplace, bookshelf, and simple furnishing should read as home on sight.
- **General Store / Blacksmith:** functional, modest, workmanlike - each should look like what it sells (produce/goods crates for the store, forge heat and metal for the blacksmith) without needing a sign to explain itself.
- **Inn:** welcoming, slightly larger and more open than the shops, since it is the village's one space built for outsiders passing through.

## Landmarks

- **Village Green + Well:** the map's visual and social center; the well itself should read as a landmark from any approach within the village.
- **Village Memorial:** a distinct, small monument-scale landmark near the Green - not a full building, but visually distinguishable from ordinary decoration at a glance.
- **Optional Viewpoint:** a spot at the village's edge (near the Blacksmith or the exit path, per the specification) framed so the player's eye is drawn outward toward the coming overworld - at least one overworld landmark silhouette should be composable here even before that overworld map exists in full, per the Journey Principle's "anticipation" requirement.

## Environmental Storytelling

Per the Map Quality Standard's "believable environmental detail" requirement, and grounded in the specification's Section 6/7 interactables and secrets:

- Worn dirt paths connecting the Green to each building, more worn nearest the shops and Green, thinner near the Optional Viewpoint (a path less traveled).
- A small tended garden/flowerbed at Rowan's Cottage (Elara's, per the specification) - the Hidden Herb secret's location.
- Barrels/crates clustered near the General Store and Blacksmith, workmanlike rather than decorative.
- Shop signage at each of the three commercial buildings (General Store, Blacksmith, Inn), each distinct enough to read at a glance.
- The Village Memorial should look old relative to the rest of the village - a detail that rewards a second look, tying into the "history" cybersecurity concept from specification Section 8.

## Composition Notes

- Paths should curve or branch naturally around the Green rather than forming a rigid grid, per the Map Quality Standard's composition guidance.
- Building placement should be irregular, not aligned to a uniform grid - see Road Layout and Building Placement below for required relative positions; exact rotation/facing and minor offset is Codex's discretion.
- Negative space (open grass, garden plots) should be used intentionally as breathing room around the Green and gardens, never as unshaped filler at the map's edges - if a stretch of the map has no path, encounter relevance, or environmental detail, it should be trimmed rather than padded, per `projects/the-last-sword-protocol/design/anti-patterns.md`'s Empty Overworld Maps entry (the same discipline applies at village scale).

## Road Layout And Building Placement Relationships

Restating and making concrete the spatial relationships from the specification's Section 2, for direct map-building use:

- Exactly **one** village exit/entrance connects to the Ashford Vale overworld. No second redundant exit exists in this scope.
- **Rowan's Cottage** sits nearest that exit/entrance, so the opening sequence (wake at home, brief scene, head toward the Green) flows outward without doubling back across the village.
- The **Village Green** (with the well and memorial) sits at the physical center, visually reachable from most points in the village.
- The **General Store** and **Blacksmith** sit near each other, along the main path between the Green and the village's other approach (a "commerce cluster"), not scattered to opposite corners.
- The **Inn** sits nearer the exit toward the overworld than the Green, consistent with its role as a waypoint for travelers.
- The **Optional Viewpoint** sits at the village's outer edge, near the Blacksmith or the exit path, oriented outward toward the overworld.

## Elevation

Ashford Village should use one gentle elevation change - for example, Rowan's Cottage and its garden sitting on slightly raised ground reached by a few steps - consistent with classic small-village staging. No cliffs, multi-tier verticality, or elevation-based puzzles are called for; the Map Quality Standard's elevation guidance exists here to add visual interest and orient the player, not to add traversal complexity, consistent with `anti-patterns.md`'s rejection of puzzle-first gameplay.

## Foliage Density

Moderate, not sparse and not overgrown: enough trees, bushes, and grass texture bordering the map and softening building edges to avoid a bare, boxy feel, without obscuring sightlines to landmarks or paths. Denser near the map's natural edges (framing the playable space), lighter near the Green and paths (keeping the social hub open and legible).

## Decoration Density

Light-to-moderate and purposeful: every placed decoration should trace back to an item in Section 6 or 7 of the specification (barrels, flowers, signs, the memorial) or to a genuine environmental-storytelling beat above (worn paths, forge details). Avoid repeated decoration patterns stamped uniformly across the map, per the Map Quality Standard's explicit prohibition on "sloppy repeated decoration patterns."

## Acceptance Criteria

A completed Ashford Village map set is accepted only when it also satisfies `bridges/rpg-maker-mz/map-quality-standard.md`'s Acceptance section (visually coherent, playable, passability-correct, aligned to the JRPG Design Bible, faithful to this brief, reviewed against the sample-map quality bar) and `bridges/rpg-maker-mz/passability-rule.md`'s Required Validation section (player start passable, all required NPCs/transfers/events reachable, no unintended blocking or walkable terrain). See `ashford-village-implementation-checklist.md` for the concrete, checkable form of these criteria.

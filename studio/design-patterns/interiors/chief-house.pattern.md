---
pattern_id: PAT-INTERIOR-CHIEF-HOUSE
name: Interior Pattern - Chief's House
version: 1.0
category: interior
status: accepted
confidence: medium
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map024.json (RPG Maker MZ official sample project, map tree name 'Chief's House 1F', tileset 'Inside', 20x17)"
  - "TheLastSwordProtocol-Game/data/Map025.json (RPG Maker MZ official sample project, map tree name 'Chief's House 2F', tileset 'Inside', 20x17)"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "studio/design-patterns interior-pattern-corpus extraction, WO-0025 (no standalone report; extraction performed directly against data/Map024.json and data/Map025.json - see reports/design-patterns/interior-pattern-corpus-review.md for the comparative evidence trail)"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - Chief's House v1.0

## Name

A two-floor notable's residence: a symmetric, formal ground-floor hall connected by an internal multi-tile staircase to an upper floor of several small private chambers - the most structurally complex interior in the observed corpus, appropriate to its occupant's elevated narrative status.

## Category

`interior`. Distinct from `house.pattern.md` (ordinary single-room dwelling), `inn.pattern.md` (single-floor, two-zone building), and every other pattern in this corpus by being the only observed **multi-floor** interior, and the only one whose upper floor uses a true multi-room chamber layout rather than one open room.

## Source

Derived from two official RPG Maker MZ sample maps that together form one building: "Chief's House 1F" (`Map024.json`) and "Chief's House 2F" (`Map025.json`), both in the official sample project bundled with the engine, both 20x17 tiles on the `Inside` tileset family. **Evidence caveat:** unlike `house.pattern.md`'s two independent buildings, these two maps are two floors of the *same* structure - they corroborate each other's internal consistency (shared shell size, shared threshold and flame conventions) but do not constitute two independent building samples. Extraction was performed directly against both map JSONs and cross-checked against `Tilesets.json` tileset 3 ("Inside") for `WO-0025`.

## Confidence

**Medium**, with an explicit caveat distinguishing it from an ordinary two-map Medium-to-High case. Per `PATTERN_CONFIDENCE_MODEL.md`, two maps corroborating the same rule would normally support High confidence - but that bar assumes the two maps are *independent* samples. Here, both maps are floors of one building, authored as a matched pair, so agreement between them is expected internal consistency rather than independent corroboration. This pattern is filed at Medium and should be promoted to High only when a genuinely separate second notable's-residence sample (a different building, ideally from a different source) corroborates the same multi-floor, hall-plus-chambers structure.

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map024.json` ("Chief's House 1F") | RPG Maker MZ official sample project | 20x17 shell, one large symmetric formal hall with a centered furniture arrangement, an internal three-tile-wide staircase in a partially walled-off alcove, an interior hearth-style flame near the stair landing plus one top-wall flame, and a near-centered exterior door/threshold. |
| `Map025.json` ("Chief's House 2F") | RPG Maker MZ official sample project | 20x17 shell, no exterior door (upper floor, reached only via the internal staircase), a multi-room chamber layout (several small private rooms connected by a single corridor spine), a matching three-tile-wide staircase down to 1F in the same alcove position, and three decorative flames (two top-wall, one interior). |

## Applicable Genres

`jrpg`, `dragon-quest-style`. Same reasoning as the rest of the corpus. Especially well suited to a named or narratively significant NPC's residence, given its scale and formality relative to `house.pattern.md`.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is a **two-floor building** for a single, narratively significant resident (a village leader, elder, or similarly elevated NPC) - not an ordinary villager's home.
- The ground floor's primary function is a **formal hall** (a gathering/audience space), and the upper floor's primary function is **private chambers**.
- The two floors are connected by an **internal staircase**, not by a separate exterior entrance to each floor.
- The building is reached from a town or village exterior map at ground level only.

If the residence is single-floor, use `house.pattern.md` instead - do not apply this pattern's multi-floor and internal-staircase rules to a single-story building.

## Layout Rules

- Use a larger shell than the ordinary house or shop: both observed floors are 20x17, matching `inn.pattern.md`'s scale rather than the 17x13 shell shared by `shop.pattern.md`, `house.pattern.md`, `weapon-shop.pattern.md`/`armor-shop.pattern.md`, and `bar.pattern.md`. A building meant to read as more important than an ordinary home should scale up accordingly.
- Connect the two floors with an **internal staircase that is wider than a standard exterior doorway** - both observed floors use a three-tile-wide staircase (versus the one-tile-wide threshold used everywhere else in the corpus), placed at the identical position on both floors so the stair reads as a continuous architectural feature when the player moves between them.
- Place the internal staircase in its **own partially walled alcove**, accessible from the main floor via an open connection rather than a narrow single-tile chokepoint - distinct from `inn.pattern.md`'s narrow-corridor zone separation. The observed 1F staircase alcove is walled on three sides with one open edge connecting to the main hall's floor.
- On the ground floor, organize the primary hall **symmetrically around a central axis**, with a formal furniture arrangement (a central feature flanked by matching left/right clusters) - more elaborate and more strictly bilateral than `shop.pattern.md`'s "counterbalancing without mirroring" rule. The observed 1F hall's furniture is close to a true mirror image left-to-right around its centerline.
- On the upper floor, use a **true multi-room chamber layout**: several small private rooms (roughly 3x5 to 3x6 tiles each), separated by internal walls, connected by a single corridor spine rather than one open floor. This is a structurally new convention not seen anywhere else in the corpus, including `inn.pattern.md` (which zones by open-area-plus-partition-rhythm, not by fully walled separate rooms).
- Keep the exterior ground-floor door near, but not necessarily exactly on, the building's horizontal center - the observed 1F door sits close to the map's midpoint, consistent with `shop.pattern.md`'s and `house.pattern.md`'s centering default, unlike `inn.pattern.md`'s and `bar.pattern.md`'s deliberately off-center doors.

## Composition Rules

- Reserve the **most formal, symmetric composition in the corpus** for the ground-floor hall - denser and more mirror-balanced than any single-room pattern, appropriate to a hall meant for gathering or audience rather than private living.
- Use an **interior hearth-style flame** (placed away from the top wall, near a functional feature such as the staircase landing) in addition to the standard top-wall flame convention shared with `shop.pattern.md` and `house.pattern.md`. Both observed floors place at least one flame away from the top wall - this is the corpus's second observed instance of a non-top-wall flame (the first being `inn.pattern.md`'s wall-mounted sconce), but here it reads as a floor-standing hearth rather than a wall sconce.
- Scale flame count with floor complexity rather than floor size alone: the observed 1F (one large hall plus a stair alcove) uses two flames; the observed 2F (several small chambers) uses three, distributed so multiple chambers each get ambient light rather than concentrating them near one feature - consistent with `inn.pattern.md`'s "scale flame count to zones, not room size" finding, now corroborated by a second, structurally different multi-zone building.
- Keep private chamber furniture on the upper floor modest and varied per room rather than uniform - the observed 2F's small chambers each carry distinct, room-specific furniture groupings rather than a repeated unit (unlike `inn.pattern.md`'s guest-quarters wing, which deliberately repeats a near-identical partition rhythm across its bed nooks). A private chamber in this pattern should read as individually furnished; a lodging nook in the inn pattern should read as a repeated module.

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`, extending `shop.pattern.md`'s and `inn.pattern.md`'s rules to a multi-floor case:

- Both floors' staircase tiles function as the inter-floor transfer, using the same player-touch-transfer-plus-stairs-tile convention as an exterior doorway, but repeated across the full three-tile stair width rather than a single tile - verify all three stair tiles carry equivalent transfer events, not just the center one.
- The staircase alcove must be reachable from the main floor's open area on at least one side; it must not be sealed off from the rest of the floor by the partial wall enclosure that gives it its alcove read.
- On the upper floor, each private chamber must be reachable from the connecting corridor spine via at least one open doorway gap - a chamber with no walkable connection to the spine is a dead room and fails route validation.
- The upper floor has **no exterior transfer event** - it is only reachable via the internal staircase from the ground floor. Do not add a second exterior door to the upper floor; that would contradict the observed convention and most buildings' physical logic.
- Route validation for this pattern should confirm, at minimum: `exterior entrance -> ground floor hall`, `ground floor hall -> staircase alcove`, `staircase (1F) -> staircase (2F)`, and `2F corridor spine -> each private chamber`.

## Event Rules

- This pattern governs **residence atmosphere, hall/chamber zoning, and inter-floor connection only** - it does not prescribe the chief/leader NPC's placement, dialogue, or any quest-relevant furniture (a chest, a map table, a seat of office) a specific implementation contract may require. Neither observed floor contains an NPC event.
- Do not assume this pattern's hall automatically implies an occupant NPC event - both observed floors demonstrate a fully furnished, formally composed residence with zero character events, consistent with every other pattern in this corpus.
- The inter-floor staircase must use exactly the same player-touch-transfer-plus-SE convention as an exterior doorway transfer, applied redundantly across all stair tiles rather than a single tile, per Passability Rules above.
- Decorative flame events (top-wall and interior hearth-style alike) remain free of gameplay commands, identical to every other pattern in this corpus.

## Common Mistakes

- Using a single-tile staircase instead of a multi-tile one - this pattern's evidence specifically shows a three-tile-wide internal stair, wider than the standard exterior threshold.
- Treating the upper floor as one open room instead of a true multi-room chamber layout - collapsing it into an open floor loses the structural distinction that makes this pattern's upper floor different from every other pattern in the corpus.
- Adding a second exterior transfer on the upper floor - the observed convention is strictly internal-staircase-only access to the second floor.
- Under-symmetrizing the ground-floor hall - this pattern calls for a stricter bilateral arrangement than `shop.pattern.md`'s looser "counterbalancing without mirroring" rule.
- Treating this pattern's two-source-map evidence as equivalent to `house.pattern.md`'s independent two-building corroboration - both maps here are floors of one building, and the Confidence section above states this caveat explicitly; do not round it up to High without a genuinely independent second sample.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/house.pattern.md` - the single-floor, lower-status counterpart to this pattern; several structural conventions (shell family, no-NPC-by-default, threshold construction) carry over.
- `studio/design-patterns/interiors/inn.pattern.md` - shares this pattern's "scale flame count to zones" finding and offers the closest comparison for multi-zone connection logic, despite using a corridor-chokepoint rather than a true walled multi-room layout.
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence trail across the interior corpus.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Category tier, currently no materialized parent)
- Created by `work-orders/WO-0025-interior-pattern-corpus.md`

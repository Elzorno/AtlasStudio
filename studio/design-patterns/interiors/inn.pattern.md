---
pattern_id: PAT-INTERIOR-INN
name: Interior Pattern - Inn
version: 1.0
category: interior
status: accepted
confidence: medium
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map020.json (RPG Maker MZ official sample project, map tree name 'Inn', tileset 'Inside', 20x17)"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "studio/design-patterns interior-pattern-corpus extraction, WO-0025 (no standalone report; extraction performed directly against data/Map020.json - see reports/design-patterns/interior-pattern-corpus-review.md for the comparative evidence trail)"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - Inn v1.0

## Name

A two-zone lodging interior combining an open common room with a separate, partitioned guest-quarters wing, larger and more structurally divided than a single-room house or shop.

## Category

`interior`. Distinct from `house.pattern.md` and `shop.pattern.md` specifically because it is the first pattern in the corpus that is not a single undivided room - it introduces internal zoning (common room vs. guest quarters) within one building.

## Source

Derived from one official RPG Maker MZ sample map: "Inn" (`Map020.json`), in the official sample project bundled with the engine. The map is 20x17 tiles on the `Inside` tileset family - larger than the 17x13 shell shared by `shop.pattern.md`, `house.pattern.md`, `weapon-shop.pattern.md`/`armor-shop.pattern.md`, and `bar.pattern.md`. Extraction was performed directly against the map JSON and cross-checked against `Tilesets.json` tileset 3 ("Inside") for `WO-0025`; see `reports/design-patterns/interior-pattern-corpus-review.md` for the full comparative evidence.

## Confidence

**Medium.** Corroborated by exactly one official sample map, with no second source on file. Per `PATTERN_CONFIDENCE_MODEL.md`, apply by default but flag as single-source evidence in any build report that uses it. Eligible for promotion to High once a second official sample inn, or one accepted and playtested AtlasStudio inn build, corroborates the zoning, threshold, and event conventions below.

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map020.json` ("Inn") | RPG Maker MZ official sample project | Full extraction: 20x17 shell, two-zone internal structure (open common room + partitioned guest-quarters wing), off-center threshold aligned to the common room's own sub-axis, a narrow shared spine corridor connecting both guest-room clusters, four decorative flames (three wall-mounted, one floor-adjacent), no NPC event. |

## Applicable Genres

`jrpg`, `dragon-quest-style`. Same reasoning as `shop.pattern.md` and `house.pattern.md`.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is **larger than a single small room** and combines at least two functionally distinct zones under one roof (here: a common/gathering area and a lodging area).
- The interior has **exactly one primary exterior entrance/exit**, even though it may contain multiple interior sub-zones.
- The interior's function is **lodging-for-hire or a comparable multi-purpose gathering-plus-private-space building**.
- The interior is reached from a town or village exterior map.

If the building is a genuinely single-room space, use `shop.pattern.md` or `house.pattern.md` instead - this pattern's zoning rules do not apply to an undivided room.

## Layout Rules

- Do not center the exterior door on the full building's bounding box. The observed inn centers its door on the **common room's own sub-axis**, not the midpoint of the full 20-tile-wide shell - the common room is the zone the exterior door actually serves, and it is offset to one side of the building as a whole because the guest-quarters wing occupies the other side. This is a direct, evidence-based refinement of `shop.pattern.md`'s "center the entrance on the room's primary axis" rule: for a multi-zone building, "primary axis" means the axis of the zone the door opens into, not the axis of the whole footprint.
- Divide the building into at least two zones separated by a solid interior wall band, connected by a single narrow spine (in the observed map, a two-tile-wide vertical corridor) rather than one continuous open floor. Do not let the common room and the guest-quarters wing share one undivided open area - the observed inn keeps them structurally separate, with the corridor as the only connection.
- Within the guest-quarters wing, repeat a smaller partitioned unit (a bed/desk nook) side by side along one wall, mirrored above and below the connecting spine if the wing has multiple clusters. The observed inn uses near-identical partition rhythm in its upper and lower guest clusters.
- Keep the exterior threshold construction identical to `shop.pattern.md` and `house.pattern.md`: a stairs-family tile one row above a floor tile carrying the transfer event, but placed in its own small vestibule alcove reached by a single narrow chokepoint from the common room, not opening directly onto the main floor.

## Composition Rules

- Treat the common room and the guest-quarters wing as having **different composition logic**, not a shared one. The common room in the observed map carries lighter, more open furniture (consistent with `bar.pattern.md`'s open-floor gathering convention - see that pattern for the fuller version of this composition logic); the guest wing carries dense, regular, repeated small-furniture partitions (bed/desk nooks), which is a composition style neither `shop.pattern.md` nor `house.pattern.md` uses.
- Use **wall-mounted decorative flames** for zones the player does not walk directly beneath, in addition to the floor-adjacent flame convention already established by `shop.pattern.md` and `house.pattern.md`. The observed inn places a flame directly on a wall tile within the guest wing's dividing wall band, unreachable and clearly a sconce rather than a floor-standing feature - a genuinely new decorative placement not seen in the single-room patterns.
- Scale flame count to the number of zones, not to overall room size alone. The observed inn (four flames across two zones) has more decorative lighting than any single-room pattern in this corpus, distributed so each zone (common room, upper guest cluster, lower/shared wing) gets its own light rather than concentrating all of them near one focal point.

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`, consistent with `shop.pattern.md` and `house.pattern.md`:

- Each zone's walkable area must be reachable from the entrance, but zones may only connect through a single deliberate chokepoint (the spine corridor) rather than a wide open boundary. Verify route validation zone-by-zone: `entrance -> common room`, `common room -> spine corridor`, `spine corridor -> each guest cluster`.
- The exterior threshold's vestibule alcove is a **dead-end reachable only from the common room**, not directly from the guest wing - do not create a shortcut from the guest quarters straight to the exterior door.
- Structural furniture inside guest-room partitions blocks movement the same way shelving does in `shop.pattern.md` and `house.pattern.md` - a bed/desk nook's furniture must not be walked through, and the aisle in front of each nook must remain walkable.
- Wall-mounted decorative flames are, by construction, on a wall tile and are never intended to be walkable or interactable - do not apply the reachability-ring requirement to them the way it applies to floor-standing display objects.

## Event Rules

- This pattern governs **inn atmosphere, zoning, and spatial layout only** - it does not prescribe an innkeeper NPC, a "rest here" interaction, a price, or any Sleep/Recover game system. The observed inn contains zero NPC or interaction events beyond the exterior door transfer.
- Do not assume an inn interior requires an innkeeper NPC or a functioning rest-and-heal event by default - the official sample demonstrates a fully zoned, furnished inn with no such system wired in. If required by the citing contract, the innkeeper's placement (likely near the common room, given that is the only zone with open approach floor) and the rest-interaction event must be specified there.
- Keep decorative/atmosphere flame events free of gameplay commands, identical to `shop.pattern.md` and `house.pattern.md`.
- The exterior entrance/exit uses exactly one player-touch transfer event, identical to the single-room patterns. This pattern does not observe or require any additional transfer event between the inn's own internal zones (common room and guest wing connect by walkable corridor, not by a transfer event).

## Common Mistakes

- Centering the exterior door on the full building footprint instead of on the common room's own sub-axis, producing a door that appears to open into a wall of the guest-quarters wing.
- Connecting the common room and guest-quarters wing with an open boundary instead of a single deliberate corridor chokepoint, collapsing the two-zone read into one undifferentiated room.
- Reusing `shop.pattern.md`'s or `house.pattern.md`'s single-zone composition rules uniformly across the whole inn instead of varying composition by zone.
- Treating the wall-mounted flame convention as universal - it is specific to zones the player does not walk directly under (dividing walls, guest-wing partitions), not a replacement for the floor-adjacent flame convention used elsewhere.
- Assuming this pattern's single-source Medium confidence license a stronger claim than it supports - it has not yet been checked against a second official inn sample.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/shop.pattern.md`, `house.pattern.md` - source of the single-room threshold, spawn, and event conventions this pattern extends to a multi-zone building.
- `studio/design-patterns/interiors/bar.pattern.md` - shares this pattern's open-common-room composition logic.
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence trail across the interior corpus.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Category tier, currently no materialized parent)
- Created by `work-orders/WO-0025-interior-pattern-corpus.md`

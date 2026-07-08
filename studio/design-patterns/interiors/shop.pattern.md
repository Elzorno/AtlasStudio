---
pattern_id: PAT-INTERIOR-SHOP
name: Interior Pattern - Shop
version: 1.0
category: interior
status: accepted
confidence: medium
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map021.json (RPG Maker MZ official sample project, map tree name 'Item Shop', tileset 'Inside', 17x13)"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - Shop v1.0

## Name

A small, single-room retail interior (general store, item shop, apothecary-style shop) that reads as stocked and purposeful within a compact footprint, and gets the player in, oriented, and out without maze-like navigation.

## Category

`interior`. This pattern is scoped to small, single-room commercial interiors specifically - it is not a general "any interior" pattern. A multi-room shop, a shop with a back office, or a market stall in an open exterior square is out of scope (see Required Conditions).

## Source

Derived from one official RPG Maker MZ sample map: the "Item Shop" map (`Map021.json`) in the official sample project bundled with the engine, as reverse-engineered in `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md`. That map is 17x13 tiles on the `Inside` tileset family, with a playable architectural footprint smaller than the full map bounds. This pattern abstracts that report's `Layout`, `Tile Usage`, `Composition`, `Passability`, and `Event Design` findings into reusable rules; it does not reproduce the source map's tile grid, coordinates, or JSON.

## Confidence

**Medium.** This pattern is corroborated by exactly one official sample map, with no second source yet on file. Per `PATTERN_CONFIDENCE_MODEL.md`, apply it by default, but flag it as single-source evidence in any build report that uses it. It is eligible for promotion to High the moment a second official sample map, or one accepted and playtested AtlasStudio shop build, corroborates the same rules (`observed_maps` would then gain a second entry).

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map021.json` ("Item Shop") | RPG Maker MZ official sample project | Full extraction: room shell proportions, doorway/threshold construction, display and shelf placement, walkable-lane structure, decoration density gradient, and event inventory (see `source_report` for full citations). |

## Applicable Genres

`jrpg`, `dragon-quest-style`. This pattern assumes a town-embedded interior the player enters and exits deliberately (per `bridges/rpg-maker-mz/map-quality-standard.md`'s Dragon Quest alignment model), not a screen-chain puzzle room. It has not been checked against action-RPG or screen-chain-heavy genre conventions and should not be assumed to transfer there without a fresh extraction pass.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is a **single room**, not a multi-room shop, shop-plus-back-office, or shop-plus-living-quarters layout.
- The interior has **exactly one primary entrance/exit** shared by both directions of travel.
- The interior's commercial function is **retail browsing**, not a market stall, auction hall, or crafting workshop.
- The interior is reached from a town or village exterior map, not from a dungeon or wilderness screen.

If any of these do not hold, treat this pattern as a starting reference only, and note the deviation explicitly in the citing implementation contract rather than applying the pattern's rules as binding.

## Layout Rules

- Keep the room compact. A small shop interior does not need a large map; a modest full-map footprint with an even smaller playable architectural shell inside it is sufficient and reads as more intentional than an oversized room.
- Center the entrance on the room's primary axis of symmetry unless a specific narrative or spatial reason requires an off-center door.
- Place the player's spawn point one tile inside the doorway on entry - not deep inside the room. This gives immediate visual access to the whole space and avoids a dead entry corridor.
- Mark the doorway with a visible threshold tile distinct from the surrounding floor, paired with a player-touch transfer event on or immediately adjacent to it, so the exit is legible and reliable without needing an on-screen prompt.
- Preserve a direct, unobstructed centerline from the entrance to the room's focal point (the primary display, counter, or back-wall feature).
- Maintain at least a one-tile-wide customer lane along that centerline at all times; widen to two-plus tiles where the lane branches into a browsing loop.
- Anchor all shelving and heavy storage furniture directly against a wall. Do not leave shelf-type objects floating in open floor - every shelf cluster should terminate cleanly into a wall or into an adjacent storage object, never trail off into empty floor.
- Divide the room conceptually into zones - entry threshold, center aisle, browse loop, wall stock, focal back-wall feature - and design each zone's density independently rather than treating the room as one undifferentiated space.

## Composition Rules

- Organize the room bilaterally around its primary axis: doorway, center aisle, and focal back-wall feature on or near the centerline, with left- and right-side merchandise clusters counterbalancing each other in mass without being mirrored tile-for-tile.
- Group goods by surface and storage purpose (shelved stock, table displays, side clusters), not scattered as isolated decorative objects. Clustering reads as a real shop's storage logic; scattering reads as noise.
- Use a floor accent (rug, mat, or similar) to mark the primary browsing/focal zone and visually distinguish it from the plain walkway floor.
- Alternate density along the path from entrance to back wall: dense wall stock, open aisle, dense central display, open aisle, dense back wall. This rhythm keeps the room feeling stocked without making the walkable path feel cluttered or confusing.
- Reserve at least one small animated or decorative detail (a lit flame, a hanging sign, similar) near the room's focal area to make an otherwise static room feel inhabited, without requiring any gameplay logic.
- Treat negative space as the customer's path, not as leftover filler - every open tile in the layout should correspond to a place the player is meant to walk.
- Use dense object placement at the room's perimeter and progressively lighter object placement toward the center, so the walkable core stays clear and readable.

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`:

- The full walkable set must form a single connected loop reachable from the entrance - door, center aisle, and browse-zone approach tiles, with no isolated pocket of walkable floor unreachable from the spawn point.
- Every intended interactable or display object must satisfy a **reachability ring**: at least one adjacent walkable tile the player can stand on to approach it. An object with no adjacent walkable tile is not usable and should either gain one or be reclassified as pure background dressing.
- Structural furniture (shelves, tables, storage clusters) blocks movement by default. Do not rely on visual appearance alone to imply a tile is walkable or blocked - set collision explicitly per `bridges/rpg-maker-mz/passability-rule.md`.
- The doorway/threshold tile and the tile(s) carrying the exit transfer event must always be walkable and must round-trip correctly with whatever exterior transfer leads into the room.
- Use void/darkness or an equivalent architectural boundary outside the room shell to keep the interior's walkable silhouette crisp and prevent the player from wandering into non-architectural space.
- A route validation pass (per `bridges/rpg-maker-mz/passability-rule.md`, "Route Validation") should at minimum confirm: `entrance -> center aisle`, `center aisle -> each display cluster`, and `center aisle -> exit`.

## Event Rules

- This pattern governs **shop atmosphere and spatial layout only.** It does not prescribe, and must not be read as prescribing, RPG Maker Shop Processing configuration, an inventory list, or shopkeeper dialogue - those are implementation-packet or game-design decisions, not layout-pattern decisions (see `PATTERN_SCHEMA.md`, "Event Rules").
- Do not assume a shop interior requires a shopkeeper NPC event by default. A shop can be built as a pure atmosphere/browsing space first, with commerce functionality (a shopkeeper event, Shop Processing, an interaction trigger) layered on separately by whatever contract or packet actually requires it.
- If a shopkeeper or clerk NPC event is required by the citing contract, its placement needs a deliberate service point (a counter-adjacent reachable tile facing the counter) - this pattern's default browse-first layout does not automatically provide one, and the contract must specify it.
- Keep decorative/atmosphere events (animated flames, ambient details) free of gameplay commands. Their purpose is visual life, not interaction logic.
- Every entrance/exit must use exactly one player-touch transfer event per direction of travel, per `bridges/rpg-maker-mz/passability-rule.md`'s general transfer-reachability requirement.

## Common Mistakes

- Building the room larger than the shop's actual stock justifies, producing dead, undecorated floor space that does not correspond to a walking path.
- Off-centering the entrance without a stated reason, breaking the bilateral composition this pattern relies on.
- Leaving a shelf or storage cluster floating mid-floor instead of terminating it into a wall.
- Placing a display or interactable object with no adjacent walkable tile, failing the reachability ring requirement.
- Assuming a shop-shaped room automatically implies a functioning shopkeeper and Shop Processing - the room's visual genre and its mechanical systems are independent and must both be verified.
- Treating this pattern's `Medium` confidence as `High` in a citing contract - it has one corroborating source, not two.
- Copying source-map tile coordinates directly into a new build instead of re-deriving proportional placement for the new map's own dimensions.

## References

- Source report: `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md`
- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- Precedent for citing a build target's ledger/ownership state rather than asserting it independently: `reports/implementation-contracts/ashford-shop-build-contract.md`
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Category tier, parent of `interiors/weapon-shop.pattern.md` and `interiors/armor-shop.pattern.md`; see that document's "The Shop / Item Shop Double Duty" for why no separate Item Shop specialization exists yet)
- Created by `work-orders/WO-0024-design-pattern-library.md`

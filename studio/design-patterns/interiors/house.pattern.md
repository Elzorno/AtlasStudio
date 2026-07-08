---
pattern_id: PAT-INTERIOR-HOUSE
name: Interior Pattern - House
version: 1.0
category: interior
status: accepted
confidence: high
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map018.json (RPG Maker MZ official sample project, map tree name 'House 1', tileset 'Inside', 17x13)"
  - "TheLastSwordProtocol-Game/data/Map019.json (RPG Maker MZ official sample project, map tree name 'House 2', tileset 'Inside', 17x13)"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "studio/design-patterns interior-pattern-corpus extraction, WO-0025 (no standalone report; extraction performed directly against data/Map018.json and data/Map019.json - see reports/design-patterns/interior-pattern-corpus-review.md for the comparative evidence trail)"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - House v1.0

## Name

A small, single-room domestic interior (a villager's or townsperson's home) that reads as lived-in rather than stocked, prioritizing open floor for dwelling over dense merchandise display.

## Category

`interior`. Scoped to ordinary single-room residential interiors - not a shop, not an inn, not a multi-floor notable's residence (see `chief-house.pattern.md` for that case, which is a distinct pattern precisely because it deviates from this one).

## Source

Derived from two official RPG Maker MZ sample maps: "House 1" (`Map018.json`) and "House 2" (`Map019.json`), both in the official sample project bundled with the engine. Both maps are 17x13 tiles on the `Inside` tileset family, with the same architectural shell dimensions and position as the already-accepted `shop.pattern.md` (`PAT-INTERIOR-SHOP`). Extraction was performed directly against the map JSON and cross-checked against `Tilesets.json` tileset 3 ("Inside") for this work order (`WO-0025`); see `reports/design-patterns/interior-pattern-corpus-review.md` for the full comparative evidence and rule-by-rule corroboration table. This pattern abstracts findings from both maps into reusable rules; it does not reproduce either source map's tile grid, coordinates, or JSON.

## Confidence

**High.** Two independent official sample maps ("House 1" and "House 2") were extracted separately and found to agree on every Layout, Passability, and Event rule stated below, and on all but one Composition rule (furniture density and clustering), which itself agreed in both maps. This meets `PATTERN_CONFIDENCE_MODEL.md`'s High bar directly: "observed repeatedly, in more than one official RPG Maker sample map, with consistent results." Unlike `shop.pattern.md` v1.0 (filed at Medium on a single source), this pattern starts at High because its second corroborating source was available at initial authoring time rather than needing a later promotion.

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map018.json` ("House 1") | RPG Maker MZ official sample project | Full extraction: 17x13 shell, centered door/threshold, continuous back-wall shelf run, two decorative flames (bilateral), wide open central floor, no NPC event. |
| `Map019.json` ("House 2") | RPG Maker MZ official sample project | Full extraction: identical 17x13 shell and threshold construction, continuous back-wall shelf run, one decorative flame (centered), single small central furniture accent, fully open central floor, no NPC event. |

## Applicable Genres

`jrpg`, `dragon-quest-style`. Same reasoning as `shop.pattern.md`: assumes a town-embedded interior entered and exited deliberately, not a screen-chain puzzle room. Not checked against action-RPG or screen-chain genre conventions.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is a **single room**, not a multi-room house or a multi-floor residence.
- The interior has **exactly one primary entrance/exit**.
- The interior's function is **domestic dwelling**, not commerce, lodging-for-hire, or a notable NPC's seat of authority (see `chief-house.pattern.md` for the last case).
- The interior is reached from a town or village exterior map.

If any of these do not hold, treat this pattern as a starting reference only and note the deviation explicitly in the citing implementation contract.

## Layout Rules

- Use the same compact 17x13-class shell as `shop.pattern.md`: a small full-map footprint with an even smaller playable architectural shell inside it. Both observed houses use the identical shell size and position as the observed shop map - this is strong evidence that the engine's `Inside` tileset family has a default "small single room" shell size AtlasStudio should treat as a safe default across residential and commercial interiors alike, not something to re-derive per building type.
- Center the entrance on the room's primary axis, matching `shop.pattern.md`'s default. Both observed houses center their door at the shell's horizontal midpoint.
- Place the player's spawn point one tile inside the doorway, identical to `shop.pattern.md`.
- Mark the doorway with the same visible-threshold-plus-player-touch-transfer construction as `shop.pattern.md` (stairs-family tile one row above a floor tile carrying the transfer event, one row above the map's outer edge).
- Run structural storage furniture (shelving) as a **continuous run against the back wall**, not as individually spaced items. Both observed houses use one long, unbroken shelf run spanning nearly the entire back wall, differing from the weapon-shop convention (see `weapon-shop.pattern.md`) of individually spaced wall-mounted items.
- Keep the rest of the floor **open**. Unlike a shop, a house does not need side clusters, table displays, or a browsing loop - both observed houses leave the center and lower floor almost entirely clear, with at most one small furniture accent away from the back wall.

## Composition Rules

- Use a **markedly lower decoration density** than `shop.pattern.md`. Both observed houses concentrate essentially all their furniture into the single back-wall shelf run, with the remaining floor left open. This is the primary composition difference between "house" and "shop": a shop clusters goods at the perimeter *and* in side/table displays; a house clusters its one storage feature at the back wall only and otherwise reads as empty, walkable living space.
- Where a secondary furniture accent exists away from the back wall, keep it to a single small piece near the room's center or a corner (a hearth-like or table-like accent), not a cluster. One observed house omits this accent from the direct centerline (placed off-axis, one tile from center); the other places it in a single-tile position near the room's middle. Neither observed house uses more than one such accent.
- Do not force bilateral left/right symmetry the way `shop.pattern.md` recommends for merchandise clusters. A house's open floor does not need counterbalancing side masses - both observed houses read as balanced through their shared back-wall shelf and open floor alone, without side clusters to balance.
- Reserve exactly one to two small animated/decorative details (a lit flame) near the top of the room. Both observed houses use this convention; one places a single flame at room-center, the other places two flames in a bilateral pair. Either is acceptable - the flame count should scale with how much back-wall symmetry the room's shelf layout already has, not with room size (both houses are the same size).

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`, consistent with `shop.pattern.md`:

- The full walkable set must form a single connected area reachable from the entrance, with no isolated pocket. Both observed houses satisfy this trivially, since their open-floor composition leaves almost the entire non-shelf area walkable.
- Structural furniture (the back-wall shelf run) blocks movement by default and must terminate cleanly into the walls at both ends - both observed houses confirm this.
- The doorway/threshold tile and exit-transfer tile must always be walkable and round-trip correctly with the exterior transfer that leads into the room, identical to `shop.pattern.md`.
- Use void/darkness outside the room shell, identical to `shop.pattern.md`.
- A house's reachability ring requirement is looser in practice than a shop's, because a house has far fewer interactable display objects to begin with - but any object the citing contract does intend as interactable (a bed, a chest, a hearth) still needs at least one adjacent walkable tile, per the general rule.

## Event Rules

- This pattern governs **house atmosphere and spatial layout only**, not resident NPC placement, dialogue, or any interactive furniture (chests, beds) a specific implementation contract may require. Neither observed house contains an NPC event.
- Do not assume a house interior requires a resident NPC event by default - both observed samples demonstrate a fully furnished, atmospheric house with zero character events. If a resident is required by the citing contract, its placement and service point (if any) must be specified there, not inferred from this pattern.
- Keep decorative/atmosphere flame events free of gameplay commands, identical to `shop.pattern.md`.
- Every entrance/exit uses exactly one player-touch transfer event per direction of travel, identical to `shop.pattern.md`.

## Common Mistakes

- Importing `shop.pattern.md`'s side-cluster and rug-accent composition rules wholesale into a house build - a house's lower decoration density is a deliberate, corroborated difference, not an oversight to "fix."
- Leaving the back-wall shelf run broken into disconnected segments instead of one continuous run terminating cleanly at both walls.
- Adding more than one or two decorative flames, or scattering them off the top wall band, without a stated reason - both observed houses keep flames near the top wall.
- Treating a house's low furniture count as license to skip the reachability-ring check on the pieces that *are* meant to be interactable.
- Assuming this pattern extends to multi-floor or notable-NPC residences - see `chief-house.pattern.md`, which corroborates several of this pattern's structural rules (shell, threshold, no-NPC-by-default) but diverges sharply on composition and passability once a second floor and a status-appropriate hearth are introduced.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/shop.pattern.md` - shares this pattern's shell, threshold, and event conventions; diverges on decoration density and clustering.
- `studio/design-patterns/interiors/chief-house.pattern.md` - the multi-floor, higher-status counterpart to this pattern.
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence trail across the interior corpus.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Category tier, currently no materialized parent - see that document's "Materialized vs. Virtual Nodes")
- Created by `work-orders/WO-0025-interior-pattern-corpus.md`

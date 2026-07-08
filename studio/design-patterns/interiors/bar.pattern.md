---
pattern_id: PAT-INTERIOR-BAR
name: Interior Pattern - Bar
version: 1.0
category: interior
status: accepted
confidence: medium
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map023.json (RPG Maker MZ official sample project, map tree name 'Bar', tileset 'Inside', 17x13)"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "studio/design-patterns interior-pattern-corpus extraction, WO-0025 (no standalone report; extraction performed directly against data/Map023.json - see reports/design-patterns/interior-pattern-corpus-review.md for the comparative evidence trail)"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - Bar v1.0

## Name

A single-room social/gathering interior with the densest, most scattered furniture floor in the observed interior corpus - many small seating islands rather than wall-anchored storage.

## Category

`interior`. Scoped to single-room social/gathering interiors (a tavern-style common room). Shares its base shell and threshold conventions with `shop.pattern.md`, but is the corpus's clearest counterexample to `shop.pattern.md`'s wall-anchoring composition rule.

## Source

Derived from one official RPG Maker MZ sample map: "Bar" (`Map023.json`), in the official sample project bundled with the engine. The map is 17x13 tiles on the `Inside` tileset family, using a narrower two-tile outer void margin than the four-tile margin seen in `shop.pattern.md`, `house.pattern.md`, and `weapon-shop.pattern.md`/`armor-shop.pattern.md` - the playable architectural shell is correspondingly larger within the same overall map size. Extraction was performed directly against the map JSON and cross-checked against `Tilesets.json` tileset 3 ("Inside") for `WO-0025`.

## Confidence

**Medium.** Corroborated by exactly one official sample map, with no second source on file. Per `PATTERN_CONFIDENCE_MODEL.md`, apply by default but flag as single-source evidence. Eligible for promotion to High once a second official sample bar/tavern, or one accepted and playtested AtlasStudio bar build, corroborates the floating-furniture composition convention below.

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map023.json` ("Bar") | RPG Maker MZ official sample project | Full extraction: 17x13 map with a larger-than-usual interior shell, a single large open room densely scattered with multiple small furniture islands across nearly the entire floor (not confined to walls or a single central display), an off-center threshold, and three decorative flames spread across the top wall band. No NPC event. |

## Applicable Genres

`jrpg`, `dragon-quest-style`. Same reasoning as `shop.pattern.md`.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is a **single room** whose primary function is **social gathering/seating**, not merchandise storage or display.
- The interior has **exactly one primary entrance/exit**.
- Furniture is meant to represent **many small seating groups** (tables and stools) distributed across the floor, not goods clustered at the perimeter.
- The interior is reached from a town or village exterior map.

If the room's furniture should represent stocked merchandise rather than seating, use `shop.pattern.md`, `weapon-shop.pattern.md`, or `armor-shop.pattern.md` instead - this pattern's floating-furniture convention is specific to social/seating spaces.

## Layout Rules

- Use the same general threshold construction as `shop.pattern.md` (stairs-family tile above a floor tile carrying the transfer event), but do not assume the door must center on the room. The observed map's door is offset toward one side of the room rather than on its horizontal midpoint - a single-room counterexample to `shop.pattern.md`'s default centering rule, distinct from `inn.pattern.md`'s off-center door (which is explained by multi-zone structure). Here, the offset appears to be a deliberate composition choice rather than a structural necessity, meaning "center the door unless there is a reason not to" (`shop.pattern.md`) should be read literally: sometimes the reason is simply that the room's furniture composition does not need bilateral symmetry to read as balanced.
- Use a **wider interior shell relative to the overall map** than the shop/house default - the observed bar uses a two-tile outer void margin rather than four, yielding more usable floor within the same 17x13 map footprint. This is a legitimate scale variant for a room whose function needs more floor area (many seating islands) than a shop or house needs.
- Do not organize the floor around a single centerline aisle the way `shop.pattern.md` does. The observed bar has no single dominant walking spine - the walkable floor is a connected mesh threading between furniture islands, reachable from multiple directions rather than funneled along one axis.

## Composition Rules

- **This pattern overrides `shop.pattern.md`'s "anchor furniture to a wall" rule.** The observed bar's furniture is overwhelmingly *not* wall-anchored - it is scattered as small islands throughout the open floor, which is correct and intentional for a social/seating space. `shop.pattern.md`'s Common Mistake ("leaving a shelf or storage cluster floating mid-floor") is a shop/storage-specific rule and must not be applied to a bar. This is the clearest, most load-bearing comparative finding in the interior corpus: wall-anchoring is a display-furniture convention, not a universal interior rule.
- Distribute furniture as **many small islands (2-4 tiles each)** rather than a few large clusters. The observed bar has roughly half a dozen distinguishable furniture groups spread across the room, none dominating the space the way a shop's back-wall shelf or an armor shop's counter does.
- Accept **higher overall floor coverage by furniture** than any other pattern in this corpus - the observed bar's furniture-to-floor ratio is visibly denser than the shop, house, or weapon/armor shop maps, appropriate for a room whose purpose is to feel busy and populated rather than easy to browse in a straight line.
- Use **more than one decorative flame spread across the room's width**, rather than one flame near a single focal point. The observed bar places three flames near the top wall, spread left, center-right, and right rather than clustered - lighting the whole open floor rather than anchoring one feature.

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`:

- The walkable floor must form a connected mesh reachable from the entrance - not necessarily a single centerline aisle, but every furniture island must have open floor accessible around at least part of its perimeter.
- Furniture islands block movement the same way shop shelving does - a table/stool group must not be walked through, but unlike shop stock, a bar's furniture islands do not need to satisfy a browsing "reachability ring" for merchandise-examination purposes, since the object is seating, not a display to interact with (unless a citing contract specifies an actual seating/interaction event).
- The threshold and exit-transfer passability rules are identical to `shop.pattern.md`, independent of where the door sits on the room's axis.
- Verify no furniture island fully seals off a section of open floor from the rest of the room - a dense floor plan increases the risk of accidentally trapping a walkable pocket, which route validation should specifically check for in a busy layout like this one.

## Event Rules

- This pattern governs **bar atmosphere and open-floor seating composition only** - it does not prescribe a bartender NPC, patron NPCs, dialogue, or any drink/service system. The observed source map has zero NPC events.
- Do not assume a scattered-furniture floor implies populated NPC seating - the official sample demonstrates a fully furnished, atmospheric bar with no characters present at all. Patron and bartender placement, if required, must be specified by the citing contract.
- Decorative flame and threshold-transfer event conventions are identical to `shop.pattern.md`.

## Common Mistakes

- Applying `shop.pattern.md`'s wall-anchoring rule to a bar's furniture, which would flatten the busy, populated floor read this pattern depends on.
- Forcing a single centerline aisle through a bar's floor plan instead of a multi-directional walkable mesh between furniture islands.
- Under-furnishing a bar to match a shop's or house's lower decoration density - this pattern's higher floor coverage is a deliberate, corroborated difference, not excess to trim.
- Assuming the door must be centered - the observed sample corroborates that a single-room interior can read as balanced without a centered entrance.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/shop.pattern.md` - shares threshold/event conventions; this pattern explicitly overrides its wall-anchoring composition rule for social/seating spaces.
- `studio/design-patterns/interiors/inn.pattern.md` - shares this pattern's open-common-room composition logic for its own common-room zone.
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence trail across the interior corpus.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Category tier, sibling of `interiors/shop.pattern.md`, not its child - see that document's "Override Behavior" for why this pattern's relationship to `shop.pattern.md`'s wall-anchoring rule is a cross-branch clarification rather than a vertical override, and `reports/design-patterns/inheritance-examples.md` Example 4 for the full worked correction)
- Created by `work-orders/WO-0025-interior-pattern-corpus.md`

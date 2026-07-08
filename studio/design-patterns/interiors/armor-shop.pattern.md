---
pattern_id: PAT-INTERIOR-ARMOR-SHOP
name: Interior Pattern - Armor Shop
version: 1.0
category: interior
status: accepted
confidence: medium
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map022.json (RPG Maker MZ official sample project, map tree name 'Weapon & Armor Shop', tileset 'Inside', 17x13) - counter/table display zone only; see Source note below"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "studio/design-patterns interior-pattern-corpus extraction, WO-0025 (no standalone report; extraction performed directly against data/Map022.json - see reports/design-patterns/interior-pattern-corpus-review.md for the comparative evidence trail)"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - Armor Shop v1.0

## Name

A small, single-room retail interior specialized for armor stock, distinguished from `weapon-shop.pattern.md` by a counter/table display convention rather than a wall-mounted rack.

## Category

`interior`. Scoped to the counter/table-display sub-convention of a small retail interior. Shares its base shell, threshold, and event conventions with `shop.pattern.md`; differs specifically in which display convention dominates the room.

## Source

**Important evidence caveat, stated up front:** identical to `weapon-shop.pattern.md`, the official RPG Maker MZ sample project does not contain a standalone, dedicated armor-only shop map. The only available source is "Weapon & Armor Shop" (`Map022.json`), the same combined interior `weapon-shop.pattern.md` draws from. This pattern describes that map's left-of-center counter/table display convention specifically, as distinct from the map's right-wall rack cluster (covered by `weapon-shop.pattern.md`). Both patterns are derived from **the same single source map**, not from two independent buildings. Extraction was performed directly against the map JSON and cross-checked against `Tilesets.json` tileset 3 ("Inside") for `WO-0025`.

## Confidence

**Medium**, with the same explicit caveat as `weapon-shop.pattern.md`. The counter/table-vs-rack split within `Map022.json` is spatially clear and internally consistent, meeting the literal single-map Medium bar in `PATTERN_CONFIDENCE_MODEL.md` - but because this pattern and `weapon-shop.pattern.md` both trace to zones of one shared map, this is the weaker end of Medium. It should not be promoted toward High on the strength of the shared map alone; promotion requires an independent second source (a second official armor-shop sample, or an accepted, playtested AtlasStudio armor-shop build).

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map022.json` ("Weapon & Armor Shop") | RPG Maker MZ official sample project | Left-of-center counter/table display (a compact, multi-tile display surface set back from the entrance, distinct from the room's individually spaced back-wall and side-wall rack items). Shares the map's single centered threshold and single off-center decorative flame with `weapon-shop.pattern.md`. |

## Applicable Genres

`jrpg`, `dragon-quest-style`. Same reasoning as `shop.pattern.md`.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is a **single room** dedicated primarily to armor sales (or an armor-sales zone within a combined weapon-and-armor shop, per its source).
- The interior has **exactly one primary entrance/exit**.
- Stock is meant to read as **displayed pieces on a counter or table surface** (armor set out for inspection) rather than wall-hung or wall-racked goods.
- The interior is reached from a town or village exterior map.

If the shop's stock should read as wall-mounted or wall-racked goods, use `weapon-shop.pattern.md`'s convention instead; if it should read as uniform shelved goods, use `shop.pattern.md`.

## Layout Rules

- Use the same 17x13-class shell, centered threshold, and one-tile-inside-doorway spawn as `shop.pattern.md` - identical structural base to `weapon-shop.pattern.md`, since both derive from the same source map.
- Place the primary display as a **compact counter/table cluster set back from the entrance**, not against the very back wall and not spanning a full wall run. The observed map's counter sits left-of-center, one to two tiles off the room's true centerline, functioning as a secondary focal mass rather than the room's single dominant feature (that role belongs to the wall-rack cluster, per `weapon-shop.pattern.md`).
- Keep the counter's footprint small relative to the room - a few tiles, not a full wall run. This differentiates it from both `shop.pattern.md`'s larger central table display and `weapon-shop.pattern.md`'s deep wall-rack cluster.
- Do not center the counter exactly on the entrance centerline. The observed map's counter is offset toward one side, leaving the direct centerline clear for the wall-rack focal item at the back wall (see `weapon-shop.pattern.md`) - in a combined shop, the counter functions as a secondary, not primary, waypoint along the browsing path.

## Composition Rules

- Treat the counter as a **secondary display mass**, smaller and less visually dominant than the wall-stock convention it shares a room with. Where `weapon-shop.pattern.md` calls for a deep, tall wall cluster, this pattern's counter should read as a modest, approachable browsing surface - the contrast between the two is part of what visually distinguishes "armor for close inspection" from "weapons mounted for display."
- Cluster armor pieces on the counter surface itself rather than spreading them across multiple small tables - the observed map uses one compact multi-tile counter rather than several scattered single-tile displays.
- Share the room's single decorative flame and general perimeter-dense/center-open rhythm with `weapon-shop.pattern.md` - both patterns describe the same room, so overall room-level composition rhythm (not display-specific rules) is identical between them by construction.

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`, consistent with `shop.pattern.md`:

- The counter must satisfy the reachability ring the same way any shop display object does: at least one adjacent walkable tile. Verified directly against the observed map: the counter cluster has open floor adjacent on at least one side.
- The counter blocks movement by default - a player must not be able to walk onto or through it; the walkable aisle wraps around it, not across it.
- The threshold, spawn, and exit-transfer passability rules are identical to `shop.pattern.md` and `weapon-shop.pattern.md`.

## Event Rules

- This pattern governs **armor-shop atmosphere and counter-display arrangement only** - it does not prescribe a shopkeeper, Shop Processing, or an armor inventory list. The observed source map has zero NPC events.
- Do not assume a counter display implies a functioning armor vendor - identical reasoning to `shop.pattern.md`'s and `weapon-shop.pattern.md`'s Event Rules.
- If a shopkeeper is required by a citing contract, the counter is the natural service point (a counter-adjacent reachable tile facing the counter), matching `shop.pattern.md`'s general guidance that a service point must be deliberately specified, not assumed.
- Decorative flame and threshold-transfer event conventions are identical to `shop.pattern.md`.

## Common Mistakes

- Making the counter the room's largest or most dominant feature - in the observed map it is deliberately secondary to the wall-rack cluster; inflating it collapses the distinction this pattern depends on.
- Treating this pattern as independently corroborated to the same degree as `house.pattern.md` - it and `weapon-shop.pattern.md` share one source map, not two independent ones. State this explicitly in any citing contract.
- Centering the counter exactly on the entrance centerline, which crowds out the wall-rack focal point this room's centerline is meant to lead to.
- Assuming a counter automatically implies a shopkeeper service point is already wired - it must be specified by the citing contract, per Event Rules above.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/shop.pattern.md` - shared shell, threshold, and event conventions.
- `studio/design-patterns/interiors/weapon-shop.pattern.md` - the wall-rack convention observed in the same source map.
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence trail, including the shared-source caveat discussion.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Specialization tier, child of `interiors/shop.pattern.md`)
- Created by `work-orders/WO-0025-interior-pattern-corpus.md`

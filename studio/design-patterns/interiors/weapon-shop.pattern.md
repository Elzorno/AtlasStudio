---
pattern_id: PAT-INTERIOR-WEAPON-SHOP
name: Interior Pattern - Weapon Shop
version: 1.0
category: interior
status: accepted
confidence: medium
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map022.json (RPG Maker MZ official sample project, map tree name 'Weapon & Armor Shop', tileset 'Inside', 17x13) - weapon-rack wall zone only; see Source note below"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "studio/design-patterns interior-pattern-corpus extraction, WO-0025 (no standalone report; extraction performed directly against data/Map022.json - see reports/design-patterns/interior-pattern-corpus-review.md for the comparative evidence trail)"
created: 2026-07-08
last_reviewed: 2026-07-08
---

# Interior Pattern - Weapon Shop v1.0

## Name

A small, single-room retail interior specialized for weapon stock, distinguished from the general `shop.pattern.md` by a dense wall-mounted rack convention instead of continuous shelving.

## Category

`interior`. Scoped to the weapons-display sub-convention of a small retail interior. Shares its base shell, threshold, and event conventions with `shop.pattern.md`; differs specifically in how wall stock is arranged.

## Source

**Important evidence caveat, stated up front:** the official RPG Maker MZ sample project does not contain a standalone, dedicated weapon-only shop map. The only available source is "Weapon & Armor Shop" (`Map022.json`), a single combined interior that visibly separates into two display conventions within one room: a dense, individually-spaced wall-mounted rack cluster along the right wall, and a shorter table/counter display left-of-center. This pattern describes the wall-mounted rack convention specifically; `armor-shop.pattern.md` describes the counter/table convention from the same map. Both patterns are derived from **the same single source map**, not from two independent buildings - this is weaker evidence than `house.pattern.md`'s two-independent-buildings corroboration, and weaker than a hypothetical dedicated weapon-shop sample would provide. Extraction was performed directly against the map JSON and cross-checked against `Tilesets.json` tileset 3 ("Inside") for `WO-0025`.

## Confidence

**Medium**, with an explicit caveat beyond the ordinary single-map Medium bar. Per `PATTERN_CONFIDENCE_MODEL.md`, one official sample map corroborating a stated rule meets the literal Medium bar - and the rack-vs-counter split observed within `Map022.json` is internally consistent and clearly intentional (two distinct, spatially separated display treatments, not incidental variation). But because this pattern and `armor-shop.pattern.md` both trace to zones of one shared map rather than to independent whole-map sources, this pattern should be treated as the **weaker end of Medium**. It should not be promoted toward High on the strength of a second zone within the same map - promotion requires a genuinely independent second source (a second official weapon-shop sample, or an accepted, playtested AtlasStudio weapon-shop build), per `PATTERN_CONFIDENCE_MODEL.md`'s "Medium to High" rule.

## Observed Maps

| Map | Source | What was observed |
|---|---|---|
| `Map022.json` ("Weapon & Armor Shop") | RPG Maker MZ official sample project | Right-wall vertical stock cluster (individually spaced rack-style items, rows spanning most of the room's depth against one wall) and back-wall row of individually spaced mounted items, both distinct from the continuous shelf-run convention observed in `shop.pattern.md` and `house.pattern.md`. Shares the map's single centered threshold and single off-center decorative flame with `armor-shop.pattern.md`. |

## Applicable Genres

`jrpg`, `dragon-quest-style`. Same reasoning as `shop.pattern.md`.

## Required Conditions

This pattern applies only when all of the following are true:

- The interior is a **single room** dedicated primarily to weapon sales (or a weapon-sales zone within a combined weapon-and-armor shop, per its source).
- The interior has **exactly one primary entrance/exit**.
- Wall stock is meant to read as **individual mounted items** (racked weapons, hung blades) rather than uniform shelved goods.
- The interior is reached from a town or village exterior map.

If the shop's stock should read as uniform shelved goods rather than individually mounted items, use `shop.pattern.md`'s continuous-shelf convention instead.

## Layout Rules

- Use the same 17x13-class shell, centered threshold, and one-tile-inside-doorway spawn as `shop.pattern.md` - the observed source map is structurally identical to the Item Shop map in every respect except stock arrangement.
- Anchor weapon stock to a wall as a **vertical run of individually spaced items**, not a continuous shelf. The observed map places its densest weapon stock along one full side wall (not the back wall), spanning most of the room's depth from just below the top wall band down to near the doorway level - a taller, deeper cluster than the back-wall-only shelving seen in `shop.pattern.md` and `house.pattern.md`.
- Reserve the back wall for **individually spaced mounted items** rather than a continuous run, with visible gaps between pieces (unlike `house.pattern.md`'s and `shop.pattern.md`'s back-wall pattern, which is closer to continuous). This produces a rack-like read appropriate for a small number of larger, individually notable weapon pieces rather than many small stacked goods.
- Preserve the direct centerline from entrance to a back-wall focal item. The observed map places one mounted item exactly on the centerline at the back wall, making the centerline terminate at, not merely pass near, the room's most prominent display piece - a stronger version of `shop.pattern.md`'s "preserve a direct centerline to the focal point" rule.

## Composition Rules

- Treat wall stock as **discrete, individually readable pieces** rather than a single uniform mass. The visual goal is a wall of distinct weapons, not a wall of shelving - space items with visible gaps rather than packing them edge to edge.
- A counter or table display may still anchor the room's center-left, functioning the same way `shop.pattern.md`'s table displays do, but the dominant visual mass in a weapon shop should be the wall rack, not the counter.
- Use a single decorative flame, positioned near but not exactly on the room's centerline - the observed map's flame sits one tile off the true horizontal center, a minor variance also seen in `shop.pattern.md`'s own source map, suggesting near-center (not exact-center) flame placement may be an incidental convention across this tileset's samples rather than a deliberate rule. Treat it as optional stylistic flexibility, not a required offset.

## Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`, consistent with `shop.pattern.md`:

- Every intended interactable wall-mounted item needs the same reachability ring as any shop display object: at least one adjacent walkable tile. Verified directly against the observed map: every back-wall mounted item has at least one adjacent open floor tile, satisfying the ring even though the items are individually spaced rather than in a continuous run.
- Deep corner stock (a rack item with no adjacent walkable tile, boxed in by other stock on every side) is acceptable as pure visual mass, identical to `shop.pattern.md`'s "treat back-wall stock as visual mass unless explicit examine/shop events are required" rule - confirmed present in the observed map's densest wall-rack corner.
- The threshold, spawn, and exit-transfer passability rules are identical to `shop.pattern.md`.

## Event Rules

- This pattern governs **weapon-shop atmosphere and wall-stock arrangement only** - it does not prescribe a shopkeeper, Shop Processing, or a weapon inventory list. The observed source map has zero NPC events.
- Do not assume a weapon-rack wall implies a functioning weapon vendor - identical reasoning to `shop.pattern.md`'s Event Rules.
- Decorative flame and threshold-transfer event conventions are identical to `shop.pattern.md`.

## Common Mistakes

- Building a weapon shop's wall stock as a continuous shelf run (the `shop.pattern.md`/`house.pattern.md` convention) instead of individually spaced mounted items - this collapses the weapon-shop's distinguishing visual identity.
- Treating this pattern as independently corroborated to the same degree as `house.pattern.md` - it and `armor-shop.pattern.md` share one source map, not two independent ones. State this explicitly in any citing contract.
- Packing wall-mounted items edge to edge with no gaps, losing the "individually readable weapon" read this pattern depends on.
- Placing a wall-mounted item with zero adjacent walkable tiles when the citing contract intends it to be examinable - verify the reachability ring for any item the build actually wants interactive.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/shop.pattern.md` - shared shell, threshold, and event conventions.
- `studio/design-patterns/interiors/armor-shop.pattern.md` - the counter/stand convention observed in the same source map.
- `bridges/rpg-maker-mz/passability-rule.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence trail, including the shared-source caveat discussion.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - this pattern's place in the hierarchy (Specialization tier, child of `interiors/shop.pattern.md`)
- Created by `work-orders/WO-0025-interior-pattern-corpus.md`

# RPG Maker MZ Sample Project Analysis

## Purpose

This analysis studies `references/rpg-maker-mz-samples/official sample project/` for composition, density, and structural lessons, per `bridges/rpg-maker-mz/map-quality-standard.md`'s comparable-quality-target requirement. **No map, event, or dialogue content from the sample project is reproduced anywhere in AtlasStudio or the target repository.** Everything below is a lesson extracted from studying the sample data directly (99 maps inspected, `MV_SampleMap_en` data set), not copied content.

## Average Map Sizes

Measuring all 99 maps in the sample set:

- Average map area: approximately 1,682 tiles (this figure is dominated by a handful of very large overworld/"World" maps and should not be read as a per-building target).
- **World/overworld maps** (`World 1`-`World 5`): 60x60 to 140x140 tiles - these are large, continent-scale exploration maps, not comparable in scale to a single starting village.
- **Town/settlement-scale maps** (e.g. `Fortress`, `Lost Forest`, `Forest of Decay`): roughly 50x50 to 60x60 tiles.
- **Interior maps** (houses, shops, classrooms): consistently small, **13x13 to 21x18 tiles**, regardless of building type - a shop, a house, and a classroom in this sample set occupy roughly the same footprint.

**Lesson for Ashford Village:** a starting village exterior should sit well below the "World" scale and closer to, but still smaller than, the sample set's mid-scale town maps, since Ashford Village has only four buildings and a green - this is exactly why `ashford-village-map-brief.md` (produced under `WP-03`) targets roughly 32x28 to 36x32 for the exterior rather than reaching for the sample set's larger town sizes. Interiors should stay in the 11x9 to 17x14 range observed across every interior sample studied, matching what `TheLastSwordProtocol-Game`'s own Map002/Map003 already do (17x13 each).

## Decoration Density

Direct inspection shows most sample maps (59 of the 99 examined) ship with **zero events** - they are tile-art composition demos, not populated, event-rich towns. This is an important caveat: **the sample project is a much better reference for tile composition, autotile usage, and visual layout than it is for event or NPC density.** Where samples do carry decoration, it reads as sparse and purposeful rather than dense - a handful of distinct objects (a well, a sign, a cart) rather than uniform repeated scatter. This directly supports `bridges/rpg-maker-mz/map-quality-standard.md`'s prohibition on "sloppy repeated decoration patterns": the official samples themselves do not rely on repetition for texture.

## Environmental Storytelling

Sample maps that do carry detail favor a small number of specific, named landmarks over generic scatter - e.g., distinguishing a "Fishing Village" from a "Mountain Village" or a "Nomad Camp" primarily through a couple of signature structures and terrain choices rather than through event count. The lesson generalizes directly to Ashford Village's Village Memorial and Optional Viewpoint (`ashford-village-map-brief.md`): a small number of specific, well-placed landmarks does more storytelling work than a larger number of generic decorations.

## Landmark Usage

World-scale sample maps use large terrain features (mountains, coastlines, forests) as orientation landmarks; town/interior maps rely on a central structure or object (a fountain, a shop counter, a distinctive room feature) as the map's orientation anchor. Ashford Village's Village Green + Well, as specified in `ashford-village-map-brief.md`, follows this same "one central anchor" pattern correctly.

## Interior Layouts

Across every interior sample inspected (houses, shops, an inn's second floor, a classroom), the layout consistently reserves a small entry/circulation area near the door and clusters furniture/functional objects (counter, bed, table) toward the map's interior - none of the samples pack furniture against the entry point. This is a useful, concrete composition rule for Rowan's Cottage, the General Store, the Blacksmith, and the Inn interiors, independent of the character/canon question raised in `implementation-preflight.md`.

## Event Density

Among the 40 sample maps that do carry events, the average is approximately **7 events per map**. This is markedly lower than what is already implemented in the real target repository's own Map001 (`TWN_Ashford_Exterior`, 23 events) and Map002 (`INT_Ashford_ElaraHouse`, 10 events) - both of which exceed the sample project's typical density. **The real target repository, not the sample project, should be treated as the primary event-density benchmark for Ashford Village going forward**, since it is a purpose-built, story-integrated map rather than a generic composition demo.

## Composition Principles Extracted

1. Interior maps are small (roughly 11x9 to 21x18) regardless of building purpose - do not over-size a shop or cottage relative to a house.
2. Exterior/town maps should be sized to their actual content, not to a generic "town" template - the sample set's own town-scale maps vary from roughly 50x50 down to much smaller depending on what they actually contain.
3. Decoration should be sparse, specific, and purposeful rather than dense or repeated.
4. A single strong central landmark orients a map better than several minor ones.
5. Entry points should stay clear of furniture/object clutter in interiors.
6. The sample project measures composition and scale well; it does not measure event density well. Use the real target repository's own existing maps (Map001-003) as the event-density and naming-convention benchmark instead, once the primary blocker in `implementation-preflight.md` is resolved.

## What Was Not Reproduced

No tile arrangement, no event script, no message text, and no specific building layout from the sample project appears in any AtlasStudio document or in `TheLastSwordProtocol-Game`. Every lesson above is stated as a general principle (scale range, density pattern, composition rule), never as a specific map to copy, per `WP-03-preflight`'s explicit constraint.
